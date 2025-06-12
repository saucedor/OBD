from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse 
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Profile
from OBD_Campaigns.models import Campana 

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try: 
            profile = request.user.profile
        except:
            return redirect('account_login')
    return render(request, 'OBD_users/profile.html', {'profile':profile})

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else: 
        onboarding = False
        
    return render(request, 'OBD_users/profile_edit.html', {'form':form, 'onboarding':onboarding})

@login_required
def profile_settings_view(request):
    return render(request, 'OBD_users/profile_settings.html')

@login_required
def profile_emailchange(request):

    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():

            #check if email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use')
                return redirect('profile-settings')
            
            form.save()

            #Then signal updates emailaddress and set the verified to false

            #Then send confirmation email
            send_email_confirmation(request, request.user)

            return redirect('profile-settings')
        
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')

    return redirect('home')

@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Cuenta eliminada')
        return redirect('home')

    return render(request, 'OBD_users/profile_delete.html')

# Vista de lista de usuarios
@login_required 
def users_list(request):
    query = request.GET.get("q", "")
    role_filter = request.GET.get("role", "")
    staff_filter = request.GET.get("staff", "")
    superuser_filter = request.GET.get("superuser", "")
    page = request.GET.get("page")

    perfiles = Profile.objects.select_related('user').order_by('-user__date_joined')

    # Filtros
    if query:
        perfiles = perfiles.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        )
    
    if role_filter in ['cliente', 'vendedor']:
        perfiles = perfiles.filter(role=role_filter)

    if staff_filter == "true":
        perfiles = perfiles.filter(user__is_staff=True)
    elif staff_filter == "false":
        perfiles = perfiles.filter(user__is_staff=False)

    if superuser_filter == "true":
        perfiles = perfiles.filter(user__is_superuser=True)
    elif superuser_filter == "false":
        perfiles = perfiles.filter(user__is_superuser=False)

    # Paginación
    paginator = Paginator(perfiles, 8)  # 8 perfiles por página
    page_obj = paginator.get_page(page)

    context = {
        "page_obj": page_obj,
        "query": query,
        "role_filter": role_filter,
        "staff_filter": staff_filter,
        "superuser_filter": superuser_filter,
    }

    print("PERFILES FILTRADOS:", perfiles.count())

    return render(request, "OBD_users/users_list.html", context)

# Vista para el detalle de un usuario
@login_required
def detalle_usuario(request, pk):
    perfil = get_object_or_404(Profile, pk=pk)

    # Ejemplo: obtener campañas en las que está involucrado
    campañas = Campana.objects.filter(comentario__perfil=perfil).distinct() if hasattr(perfil, 'comentario') else []

    context = {
        "perfil": perfil,
        "campañas": campañas,
    }
    return render(request, "OBD_users/detalle_usuario.html", context)

# Vista para editar un usuario
@login_required
@staff_member_required
def editar_usuario(request, pk):
    perfil = get_object_or_404(Profile, pk=pk)
    user = perfil.user

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('detalle_usuario', pk=pk)
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=perfil)

    return render(request, "OBD_users/editar_usuario.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "perfil": perfil
    })
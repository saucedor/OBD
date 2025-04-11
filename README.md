# OBD
https://docs.google.com/document/d/14DAHLcBMwYaiGtwhRbNzJSZ6TZcBDdfYWEKOUhshN60/edit?usp=sharing

# SMAdmin

**SMAdmin** es una solución administrativa diseñada para facilitar la gestión eficiente de pequeñas y medianas empresas (PyMEs). El sistema ofrece herramientas para controlar procesos clave como inventarios, clientes, ventas y reportes, con una interfaz intuitiva y centrada en la experiencia del usuario.

Este proyecto fue desarrollado como parte del curso de Ingeniería de Software por el equipo **OBD**, conformado por:

- **Aksel Deneken**  
- **Alex Styer**  
- **César Ignacio Saucedo**

Nuestro objetivo principal fue aplicar los principios de análisis y diseño de software para construir un sistema robusto, escalable y fácil de mantener, documentado de forma completa en la guía del proyecto incluida.

## 📊 Diagrama de Contexto

El siguiente diagrama muestra cómo interactúan los distintos actores con el **Sistema de Gestión de Pedidos y Clientes para Ventas en Redes Sociales (SMAdmin)**. Este sistema centraliza la información proveniente de redes sociales, clientes, vendedores y administradores, y facilita la gestión de pedidos, descuentos, reportes y análisis.

![Diagrama de Contexto](diagrama_de_contexto.png)

**Figura 1.** Diagrama de Contexto – desarrollado por César Ignacio Saucedo.

## ✅ Requisitos Funcionales

A continuación se listan los requisitos funcionales definidos para el sistema **SMAdmin**. Estos requisitos representan las capacidades clave que el sistema debe cumplir para satisfacer las necesidades organizacionales:

| ID    | Nombre del requisito funcional                | Descripción del requerimiento organizacional que cubre |
|-------|-----------------------------------------------|---------------------------------------------------------|
| RF01  | Gestión de usuarios                           | Permitir al administrador registrar, editar y eliminar usuarios con roles específicos (vendedor o administrador) para controlar el acceso y uso del sistema. |
| RF02  | Carga de condicionantes de búsqueda (Excel)   | Integrar al sistema los archivos de condicionantes que vinculan productos con palabras clave provenientes de redes sociales. |
| RF03  | Procesamiento de comentarios                  | Extraer, analizar y relacionar comentarios de redes sociales con productos registrados mediante los condicionantes de búsqueda. |
| RF04  | Identificación automática                     | Crear automáticamente un cliente con nombre de perfil e ID cuando se detecta interés en un producto desde redes sociales. |
| RF05  | Asignación de vendedores a clientes           | Permitir al administrador asignar un vendedor a cada cliente utilizando un panel desplegable. |
| RF06  | Carga de ediciones externas (Excel)           | Importar archivos Excel con ediciones realizadas fuera del sistema que deben impactar en los pedidos. |
| RF07  | Visualización de pedidos y clientes asignados | Permitir a los vendedores consultar en tiempo real a sus clientes y los pedidos correspondientes. |
| RF08  | Edición de pedidos                             | Permitir que los vendedores modifiquen pedidos: productos, cantidades y descuentos según lo autorizado. |
| RF09  | Generación y descarga de cotizaciones         | Generar documentos en PDF o Excel con el detalle del pedido, aplicando descuentos y mostrando el total final. |
| RF10  | Registro inalterable de modificaciones        | Registrar toda acción realizada sobre el sistema (ediciones, asignaciones, eliminaciones) con trazabilidad completa. |
| RF11  | Generación de reportes de ventas              | Producir reportes que incluyan: ventas por vendedor, pedidos por día, totales con y sin descuento. |
| RF12  | Validación y estructura de archivos Excel     | Validar la estructura y contenido de cada archivo Excel antes de ser procesado, rechazando los que no cumplan el formato requerido. |

## 🧩 Diagrama de Casos de Uso

El siguiente diagrama representa las principales interacciones entre los actores del sistema **SMAdmin** y sus funcionalidades clave. Se identifican los casos de uso necesarios para cubrir los requisitos funcionales del sistema de gestión de pedidos y clientes para ventas en redes sociales.

![Diagrama de Casos de Uso](diagrama_de_casos_de_uso.png)

**Figura 2.** Diagrama de Casos de Uso – elaborado para representar la estructura funcional del sistema.

## 🧮 Tabla de Priorización de Requisitos Funcionales

La siguiente tabla muestra el análisis de priorización de los requisitos funcionales del sistema **SMAdmin**, considerando los criterios de valor, riesgo, complejidad y estabilidad. La prioridad global se establece con base en estos factores para facilitar la planeación del desarrollo.

| ID    | Nombre del requisito                                | Valor | Riesgo | Complejidad | Estabilidad | Prioridad Global |
|-------|------------------------------------------------------|-------|--------|-------------|-------------|------------------|
| RF01  | Gestión de usuarios                                  | Alta  | Baja   | Media       | Alta        | Alta             |
| RF02  | Carga de condicionantes de búsqueda (Excel)          | Alta  | Media  | Alta        | Media       | Alta             |
| RF03  | Procesamiento de comentarios                         | Alta  | Alta   | Alta        | Baja        | Alta             |
| RF04  | Identificación automática de clientes                | Alta  | Alta   | Alta        | Media       | Alta             |
| RF05  | Asignación de vendedores                             | Media | Baja   | Media       | Alta        | Media            |
| RF06  | Carga de ediciones externas (Excel)                  | Alta  | Media  | Media       | Media       | Alta             |
| RF07  | Visualización de pedidos/clientes asignados          | Alta  | Baja   | Media       | Alta        | Alta             |
| RF08  | Edición de pedidos                                   | Alta  | Alta   | Alta        | Media       | Alta             |
| RF09  | Generación y descarga de cotizaciones                | Alta  | Media  | Media       | Alta        | Alta             |
| RF10  | Registro inalterable de modificaciones               | Media | Baja   | Media       | Alta        | Media            |
| RF11  | Generación de reportes de ventas                     | Media | Media  | Baja        | Alta        | Media            |
| RF12  | Validación de archivos Excel                         | Alta  | Media  | Alta        | Alta        | Alta             |



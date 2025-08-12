
# Diseño del Sistema CRM Inmobiliario Automatizado

## 1. Introducción

El presente documento detalla el diseño arquitectónico de un sistema CRM inmobiliario automatizado, cuyo objetivo principal es maximizar la conversión de leads a visitas presenciales de proyectos inmobiliarios. Este sistema integrará diversas herramientas digitales para optimizar la gestión de prospectos desde su origen en redes sociales hasta el cierre de la venta, enfocándose en la eficiencia del proceso comercial mediante la automatización inteligente.

## 2. Requisitos del Sistema

Basado en la situación, tarea, objetivo, conocimiento, instrucciones específicas y restricciones proporcionadas, se han identificado los siguientes requisitos clave:

### 2.1. Funcionalidades Principales

*   **Registro Automático de Leads:** Los leads generados en redes sociales deben registrarse automáticamente en Google Sheets.
*   **Respuestas Automáticas por WhatsApp Business:** Generación de respuestas personalizadas y automáticas a través de WhatsApp Business API, utilizando un repositorio de preguntas frecuentes.
*   **Actualización de Estado de Leads en Tiempo Real:** El estado de los leads debe actualizarse automáticamente en Google Sheets después de cada interacción.
*   **Agendamiento de Visitas en Google Calendar:** Capacidad para agendar visitas presenciales directamente en Google Calendar.
*   **Visualización del Embudo de Ventas:** Un dashboard visual que muestre el estado de los leads en el embudo de ventas, clasificados por etapas y con código de colores pastel.
*   **Gestión de Repositorio de Preguntas Frecuentes (FAQ):** Utilización de un repositorio de 20 preguntas frecuentes para generar respuestas personalizadas.
*   **Seguimiento Detallado de Interacciones:** Mantenimiento de un registro histórico de todas las interacciones con cada lead.

### 2.2. Criterios de Clasificación y Priorización de Leads

*   **Análisis de Leads:** Cada lead debe ser analizado con criterios definidos por el embudo de ventas.
*   **Clasificación por Etapa:** Los leads deben clasificarse en las siguientes etapas del embudo de ventas: Prospecto, Interesado, Visita Programada, Cotización y Cierre.
*   **Código de Colores Pastel:** Cada etapa del embudo debe asociarse con un código de colores pastel para la visualización.
*   **Priorización:** Los leads con mayor potencial de conversión deben ser priorizados.

### 2.3. Comunicación y Restricciones

*   **Comunicación Profesional y Amigable:** Todas las comunicaciones deben mantener un tono profesional y amigable.
*   **Privacidad de Datos:** Respeto estricto de la privacidad de los datos de los leads.
*   **Evitar Spam:** Prohibición de spam o comunicaciones no deseadas.
*   **Registro de Métricas:** Registro de métricas de efectividad del sistema.
*   **Uso de Información del Proyecto:** Utilización exclusiva de información específica del proyecto de la carpeta de datos proporcionada.

### 2.4. Formato de Respuesta WhatsApp

*   Mensaje inicial personalizado.
*   Información concreta del proyecto.
*   Call-to-action para agendar visita.
*   Opción de más información.
*   Referencia a preguntas frecuentes.

### 2.5. Consideraciones Técnicas

*   **Integración Fluida:** Integración sin problemas entre todas las plataformas (Google Sheets, N8N, WhatsApp Business API, Google Calendar).
*   **Respaldo de Información:** Mecanismos para el respaldo de la información.
*   **Escalabilidad:** El sistema debe ser escalable para manejar un volumen creciente de leads.
*   **Mínima Intervención Manual:** Reducción al mínimo de la intervención manual en el proceso.

## 3. Arquitectura del Sistema

El sistema se basará en una arquitectura modular, permitiendo la integración de componentes especializados para cada funcionalidad. La herramienta central de automatización será N8N, que actuará como orquestador de los flujos de trabajo.

### 3.1. Componentes Principales

*   **Redes Sociales (Fuente de Leads):** Plataformas como Facebook, Instagram, etc., donde se generarán los leads.
*   **Google Sheets (Base de Datos de Leads y FAQ):** Servirá como la base de datos principal para almacenar la información de los leads, su estado, historial de interacciones y el repositorio de preguntas frecuentes.
*   **N8N (Motor de Automatización):** Plataforma de automatización de código abierto que conectará todas las herramientas y orquestará los flujos de trabajo.
*   **WhatsApp Business API (Canal de Comunicación):** Permitirá el envío y recepción de mensajes automatizados y personalizados con los leads.
*   **Google Calendar (Agendamiento de Visitas):** Gestionará la programación de las visitas presenciales a los proyectos.
*   **Dashboard de Visualización (Interfaz de Usuario):** Una interfaz web o una hoja de cálculo avanzada en Google Sheets para visualizar el embudo de ventas y las métricas clave.

### 3.2. Flujo de Datos y Procesos

El flujo de datos y procesos se puede describir en las siguientes etapas:

#### 3.2.1. Captura y Registro de Leads

1.  **Generación de Lead:** Un usuario interactúa con un anuncio o contenido en redes sociales, generando un lead.
2.  **Webhook/Integración Directa:** La información del lead (nombre, contacto, interés) es capturada y enviada a N8N a través de un webhook o una integración directa de la plataforma de redes sociales.
3.  **Registro en Google Sheets:** N8N recibe la información del lead y la registra automáticamente en una nueva fila en la hoja de cálculo de Google Sheets designada para leads. Se asigna un estado inicial de 'Prospecto'.

#### 3.2.2. Interacción Inicial y Clasificación

1.  **Activación de Flujo de WhatsApp:** Una vez registrado el lead en Google Sheets, N8N activa un flujo para enviar un mensaje inicial personalizado a través de WhatsApp Business API.
2.  **Respuesta Automática:** El mensaje incluirá información del proyecto, un call-to-action para agendar una visita y una opción para más información (referencia a FAQ).
3.  **Análisis de Respuesta del Lead:** N8N monitorea las respuestas del lead en WhatsApp. Utilizará procesamiento de lenguaje natural (NLP) básico o reglas predefinidas para interpretar la intención del lead.
4.  **Actualización de Estado:** Basado en la respuesta, N8N actualiza el estado del lead en Google Sheets a 'Interesado' si muestra interés en el proyecto o en agendar una visita.

#### 3.2.3. Gestión de Preguntas Frecuentes (FAQ)

1.  **Consulta de FAQ:** Si el lead solicita más información o hace una pregunta, N8N consultará el repositorio de preguntas frecuentes almacenado en Google Sheets.
2.  **Generación de Respuesta Personalizada:** N8N seleccionará la respuesta más relevante del FAQ y la enviará al lead a través de WhatsApp Business API. Si la pregunta no está en el FAQ, se puede escalar para intervención manual o una respuesta genérica.

#### 3.2.4. Agendamiento de Visitas

1.  **Solicitud de Visita:** Si el lead expresa interés en agendar una visita, N8N iniciará el proceso de agendamiento.
2.  **Disponibilidad en Google Calendar:** N8N consultará la disponibilidad en el Google Calendar del equipo de ventas.
3.  **Confirmación y Agendamiento:** N8N propondrá horarios al lead vía WhatsApp. Una vez confirmado, N8N creará un evento en Google Calendar con los detalles de la visita y el lead. El estado del lead en Google Sheets se actualizará a 'Visita Programada'.

#### 3.2.5. Seguimiento y Actualización Continua

1.  **Registro de Interacciones:** Cada interacción (mensaje enviado/recibido, actualización de estado, agendamiento) se registrará en un historial de interacciones asociado al lead en Google Sheets.
2.  **Actualización de Etapas:** El equipo de ventas o N8N (basado en acciones como la realización de la visita o el envío de una cotización) actualizará el estado del lead a 'Cotización' o 'Cierre' en Google Sheets.

#### 3.2.6. Visualización del Embudo de Ventas

1.  **Extracción de Datos:** El dashboard de visualización extraerá los datos de los leads y sus estados de Google Sheets.
2.  **Representación Visual:** Los leads se mostrarán en el embudo de ventas, clasificados por etapa y con el código de colores pastel definido. Esto permitirá una visión rápida del progreso de los leads y la identificación de cuellos de botella.

## 4. Estructura de Datos (Google Sheets)

Se propondrán las siguientes hojas de cálculo y columnas en Google Sheets:

### 4.1. Hoja: `Leads`

Esta hoja contendrá la información principal de cada lead.

| Columna             | Tipo de Dato | Descripción                                                              | Ejemplo                                   |
| :------------------ | :----------- | :----------------------------------------------------------------------- | :---------------------------------------- |
| `ID_Lead`           | Texto        | Identificador único del lead (generado automáticamente)                  | `LEAD-20250812-001`                       |
| `Fecha_Registro`    | Fecha/Hora   | Fecha y hora en que el lead fue registrado                               | `2025-08-12 10:30:00`                     |
| `Nombre_Lead`       | Texto        | Nombre completo del lead                                                 | `Juan Pérez`                              |
| `Telefono_WhatsApp` | Texto        | Número de teléfono del lead con código de país                           | `+5215512345678`                          |
| `Origen_Lead`       | Texto        | Plataforma de redes sociales de donde proviene el lead                   | `Facebook Ads`                            |
| `Interes_Inicial`   | Texto        | Descripción del interés inicial del lead (ej. proyecto específico)       | `Proyecto 


Residencial Sol`                        |
| `Etapa_Embudo`      | Texto        | Etapa actual del lead en el embudo de ventas                             | `Prospecto`                               |
| `Color_Embudo`      | Texto        | Código de color pastel asociado a la etapa del embudo                    | `#FFD1DC` (Rosa Pastel)                    |
| `Prioridad`         | Texto        | Nivel de prioridad del lead (Alto, Medio, Bajo)                          | `Medio`                                   |
| `Ultima_Interaccion`| Fecha/Hora   | Fecha y hora de la última interacción con el lead                        | `2025-08-12 11:00:00`                     |
| `Notas`             | Texto Largo  | Campo para notas adicionales sobre el lead                               | `Interesado en 3 recámaras.`              |

### 4.2. Hoja: `Interacciones`

Esta hoja registrará todas las interacciones con los leads, permitiendo un seguimiento detallado.

| Columna             | Tipo de Dato | Descripción                                                              | Ejemplo                                   |
| :------------------ | :----------- | :----------------------------------------------------------------------- | :---------------------------------------- |
| `ID_Interaccion`    | Texto        | Identificador único de la interacción (generado automáticamente)         | `INT-20250812-001`                        |
| `ID_Lead`           | Texto        | Referencia al `ID_Lead` de la hoja `Leads`                               | `LEAD-20250812-001`                       |
| `Fecha_Hora`        | Fecha/Hora   | Fecha y hora de la interacción                                           | `2025-08-12 11:00:00`                     |
| `Tipo_Interaccion`  | Texto        | Tipo de interacción (WhatsApp, Llamada, Email, Visita)                   | `WhatsApp`                                |
| `Contenido`         | Texto Largo  | Contenido del mensaje o resumen de la interacción                        | `Mensaje inicial enviado.`                |
| `Remitente`         | Texto        | Quién inició la interacción (Sistema, Lead, Agente)                      | `Sistema`                                 |
| `Estado_Actualizado`| Texto        | Nuevo estado del lead después de la interacción (si aplica)              | `Interesado`                              |

### 4.3. Hoja: `FAQ`

Esta hoja contendrá el repositorio de preguntas frecuentes y sus respuestas asociadas.

| Columna             | Tipo de Dato | Descripción                                                              | Ejemplo                                   |
| :------------------ | :----------- | :----------------------------------------------------------------------- | :---------------------------------------- |
| `ID_Pregunta`       | Texto        | Identificador único de la pregunta                                       | `FAQ-001`                                 |
| `Pregunta`          | Texto Largo  | Texto completo de la pregunta frecuente                                  | `¿Cuál es el precio de las viviendas?`    |
| `Respuesta`         | Texto Largo  | Respuesta detallada a la pregunta                                        | `Los precios varían según el modelo...`   |
| `Palabras_Clave`    | Texto        | Palabras clave asociadas a la pregunta para facilitar la búsqueda        | `precio, costo, valor, inversión`         |

## 5. Integraciones Clave

### 5.1. N8N

N8N será el orquestador principal de todas las automatizaciones. Se configurarán los siguientes flujos de trabajo (workflows):

*   **Workflow 1: Captura y Registro de Leads:**
    *   **Trigger:** Webhook (para recibir datos de redes sociales) o módulo de integración directa con la plataforma de redes sociales.
    *   **Acción:** Añadir fila en Google Sheets (`Leads` hoja).
    *   **Acción:** Añadir fila en Google Sheets (`Interacciones` hoja) para registrar el registro del lead.
    *   **Acción:** Activar Workflow 2 (Envío de Mensaje Inicial WhatsApp).

*   **Workflow 2: Envío de Mensaje Inicial WhatsApp y Clasificación:**
    *   **Trigger:** Activado por Workflow 1 o por un nuevo lead en Google Sheets.
    *   **Acción:** Enviar mensaje a WhatsApp Business API (utilizando la plantilla definida).
    *   **Acción:** Esperar respuesta del lead (webhook de WhatsApp Business API).
    *   **Acción:** Procesar respuesta del lead (condicionales basadas en palabras clave o intención).
    *   **Acción:** Actualizar fila en Google Sheets (`Leads` hoja) para cambiar `Etapa_Embudo` y `Color_Embudo`.
    *   **Acción:** Añadir fila en Google Sheets (`Interacciones` hoja) para registrar el mensaje enviado y la respuesta del lead.

*   **Workflow 3: Gestión de FAQ por WhatsApp:**
    *   **Trigger:** Recepción de mensaje en WhatsApp Business API con una pregunta.
    *   **Acción:** Buscar en Google Sheets (`FAQ` hoja) la respuesta más relevante basada en palabras clave del mensaje.
    *   **Acción:** Enviar respuesta al lead vía WhatsApp Business API.
    *   **Acción:** Añadir fila en Google Sheets (`Interacciones` hoja).

*   **Workflow 4: Agendamiento de Visitas:**
    *   **Trigger:** Detección de intención de agendar visita en WhatsApp o acción manual.
    *   **Acción:** Consultar disponibilidad en Google Calendar.
    *   **Acción:** Proponer horarios al lead vía WhatsApp.
    *   **Acción:** Esperar confirmación del lead.
    *   **Acción:** Crear evento en Google Calendar.
    *   **Acción:** Actualizar fila en Google Sheets (`Leads` hoja) a `Visita Programada`.
    *   **Acción:** Añadir fila en Google Sheets (`Interacciones` hoja).

*   **Workflow 5: Actualización Manual/Automática de Etapas:**
    *   **Trigger:** Actualización manual en Google Sheets o evento externo (ej. visita realizada).
    *   **Acción:** Actualizar `Etapa_Embudo` y `Color_Embudo` en Google Sheets (`Leads` hoja).
    *   **Acción:** Añadir fila en Google Sheets (`Interacciones` hoja).

### 5.2. WhatsApp Business API

La integración con WhatsApp Business API se realizará a través de N8N. Se requerirá la configuración de plantillas de mensajes pre-aprobadas para las comunicaciones iniciales y de seguimiento. La API permitirá:

*   Envío de mensajes de texto, imágenes y documentos.
*   Recepción de mensajes de los leads.
*   Configuración de webhooks para notificaciones en tiempo real a N8N.

### 5.3. Google Calendar

La integración con Google Calendar permitirá:

*   Consultar la disponibilidad de los agentes de ventas.
*   Crear eventos de visitas con detalles del lead y del proyecto.
*   Enviar recordatorios automáticos a los leads y agentes.

## 6. Visualización del Embudo de Ventas

El dashboard de visualización se puede implementar de varias maneras, siendo la más sencilla y accesible una hoja de cálculo avanzada en Google Sheets o una herramienta de BI conectada a Google Sheets. La visualización incluirá:

*   **Gráfico de Embudo:** Un gráfico que muestre el número de leads en cada etapa del embudo.
*   **Tabla de Leads:** Una tabla dinámica que permita filtrar y ordenar leads por etapa, prioridad, fecha de última interacción, etc.
*   **Código de Colores Pastel:** Cada etapa del embudo tendrá un color pastel asignado para una identificación visual rápida:
    *   **Prospecto:** `#ADD8E6` (Azul Claro)
    *   **Interesado:** `#90EE90` (Verde Claro)
    *   **Visita Programada:** `#FFD700` (Dorado)
    *   **Cotización:** `#FFA07A` (Salmón Claro)
    *   **Cierre:** `#DDA0DD` (Ciruela Claro)

## 7. Consideraciones Adicionales

### 7.1. Repositorio de Preguntas Frecuentes (FAQ)

El repositorio de FAQ se almacenará en la hoja `FAQ` de Google Sheets. Será crucial mantener este repositorio actualizado y expandirlo con nuevas preguntas a medida que surjan. La lógica de búsqueda de respuestas en N8N deberá ser robusta, utilizando palabras clave y, si es posible, una lógica de coincidencia difusa para mejorar la precisión.

### 7.2. Carpeta de Datos del Proyecto

La información específica del proyecto (imágenes, brochures, planos, etc.) se almacenará en una carpeta de Google Drive o similar. N8N podrá acceder a estos recursos para adjuntarlos en las respuestas de WhatsApp cuando sea necesario.

### 7.3. Métricas de Efectividad

Se registrarán las siguientes métricas para evaluar la efectividad del sistema:

*   Número de leads generados por fuente.
*   Tasas de conversión entre cada etapa del embudo.
*   Tiempo promedio de conversión de lead a visita.
*   Número de visitas programadas y realizadas.
*   Número de cotizaciones y cierres.
*   Tiempo de respuesta promedio a los leads.

### 7.4. Escalabilidad y Mantenimiento

El uso de Google Sheets y N8N (que puede ser auto-hospedado o en la nube) proporciona una buena base para la escalabilidad. El mantenimiento incluirá la actualización de las plantillas de WhatsApp, la expansión del FAQ y la monitorización de los flujos de N8N para asegurar su correcto funcionamiento.

## 8. Conclusión

Este diseño propone un sistema CRM inmobiliario automatizado robusto y eficiente, capaz de gestionar leads desde su origen en redes sociales hasta la conversión en visitas presenciales. La integración de Google Sheets, N8N, WhatsApp Business API y Google Calendar, junto con un dashboard de visualización, permitirá una gestión inteligente y una optimización continua del proceso comercial.


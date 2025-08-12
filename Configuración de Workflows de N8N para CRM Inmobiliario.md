# Configuración de Workflows de N8N para CRM Inmobiliario

## Introducción

Este documento proporciona las configuraciones detalladas para los workflows de N8N que automatizarán el sistema CRM inmobiliario. Cada workflow está diseñado para manejar una parte específica del proceso de gestión de leads, desde la captura inicial hasta la conversión en visitas programadas.

## Prerequisitos

Antes de configurar los workflows, asegúrate de tener:

1. **N8N instalado y configurado** (puede ser la versión cloud o self-hosted)
2. **Credenciales configuradas** para:
   - Google Sheets API
   - WhatsApp Business API
   - Google Calendar API
3. **URLs de webhook** configuradas para recibir datos de redes sociales
4. **Hoja de cálculo de Google Sheets** creada con las hojas: Leads, Interacciones, FAQ

## Workflow 1: Captura y Registro de Leads

### Propósito
Recibir leads de redes sociales y registrarlos automáticamente en Google Sheets.

### Configuración del Workflow

#### Nodo 1: Webhook (Trigger)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/lead-capture`
- **Configuración:**
  ```json
  {
    "httpMethod": "POST",
    "path": "lead-capture",
    "responseMode": "responseNode",
    "options": {}
  }
  ```

#### Nodo 2: Generar ID de Lead
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
  const timeStr = now.toTimeString().slice(0, 8).replace(/:/g, '');
  const leadId = `LEAD-${dateStr}-${timeStr}`;
  
  return [{
    json: {
      ...items[0].json,
      ID_Lead: leadId,
      Fecha_Registro: now.toISOString(),
      Etapa_Embudo: 'Prospecto',
      Color_Embudo: '#ADD8E6',
      Prioridad: 'Medio',
      Ultima_Interaccion: now.toISOString()
    }
  }];
  ```

#### Nodo 3: Agregar Lead a Google Sheets
- **Tipo:** Google Sheets
- **Operación:** Append
- **Configuración:**
  - **Spreadsheet ID:** [ID de tu hoja de cálculo]
  - **Sheet:** Leads
  - **Mapeo de columnas:**
    ```json
    {
      "ID_Lead": "={{$json.ID_Lead}}",
      "Fecha_Registro": "={{$json.Fecha_Registro}}",
      "Nombre_Lead": "={{$json.Nombre_Lead}}",
      "Telefono_WhatsApp": "={{$json.Telefono_WhatsApp}}",
      "Origen_Lead": "={{$json.Origen_Lead}}",
      "Interes_Inicial": "={{$json.Interes_Inicial}}",
      "Etapa_Embudo": "={{$json.Etapa_Embudo}}",
      "Color_Embudo": "={{$json.Color_Embudo}}",
      "Prioridad": "={{$json.Prioridad}}",
      "Ultima_Interaccion": "={{$json.Ultima_Interaccion}}",
      "Notas": "={{$json.Notas || ''}}"
    }
    ```

#### Nodo 4: Registrar Interacción Inicial
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const now = new Date();
  const interactionId = `INT-${now.toISOString().slice(0, 10).replace(/-/g, '')}-${now.toTimeString().slice(0, 8).replace(/:/g, '')}`;
  
  return [{
    json: {
      ID_Interaccion: interactionId,
      ID_Lead: items[0].json.ID_Lead,
      Fecha_Hora: now.toISOString(),
      Tipo_Interaccion: 'Sistema',
      Contenido: 'Lead registrado automáticamente desde ' + items[0].json.Origen_Lead,
      Remitente: 'Sistema',
      Estado_Actualizado: 'Prospecto'
    }
  }];
  ```

#### Nodo 5: Agregar Interacción a Google Sheets
- **Tipo:** Google Sheets
- **Operación:** Append
- **Configuración:**
  - **Spreadsheet ID:** [ID de tu hoja de cálculo]
  - **Sheet:** Interacciones
  - **Mapeo de columnas:** Mapear todos los campos del nodo anterior

#### Nodo 6: Activar Workflow de WhatsApp
- **Tipo:** HTTP Request
- **Método:** POST
- **URL:** `http://localhost:5678/webhook/whatsapp-initial`
- **Body:**
  ```json
  {
    "ID_Lead": "={{$json.ID_Lead}}",
    "Telefono_WhatsApp": "={{$json.Telefono_WhatsApp}}",
    "Nombre_Lead": "={{$json.Nombre_Lead}}"
  }
  ```

#### Nodo 7: Respuesta del Webhook
- **Tipo:** Respond to Webhook
- **Configuración:**
  ```json
  {
    "status": 200,
    "message": "Lead registrado exitosamente",
    "leadId": "={{$json.ID_Lead}}"
  }
  ```

## Workflow 2: Envío de Mensaje Inicial WhatsApp y Clasificación

### Propósito
Enviar mensaje inicial personalizado por WhatsApp y clasificar leads según sus respuestas.

### Configuración del Workflow

#### Nodo 1: Webhook (Trigger)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/whatsapp-initial`

#### Nodo 2: Obtener Datos del Lead
- **Tipo:** Google Sheets
- **Operación:** Lookup
- **Configuración:**
  - **Spreadsheet ID:** [ID de tu hoja de cálculo]
  - **Sheet:** Leads
  - **Lookup Column:** ID_Lead
  - **Lookup Value:** `={{$json.ID_Lead}}`

#### Nodo 3: Generar Mensaje Personalizado
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const nombre = items[0].json.Nombre_Lead;
  const interes = items[0].json.Interes_Inicial || 'nuestro proyecto inmobiliario';
  
  const mensaje = `¡Hola ${nombre}! 👋
  
  Gracias por tu interés en ${interes}. Estamos emocionados de poder ayudarte a encontrar tu hogar ideal.
  
  🏠 Te invitamos a conocer nuestro proyecto con:
  ✅ Ubicación privilegiada
  ✅ Acabados de primera calidad
  ✅ Amenidades exclusivas
  ✅ Financiamiento disponible
  
  ¿Te gustaría agendar una visita para conocer el proyecto? 📅
  
  También puedes escribir "INFO" para recibir más detalles o hacer cualquier pregunta que tengas.
  
  ¡Esperamos conocerte pronto! 🏡`;
  
  return [{
    json: {
      ...items[0].json,
      mensaje_whatsapp: mensaje
    }
  }];
  ```

#### Nodo 4: Enviar Mensaje WhatsApp
- **Tipo:** HTTP Request
- **Método:** POST
- **URL:** `https://graph.facebook.com/v17.0/[PHONE_NUMBER_ID]/messages`
- **Headers:**
  ```json
  {
    "Authorization": "Bearer [ACCESS_TOKEN]",
    "Content-Type": "application/json"
  }
  ```
- **Body:**
  ```json
  {
    "messaging_product": "whatsapp",
    "to": "={{$json.Telefono_WhatsApp}}",
    "type": "text",
    "text": {
      "body": "={{$json.mensaje_whatsapp}}"
    }
  }
  ```

#### Nodo 5: Registrar Mensaje Enviado
- **Tipo:** Code (JavaScript) + Google Sheets Append
- **Propósito:** Registrar la interacción en la hoja Interacciones

#### Nodo 6: Webhook para Respuestas (Trigger separado)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/whatsapp-response`
- **Configuración:** Recibe respuestas de WhatsApp Business API

#### Nodo 7: Procesar Respuesta del Lead
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const mensaje = items[0].json.message.text.body.toLowerCase();
  let nuevaEtapa = 'Prospecto';
  let nuevoColor = '#ADD8E6';
  
  // Palabras clave para clasificar interés
  const palabrasInteres = ['si', 'sí', 'interesa', 'visita', 'agendar', 'cuando', 'horario', 'disponible'];
  const palabrasInfo = ['info', 'información', 'detalles', 'precio', 'costo', 'ubicación'];
  
  if (palabrasInteres.some(palabra => mensaje.includes(palabra))) {
    nuevaEtapa = 'Interesado';
    nuevoColor = '#90EE90';
  } else if (palabrasInfo.some(palabra => mensaje.includes(palabra))) {
    nuevaEtapa = 'Interesado';
    nuevoColor = '#90EE90';
  }
  
  return [{
    json: {
      ...items[0].json,
      nueva_etapa: nuevaEtapa,
      nuevo_color: nuevoColor,
      respuesta_lead: mensaje
    }
  }];
  ```

#### Nodo 8: Actualizar Estado en Google Sheets
- **Tipo:** Google Sheets
- **Operación:** Update
- **Configuración:** Actualizar la etapa del lead basada en la respuesta

## Workflow 3: Gestión de FAQ por WhatsApp

### Propósito
Responder automáticamente preguntas frecuentes basadas en el repositorio de FAQ.

### Configuración del Workflow

#### Nodo 1: Webhook (Trigger)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/faq-query`

#### Nodo 2: Obtener FAQ de Google Sheets
- **Tipo:** Google Sheets
- **Operación:** Read
- **Configuración:**
  - **Spreadsheet ID:** [ID de tu hoja de cálculo]
  - **Sheet:** FAQ

#### Nodo 3: Buscar Respuesta Relevante
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const preguntaUsuario = items[0].json.message.text.body.toLowerCase();
  const faqs = items.slice(1); // Todos los FAQs excepto el primer item (que es la pregunta)
  
  let mejorCoincidencia = null;
  let mayorPuntuacion = 0;
  
  faqs.forEach(faq => {
    const palabrasClave = faq.json.Palabras_Clave.toLowerCase().split(',');
    let puntuacion = 0;
    
    palabrasClave.forEach(palabra => {
      if (preguntaUsuario.includes(palabra.trim())) {
        puntuacion++;
      }
    });
    
    if (puntuacion > mayorPuntuacion) {
      mayorPuntuacion = puntuacion;
      mejorCoincidencia = faq.json;
    }
  });
  
  return [{
    json: {
      ...items[0].json,
      respuesta_faq: mejorCoincidencia ? mejorCoincidencia.Respuesta : 'Lo siento, no tengo información específica sobre esa pregunta. Un agente se pondrá en contacto contigo pronto.',
      coincidencia_encontrada: mejorCoincidencia !== null
    }
  }];
  ```

#### Nodo 4: Enviar Respuesta por WhatsApp
- **Tipo:** HTTP Request
- **Configuración:** Similar al nodo de envío de WhatsApp anterior

## Workflow 4: Agendamiento de Visitas

### Propósito
Gestionar el agendamiento de visitas en Google Calendar.

### Configuración del Workflow

#### Nodo 1: Webhook (Trigger)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/schedule-visit`

#### Nodo 2: Consultar Disponibilidad en Google Calendar
- **Tipo:** Google Calendar
- **Operación:** Get Events
- **Configuración:**
  - **Calendar ID:** [ID del calendario de ventas]
  - **Time Min:** Fecha actual
  - **Time Max:** Fecha actual + 30 días

#### Nodo 3: Generar Horarios Disponibles
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  // Lógica para generar horarios disponibles basada en eventos existentes
  const eventos = items.slice(1);
  const horariosDisponibles = [];
  
  // Generar horarios de 9 AM a 6 PM, lunes a sábado
  for (let dia = 1; dia <= 7; dia++) {
    const fecha = new Date();
    fecha.setDate(fecha.getDate() + dia);
    
    if (fecha.getDay() !== 0) { // No domingos
      for (let hora = 9; hora <= 18; hora += 2) {
        const horario = new Date(fecha);
        horario.setHours(hora, 0, 0, 0);
        
        // Verificar si el horario está ocupado
        const ocupado = eventos.some(evento => {
          const inicioEvento = new Date(evento.json.start.dateTime);
          return Math.abs(horario - inicioEvento) < 2 * 60 * 60 * 1000; // 2 horas de diferencia
        });
        
        if (!ocupado) {
          horariosDisponibles.push({
            fecha: horario.toLocaleDateString('es-ES'),
            hora: horario.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
            datetime: horario.toISOString()
          });
        }
      }
    }
  }
  
  return [{
    json: {
      ...items[0].json,
      horarios_disponibles: horariosDisponibles.slice(0, 6) // Primeros 6 horarios
    }
  }];
  ```

#### Nodo 4: Enviar Opciones de Horarios por WhatsApp
- **Tipo:** Code (JavaScript) + HTTP Request
- **Código para generar mensaje:**
  ```javascript
  const horarios = items[0].json.horarios_disponibles;
  let mensaje = `¡Perfecto! Tenemos los siguientes horarios disponibles para tu visita:\n\n`;
  
  horarios.forEach((horario, index) => {
    mensaje += `${index + 1}. ${horario.fecha} a las ${horario.hora}\n`;
  });
  
  mensaje += `\nPor favor, responde con el número del horario que prefieras (ejemplo: "1" para la primera opción).`;
  
  return [{
    json: {
      ...items[0].json,
      mensaje_horarios: mensaje
    }
  }];
  ```

#### Nodo 5: Procesar Confirmación de Horario
- **Tipo:** Webhook (Trigger separado) + Code (JavaScript)
- **Propósito:** Recibir la selección del lead y crear el evento en Google Calendar

#### Nodo 6: Crear Evento en Google Calendar
- **Tipo:** Google Calendar
- **Operación:** Create Event
- **Configuración:**
  ```json
  {
    "summary": "Visita - {{$json.Nombre_Lead}}",
    "description": "Visita programada para el lead {{$json.ID_Lead}}\nTeléfono: {{$json.Telefono_WhatsApp}}\nInterés: {{$json.Interes_Inicial}}",
    "start": {
      "dateTime": "{{$json.fecha_seleccionada}}",
      "timeZone": "America/Mexico_City"
    },
    "end": {
      "dateTime": "{{$json.fecha_fin}}",
      "timeZone": "America/Mexico_City"
    },
    "attendees": [
      {
        "email": "ventas@inmobiliaria.com"
      }
    ]
  }
  ```

#### Nodo 7: Actualizar Estado del Lead
- **Tipo:** Google Sheets
- **Operación:** Update
- **Configuración:** Cambiar etapa a "Visita Programada" y color a "#FFD700"

## Workflow 5: Actualización Manual/Automática de Etapas

### Propósito
Permitir actualizaciones manuales o automáticas del estado de los leads.

### Configuración del Workflow

#### Nodo 1: Webhook (Trigger)
- **Tipo:** Webhook
- **Método HTTP:** POST
- **Ruta:** `/webhook/update-lead-status`

#### Nodo 2: Validar Datos de Entrada
- **Tipo:** Code (JavaScript)
- **Código:**
  ```javascript
  const etapasValidas = ['Prospecto', 'Interesado', 'Visita Programada', 'Cotización', 'Cierre'];
  const colores = {
    'Prospecto': '#ADD8E6',
    'Interesado': '#90EE90',
    'Visita Programada': '#FFD700',
    'Cotización': '#FFA07A',
    'Cierre': '#DDA0DD'
  };
  
  const nuevaEtapa = items[0].json.nueva_etapa;
  
  if (!etapasValidas.includes(nuevaEtapa)) {
    throw new Error('Etapa no válida');
  }
  
  return [{
    json: {
      ...items[0].json,
      color_embudo: colores[nuevaEtapa],
      fecha_actualizacion: new Date().toISOString()
    }
  }];
  ```

#### Nodo 3: Actualizar Lead en Google Sheets
- **Tipo:** Google Sheets
- **Operación:** Update
- **Configuración:** Actualizar etapa, color y fecha de última interacción

#### Nodo 4: Registrar Interacción de Actualización
- **Tipo:** Google Sheets
- **Operación:** Append
- **Configuración:** Agregar registro en hoja Interacciones

## Consideraciones de Implementación

### Seguridad
- Configurar autenticación adecuada para todos los webhooks
- Usar HTTPS para todas las comunicaciones
- Validar todos los datos de entrada

### Monitoreo
- Configurar logs detallados en N8N
- Implementar alertas para errores en workflows
- Monitorear tasas de éxito de cada workflow

### Escalabilidad
- Configurar límites de rate limiting apropiados
- Implementar colas para manejar picos de tráfico
- Considerar la implementación de workflows paralelos para mayor throughput

### Mantenimiento
- Documentar todas las configuraciones
- Implementar versionado de workflows
- Crear backups regulares de las configuraciones de N8N


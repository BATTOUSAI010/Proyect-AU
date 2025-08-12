# Guía de Configuración de N8N para CRM Inmobiliario

## Instalación de N8N

### Opción 1: N8N Cloud (Recomendado para principiantes)
1. Ve a [n8n.cloud](https://n8n.cloud)
2. Crea una cuenta
3. Selecciona un plan (el plan gratuito permite hasta 5,000 ejecuciones por mes)

### Opción 2: Instalación Local con Docker
```bash
# Instalar N8N con Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Opción 3: Instalación con npm
```bash
# Instalar N8N globalmente
npm install n8n -g

# Ejecutar N8N
n8n start
```

## Configuración Inicial

### 1. Acceso a N8N
- Abre tu navegador y ve a `http://localhost:5678` (instalación local) o tu URL de N8N Cloud
- Crea tu cuenta de administrador

### 2. Configuración de Credenciales

#### Google Sheets API
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Google Sheets
4. Crea credenciales (Service Account)
5. Descarga el archivo JSON de credenciales
6. En N8N:
   - Ve a `Settings > Credentials`
   - Añade nueva credencial `Google Sheets API`
   - Sube el archivo JSON o copia el contenido

#### WhatsApp Business API
1. Configura tu cuenta de WhatsApp Business
2. Obtén tu Access Token y Phone Number ID desde Meta for Developers
3. En N8N:
   - Ve a `Settings > Credentials`
   - Añade nueva credencial `HTTP Request`
   - Configura headers de autorización

#### Google Calendar API
1. En Google Cloud Console, habilita la API de Google Calendar
2. Usa las mismas credenciales de Service Account
3. En N8N:
   - Ve a `Settings > Credentials`
   - Añade nueva credencial `Google Calendar API`

## Importación de Workflows

### Método 1: Importar desde archivo JSON
1. Crea los archivos JSON de workflows (proporcionados a continuación)
2. En N8N, ve a `Workflows`
3. Haz clic en `Import from file`
4. Selecciona el archivo JSON

### Método 2: Crear workflows manualmente
Sigue las configuraciones detalladas en `n8n_workflows.md`

## Archivos JSON de Workflows

### Workflow 1: Captura y Registro de Leads
```json
{
  "name": "CRM - Captura y Registro de Leads",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "lead-capture",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "webhook-lead-capture",
      "name": "Webhook Lead Capture",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "jsCode": "const now = new Date();\nconst dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');\nconst timeStr = now.toTimeString().slice(0, 8).replace(/:/g, '');\nconst leadId = `LEAD-${dateStr}-${timeStr}`;\n\nreturn [{\n  json: {\n    ...items[0].json,\n    ID_Lead: leadId,\n    Fecha_Registro: now.toISOString(),\n    Etapa_Embudo: 'Prospecto',\n    Color_Embudo: '#ADD8E6',\n    Prioridad: 'Medio',\n    Ultima_Interaccion: now.toISOString()\n  }\n}];"
      },
      "id": "generate-lead-id",
      "name": "Generate Lead ID",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "operation": "append",
        "documentId": "TU_SPREADSHEET_ID_AQUI",
        "sheetName": "Leads",
        "columnMappings": {
          "mappingMode": "defineBelow",
          "value": {
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
        }
      },
      "id": "add-lead-to-sheets",
      "name": "Add Lead to Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 4,
      "position": [680, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "{\n  \"status\": \"success\",\n  \"message\": \"Lead registrado exitosamente\",\n  \"leadId\": \"={{$json.ID_Lead}}\"\n}"
      },
      "id": "respond-to-webhook",
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [900, 300]
    }
  ],
  "connections": {
    "Webhook Lead Capture": {
      "main": [
        [
          {
            "node": "Generate Lead ID",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Lead ID": {
      "main": [
        [
          {
            "node": "Add Lead to Sheets",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Add Lead to Sheets": {
      "main": [
        [
          {
            "node": "Respond to Webhook",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {},
  "versionId": "1"
}
```

## Configuración de Webhooks

### URLs de Webhook para tu implementación
Una vez que tengas N8N ejecutándose, las URLs de webhook serán:

- **Captura de Leads:** `https://tu-n8n-instance.com/webhook/lead-capture`
- **Respuestas WhatsApp:** `https://tu-n8n-instance.com/webhook/whatsapp-response`
- **Consultas FAQ:** `https://tu-n8n-instance.com/webhook/faq-query`
- **Agendamiento:** `https://tu-n8n-instance.com/webhook/schedule-visit`
- **Actualización de Estado:** `https://tu-n8n-instance.com/webhook/update-lead-status`

### Configuración en Redes Sociales
1. **Facebook/Instagram Ads:**
   - Ve a tu Business Manager
   - Configura el webhook de leads en la configuración de formularios
   - Usa la URL: `https://tu-n8n-instance.com/webhook/lead-capture`

2. **WhatsApp Business API:**
   - Configura el webhook en Meta for Developers
   - URL de webhook: `https://tu-n8n-instance.com/webhook/whatsapp-response`

## Variables de Entorno

Crea un archivo `.env` con las siguientes variables:

```env
# N8N Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=tu_password_seguro

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=tu_spreadsheet_id

# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=tu_access_token
WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id

# Google Calendar
GOOGLE_CALENDAR_ID=tu_calendar_id
```

## Testing de Workflows

### 1. Test de Captura de Leads
```bash
curl -X POST https://tu-n8n-instance.com/webhook/lead-capture \
  -H "Content-Type: application/json" \
  -d '{
    "Nombre_Lead": "Juan Pérez",
    "Telefono_WhatsApp": "+5215512345678",
    "Origen_Lead": "Facebook Ads",
    "Interes_Inicial": "Proyecto Residencial Sol",
    "Notas": "Interesado en 3 recámaras"
  }'
```

### 2. Test de Respuesta WhatsApp
```bash
curl -X POST https://tu-n8n-instance.com/webhook/whatsapp-response \
  -H "Content-Type: application/json" \
  -d '{
    "message": {
      "from": "+5215512345678",
      "text": {
        "body": "Sí, me interesa agendar una visita"
      }
    }
  }'
```

## Monitoreo y Logs

### Configuración de Logs
1. En N8N, ve a `Settings > Log level`
2. Configura el nivel de log a `info` o `debug` para desarrollo
3. Revisa los logs en `Settings > Logs`

### Métricas Importantes
- Número de leads procesados por día
- Tasa de éxito de envío de WhatsApp
- Tiempo de respuesta promedio
- Errores en workflows

## Troubleshooting

### Problemas Comunes

1. **Error de autenticación con Google Sheets:**
   - Verifica que el Service Account tenga permisos en la hoja
   - Asegúrate de que la API esté habilitada

2. **WhatsApp no envía mensajes:**
   - Verifica el Access Token
   - Confirma que el número esté verificado
   - Revisa los límites de rate limiting

3. **Webhook no recibe datos:**
   - Verifica que la URL sea accesible públicamente
   - Confirma que el método HTTP sea correcto
   - Revisa los headers requeridos

### Logs de Debug
Para activar logs detallados:
```bash
# Si usas Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e N8N_LOG_LEVEL=debug \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## Backup y Restauración

### Backup de Workflows
1. Ve a `Settings > Import/Export`
2. Exporta todos los workflows
3. Guarda el archivo JSON en un lugar seguro

### Backup de Credenciales
Las credenciales se almacenan encriptadas. Para hacer backup:
1. Copia la carpeta `~/.n8n` completa
2. O exporta/importa credenciales individualmente

## Escalamiento

### Para mayor volumen de leads:
1. Considera usar N8N con base de datos externa (PostgreSQL)
2. Implementa colas con Redis
3. Usa múltiples instancias de N8N con load balancer
4. Configura auto-scaling en cloud providers

### Optimización de Performance:
1. Usa batch operations para Google Sheets
2. Implementa caching para consultas frecuentes
3. Configura timeouts apropiados
4. Monitorea el uso de memoria y CPU


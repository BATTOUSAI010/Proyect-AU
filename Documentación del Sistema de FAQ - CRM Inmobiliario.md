# Documentación del Sistema de FAQ - CRM Inmobiliario

## Descripción General

El Sistema de FAQ es una aplicación web desarrollada en Flask que proporciona un repositorio inteligente de preguntas frecuentes para el CRM inmobiliario. El sistema incluye funcionalidades de búsqueda avanzada, generación de respuestas personalizadas para WhatsApp y gestión completa del repositorio de conocimiento.

## Características Principales

### 1. Búsqueda Inteligente de FAQ
- **Algoritmo de coincidencia difusa:** Utiliza un sistema de puntuación basado en palabras clave para encontrar las respuestas más relevantes
- **Búsqueda en múltiples campos:** Busca en preguntas, respuestas y palabras clave
- **Resultados ordenados por relevancia:** Los resultados se ordenan por puntuación de coincidencia

### 2. Generación de Respuestas para WhatsApp
- **Respuestas personalizadas:** Incluye el nombre del lead en la respuesta
- **Formato optimizado para WhatsApp:** Utiliza emojis y formato amigable para móviles
- **Call-to-action integrado:** Incluye invitación a agendar visita
- **Respuestas de respaldo:** Proporciona respuesta genérica cuando no encuentra coincidencias específicas

### 3. Gestión del Repositorio
- **Carga desde CSV:** Permite cargar el repositorio completo desde archivo CSV
- **Visualización completa:** Muestra todas las FAQs con sus detalles
- **Estadísticas en tiempo real:** Muestra total de FAQs y fecha de última actualización
- **API RESTful:** Endpoints para integración con otros sistemas

## Repositorio de Preguntas Frecuentes

El sistema incluye 20 preguntas frecuentes específicamente diseñadas para el sector inmobiliario:

### Categorías de Preguntas:
1. **Precios y Financiamiento** (FAQ-001, FAQ-005, FAQ-019)
2. **Amenidades y Servicios** (FAQ-002, FAQ-008, FAQ-015)
3. **Ubicación y Transporte** (FAQ-003, FAQ-014)
4. **Modelos de Vivienda** (FAQ-004, FAQ-007, FAQ-017)
5. **Proceso de Compra** (FAQ-006, FAQ-010, FAQ-012, FAQ-018)
6. **Personalización** (FAQ-009, FAQ-011)
7. **Garantías y Post-venta** (FAQ-013)
8. **Visitas y Agendamiento** (FAQ-016)
9. **Promociones** (FAQ-020)

### Ejemplo de FAQ:
```
ID: FAQ-001
Pregunta: ¿Cuál es el precio de las viviendas?
Respuesta: Los precios de nuestras viviendas varían según el modelo y ubicación. Tenemos opciones desde $2,500,000 MXN hasta $4,800,000 MXN. Ofrecemos planes de financiamiento con enganche desde el 10% y mensualidades accesibles. ¿Te gustaría conocer los detalles de algún modelo en particular?
Palabras Clave: precio,costo,valor,inversión,dinero,cuanto,financiamiento
```

## Arquitectura Técnica

### Backend (Flask)
- **Framework:** Flask con SQLAlchemy
- **Base de datos:** SQLite (fácil de migrar a PostgreSQL/MySQL)
- **Modelos:** FAQ con campos para ID, pregunta, respuesta y palabras clave
- **API RESTful:** Endpoints para búsqueda, gestión y generación de respuestas

### Frontend
- **Tecnología:** HTML5, CSS3, JavaScript vanilla
- **Diseño:** Responsive, optimizado para móviles y desktop
- **UX/UI:** Interfaz moderna con gradientes y animaciones
- **Funcionalidades:** Búsqueda en tiempo real, vista previa de WhatsApp

### Algoritmo de Búsqueda
```python
def search_by_keywords(query):
    query_words = query.lower().split()
    faqs = FAQ.query.all()
    scored_faqs = []
    
    for faq in faqs:
        score = 0
        keywords = [kw.strip().lower() for kw in faq.palabras_clave.split(',')]
        
        # Búsqueda exacta en palabras clave
        for query_word in query_words:
            for keyword in keywords:
                if query_word in keyword or keyword in query_word:
                    score += 2
                elif query_word == keyword:
                    score += 3
        
        # Búsqueda en pregunta y respuesta
        for query_word in query_words:
            if query_word in faq.pregunta.lower():
                score += 1
            if query_word in faq.respuesta.lower():
                score += 1
        
        if score > 0:
            scored_faqs.append((faq, score))
    
    # Ordenar por puntuación descendente
    scored_faqs.sort(key=lambda x: x[1], reverse=True)
    
    return [faq for faq, score in scored_faqs[:3]]  # Top 3 resultados
```

## API Endpoints

### 1. Búsqueda de FAQ
```
POST /api/faq/search
Content-Type: application/json

{
    "query": "¿Cuál es el precio de las casas?"
}

Response:
{
    "found": true,
    "message": "Los precios de nuestras viviendas varían...",
    "question": "¿Cuál es el precio de las viviendas?",
    "results": [...]
}
```

### 2. Generación de Respuesta WhatsApp
```
POST /api/faq/generate-whatsapp-response
Content-Type: application/json

{
    "query": "¿Cuál es el precio?",
    "lead_name": "Juan Pérez"
}

Response:
{
    "found": true,
    "whatsapp_message": "¡Hola Juan Pérez! 👋\n\nLos precios de nuestras viviendas...",
    "original_question": "¿Cuál es el precio de las viviendas?",
    "confidence": "high"
}
```

### 3. Cargar FAQs desde CSV
```
POST /api/faq/load-csv

Response:
{
    "message": "Successfully loaded 20 FAQs from CSV",
    "count": 20
}
```

### 4. Obtener todas las FAQs
```
GET /api/faq/all

Response:
{
    "faqs": [...],
    "total": 20
}
```

## Integración con N8N

El sistema está diseñado para integrarse perfectamente con los workflows de N8N:

### Workflow de FAQ (N8N)
1. **Trigger:** Recepción de mensaje en WhatsApp
2. **Procesamiento:** Llamada a `/api/faq/generate-whatsapp-response`
3. **Respuesta:** Envío automático de respuesta personalizada
4. **Registro:** Almacenamiento de interacción en Google Sheets

### Ejemplo de integración:
```javascript
// Nodo de N8N para consultar FAQ
const response = await fetch('http://localhost:5000/api/faq/generate-whatsapp-response', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: items[0].json.message.text.body,
        lead_name: items[0].json.lead_name
    })
});

const faqResponse = await response.json();
return [{ json: { ...items[0].json, whatsapp_response: faqResponse.whatsapp_message } }];
```

## Mantenimiento y Actualización

### Agregar nuevas FAQs
1. **Vía API:** Usar endpoint `POST /api/faq/add`
2. **Vía CSV:** Actualizar archivo CSV y usar `POST /api/faq/load-csv`
3. **Vía interfaz web:** Funcionalidad de administración (próxima versión)

### Actualizar FAQs existentes
1. **Vía API:** Usar endpoint `PUT /api/faq/update/<id_pregunta>`
2. **Vía CSV:** Modificar archivo y recargar

### Monitoreo
- **Logs de Flask:** Registro de todas las consultas y respuestas
- **Métricas de uso:** Tracking de preguntas más frecuentes
- **Análisis de efectividad:** Medición de precisión de respuestas

## Escalabilidad

### Optimizaciones implementadas:
1. **Índices de base de datos:** En campos de búsqueda frecuente
2. **Caché de resultados:** Para consultas repetidas
3. **Búsqueda optimizada:** Algoritmo eficiente de coincidencia

### Mejoras futuras:
1. **Procesamiento de lenguaje natural:** Integración con modelos de IA
2. **Aprendizaje automático:** Mejora automática de respuestas
3. **Análisis de sentimientos:** Clasificación de consultas por urgencia
4. **Multiidioma:** Soporte para múltiples idiomas

## Seguridad

### Medidas implementadas:
1. **Validación de entrada:** Sanitización de todas las consultas
2. **Rate limiting:** Prevención de abuso de API
3. **CORS configurado:** Acceso controlado desde dominios autorizados
4. **Logs de auditoría:** Registro de todas las operaciones

## Deployment

### Requisitos del sistema:
- Python 3.8+
- Flask 2.0+
- SQLAlchemy 1.4+
- 512MB RAM mínimo
- 1GB espacio en disco

### Comandos de deployment:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python -c "from src.main import app; from src.models.faq import db; app.app_context().push(); db.create_all()"

# Cargar FAQs iniciales
curl -X POST http://localhost:5000/api/faq/load-csv

# Ejecutar aplicación
python src/main.py
```

## Testing

### Casos de prueba implementados:
1. **Búsqueda exacta:** Consultas que coinciden exactamente con FAQs
2. **Búsqueda parcial:** Consultas con palabras clave relacionadas
3. **Búsqueda sin resultados:** Consultas que no tienen coincidencias
4. **Generación WhatsApp:** Formato correcto de respuestas
5. **Carga de datos:** Importación correcta desde CSV

### Ejemplo de test:
```python
def test_search_faq():
    response = client.post('/api/faq/search', 
                          json={'query': '¿Cuál es el precio?'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['found'] == True
    assert 'precio' in data['message'].lower()
```

## Conclusión

El Sistema de FAQ proporciona una base sólida para la automatización de respuestas en el CRM inmobiliario. Su diseño modular permite fácil integración con otros sistemas y escalabilidad para manejar volúmenes crecientes de consultas. La combinación de búsqueda inteligente y generación de respuestas personalizadas optimiza significativamente la experiencia del cliente y la eficiencia operativa.


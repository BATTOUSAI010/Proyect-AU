import csv

def create_leads_csv(filename='leads.csv'):
    headers = ['ID_Lead', 'Fecha_Registro', 'Nombre_Lead', 'Telefono_WhatsApp', 'Origen_Lead', 'Interes_Inicial', 'Etapa_Embudo', 'Color_Embudo', 'Prioridad', 'Ultima_Interaccion', 'Notas']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    print(f'Archivo {filename} creado con éxito.')

def create_interacciones_csv(filename='interacciones.csv'):
    headers = ['ID_Interaccion', 'ID_Lead', 'Fecha_Hora', 'Tipo_Interaccion', 'Contenido', 'Remitente', 'Estado_Actualizado']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    print(f'Archivo {filename} creado con éxito.')

def create_faq_csv(filename='faq.csv'):
    headers = ['ID_Pregunta', 'Pregunta', 'Respuesta', 'Palabras_Clave']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
    print(f'Archivo {filename} creado con éxito.')

if __name__ == '__main__':
    create_leads_csv()
    create_interacciones_csv()
    create_faq_csv()



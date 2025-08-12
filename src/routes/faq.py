import csv
import os
from flask import Blueprint, jsonify, request
from ..models.faq import FAQ, db

faq_bp = Blueprint('faq', __name__)


@faq_bp.route('/search', methods=['POST'])
def search_faq():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    results = FAQ.search_by_keywords(query) if query else []

    if results:
        best = results[0]
        return jsonify({
            'found': True,
            'question': best.pregunta,
            'message': best.respuesta,
            'results': [faq.to_dict() for faq in results]
        })
    return jsonify({'found': False, 'message': 'No se encontró información para la consulta.'}), 404


@faq_bp.route('/generate-whatsapp-response', methods=['POST'])
def generate_whatsapp_response():
    data = request.get_json() or {}
    query = data.get('query', '').strip()
    lead_name = data.get('lead_name', 'Cliente')
    results = FAQ.search_by_keywords(query) if query else []

    if results:
        best = results[0]
        message = f"Hola {lead_name}, {best.respuesta}"
    else:
        message = (
            f"Hola {lead_name}, gracias por tu consulta. Un agente se pondrá en "
            "contacto contigo pronto."
        )
    return jsonify({'whatsapp_message': message, 'results': [faq.to_dict() for faq in results]})


@faq_bp.route('/load-csv', methods=['POST'])
def load_csv():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'faq_repository.csv')
    if not os.path.exists(csv_path):
        return jsonify({'error': 'Archivo CSV no encontrado'}), 404

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        FAQ.query.delete()
        for row in reader:
            faq = FAQ(
                id_pregunta=row['ID_Pregunta'],
                pregunta=row['Pregunta'],
                respuesta=row['Respuesta'],
                palabras_clave=row['Palabras_Clave']
            )
            db.session.add(faq)
        db.session.commit()

    total = FAQ.query.count()
    return jsonify({'message': 'FAQs cargadas correctamente', 'total': total})


@faq_bp.route('/all', methods=['GET'])
def all_faqs():
    faqs = FAQ.query.all()
    return jsonify({'faqs': [f.to_dict() for f in faqs], 'total': len(faqs)})

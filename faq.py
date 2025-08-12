from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class FAQ(db.Model):
    __tablename__ = 'faq'
    
    id = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.String(20), unique=True, nullable=False)
    pregunta = db.Column(db.Text, nullable=False)
    respuesta = db.Column(db.Text, nullable=False)
    palabras_clave = db.Column(db.Text, nullable=False)
    
    def __init__(self, id_pregunta, pregunta, respuesta, palabras_clave):
        self.id_pregunta = id_pregunta
        self.pregunta = pregunta
        self.respuesta = respuesta
        self.palabras_clave = palabras_clave
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_pregunta': self.id_pregunta,
            'pregunta': self.pregunta,
            'respuesta': self.respuesta,
            'palabras_clave': self.palabras_clave.split(',')
        }
    
    @staticmethod
    def search_by_keywords(query):
        """
        Busca FAQs basándose en palabras clave con coincidencia difusa
        """
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


from utils.data_loader import load_csv_data, setup_chroma_db
from config import OPENAI_API_KEY, OPENAI_MODEL_NAME
import openai
from sentence_transformers import SentenceTransformer

class RecommendationEngine:
    def __init__(self):
        self.data = load_csv_data('data/empresas_solares_ficticias.csv')
        self.chroma_collection = setup_chroma_db(self.data)
        openai.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL_NAME
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')

    def get_recommendations(self, user_input):
        query_embedding = self.embeddings.encode(user_input['description']).tolist()
        query_results = self.chroma_collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        recommendations = []
        for i, doc_id in enumerate(query_results['ids'][0]):
            company_data = self.data[self.data['Nome da Empresa'] == doc_id].iloc[0]
            recommendations.append({
                "rank": i + 1,
                "company_name": company_data['Nome da Empresa'],
                "location": company_data['Localidade'],
                "system_type": company_data['Tipo de Sistema Oferecido'],
                "score": query_results['distances'][0][i]
            })
        
        refined_recommendations = self.refine_recommendations(recommendations, user_input)
        return refined_recommendations

    def refine_recommendations(self, recommendations, user_input):
        prompt = f"Com base nas seguintes informações do usuário: {user_input['description']}, e nas recomendações iniciais: {recommendations}, forneça uma análise detalhada das 3 melhores opções para o usuário, explicando por que cada uma é adequada."
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

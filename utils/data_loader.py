import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    print("Primeiras linhas do DataFrame:")
    print(df.head())
    return df

def setup_chroma_db(data):
    print("Colunas disponíveis:", data.columns.tolist())
    
    client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    
    # Verificar se a coleção já existe
    try:
        collection = client.get_collection("solar_companies")
        print("Coleção 'solar_companies' já existe. Usando a coleção existente.")
    except ValueError:
        # Se a coleção não existir, crie-a
        collection = client.create_collection("solar_companies")
        print("Criando nova coleção 'solar_companies'.")
    
    # Verificar se a coleção está vazia
    if collection.count() == 0:
        # Usar o nome da empresa como ID
        ids = data['Nome da Empresa'].astype(str).tolist()
        
        # Usar a coluna 'Nome da Empresa' como documento principal
        documents = data['Nome da Empresa'].tolist()
        
        # Criar metadados com todas as outras colunas
        metadatas = data.drop('Nome da Empresa', axis=1).to_dict('records')
        
        # Gerar embeddings usando Sentence Transformers
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(documents).tolist()
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
            ids=ids
        )
        print(f"Adicionados {len(ids)} itens à coleção.")
    else:
        print(f"A coleção já contém {collection.count()} itens. Nenhum dado novo adicionado.")
    
    return collection

# Remova ou comente estas linhas:
# df = load_csv_data('data/empresas_solares_ficticias.csv')
# chroma_collection = setup_chroma_db(df)

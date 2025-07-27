import os
from sqlalchemy import create_engine
from app.database.models import Base

DATA_DIR = "data"
DB_FILENAME = "tars_main.db"
DB_PATH = os.path.join(DATA_DIR, DB_FILENAME)

def initialize_database():
    """
    Cria a pasta de dados e o banco de dados principal com todas as tabelas,
    se eles ainda não existirem.
    """
    print("Iniciando a configuração do banco de dados...")

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Diretório '{DATA_DIR}' criado.")

    engine = create_engine(f'sqlite:///{DB_PATH}')

    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(engine)

    print("---")
    print(f"Banco de dados inicializado com sucesso em: '{DB_PATH}'")
    print("---")

if __name__ == "__main__":
    initialize_database()
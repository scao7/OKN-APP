import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from openai import OpenAI
from db_models import *
class ResourcesLoader:
    def __init__(self, env_file='.env'):
        self.env_file = env_file
        self.load_environment_variables()
        self.initialize_database()
        self.initialize_openai_client()

    def load_environment_variables(self):
        load_dotenv(self.env_file, override=True)
        self.neo4j_uri = os.getenv('NEO4J_URI')
        self.neo4j_username = os.getenv('NEO4J_USER')
        self.neo4j_password = os.getenv('NEO4J_PWD')
        self.neo4j_database = os.getenv('NEO4J_DB')
        self.openai_api_key = os.getenv('OPENAI_API_KEY_TEAM')
        os.environ['OPENAI_API_KEY'] = self.openai_api_key
        self.openai_endpoint_em = os.getenv('OPENAI_ENDPOINT_EM')
        self.llm_model = "gpt-4o"
        self.embedding_model = 'text-embedding-3-small'

    def initialize_database(self):
        password = os.environ["okn_database"]
        # self.engine = create_engine('postgresql+psycopg2://xiaoming:11111111@127.0.0.1:5432/okndb')
        self.engine = create_engine(f'postgresql+psycopg2://saillab:{password}@127.0.0.1:5432/okn')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def initialize_openai_client(self):
        self.openai_client = OpenAI(
            api_key=self.openai_api_key
        )

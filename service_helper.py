# treatment_service_search.py
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from db_models import *
import faiss
import numpy as np
import json
from geopy.distance import geodesic

class ServiceHelper:
    def __init__(self, resources):
        self.data = []
        self.resources = resources
        self._initialize_faiss_index_county()
    
    def initialize(self, data):
        self.data = data
    
    def search(self, query):
        # For simplicity, we'll do a basic case-insensitive search in the name and description
        results = [item for item in self.data if query.lower() in item['name'].lower() or query.lower() in item['description'].lower()]
        return results
    
    def _clean_json_response(self, response):
        # Remove code block formatting if present
        response = response.strip('```json').strip('```')
        # Remove any leading or trailing whitespaces
        response = response.strip()
        # Replace any newline characters
        response = response.replace('\n', '')
        return response
    
    def client_request(self, client_question):
        response_json = {}
        response_json["answer"] = "I am sorry, I am not able to help you at the moment."
        if client_question:
            res = self._request_type(client_question)
        # Parse the response into a JSON object
        res = self._clean_json_response(res)
        json_obj = json.loads(res)
        need_help = json_obj['needhelp']
        county = json_obj['county']
        state = json_obj['state']
        service_related = json_obj['service_related']
        substance_abuse_sympton = json_obj['substance_abuse_sympton']
        mental_health_sympton = json_obj['mental_health_sympton']
        if need_help or service_related:
            if county and state:
                cty_id = self._find_closest_county_faiss(county, state)
                print(cty_id)
                if cty_id:
                    lat, lon = self.get_county_centroid(cty_id)
                    nearby_providers, distances = self.find_providers_within_radius(lat, lon)
                    provider_ids = [provider.tp_id for provider in nearby_providers]
                    print(provider_ids)
                    if provider_ids:
                        response_json["provider_ids"] = provider_ids
                        services_available = self.resources.session.query(TPServices).filter(TPServices.tp_id.in_(provider_ids)).all()

                else:
                    print("County not found")
        return response_json
    
    # Initialize the Faiss index for county embeddings
    def _initialize_faiss_index_county(self):
        # Load county embeddings from the database
        session = self.resources.session
        all_county_embeddings = session.query(CountyEmbedding).all()
        self.db_embeddings = np.array([embedding.county_state_embedding for embedding in all_county_embeddings], dtype=float)
        self.county_ids = np.array([embedding.county_id for embedding in all_county_embeddings])

        # Build the Faiss index
        d = self.db_embeddings.shape[1]  # Dimension of the embeddings
        self.index_county = faiss.IndexFlatL2(d)  # Create a Faiss index for L2 (Euclidean) distance
        self.index_county.add(self.db_embeddings)  # Add the embeddings to the Faiss index

    
    def _request_type(self, client_question):
        llm = ChatOpenAI(temperature=0.0, model=self.resources.llm_model)
        prompt_1 = ChatPromptTemplate.from_template(
            "Please extract the geolocation information in the question and \
            determine whether the user needs help or query treatment services from a drug treatment agency based on the situation. \
            Use bool value for 'needhelp' and 'service_related' attributes. For other attributes, if there is no related informatioin, \
            assign empty string to them.\
            If the description contains symptons related to substance abuse or mental health, also summarize . \
            the question is: ({client_question}?) \
            Please return the extracted geolocation information in the pure JSON format without any extra explanation or comment: \
            {{'county': 'Jefferson', 'state': 'Alabama', 'service_related': True/False, 'needhelp': True/False, 'substance_abuse_sympton': 'Anxious after using cocaine', 'mental_health_sympton': 'Aggressive'}}",
        )
        chain = LLMChain(llm=llm, prompt=prompt_1, verbose=True)
        response_1 = chain.run(client_question)
        return response_1
    
    
    def _find_closest_county_faiss(self, county, state):
        county_infomation = f"{county}, {state}"
        input_embedding = self._get_embedding(county_infomation)
        # Ensure the input embedding is a 2D NumPy array with the correct shape (1, d)
        input_embedding = np.array(input_embedding).reshape(1, -1)

        # Search the index for the nearest neighbor (1 nearest neighbor)
        _, indices = self.index_county.search(input_embedding, 1)
        closest_county_id = self.county_ids[indices[0][0]]

        return closest_county_id
    
    # Convert text to an embedding using OpenAI's API
    # Float vector of 1536 dimensions
    def _get_embedding(self, text):
        response = self.resources.openai_client.embeddings.create(input=text, model=self.resources.embedding_model)
        text_embedding = response.data[0].embedding
        return text_embedding
    
    def get_county_centroid(self, county_id):
        session = self.resources.session
        county_id = int(county_id)
        cty = session.query(County).filter_by(county_id=county_id).first()
        if cty:
            return cty.latitude, cty.longitude
        else:
            return None

    def find_providers_within_radius(self, client_latitude, client_longitude, radius=15):
        session = self.resources.session
        providers = session.query(MHTreatmentProvider).all()
        nearby_providers = []
        distances = []

        for provider in providers:
            provider_location = (provider.latitude, provider.longitude)
            client_location = (client_latitude, client_longitude)
            distance = geodesic(client_location, provider_location).miles

            if distance <= radius:
                nearby_providers.append(provider)
                distances.append(distance)

        return nearby_providers, distances


    
'''
Test client_request:
http://127.0.0.1:5000/client_request?query=I+am+from+Jefferson+County%2C+Alabama+and+I+am+feeling+very+anxious+after+using+cocaine.+I+don%27t+know+what+to+do.+Can+you+help+me%3F+I+also+have+eager+to+hit+someone.+I+am+feeling+very+aggressive.
'''

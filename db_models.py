# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, ARRAY, Numeric, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PersonNSDUH(Base):
    __tablename__ = 'person_nsduh'
    person_id = Column(BigInteger, primary_key=True, nullable=False)
    gender = Column(Integer)
    age_range_id = Column(Integer)
    rural_urban_id = Column(Integer)
    source_dataset = Column(Integer)
    year = Column(Integer)

class Substance(Base):
    __tablename__ = 'substance'
    substance_id = Column(Integer, primary_key=True, nullable=False)
    substance_code = Column(String(10))
    substance_name = Column(String(80))
    other_names = Column(String(80))
    source_dataset = Column(Integer)
    year = Column(Integer)

class Gender(Base):
    __tablename__ = 'gender'
    gender_id = Column(Integer, primary_key=True, nullable=False)
    gender_name = Column(String(20))
    source_dataset = Column(Integer)
    year = Column(Integer)

class AgeRange(Base):
    __tablename__ = 'age_range'
    age_range_id = Column(Integer, primary_key=True, nullable=False)
    age_range_lvalue = Column(Integer)
    age_range_rvalue = Column(Integer)
    source_dataset = Column(Integer)
    year = Column(Integer)

class RuralUrban(Base):
    __tablename__ = 'rural_urban'
    rural_urban_id = Column(Integer, primary_key=True, nullable=False)
    rural_urban_code = Column(String(10))
    rural_urban_description = Column(String(120))
    year = Column(Integer)
    population = Column(Integer)
    state_code = Column(String(2))
    county_name = Column(String(40))
    rucc = Column(Integer)

class SubstanceIncidentCase(Base):
    __tablename__ = 'substance_incident_case'
    sic_id = Column(BigInteger, primary_key=True, nullable=False)
    person_id = Column(BigInteger)
    sit_id = Column(Integer)
    substance_id = Column(Integer)
    source_dataset = Column(Integer)
    year = Column(Integer)

class SubstanceIncidentType(Base):
    __tablename__ = 'substance_incident_type'
    sit_id = Column(Integer, primary_key=True, nullable=False)
    sit_name = Column(String(128))
    source_dataset = Column(Integer)
    year = Column(Integer)

class Dataset(Base):
    __tablename__ = 'dataset'
    dataset_id = Column(Integer, primary_key=True, nullable=False)
    dataset_name = Column(String(50))
    organization = Column(String(50))
    ontology_prefix = Column(String(100))
    dataset_description = Column(String(512))
    year = Column(Integer)

class State(Base):
    __tablename__ = 'state'
    state_id = Column(Integer, primary_key=True, nullable=False)
    state_name = Column(String(20))
    state_abbr = Column(String(2))
    fips = Column(String(2))

class County(Base):
    __tablename__ = 'county'
    county_id = Column(Integer, primary_key=True, nullable=False)
    county_name = Column(String(40))
    fips = Column(String(5))
    state_id = Column(Integer)
    state_abbr = Column(String(2))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))

class MHTreatmentProvider(Base):
    __tablename__ = 'mh_treatment_provider'
    tp_id = Column(Integer, primary_key=True, nullable=False)
    tp_name = Column(String(64))
    tp_name_sub = Column(String(64))
    address_line_1 = Column(String(128))
    address_line_2 = Column(String(128))
    city_id = Column(Integer)
    state_code = Column(String(2))
    zip_code = Column(String(5))
    phone = Column(String(32))
    intake1 = Column(String(32))
    intake2 = Column(String(32))
    intake1a = Column(String(32))
    intake2a = Column(String(32))
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))

class MentalHealthIssue(Base):
    __tablename__ = 'mental_health_issue'
    mhi_id = Column(Integer, primary_key=True, nullable=False)
    mhi_name = Column(String(128))
    mhi_code = Column(String(128))
    mhi_description = Column(String(256))
    source_dataset = Column(Integer)
    year = Column(Integer)

class MentalHealthCase(Base):
    __tablename__ = 'mental_health_case'
    mhi_case_id = Column(BigInteger, primary_key=True)
    person_id = Column(BigInteger)
    mhi_id = Column(Integer)
    time_id = Column(Integer)
    description = Column(String(128))

class RUCC(Base):
    __tablename__ = 'rucc'
    rucc_id = Column(Integer, primary_key=True, nullable=False)
    rucc_code = Column(Integer)
    year = Column(Integer)
    description = Column(String(512))

class MHServiceCategory(Base):
    __tablename__ = 'mh_service_category'
    mhsc_id = Column(Integer, primary_key=True, nullable=False)
    mhsc_name = Column(String(64))
    mhsc_code = Column(String(16))
    mhsc_year = Column(Integer)

class MHService(Base):
    __tablename__ = 'mh_service'
    mhs_id = Column(Integer, primary_key=True, nullable=False)
    mhs_code = Column(String(16))
    mhs_name = Column(String(256))
    mhs_description = Column(String(2048))
    mhs_year = Column(Integer)
    mhsc_id = Column(Integer)

class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True, nullable=False)
    city_name = Column(String(64))
    county_id = Column(Integer)
    state_id = Column(Integer)
    latitude = Column(Numeric(9, 6))
    longitude = Column(Numeric(9, 6))
    year = Column(Integer, default=2024)
    population = Column(Integer)
    ranking = Column(Integer)
    density = Column(Numeric(7, 1))
    incorporated = Column(Boolean)
    zips = Column(String(2048))

class TPServices(Base):
    __tablename__ = 'tp_services'
    id = Column(Integer, primary_key=True)
    tp_id = Column(Integer)
    mhs_id = Column(Integer)
    year = Column(Integer)

class MHServiceEmbedding(Base):
    __tablename__ = 'mh_service_embedding'
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    mhs_id = Column(Integer)
    mhs_name_embedding = Column(ARRAY(Numeric))
    mhs_description_embedding = Column(ARRAY(Numeric))
    em_year = Column(Integer)

class CountyEmbedding(Base):
    __tablename__ = 'county_embedding'
    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    county_id = Column(Integer)
    county_state_embedding = Column(ARRAY(Numeric))
    em_year = Column(Integer)

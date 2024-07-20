from gptpdf import parse_pdf
api_key = 'sk-proj-ZFlXSJ1BusV16nVt7t5sT3BlbkFJ8v3rxvP3mykr8qfg6Z89'
pdf_path = r"D:\OKN_Front_End\Datasets\Datasets\codebook\NIBRS-2022-38925-0003-Codebook-ICPSR.pdf"

prompt = {
  "prompt": """The main purpose of the NSDUH dataset is to provide nationally representative data on the use of tobacco, alcohol, and drugs; substance use disorders; mental health issues; and receipt of substance use and mental health treatment among the civilian, noninstitutionalized population aged 12 or older in the United States. This data allows researchers, clinicians, policymakers, and the general public to better understand and improve the nation’s behavioral health. 
	You are an expert on Ontology, Social science and you are currently working on the NSDUH dataset codebook to extract entities for constructing an Ontology. The Ontology is for the topic of "substance abuse, mental health, and rural resilience". So entities that are related to substance, economic status, education, mental health, rural area, infrastructure, law, and so on, are related to this topic and potentially support the reasoning of this research. 
	Currently, we have a list of extracted entities and relations. The entities and relations may be extracted from the documents directly, or they are summarized or categorized in a reasonable way.
	Please extract entities and relationships that can serve the topic from the text in the image of the NSDUH survey sheet: 
  Please generate the results in JSON format as follows:
	{
  "entities": [
    {
      "entity": "SurveyPeriod",
      "description": "The time frame of the past 30 days, including today's date."
    },
    {
      "entity": "SickOrInjuredDays",
      "description": "Number of whole days missed from school due to sickness or injury."
    },
    {
      "entity": "SchoolAbsenceReason",
      "description": "The reason for missing school, specifically due to being sick or injured."
    },
    {
      "entity": "FamilyCareAbsence",
      "description": "Number of days missed due to staying home with a sick child or family member."
    }
  ],
  "relationships": [
    {
      "relationship": "hasSurveyPeriod",
      "source_entity": "Survey",
      "target_entity": "SurveyPeriod",
      "description": "Relates the survey to the time period of the past 30 days."
    },
    {
      "relationship": "hasSickOrInjuredDays",
      "source_entity": "Respondent",
      "target_entity": "SickOrInjuredDays",
      "description": "Indicates the number of days the respondent missed school due to sickness or injury."
    },
    {
      "relationship": "hasAbsenceReason",
      "source_entity": "SchoolAbsence",
      "target_entity": "SchoolAbsenceReason",
      "description": "Defines the reason for the school absence, such as being sick or injured."
    },
    {
      "relationship": "hasFamilyCareAbsence",
      "source_entity": "Respondent",
      "target_entity": "FamilyCareAbsence",
      "description": "Indicates the number of days the respondent missed school due to caring for a sick child or family member."
    }
  ]
}

	
""",
  "rect_prompt":"""Please also extract the entity relations from the text in image.
	And generate the results in JSON format as follows:
	{
  "entities": [
    {
      "entity": "SurveyPeriod",
      "description": "The time frame of the past 30 days, including today's date."
    },
    {
      "entity": "SickOrInjuredDays",
      "description": "Number of whole days missed from school due to sickness or injury."
    },
    {
      "entity": "SchoolAbsenceReason",
      "description": "The reason for missing school, specifically due to being sick or injured."
    },
    {
      "entity": "FamilyCareAbsence",
      "description": "Number of days missed due to staying home with a sick child or family member."
    }
  ],
  "relationships": [
    {
      "relationship": "hasSurveyPeriod",
      "source_entity": "Survey",
      "target_entity": "SurveyPeriod",
      "description": "Relates the survey to the time period of the past 30 days."
    },
    {
      "relationship": "hasSickOrInjuredDays",
      "source_entity": "Respondent",
      "target_entity": "SickOrInjuredDays",
      "description": "Indicates the number of days the respondent missed school due to sickness or injury."
    },
    {
      "relationship": "hasAbsenceReason",
      "source_entity": "SchoolAbsence",
      "target_entity": "SchoolAbsenceReason",
      "description": "Defines the reason for the school absence, such as being sick or injured."
    },
    {
      "relationship": "hasFamilyCareAbsence",
      "source_entity": "Respondent",
      "target_entity": "FamilyCareAbsence",
      "description": "Indicates the number of days the respondent missed school due to caring for a sick child or family member."
    }
  ]
} 
""",
    "role_prompt": """You are an expert on Ontology, Social science and you are currently working on the NSDUH dataset codebook to extract entities for constructing an Ontology.
"""
}

content, image_paths = parse_pdf(
    pdf_path=pdf_path,
    output_dir='./NIBRS-2022-38925-0003-Codebook-ICPSR_entity_relation',
    model="gpt-4o",
    prompt=prompt,
    verbose=True,
)


import pandas as pd 
import os
import openai
df  = pd.read_csv(r"D:\OKN_Front_End\Datasets\nsduh_2022_codebook.csv")
# print(df.head())
# print(df["Long_Description"])
df_list = df["Long_Description"].tolist()
unique_list = list(set(df_list))
# print(unique_list)
api_key=os.environ.get("OPENAI_API_KEY")

# Authentication
client = openai.OpenAI(
	# This is the default and can be omitted
	api_key=os.environ.get("OPENAI_API_KEY")
)

for i in unique_list:
	if i !="nan":
		long_description = i
		prompt = """The main purpose of the NSDUH dataset is to provide nationally 
		representative data on the use of tobacco, alcohol, and drugs; 
		substance use disorders; mental health issues; 
		and receipt of substance use and mental health treatment among the civilian,
		noninstitutionalized population aged 12 or older in the United States.
		This data allows researchers, clinicians, policymakers, and the general public 
		to better understand and improve the nation’s behavioral health. You are an expert
		on Ontology, Social science and you are currently working on the NSDUH dataset codebook 
		to extract entities for constructing an Ontology. The Ontology is for the topic of 
		"substance abuse, mental health, and rural resilience". 
		So entities that are related to substance, economic status, education, mental health, rural area, infrastructure, law, and so on, are related to this topic and potentially support the reasoning of this research. 
		Currently, we have a list of extracted entities and relations. 
		The entities and relations may be extracted from the documents directly, or they are summarized or categorized in a reasonable way.
		Please extract entities and relationships that can serve the topic from the following questions in the NSDUH survey sheet:
		
		{%s}
		
		Please generate the results in JSON format as follows:
			
		{"entities": [
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
		""" % (long_description)

		# print(prompt)

		response = client.chat.completions.create(
            messages=[
            {
                "role": "user",
                "content": prompt,
            }
            ],
            model="gpt-4o",
        )
		model_output = response.choices[0].message.content.strip()
		print(model_output)
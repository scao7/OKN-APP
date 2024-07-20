from gptpdf import parse_pdf
api_key = 'sk-proj-ZFlXSJ1BusV16nVt7t5sT3BlbkFJ8v3rxvP3mykr8qfg6Z89'
pdf_path = r"D:\OKN_Front_End\Datasets\Datasets\codebook\NSDUH-2022-DS0001-info-codebook.pdf"

prompt = {
    "prompt": """Use plain text syntax, extract text from images and convert it into Ontology triplets in txt format. You must:
    1.Output the text in the same language as recognized in the image. For example, if the fields are recognized in English, the output content must be in English.
	2.Do not explain or output irrelevant text. Directly output triplet based the entity relations in the content from the image. 
	3.Your output format needs to be exactly like this json format {"subject":"subject term", "predicate":"predicate term", "object": "object term"} triplets each line.
	4.ignore long straight line and page number.
	Please stricktly follow the triplet format {"subject":"subject term", "predicate":"predicate term", "object": "object term"}
	For the triplets the "subject","predicate" and  "object" key remain unchange, only fill the the key content where "subject term" ,"predicate term" and "object term" loacated.
	Do not output markdown element such as ```json
	
""",
    "rect_prompt":"""We used red rectangle and name (%s) marked some area. If the area is table or image, please also try to extrac the triplet with format {"subject":"subject term", "predicate":"predicate term", "object": "object term"}. If can't, ignore the image.
""",
    "role_prompt": """You are an Ontology expert, you need to extract ontology according to given govenment survey codebook.
"""
}

content, image_paths = parse_pdf(
    pdf_path=pdf_path,
    output_dir='./NSDUH-2022-DS0001-info-codebook_triplets',
    model="gpt-4o",
    prompt=prompt,
    verbose=True,
)


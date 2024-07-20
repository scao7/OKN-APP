from gptpdf import parse_pdf
api_key = 'sk-proj-ZFlXSJ1BusV16nVt7t5sT3BlbkFJ8v3rxvP3mykr8qfg6Z89'
pdf_path = r"D:\OKN_Front_End\Datasets\Datasets\codebook\SPI-2016-Codebook.pdf"

content, image_paths = parse_pdf(
	api_key=api_key,
    pdf_path=pdf_path,
    output_dir='./SPI-2016-Codebook',
    model="gpt-4o",
    verbose=True,
)

print(content)
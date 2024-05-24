# import camelot

# # Specify the path to your PDF file
# pdf_path = r"D:\OKN_Front_End\Datasets\N-SSATS-2020-DS0001-info-codebook.pdf"

# # Extract tables from the PDF
# tables = camelot.read_pdf(pdf_path, pages='all')

# # Print the tables or save them to CSV files
# for i, table in enumerate(tables):
#     print(f"Table {i}")
#     print(table.df)
#     table.to_csv(f"table_{i}.csv")

import tabula

# Specify the path to your PDF file
pdf_path = r"D:\OKN_Front_End\Datasets\N-SSATS-2020-DS0001-info-codebook.pdf"

# Extract tables from the PDF into a list of DataFrames
tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

# Print the tables or save them to CSV files
for i, table in enumerate(tables):
    print(f"Table {i}")
    print(table)
    table.to_csv(f"table_{i}.csv", index=False)

import PyPDF2

# Open the source PDF file
with open('Computer-Networking-A-Top-Down-Approach-James-W.-Kurose-Keith-W.-Ross.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a new PDF writer
    pdf_writer = PyPDF2.PdfWriter()

    # Specify the page range you want to extract (e.g., pages 10 to 55)
    start_page = 176  # Page numbering starts from 0
    end_page = 186

    # Loop through the pages and add them to the writer
    for page_num in range(start_page, end_page + 1):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)

    # Save the extracted pages to a new PDF
    with open('unit2.pdf', 'wb') as output_file:
        pdf_writer.write(output_file)

import fitz


def extract_pages_from_pdf(pdf_path):
    pages = []

    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text()
        })

    return pages
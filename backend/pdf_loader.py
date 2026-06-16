import fitz  # PyMuPDF


def load_pdf(file_path):
    doc = fitz.open(file_path)

    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "page": i + 1,
            "text": page.get_text()
        })

    return pages
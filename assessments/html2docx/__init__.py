from io import BytesIO

from .html2docx import HTML2Docx


def html2docx(content: str, title: str, passed_doc) -> BytesIO:
    """Convert valid HTML content to a docx document and return it as a
    io.BytesIO() object.
    """
    parser = HTML2Docx(title, passed_doc)
    parser.feed(content.strip())

    buf = BytesIO()
    parser.doc.save(buf)
    return buf

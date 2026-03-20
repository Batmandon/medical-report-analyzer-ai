from PyPDF2 import PdfReader
from ai import create_embedding
from database import get_cursor

def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text

    return text

def chunk_text(text, size=1000):
    chunks = []

    for i in range(0, len(text), size):
        chunk = text[i:i+size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks

def process_document(file_path, file_id):

    text = extract_text(file_path)

    chunks = chunk_text(text)

    with get_cursor() as cursor:
        for chunk in chunks:
            embedding = create_embedding(chunk)

            cursor.execute(
                "INSERT INTO document_chunks(file_id, chunk_text, embedding) VALUES (%s, %s, %s)",
                (file_id, chunk, embedding)
            )

    return text

def search_similar_chunks(question_embedding, file_id, top_k=5):
    with get_cursor() as cursor:
        cursor.execute("""
            SELECT chunk_text, 
                       1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks
            WHERE file_id = %s
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (str(question_embedding), file_id, str(question_embedding), top_k))

        return cursor.fetchall()
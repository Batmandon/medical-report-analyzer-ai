from google import genai
from google.genai import types
from config import GEMINI_API_KEY
from database import get_cursor
from logger import logger
client = genai.Client(api_key=GEMINI_API_KEY)

def create_embedding(text):
    try:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return list(response.embeddings[0].values)
    except Exception as e:
        logger.error(f"Embedding failed: {str(e)}")
        raise
    
def response_document(text:str):
  
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=
        f"""You are a friendly medical report analyzer. Analyze this report and respond in this exact format:

**What this report is about**
One line summary only.

**Values that need attention**
* Value Name: result (normal range) — what it means in 5 words max
* Value Name: result (normal range) — what it means in 5 words max

**What's normal**
One line only.

**Bottom line**
2-3 sentences max. Simple, friendly. End with when to see a doctor.

Be concise. No medical jargon. No long paragraphs.

Report: {text}""")


    summary =  response.text
    token_used = response.usage_metadata.total_token_count

    return summary,token_used

def ask_document(context, question):

    prompt=f"""You are a helpful medical assistant analyzing a patient's medical report.
            Answer the patient's question using only the information from their report.
            Use simple, clear language that a non-medical person can understand.
            If the answer is not in the report, say so clearly.
            If a value seems concerning, mention it gently but recommend consulting a doctor.


    Report context:
    {context}

    Patience's question:
    {question}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
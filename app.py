from google import genai
from config import GEMINI_API_KEY
from Searcher import search_pdf

# 1. Initialize the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def ask_pdf(qna, user_id):
    # Step A: Search ChromaDB for relevant text chunks (only this user's)
    matching_chunks = search_pdf(qna, user_id)
    context_text = "\n\n".join(matching_chunks)

    # Step B: Send prompt + context to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""You are a helpful assistant that answers questions about documents the user has uploaded.
The context below contains the parts of those documents that best match the question.

Rules:
- Answer using ONLY the information in the context. Do not use outside knowledge.
- If the context does not contain the answer, reply exactly: "I couldn't find that in your uploaded documents."
- If the question says "I", "me", "my" or "we", read it from the point of view of the person the document is written for.
- Keep the answer clear and short. Use bullet points when listing several things.

--- CONTEXT FROM THE DOCUMENTS ---
{context_text}

--- USER QUESTION ---
{qna}"""
    )

    # Step C: Return the generated text response
    return response.text

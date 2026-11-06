from fastapi import FastAPI ,UploadFile ,HTTPException ,Header
from fastapi.middleware.cors import CORSMiddleware
from memory import creating_Db
from app import ask_pdf
from pathlib import Path
from google.genai import errors
from pypdf.errors import PdfReadError
import uuid


app = FastAPI()

# Let the website (running at a different address) call this API.
# "*" = allow any address. Fine on your own computer; restrict it before going online.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



def check_user_id(user_id):
    # Each browser sends its own random ID (a UUID) in the "X-User-Id" header.
    # Only real UUIDs are accepted, so the ID is also safe to use as a folder name.
    try:
        return str(uuid.UUID(user_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="Missing or invalid user ID.")


@app.post("/PDFUpload")
def get_pdf(file : UploadFile, x_user_id : str = Header("")):

    user_id = check_user_id(x_user_id)

    if not file.filename.lower().endswith(".pdf") :
        raise HTTPException(status_code=400, detail="only PDF files are allowed")


    # Every user gets their own folder: uploads/<user id>/
    folder = Path("uploads") / user_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / Path(file.filename).name

    with open(path, "wb") as f:
        f.write(file.file.read())

    try:
        chunk_count = creating_Db(str(path), user_id)

    except PdfReadError:
        path.unlink()
        raise HTTPException(status_code=400, detail="This file is not a valid PDF.")

    if chunk_count == 0:
        path.unlink()
        raise HTTPException(status_code=400, detail="This PDF has no readable text.")

    return {"filename": file.filename,
            "chunks" : chunk_count
    }


@app.post("/chatbot")
def send_answer(qna, x_user_id : str = Header("")):

    user_id = check_user_id(x_user_id)

    try:
        answer = ask_pdf(qna, user_id)
        return answer

    except errors.APIError:
        return "try again later"
import chromadb
from Chunker import DocumentChunker


def creating_Db(name, user_id):

    my_chunker = DocumentChunker()
    raw_text = my_chunker.read_pdf_file(name)
    text_chunks = my_chunker.chunk_text(raw_text)

    if len(text_chunks) == 0:
        return 0

    db = chromadb.PersistentClient(path="./chroma_db")

    collection = db.get_or_create_collection(name="documents")

    chunk_labels = []

    for i in range(len(text_chunks)):
        label = f"id_{f"{name}_{i}"}"           # Make label like "id_0"
        chunk_labels.append(label)   # Add it to the list

    collection.upsert(
        documents=text_chunks,
        ids=chunk_labels,
        metadatas=[{"user_id": user_id}] * len(text_chunks)   # Tag every chunk with its owner

    )

    return len(text_chunks)

    

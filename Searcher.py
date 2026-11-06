import chromadb

def search_pdf(user_question, user_id, n_result=5):

    db = chromadb.PersistentClient(path="./chroma_db")
    collection = db.get_or_create_collection(name ="documents")

    search_result = collection.query(
                
        query_texts=[user_question],
        n_results =n_result,
        where={"user_id": user_id}      # Only search this user's own chunks

    )
    
    matching_chunks = search_result['documents'][0]
    return matching_chunks
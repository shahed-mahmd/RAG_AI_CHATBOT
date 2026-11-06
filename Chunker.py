from pypdf import PdfReader

class DocumentChunker :

    def __init__(self, chunk_size = 1000):

        self.chunk_size = chunk_size

    def read_pdf_file(self, filepath):

        full_text = ""

        reader = PdfReader(filepath)

        for page in reader.pages:

            extract = page.extract_text()

           
            full_text = full_text + (extract or "")

        return full_text

    def chunk_text(self, text):
        chunks = []
        for i in range(0, len(text), self.chunk_size):

            chunk = text[ i : i + self.chunk_size ]
            
            
            chunks.append(chunk)

        return chunks



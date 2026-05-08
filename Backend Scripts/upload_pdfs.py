from openai import OpenAI
import os

client = OpenAI()

VECTOR_STORE_ID = "REPLACE WITH YOUR VECTOR STORE ID"  # <-- replace this
PDF_DIR = "knowledge"

file_ids = []

for filename in os.listdir(PDF_DIR):
    if filename.endswith(".pdf"):
        path = os.path.join(PDF_DIR, filename)
        with open(path, "rb") as f:
            uploaded = client.files.create(
                file=f,
                purpose="assistants"
            )
            file_ids.append(uploaded.id)
            print(f"Uploaded {filename}")

client.vector_stores.file_batches.create(
    vector_store_id=VECTOR_STORE_ID,
    file_ids=file_ids
)

print("All PDFs added to vector store.")

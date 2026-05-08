import os
import boto3
from pypdf import PdfReader
from openai import OpenAI

def get_openai_key():
    ssm = boto3.client("ssm", region_name="us-east-2")
    response = ssm.get_parameter(Name="/openai/api_key", WithDecryption=True)
    return response["Parameter"]["Value"]

client = OpenAI(api_key=get_openai_key())

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

vector_store = client.vector_stores.create(name="MissionControlKnowledge")

folder = "knowledge"

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        print(f"Processing {file}")
        text = extract_text_from_pdf(os.path.join(folder, file))
        chunks = chunk_text(text)

        for chunk in chunks:
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=chunk.encode("utf-8")
            )

print("Upload complete.")
print("Vector Store ID:", vector_store.id)


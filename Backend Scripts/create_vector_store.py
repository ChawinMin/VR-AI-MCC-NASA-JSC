from openai import OpenAI

client = OpenAI()

vector_store = client.vector_stores.create(
    name="capstone-knowledge"
)

print("VECTOR STORE ID:")
print(vector_store.id)


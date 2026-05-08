import boto3
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.responses import Response
import tempfile, os
from elevenlabs.client import ElevenLabs
from pydantic import BaseModel
from openai import OpenAI
import logging
import json

# ----------------------------
# App setup
# ----------------------------
app = FastAPI(title="IXL AI RAG Server")
logging.basicConfig(level=logging.INFO)

# ----------------------------
# Secure OpenAI key retrieval
# ----------------------------
def get_openai_key() -> str:
    try:
        ssm = boto3.client("ssm", region_name="us-east-2")
        response = ssm.get_parameter(
            Name="/openai/api_key",
            WithDecryption=True
        )
        return response["Parameter"]["Value"]
    except Exception as e:
        logging.error("Failed to retrieve OpenAI API key")
        raise RuntimeError("OpenAI API key not available") from e


# Initialize OpenAI client ONCE
client = OpenAI(api_key=get_openai_key())

# ----------------------------
# Vector Store
# ----------------------------
VECTOR_STORE_ID = "REPLACE WITH YOUR STORE VECTOR ID"

# ----------------------------
# Request / Response Models
# ----------------------------
class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str


# ----------------------------
# Health check (browser test)
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "service": "IXL AI RAG Server"
    }


# ----------------------------
# Unity → AI endpoint
# ----------------------------
@app.post("/ask", response_model=Answer)
def ask_ai(data: Question):
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=data.question,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [VECTOR_STORE_ID]
                }
            ],
        )

        return Answer(answer=response.output_text)

    except Exception as e:
        logging.exception("OpenAI request failed")
        raise HTTPException(
            status_code=500,
            detail="AI service failed to process the request"
        )

# ----------------------------
# Load in the API keys
# ----------------------------
with open("auth.json") as f:
	auth = json.load(f)

OPEN_AI_API_KEY = auth["api_key"]
client = OpenAI(api_key=OPEN_AI_API_KEY)

ELEVENLABS_API_KEY = auth["ELEVEN_LABS_API_KEY"]
eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

print("OpenAI key loaded:", OPEN_AI_API_KEY[:5])
print("Elevenlabs api key loaded:", ELEVENLABS_API_KEY[:5])

class AnswerRequest(BaseModel):
	prompt: str
	question: str
	rag: str = ""

# ----------------------------
# Generate a response
# ----------------------------
@app.post("/answer")
def answer(req: AnswerRequest):
	final_input = f"""{req.prompt}

Question:
{req.question}

RAG Context:
{req.rag}
"""
	response = client.chat.completions.create(model="gpt-5-nano",
	messages=[{"role": "user", "content": final_input}]
	)

	return {"response": response.choices[0].message.content}

# ----------------------------
# Transcribe a response
# ----------------------------
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), model: str = Form("whisper-1"), language: str = Form("en")):

	suffix = os.path.splitext(file.filename or "audio.wav")[1] or ".wav"
	with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
		tmp.write(await file.read())
		tmp_path = tmp.name

	try:
		with open(tmp_path, "rb") as f:
			result = client.audio.transcriptions.create(model=model, file=f, language=language)
			return {"text": result.text}
	finally:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)

# ----------------------------
# Use ElevenLabs to speak
# ----------------------------
@app.post("/speak")
def speak(payload: dict = Body(...)):
	text = payload.get("text", "").strip()
	if not text:
		return Response(status_code = 400, content = "Missing text")
	audio_stream = eleven_client.text_to_speech.convert(voice_id = "REPLACE WITH ELEVENS LABS VOICE ID", model_id="eleven_flash_v2_5", text=text, output_format="mp3_44100_128")
	audio_bytes = b"".join(audio_stream)
	return Response(content=audio_bytes, media_type="audio/mpeg")

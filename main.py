import logging
import os
from fastapi import FastAPI, UploadFile, File
import whisper
from openai import OpenAI
import pdfkit
from datetime import datetime
from dotenv import load_dotenv

# Determinar el entorno actual (desarrollo, testing, producción, etc.)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Cargar variables de entorno desde el archivo correspondiente
load_dotenv(f".env.{ENVIRONMENT}")

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Cargar modelo de Whisper (puede ser "small", "medium" o "large")
logger.info("Cargando modelo de Whisper...")
model = whisper.load_model("small")
logger.info("Modelo de Whisper cargado con éxito.")

# API Key de OpenAI desde archivo de configuración
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """Recibe un audio y devuelve su transcripción en texto."""
    file_location = f"temp_{file.filename}"
    logger.info(f"Guardando archivo en {file_location}")
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    
    logger.info("Iniciando transcripción de audio...")
    result = model.transcribe(file_location)
    transcription = result["text"]
    logger.info("Transcripción completada con éxito.")
    
    # Eliminar el archivo temporal
    os.remove(file_location)
    logger.info(f"Archivo {file_location} eliminado.")
    
    return {"transcription": transcription}

@app.post("/generate_minutes/")
async def generate_meeting_minutes(text: str):
    """Genera el acta de la reunión a partir del texto transcrito."""
    date_today = datetime.now().strftime("%Y-%m-%d")
    logger.info("Generando acta de reunión...")
    prompt = (f"Genera un acta de reunión estructurada con fecha {date_today} a partir del siguiente texto: \n{text}")
    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=500
    )
    
    meeting_minutes = response.choices[0].text.strip()
    logger.info("Acta de reunión generada exitosamente.")
    
    # Generar PDF con el acta de la reunión
    pdf_filename = f"meeting_minutes_{date_today}.pdf"
    pdfkit.from_string(meeting_minutes, pdf_filename)
    logger.info(f"Acta guardada en {pdf_filename}.")
    
    return {"meeting_minutes": meeting_minutes, "pdf": pdf_filename}

# Dockerfile
DOCKERFILE_CONTENT = """
FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

# Guardar el Dockerfile en el sistema
with open("Dockerfile", "w") as f:
    f.write(DOCKERFILE_CONTENT)

# requirements.txt
REQUIREMENTS_CONTENT = """
fastapi
uvicorn
git+https://github.com/openai/whisper.git
openai
pdfkit
python-multipart
dotenv
"""

# Guardar el archivo de dependencias
with open("requirements.txt", "w") as f:
    f.write(REQUIREMENTS_CONTENT)

# docker-compose.yml
DOCKER_COMPOSE_CONTENT = """
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    env_file:
      - .env.${ENVIRONMENT}
"""

# Guardar el archivo docker-compose.yml
with open("docker-compose.yml", "w") as f:
    f.write(DOCKER_COMPOSE_CONTENT)

# Crear archivos .env para distintos entornos si no existen
for env in ["development", "testing", "staging", "production"]:
    env_file = f".env.{env}"
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write("OPENAI_API_KEY=tu_api_key")

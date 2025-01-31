# 📌 Audio to Meeting Minutes API

## 📖 Descripción

Este proyecto es una API basada en **FastAPI** que permite:

- **Transcribir audios** utilizando **OpenAI Whisper**.
- **Generar actas de reuniones** con **GPT-4**.
- **Exportar el acta en formato PDF**.
- **Soportar múltiples entornos** (desarrollo, testing, staging, producción).
- **Desplegar con Docker y Docker Compose**.

---

## 🚀 Instalación y Configuración

### **1️⃣ Clonar el repositorio**

```bash
 git clone https://github.com/tu_usuario/tu_repositorio.git
 cd tu_repositorio
```

### **2️⃣ Configurar el entorno**

Debes definir el entorno antes de construir la imagen:

```bash
export ENVIRONMENT=development  # O el entorno que necesites
```

Si estás en Windows, usa:

```powershell
$env:ENVIRONMENT="development"
```

Crea un archivo `.env.development` y coloca la API Key:

```bash
echo "OPENAI_API_KEY=tu_api_key" > .env.development
```

### **3️⃣ Construcción y ejecución con Docker**

```bash
docker-compose build --no-cache
```

```bash
docker-compose up -d
```

La API estará disponible en:

```
http://localhost:8000/docs
```

---

## 🛠️ Uso de la API

### **1️⃣ Endpoint para transcribir audio**

- **URL:** `POST /transcribe/`
- **Descripción:** Recibe un archivo de audio y devuelve la transcripción.
- **Ejemplo con **``:

```bash
curl -X 'POST' \
  'http://localhost:8000/transcribe/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@audio.mp3'
```

### **2️⃣ Endpoint para generar actas de reunión**

- **URL:** `POST /generate_minutes/`
- **Descripción:** Recibe un texto transcrito y genera un acta en PDF.
- **Ejemplo con **``:

```bash
curl -X 'POST' \
  'http://localhost:8000/generate_minutes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{ "text": "Resumen de la reunión" }'
```

---

## 🏗️ Estructura del Proyecto

```
📂 tu_repositorio/
 ├── 📄 main.py               # Código principal de la API
 ├── 📄 Dockerfile            # Configuración de Docker
 ├── 📄 docker-compose.yml    # Configuración de Docker Compose
 ├── 📄 requirements.txt      # Dependencias
 ├── 📄 README.md             # Documentación del proyecto
 ├── 📄 .env.development      # Variables de entorno (se debe crear)
```

---

## 📝 Consideraciones

✅ **Requiere una API Key de OpenAI** para funcionar. ✅ **Configura los entornos en **`` para mayor seguridad. ✅ **Revisa los logs con:**

```bash
docker-compose logs -f
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si deseas mejorar el código, abre un **Pull Request** o crea un **Issue**.

---

## 📜 Licencia

Este proyecto está bajo la licencia **MIT**.


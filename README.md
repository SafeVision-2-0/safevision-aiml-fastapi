---

## 🚀 How to Run the Application (Local Development)

Follow the steps below to run the FastAPI application in a local environment.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/SafeVision-2-0/safevision-aiml-fastapi.git
cd safevision-aiml-fastapi
```

---

### 2️⃣ Create a Virtual Environment

#### Windows

```bash
python -m venv venv
```

#### Linux / macOS

```bash
python3 -m venv venv
```

---

### 3️⃣ Activate the Virtual Environment

#### Windows (PowerShell)

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

If successful, the terminal will display:

```text
(venv)
```

---

### 4️⃣ Install Dependencies

Make sure you are in the project root directory, then run:

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Run the FastAPI Server

Use **uvicorn** to run the FastAPI application located in `app/main.py`:

```bash
uvicorn app.main:app --reload
```

Explanation:

* `app.main` → location of the `main.py` file
* `app` → FastAPI instance
* `--reload` → enables auto-reload during development

---

### 6️⃣ Access the Application

* API root:

```
http://127.0.0.1:8000
```

* Swagger UI (API Documentation):

```
http://127.0.0.1:8000/docs
```

---

### 7️⃣ Stop the Server

Press:

```text
CTRL + C
```

---

## 📁 Entry Point Structure

```text
app/
└── main.py   ← FastAPI entry point
```

---

## ℹ️ Notes

* Make sure **Python 3.10** is installed
* The virtual environment **must be activated** during development, or you can use Docker from the **`8-docker-implementation` branch**
* Use `.env` for sensitive configuration (do not push it to GitHub)

---

Supaya repo kalian kelihatan **lebih profesional seperti open-source project**.

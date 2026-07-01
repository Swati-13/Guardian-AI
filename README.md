# 🛡️ GuardianAI: Generalized Content Moderation API

GuardianAI is a robust, production-ready **FastAPI-based text moderation service**. It analyzes user messages in real-time for **toxicity, abusive language, hate speech, and threats** using the powerful **Groq API** (powered by large language models like LLaMA). 

Designed to be easily integrated into any platform (forums, chatting apps, comment sections), GuardianAI automatically evaluates text-based inputs and makes precise decisions on whether the content should be allowed or blocked to maintain a safe community environment.

---

## 🚀 Features

- 🧠 **Advanced AI Moderation**: Utilizes Groq's high-speed LLMs to detect toxic, abusive, or harmful messages.
- ⚡ **High Performance & Async**: Built with **FastAPI** to handle concurrent requests efficiently and quickly.
- 🧱 **Standardized Responses**: Enjoy clean, predictable JSON responses wrapped in a common `APIResponse` format.
- 🛡️ **Centralized Error Handling**: Automatically catches and formats HTTP errors, unprocessable entities (422), and internal server errors (500).
- 🧹 **Robust Input Cleaning**: Pre-processes text by removing URLs, emojis, and unwanted characters using `Pydantic` and custom utilities.
- 🔑 **Secure Configuration**: Uses environment variables for managing API keys and configuration safely.
- 🌐 **CORS Ready**: Configured allowing seamless cross-origin communication for your front-end apps.

---

## 🧰 Tech Stack

| Component | Details |
|------------|----------|
| **Framework** | FastAPI `0.120.2` |
| **Language** | Python `3.13`+ |
| **External AI** | Groq API (`llama-3.3-70b-versatile`) |
| **Server** | Uvicorn |
| **Validation** | Pydantic |

---

## ⚙️ Setup & Installation

Follow these steps to get GuardianAI running locally.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/GuardianAI.git
cd GuardianAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root of the project (or export manually):

```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the server

```bash
uvicorn main:app --reload --port 8003
```

The API will start at:
👉 **[http://127.0.0.1:8003](http://127.0.0.1:8003)**

Interactive API docs available at: 
👉 **[http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs)**

---

## 🧠 API Endpoints

### `POST /analyze`

Analyze text for toxicity and get a moderation and filtering decision.

#### 🔸 Request Body

```json
{
  "text": "Your message goes here!"
}
```

#### 🔸 Successful Response (Safe Content)

```json
{
  "status": true,
  "message": "Content is safe.",
  "data": {
    "should_block": false,
    "scores": {
      "TOXICITY": 0.05,
      "INSULT": 0.01,
      "PROFANITY": 0.0,
      "IDENTITY_ATTACK": 0.0,
      "THREAT": 0.0
    },
    "flagged_words": []
  }
}
```

#### 🔸 Successful Response (Blocked Content)

```json
{
  "status": true,
  "message": "Content contains toxic language and should be blocked.",
  "data": {
    "should_block": true,
    "scores": {
      "TOXICITY": 0.85,
      "INSULT": 0.92,
      "PROFANITY": 0.76,
      "IDENTITY_ATTACK": 0.1,
      "THREAT": 0.05
    },
    "flagged_words": ["badword1"]
  }
}
```

---

## 🧪 Quick Test (cURL)

Verify your API is working correctly via the terminal:

```bash
curl -X POST "http://127.0.0.1:8003/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really appreciate your help with this project!"}'
```

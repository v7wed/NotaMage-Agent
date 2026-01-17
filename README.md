<div align="left">

# 🧙‍♂️ NotaMage Agent v1.0.0

![Status](https://img.shields.io/badge/Status-Maintained-green?style=for-the-badge)

</div>

---

## 🎉 What's New?
- First stable version released!
- Multi-provider LLM fallback system for reliability
- Autonomous tool orchestration via LangGraph

---

## 💡 About

**NotaMage Agent** (aka "The Mage") is a **LangGraph agent wrapped in a FastAPI server** that powers the AI chat functionality in the main Notamage application. It features **autonomous tool calling** to perform CRUD operations on notes and categories, and uses **multiple LLM providers** (Google Gemini → Groq → DeepSeek) to gracefully handle rate limits.

This is a private service used by the main application. You can try interacting with the agent through the chat interface in the main app.

🔗 [**Main Notamage Application Repository**](https://github.com/v7wed/Notamage)

---

## 🧰 Tech Stack

### AI & Server
<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/LangGraph-FF6B6B?style=for-the-badge" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white" alt="uv"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
</p>

### Web Application
The agent connects to the main **Notamage web application** where users can interact with it through a dedicated chat interface.

🔗 [**Main Application Repository**](https://github.com/v7wed/Notamage)

### Deployment
<p>
  <img src="https://img.shields.io/badge/Koyeb-121212?style=for-the-badge&logo=koyeb&logoColor=white" alt="Koyeb"/>
</p>

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- API keys for at least one LLM provider (Google Gemini, Groq, or DeepSeek)
- Running instance of the main Notamage Express.js backend

### Installation

```bash
# Clone the repository
git clone https://github.com/v7wed/NotaMage-Agent.git
cd NotaMage-Agent

# Configure your .env just like .env.example with your API keys and configuration

# Create a system.txt file in the main directory containing your desired system prompt
echo "Your system prompt here" > system.txt

# If you have missing/different/extra API keys or want to customize providers,
# edit agent.py get_llm() function

# Install dependencies
uv sync

# Run the server
uv run main.py
```

The agent will be running at port **8000** (or your configured PORT) and will be expecting the Express service at **5001** (or configured EXPRESS_SERVICE_URL).

---

## 🔧 Configuration

### Conversation History
The agent uses a **sliding window** approach to manage context:
- Maximum history: 7 messages (configurable via `MAX_HISTORY_MESSAGES` in [main.py](main.py))
- Automatically truncates older messages to stay within token limits

### Provider Fallback
Rate limit handling with automatic provider switching:
1. Google Gemini 2.5 Flash Lite (primary)
2. Google Gemini 2.5 Flash
3. Google Gemini 3 Flash
4. Groq Llama 3.3 70B
5. DeepSeek Chat (fallback)

Configure the order or add providers in [agent.py](my_agent/nodes/agent.py) `get_llm()` function.

---

## 📡 API Endpoints

### POST `/chat`
Main conversation endpoint.

**Request:**
```json
{
  "user_id": "mongodb_user_id",
  "user_name": "John Doe",
  "conversation_history": [
    {"role": "user", "content": "Create a note about my meeting"},
    {"role": "assistant", "content": "I've created the note..."}
  ]
}
```

**Response:**
```json
{
  "response": "I've created your note titled 'Meeting Notes'..."
}
```

### GET `/health`
Health check endpoint for monitoring.

---

## 👨‍💻 About the Developer

Built by **Ahmed Mohammed**, an AI Engineer graduate passionate about creating intelligent applications that solve real problems.

Have suggestions or want to discuss my work? Feel free to reach out!

<a href="https://www.linkedin.com/in/v7wed/">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/>
</a>
&nbsp;&nbsp;&nbsp;
<a href="https://github.com/v7wed">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</a>

---

## 📄 License

This project is open-sourced under the **MIT License**. Feel free to use it for your own projects or further development. A mention of this repo would be greatly appreciated if you find it helpful!
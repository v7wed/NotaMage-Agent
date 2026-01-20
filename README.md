<div align="left">

# 🧙‍♂️ NotaMage Agent v1.0.1

![Status](https://img.shields.io/badge/Status-Maintained-green?style=for-the-badge)

</div>

---

## 🎉 What's New?
- **v1.0.1**: Simplified to single provider (Google Gemini) for consistency
- Graceful rate limit handling with informative user messaging
- Autonomous tool orchestration via LangGraph

---

## 💡 About

**NotaMage Agent** (aka "The Mage") is a **LangGraph agent wrapped in a FastAPI server** that powers the AI chat functionality in the main Notamage application. It features **autonomous tool calling** to perform CRUD operations on notes and categories, powered by **Google Gemini 3 Flash** (customizable).

This is a private service used by the main application. You can try interacting with the agent through the chat interface in the main app, though please note the live demo runs on **free-tier resources with limited daily quota**.

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

# If you want to use a different provider or model,
# edit agent.py agent_node() function

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

### LLM Provider
The agent uses **Google Gemini 3 Flash** as its sole provider for consistency and to prevent hallucination issues that can occur when switching providers mid-conversation.

**Rate Limit Handling:**
- Automatically detects rate limit errors (429, quota exceeded, etc.)
- Returns a professional, informative message explaining the demo's limitations
- Maintains user experience even when quota is exhausted
- You can modify how rate limiting is handled in the agent_node in [agent.py](my_agent/nodes/agent.py).

You can also modify the model or provider in [agent.py](my_agent/nodes/agent.py) make sure you configure your api keys in the enviroment variables.

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
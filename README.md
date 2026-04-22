# Durable AI Research Architect 🚀

An entry-level demonstration of **Agentic Workflow Architecture** using Python and the Gemini 1.5 API. This project moves beyond simple chatbots by implementing **Persistence**, **Tool-Use**, and **Key Rotation**.

## 🏗️ Architectural Features

- **State Persistence:** Uses a `state_manager` to save progress to `agent_state.json`. If the system crashes or is interrupted (Ctrl+C), it resumes from the last completed phase.
- **Dynamic Key Rotation:** Implements a fallback strategy that rotates through multiple Google Gemini API keys to handle `429 Rate Limit` errors automatically.
- **Function Calling:** Demonstrates "Tool-Use" by allowing the LLM to trigger real-time web searches via DuckDuckGo.
- **Graceful Error Handling:** Custom signal handling for `KeyboardInterrupt` to ensure clean exits without messy tracebacks.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Model:** Gemini 1.5 Flash / Pro
- **Tools:** DuckDuckGo Search API
- **Environment:** `python-dotenv` for secret management

## 🚀 Getting Started

1. **Clone the repo:**
   ```bash
   git clone https://github.com/MSam-data/Durable_Research_Architect_Agent.git
   cd Durable_Research_Architect_Agent

2. **Install dependencies:**
- `pip install -r requirements.txt`

3. **Find .env file:**
add your API keys and log file root folder as:
- `GEMINI_KEY_1=your_first_api_key`
- `GEMINI_KEY_2=your_second_api_key`

4. **Run the application:**
- `python main.py`

# Franglais 🇫🇷🇬🇧 

A bilingual AI language tutor deployed as a self-healing Telegram bot. **Franglais** is designed to bridge the gap between English and French by providing real-time syntactic corrections, IPA pronunciation breakdowns, and natural conversational practice.

## 🏗️ Architecture & Tech Stack

This project was built with a focus on resilient infrastructure and high-speed LLM inference, moving beyond a simple API script to a production-ready containerized service.

* **Application Logic:** Python 3.11, `python-telegram-bot` (v20+ async)
* **AI/Inference:** Groq API (`openai/gpt-oss-20b`) for near-instantaneous low-latency responses.
* **Containerization:** Docker & Docker Compose for isolated, reproducible deployments.
* **State Management:** In-memory sliding window buffer to maintain multi-turn conversational context.
* **Automation & Supervision:** Linux `cron` daemon handling background service polling and automated container recovery.

## ✨ Key Features

* **Contextual Memory:** Retains the last 10 interactions in a sliding window buffer, allowing for fluid, multi-turn conversations without dropping context.
* **Bilingual Correction System:** Automatically detects input language, corrects French grammar errors, provides English explanations for the corrections, and replies naturally in French to keep the conversation moving.
* **Phonetic Breakdowns:** Supplies IPA (International Phonetic Alphabet) transcriptions formatted securely to prevent Telegram URL-parsing conflicts.
* **Self-Healing Deployment:** Configured to run in detached mode (`-d`) with scheduled system polling to ensure zero-downtime recovery in case of process failure.
* **12-Factor Config:** Strict separation of environment variables (`.env`) from application code for secure credential rotation without container rebuilds.

## 🚀 Quick Start

### Prerequisites
* [Docker](https://docs.docker.com/engine/install/) and Docker Compose installed.
* A Telegram Bot Token (from [@BotFather](https://t.me/BotFather)).
* A [Groq API Key](https://console.groq.com/keys).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Davetakesoff/Franglais.git](https://github.com/Davetakesoff/Franglais.git)
   cd Franglais

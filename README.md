# Morning News Summary Bot

A scheduled Python bot that fetches daily news, summarizes it with an LLM, and emails you a concise morning briefing.

## Features

- Fetches top headlines using NewsAPI.
- Summarizes headlines via an OpenRouter LLM (DeepSeek/GPT-style model).
- Sends the final summary to your inbox using Gmail SMTP.
- Runs automatically every morning using a cron-style scheduler.

## Tech Stack

- Python
- APScheduler
- NewsAPI
- OpenRouter (OpenAI-compatible client)
- Gmail SMTP
- python-dotenv

## Setup

1. **Clone the repo**
```
git clone https://github.com/Gauri2096/Daily-News-Bot.git
cd Daily-New-Bot
```


2. **Create and activate a virtual environment**
```
python -m venv .venv
```
Windows
```
..venv\Scripts\activate
```
macOS / Linux
```
source .venv/bin/activate
```

3. **Install dependencies**
```
pip install -r requirements.txt
```


4. **Create a `.env` file**

Create a `.env` in the project root:
```
NEWSAPI_KEY=your_newsapi_key_here
GMAIL_ADDRESS=your_gmail_address_here
GMAIL_APP_PASSWORD=your_gmail_app_password_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
## Usage

### 1. Run once manually

To test the full pipeline (fetch → summarize → email):
```
python daily_summary.py
```

This will:

- Fetch recent headlines.
- Generate a short bullet-style summary with the LLM.
- Email the summary to `GMAIL_ADDRESS`.

### 2. Run on a schedule (daily at 08:00)

Use the scheduler runner:
```
python scheduler_runner.py
```


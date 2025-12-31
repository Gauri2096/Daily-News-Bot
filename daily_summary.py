import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from openai import OpenAI
import smtplib
import ssl
from email.message import EmailMessage

load_dotenv()

NEWSAPI_KEY=os.getenv("NEWSAPI_KEY")
GMAIL_ADDRESS=os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD=os.getenv("GMAIL_APP_PASSWORD")
OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")

newsapi=NewsApiClient(api_key=NEWSAPI_KEY)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def fetch_headlines(limit=5):
    print("Calling NewsAPI get_top_headlines...")
    response = newsapi.get_top_headlines(
        language="en",
        page_size=limit,
    )
    print("Raw NewsAPI response:", response)

    status = response.get("status")
    if status != "ok":
        print("NewsAPI error status:", status)
        print("Error code:", response.get("code"))
        print("Error message:", response.get("message"))
        return "Error fetching headlines."

    articles = response.get("articles", [])
    if not articles:
        return "No articles returned by NewsAPI for this query."

    lines = []
    for a in articles:
        title = a.get("title") or ""
        description = a.get("description") or ""
        lines.append(f"- {title}: {description}")
    return "\n".join(lines)

def summarize_headlines(headlines_text: str) -> str:
    if not headlines_text.strip():
        return "No news headlines available today."

    prompt = (
        "You are a news assistant for busy professionals.\n"
        "Given a list of headlines, produce a short, clear morning briefing.\n"
        "Constraints:\n"
        "- 3–6 bullet points.\n"
        "- No sensational language.\n"
	"- No line in bold text.\n"
        "- Group related items together.\n\n"
        f"HEADLINES:\n{headlines_text}"
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",  # or another DeepSeek/GPT model you prefer
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.4,
    )

    return response.choices[0].message.content.strip()

def send_email(subject: str, body: str, to_address: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_address
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)

def main():
    print("Fetching headlines...")
    headlines = fetch_headlines()
    print("\n=== HEADLINES TEXT ===\n")
    print(headlines)

    print("\nSummarizing with OpenRouter...")
    summary = summarize_headlines(headlines)
    print("\n=== SUMMARY TEXT ===\n")
    print(summary)

    full_body = f"Good morning!\n\nHere is your news summary:\n\n{summary}\n"

    print("\nSending email...")
    send_email(
        subject="Your Morning News Summary",
        body=full_body,
        to_address=GMAIL_ADDRESS,
    )
    print("Email sent.")

if __name__== "__main__":
    main()
    
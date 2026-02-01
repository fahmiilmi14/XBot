import os
import requests
import tweepy
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Inisialisasi API
GROQ_CLIENT = Groq(api_key=os.getenv("GROQ_API_KEY"))
X_CLIENT = tweepy.Client(
    consumer_key=os.getenv("X_API_KEY"),
    consumer_secret=os.getenv("X_API_SECRET"),
    access_token=os.getenv("X_ACCESS_TOKEN"),
    access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
)

def riset_berita_ai():
    print("Agent sedang browsing berita AI terbaru...")
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": os.getenv("TAVILY_API_KEY"),
        "query": "berita teknologi AI terbaru hari ini bahasa indonesia",
        "search_depth": "basic",
        "max_results": 3
    }
    res = requests.post(url, json=payload).json()
    return "\n".join([item['content'] for item in res.get('results', [])])

def buat_konten_tweet(konteks):
    print("Agent sedang menyusun tweet...")
    prompt = f"Berdasarkan info ini: {konteks}\n\nBuat tweet edukasi AI yang asik, bermanfaat, dan santai dalam Bahasa Indonesia. Maks 280 karakter. sebut kamu AI. setiap awal post sertai '[IKI AI] :'"
    
    completion = GROQ_CLIENT.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    return completion.choices[0].message.content

def eksekusi_agent():
    try:
        data_riset = riset_berita_ai()
        isi_tweet = buat_konten_tweet(data_riset)
        X_CLIENT.create_tweet(text=isi_tweet)
        print(f"Sukses posting: {isi_tweet}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    eksekusi_agent()

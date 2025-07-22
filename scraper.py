import requests
from bs4 import BeautifulSoup
import pandas as pd

def detect_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        if "login" in response.url.lower() or "signin" in response.url.lower():
            return {"auth_required": True}

        soup = BeautifulSoup(response.text, 'html.parser')

        content = {
            "auth_required": False,
            "text": [p.text.strip() for p in soup.find_all('p') if p.text.strip()],
            "links": [a['href'] for a in soup.find_all('a', href=True)],
            "images": [img['src'] for img in soup.find_all('img', src=True)],
            "tables": [],
            "raw_html": soup
        }

        try:
            tables = pd.read_html(url)
            content["tables"] = tables
        except:
            pass  # No readable tables

        return content

    except Exception as e:
        return {"error": str(e)}

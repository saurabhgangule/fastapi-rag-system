import feedparser
import json
from bs4 import BeautifulSoup

def rss_to_json(url):
    feed = feedparser.parse(url)
    
    feed_data = {
        "title": feed.feed.get("title", ""),
        "entries": []
    }

    for entry in feed.entries:
        raw_summary = entry.get("summary", "")
        
        # Initialize BeautifulSoup to parse the summary HTML
        soup = BeautifulSoup(raw_summary, "html.parser")
        
        # Find the image tag
        img_tag = soup.find("img")
        image_url = img_tag["src"] if img_tag else None
        
        # Remove the image tag from the soup to leave only the text
        if img_tag:
            img_tag.decompose()
        
        # Get the cleaned text (strip whitespace)
        clean_summary = soup.get_text(separator=" ").strip()

        feed_data["entries"].append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published_at": entry.get("published", ""),
            "image": image_url, # Now in its own field
            "summary": clean_summary # Now text only
        })

    return json.dumps(feed_data, indent=4)
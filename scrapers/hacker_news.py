import requests

def fetch_top_stories(limit=10):
    """
    Hacker Newsから上位の記事を取得して返します。
    """
    try:
        # 上位の記事IDを取得
        top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_ids_url)
        response.raise_for_status()
        top_ids = response.json()[:limit]

        articles = []
        for item_id in top_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
            item_response = requests.get(item_url)
            item_response.raise_for_status()
            item_data = item_response.json()
            
            if 'url' in item_data:
                articles.append({
                    'title': item_data.get('title'),
                    'url': item_data.get('url'),
                    'source': 'Hacker News'
                })
        
        return articles
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")
        return []

if __name__ == "__main__":
    stories = fetch_top_stories(5)
    for s in stories:
        print(f"- {s['title']} ({s['url']})")

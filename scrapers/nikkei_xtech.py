import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_nikkei_articles(limit=10):
    """
    日経クロステックから新着記事を取得して返します。
    """
    url = "https://xtech.nikkei.com/"
    base_url = "https://xtech.nikkei.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # 新着記事リストのセレクタ
        items = soup.select('.articleList_item') or soup.select('.p-card') or soup.select('article')
        
        for item in items[:limit]:
            # タイトルのセレクタ
            title_tag = item.select_one('.articleList_itemTitle') or item.select_one('.p-card_title')
            
            a_tag = None
            if title_tag:
                a_tag = title_tag.find('a')
            
            if not a_tag:
                a_tag = item.find('a')
                
            if a_tag and a_tag.get('href'):
                title = a_tag.get_text(strip=True)
                if title:
                    link = urljoin(base_url, a_tag.get('href'))
                    articles.append({
                        'title': title,
                        'url': link,
                        'source': 'Nikkei xTech'
                    })
        
        return articles
    except Exception as e:
        print(f"Error fetching Nikkei xTech: {e}")
        return []

if __name__ == "__main__":
    articles = fetch_nikkei_articles(5)
    for a in articles:
        print(f"- {a['title']} ({a['url']})")

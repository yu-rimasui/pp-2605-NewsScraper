import os
from datetime import datetime
from scrapers.hacker_news import fetch_top_stories
from scrapers.nikkei_xtech import fetch_nikkei_articles
from utils.summarizer import summarize_articles

def generate_markdown(all_articles):
    """
    記事リストからMarkdown形式のテキストを生成します。
    """
    today = datetime.now().strftime("%Y-%m-%d")
    md_content = f"# Daily Tech News - {today}\n\n"
    
    # ソースごとにグループ化
    sources = {}
    for article in all_articles:
        source = article['source']
        if source not in sources:
            sources[source] = []
        sources[source].append(article)
    
    for source, articles in sources.items():
        md_content += f"## {source}\n\n"
        for article in articles:
            md_content += f"### [{article['title']}]({article['url']})\n"
            md_content += f"{article.get('summary', '要約なし')}\n\n"
    
    return md_content

def main():
    print("Fetching news articles...")
    hn_articles = fetch_top_stories(limit=10)
    nikkei_articles = fetch_nikkei_articles(limit=10)
    
    all_articles = hn_articles + nikkei_articles
    
    if not all_articles:
        print("No articles found.")
        return

    print(f"Found {len(all_articles)} articles. Summarizing...")
    # 記事を要約
    summarized_articles = summarize_articles(all_articles)
    
    # Markdown生成
    md_content = generate_markdown(summarized_articles)
    
    # 保存
    os.makedirs("news", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = f"news/{today}.md"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"Successfully generated: {file_path}")

if __name__ == "__main__":
    main()

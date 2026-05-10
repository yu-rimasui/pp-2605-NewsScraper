import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def summarize_articles(articles):
    """
    記事のリストを受け取り、Gemini APIを使用して要約を生成します。
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found. Skipping summarization.")
        for article in articles:
            article['summary'] = "要約なし (APIキー未設定)"
        return articles

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # プロンプトの作成
    prompt = "以下の技術ニュース記事のタイトルとURLのリストを読み、それぞれについて1〜2文で日本語で簡潔に要約してください。\n\n"
    for i, article in enumerate(articles):
        prompt += f"{i+1}. タイトル: {article['title']}\n   URL: {article['url']}\n"
    
    prompt += "\n出力形式は各記事の要約のみを箇条書きで返してください。番号は付けないでください。"

    try:
        response = model.generate_content(prompt)
        summaries = response.text.strip().split('\n')
        
        # 要約を記事リストにマッピング
        # 行数が一致しない場合のフォールバック
        for i, article in enumerate(articles):
            if i < len(summaries):
                article['summary'] = summaries[i].strip('- ').strip()
            else:
                article['summary'] = "要約の生成に失敗しました。"
                
        return articles
    except Exception as e:
        print(f"Error during summarization: {e}")
        for article in articles:
            article['summary'] = "要約エラー"
        return articles

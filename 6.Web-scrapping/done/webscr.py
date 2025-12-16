import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/all/'

try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')
    print("Результаты поиска статей по ключевым словам:", KEYWORDS)
    print("=" * 80)
    found_articles = []
    for article in articles:
        title_elem = article.find('h2', class_='tm-title')
        if not title_elem:
            continue
        title_text = title_elem.text.strip()
        title_link = title_elem.find('a')
        if title_link and 'href' in title_link.attrs:
            article_url = 'https://habr.com' + title_link['href']
        else:
            continue
        time_elem = article.find('time')
        if time_elem and 'datetime' in time_elem.attrs:
            date_str = time_elem['datetime']
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M')
            except:
                formatted_date = date_str
        else:
            formatted_date = "Дата не указана"
        preview_elem = article.find('div', class_='article-formatted-body')
        preview_text = preview_elem.text.strip().lower() if preview_elem else ""

        title_lower = title_text.lower()

        search_text = title_lower + " " + preview_text

        found_keywords = []
        for keyword in KEYWORDS:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', search_text):
                found_keywords.append(keyword)
        if found_keywords:
            found_articles.append({
                'date': formatted_date,
                'title': title_text,
                'url': article_url,
                'keywords': found_keywords
            })
    if found_articles:
        for i, article in enumerate(found_articles, 1):
            print(f"{i}. {article['date']} – {article['title']}")
            print(f"   Ссылка: {article['url']}")
            print(f"   Найдены ключевые слова: {', '.join(article['keywords'])}")
            print()
    else:
        print("Статей по заданным ключевым словам не найдено.")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке страницы: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")

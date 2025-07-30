import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import time

SITE_URL = "https://ks-yanao.ru"
RSS_FILENAME = "feed.xml"

def get_news_links():
    print("?? Ищу новости на главной странице...")
    response = requests.get(SITE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_links = []
    
    # !!! Замените '.news-item' на реальный класс/тег !!!
    for item in soup.select('.news-item'):
        link = item.find('a')['href']
        if not link.startswith('http'):
            link = SITE_URL + link
        news_links.append(link)
        print(f"Найдена ссылка: {link}")
    
    return news_links

def parse_article(article_url):
    print(f"?? Парсим статью: {article_url}")
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Заголовок (настройте селектор!)
    title = soup.find('h1').text.strip()
    
    # Основной контент (настройте селектор!)
    content = soup.select('.article-content')[0]  # Пример: класс с текстом
    
    # Чистим от ненужных элементов
    for elem in content.find_all(['script', 'style', 'iframe']):
        elem.decompose()
    
    # Исправляем ссылки на изображения
    for img in content.find_all('img'):
        if not img['src'].startswith('http'):
            img['src'] = SITE_URL + img['src']
    
    return {
        'title': title,
        'url': article_url,
        'content': str(content)
    }

def generate_rss():
    print("??? Генерирую RSS...")
    fg = FeedGenerator()
    fg.title('Новости ks-yanao.ru (полные статьи)')
    fg.link(href=SITE_URL, rel='alternate')
    fg.description('RSS с полным текстом и изображениями')

    news_links = get_news_links()
    for link in news_links[:5]:  # Ограничим 5 статьями для теста
        article = parse_article(link)
        fe = fg.add_entry()
        fe.title(article['title'])
        fe.link(href=article['url'])
        fe.description(article['content'])
        time.sleep(2)  # Пауза между запросами
    
    fg.rss_file(RSS_FILENAME)
    print(f"? Готово! RSS-лента сохранена в {RSS_FILENAME}")

if __name__ == '__main__':
    generate_rss()
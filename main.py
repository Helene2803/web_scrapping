import requests
import bs4
from datetime import datetime

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

url = 'https://habr.com/ru/articles/'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, features='lxml')

articles = soup.select('div.article-snippet')
found = False

for article in articles:
    title = article.select_one('h2.tm-title.tm-title_h2')
    link = 'https://habr.com' + title.select_one('a')['href']
    date = article.select_one('time')['title'][:10]
    date_object = datetime.strptime(date, '%Y-%m-%d')
    date = date_object.strftime('%d-%m-%Y')

    response = requests.get(link)
    article_soup = bs4.BeautifulSoup(response.text, features='lxml')

    # Поиск по preview-информации текущей страницы.
    previews = article_soup.select_one('p')

    for keyword in KEYWORDS:
        if keyword in title.text.lower() or keyword in previews.text.lower():
            print(date, '-', title.text.strip(), '-', link)
            found = True

    # Поиск по всему тексту статьи.
    paragraphs = article_soup.select('p')
    full_text = ' '.join(p.text.strip() for p in paragraphs)

    for keyword in KEYWORDS:
        if keyword in title.text.lower() or keyword in full_text.lower():
            print(date, '-', title.text.strip(), '-', link)
            found = True
            break

if not found:
    print('Нет подходящих статей.')




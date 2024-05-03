import requests
from bs4 import BeautifulSoup
from datetime import datetime
from crud import crud
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_html():
    response = requests.get('https://xn--80abh7bk0c.xn--p1ai/')
    return response.text

def get_count_quotes(src):
    soup = BeautifulSoup(src, 'lxml')
    text = soup.find('b').text.strip()
    return text

def get_count_pages(src):
    soup = BeautifulSoup(src, 'lxml')
    text = soup.input
    max = text['max']
    return max

max_workers = 6
def multithread(db, max_page):
    def process_page(db, page_number):
        url = f'https://xn--80abh7bk0c.xn--p1ai/index/{page_number}'
        page_content = requests.get(url).text
        soup = BeautifulSoup(page_content, 'lxml')

        #articles = soup.find_all('article')

        for article in soup.find_all('article'):
            quote_text = article.find('div', class_='quote__body').text.strip()
            quote_id = article.find('a', class_='quote__header_permalink').text.strip("#")
            quote_date = article.find('div', class_='quote__header_date').text.strip()
            date_format = "%d.%m.%Y в %H:%M"
            datetime_obj = datetime.strptime(quote_date, date_format)
            if crud.get_qoute(db, quote_id) is None:
                crud.add_qoutes(db, quote_id, quote_text, datetime_obj)
                #print(quote_id)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_page, db, page_number): page_number for page_number in range(1, max_page + 1)}

        for future in as_completed(futures):
            quote_id = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{quote_id} сгенерировано исключение: {exc}')
            else:
                print(f'Страница {quote_id} загружена в БД')
    db.commit()
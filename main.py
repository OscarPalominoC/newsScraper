import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://www.elespectador.com'
espectador_request = requests.get(url)
espectador_soup = BeautifulSoup(espectador_request.text, 'lxml')

articles_list = espectador_soup.find('section').find_all('div', attrs = {'class':'Card-title card-title h5'})
articles_links = []
for article in articles_list:
    articles_links.append(url+article.a.get('href'))

articles_links

def article_extraction_info(article_soup):
    article = {}
    try:
        title = article_soup.find('h1', attrs = {'class':'Article-Title'}).text
        article['title'] = title
    except Exception as e:
        title = None
        article['title'] = title
    try:
        date = article_soup.find('time', attrs = {'class':'Article-Time'}).text
        article['date'] = date
    except Exception as e:
        date = None
        article['date'] = date
    try:
        author = article_soup.find('span', attrs = {'class':'Article-Author'}).text
        article['author'] = author
    except Exception as e:
        author = None
        article['author'] = author
    try:
        body_list = article_soup.find('section').find_all('p', attrs = {'class':'font--secondary'})
        body = []
        for item in body_list:
            body.append(item.text)
        article['body'] = body
    except Exception as e:
        body = None
        article['body'] = body
    
    if article['title'] == None:
        return None
    
    return article

def scrape_article(article_link):
    try:
        article_request = requests.get(article_link)
    except Exception as e:
        print('Error scrapeando URL', url)
        print(e)
        return None
    if article_request.status_code != 200:
        print(f'Error obteniendo Artículo {url}')
        print(f'Status code: {article_request.status_code}')
        return None
    article_soup = BeautifulSoup(article_request.text, 'lxml')
    return_dict = article_extraction_info(article_soup)
    return_dict['url'] = article_link
    return return_dict

def extract_articles(articles_links):
    data = []
    for i, article_url in enumerate(articles_links):
        print(f'Scraping article {i+1}/{len(articles_links)}')
        try:
            data.append(scrape_article(article_url))
        except Exception as e:
            print('Article Empty')
            print(e)
        
    return data

articles = extract_articles(articles_links)

df = pd.DataFrame(articles)

df.to_csv('/home/oscar-dev/Platzimaster/Week10/NewsScraper/espectador-scraper.csv')
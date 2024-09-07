from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import requests
import pandas as pd


def setup_webdriver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

def fetch_page_source(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'List-results-items'))
        )
        return driver.page_source
    except TimeoutException:
        print(f"Timeout while waiting for page to load: {url}")
        return None
    
def parse_articles(soup):
    articles_data = {}
    content = soup.find('xpl-results-list')
    articles = content.find_all('div', class_="List-results-items")
    author_names = []
    for article in articles:
        title_element = article.find('a')
        title = title_element.text
        link = title_element.attrs['href']
        
        year_span = article.find('span', string=lambda t: t and 'Year:' in t)
        year = year_span.text.split(': ')[1] if year_span else 'Year not found'
        
        conference_title = article.find('div', class_='description text-base-md-lh').a.string.strip()
        
        conference_paper_span = article.find('span', string=lambda text: text and 'Conference Paper' in text)
        journal_article_span = article.find('span', string=lambda text: text and 'Journal Article' in text)
        paper_type = conference_paper_span.string if conference_paper_span else (journal_article_span.string if journal_article_span else 'Unknown')
        
        publisher_span = article.find('span', string=lambda text: text and 'Publisher:' in text)
        publisher_span_text = publisher_span.find_next_sibling('span') 
        publisher = publisher_span_text.text.strip() if publisher_span_text else 'Publisher not found'

        author_names = [author.find('span').text.strip() for author in article.find_all('a', target="_self")]
        authors = article.find_all('a', target="_self")
        if authors == []:
            authors = article.find_all('button', {'xplhighlight' : True})
            year = article.find('span', string=lambda t: t and 'Year:' in t).text.split(': ')[1]
        for author in authors:
            author_names.append(author.find('span').text.strip())
        articles_data[title] = [
            "https://ieeexplore.ieee.org" + link,
            list(set(author_names)),
            year,
            conference_title,
            paper_type,
            publisher
        ]
        author_names = []
    return articles_data

def getTitles(end_page):
    driver = setup_webdriver()
    result = {}
    
    for i in range(1, end_page):
        url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL&pageNumber={i}"
        page_source = fetch_page_source(driver, url)
        
        if page_source:
            soup = BeautifulSoup(page_source, 'html.parser')
            articles_data = parse_articles(soup)
            result.update(articles_data)
    
    driver.quit()
    return result

def load_page(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'u-mb-1'))
        )
        return driver.page_source
    except TimeoutException:
        print(f"Timeout while waiting for abstract to load on {url}")
        return None
    

def extract_abstract(soup):
    dynamic_content = soup.find('div', {'xplmathjax': True})
    if dynamic_content:
        return dynamic_content.get_text(strip=True)
    else:
        return "No abstract found"
        

def getInfo(paper_dict):
    driver = setup_webdriver()
    result = {}
    
    for paper_title, paper_info in paper_dict.items():
        url = paper_info[0] 
        page_source = load_page(driver, url)
        
        if page_source:
            soup = BeautifulSoup(page_source, 'html.parser')
            abstract = extract_abstract(soup)
            result[paper_title] = abstract
    
    driver.quit()
    return result


def dict_to_csv(publications_dict, abstract_dict):
    rows = []
    for title, details in publications_dict.items():
        rows.append({
            'Title': title,
            'Author': ', '.join(details[1]),
            'Abstract': abstract_dict.get(title, ''), 
            'Year': details[2],
            'Journal/Conference Name': details[3],
            'Conference or Journal': details[4],
            'Publisher': details[5]
    })
    df = pd.DataFrame(rows)
    df.to_csv('publications.csv', index=False)
    

if __name__ == "__main__":
    end_page = 52 
    publications_dict = getTitles(end_page)
    abstract_dict = getInfo(publications_dict)
    dict_to_csv(publications_dict, abstract_dict)
    print("CSV file 'publications.csv' saved successfully.")



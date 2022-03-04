import requests
from bs4 import BeautifulSoup
from db import PostgresqlManager
import pandas as pd


def _add_https_prefix(url):
    if 'http' in url:
        return url
    else:
        return "https://" + url


def search_google(text):
    token = "+".join(text.split(" "))
    url = f"https://www.google.com/search?q={token}&hl=en&gl=us"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'accept-language': 'en-US;q=0.9',
    }
    response = requests.get(url, headers=headers)
    html = response.text
    bs = BeautifulSoup(html, "html.parser")
    return bs


def scrape(name):
    try:
        bs = search_google(name)
        div_id_search = bs.find("div", {"id": "search"})
        first_href = div_id_search.find("a")
        first_href = first_href["href"]
        href = first_href
        href = _add_https_prefix(href)
        print(name)
        print(href)
        if 'search' in href:
            return 'failed'

        pm = PostgresqlManager(dotenv_path='../.env')
        sql = """
        INSERT INTO company(name, url)
        VALUES(%s, %s)
        """
        pm.execute_sql(sql=sql, parameters=(name, href),  commit=True)

        return href
    except AttributeError:
        return 'failed'


if __name__ == "__main__":
    df = pd.read_csv('./apples.csv')
    df["url"] = df.apply(lambda x: scrape(x.client_name), axis=1)
    df.drop(df.index[df['url'] == 'failed'], inplace=True)
    df.columns = ['name', 'url']
    df = df.drop_duplicates()
    pgm = PostgresqlManager(dotenv_path='../.env')
    pgm.copy_from(df=df, table="company", commit=True)
    pass

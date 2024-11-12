import json
from datetime import datetime
import requests


def get_news_data():
    try:
        conn = "https://api.nytimes.com/svc/archive/v1/2002/10.json?api-key=Uk0DAHWEzvDcpsjumb5ZoGp2GmgtfcSq"
        response = requests.get(conn)
        json_response = response.json()
    except Exception as e:
        print(e)


    return parse_data(json_response)


def parse_data(json_response):
    try:
        articles = []
        docs = json_response["response"]["docs"]

        for article in docs:
            authors = []
            if 'byline' in article and 'person' in article['byline']:
                for person in article['byline']['person']:
                    author = {
                        'firstname': person.get('firstname', ''),
                        'middlename': person.get('middlename', ''),
                        'lastname': person.get('lastname', ''),
                        'role': person.get('role', '')
                    }
                    authors.append(author)

            # pub_date = datetime.strptime(article['pub_date'], "%Y-%m-%dT%H:%M:%S%z")
            # formatted_date = pub_date.strftime("%B %d, %Y")

            parsed_article = {
                'abstract': article.get('abstract', ''),
                'web_url': article.get('web_url', ''),
                'headline': article['headline'].get('main', ''),
                # 'pub_date': formatted_date,
                'section_name': article.get('section_name', ''),
                'lead_paragraph': article.get('lead_paragraph', ''),
                'keywords': [kw.get('value', '') for kw in article.get('keywords', [])],
                'authors': authors
            }
            articles.append(parsed_article)

        return articles
    except KeyError as e:
        print(f"Error parsing data: {e}")
        return None


get_news_data()
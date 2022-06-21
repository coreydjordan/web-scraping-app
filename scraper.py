from bs4 import BeautifulSoup
import requests as rqs
import json
import pprint as pp
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def hacker_scrape():
    '''
    scrapes the hacker news website
    
    '''
    titles = []
    points = []
    CURRENT_PAGE = 1
    URL = "https://news.ycombinator.com/"
    res = rqs.get(URL)
    soup = BeautifulSoup(res.content, 'html.parser')
    for line in soup.find_all("tr", class_="athing"):
        lines = dict()
        lines['rank'] = line.find('span', 'rank').text.strip().replace(".", "")
        lines['rank'] = int(lines['rank'])
        lines['title'] = line.find('a', 'titlelink').text.strip().replace("\u2019", "'").replace("\u2013", "-")
        lines['source'] = line.find('span', class_='sitestr').text.strip() if line.find('span', 'sitestr') is not None else 'None'

        titles.append(lines)
    for line in soup.find_all("td", class_="subtext"):
        lines = dict()
        lines['score'] = line.find('span', class_='score').text.strip() if line.find('span', 'score') is not None else 'None'
        lines['author'] = line.find('a', class_='hnuser').text.strip() if line.find('a', 'hnuser') is not None else 'None'
        points.append(lines)
    headlines = []
    for k, v in zip(titles, points):
        k.update(v)
        headlines.append(k)
    with open("hacker-news.json", "w") as fp:
        json.dump(headlines, fp, indent=4)
    with open('hacker-news.json') as json_file:
        data = json.load(json_file)
        new_data = dict()
    for items in data:
        x=[[items['author'],items['title']] for items in data ]
        new_data.update(items)
        authors = new_data['author']
        headline_title = new_data['title']
        r = {
            'author':authors,
            'title':headline_title
        }
    return render_template('index.html', x=x)

if __name__ == '__main__':
    # hacker_scrape()
    app.run(host='127.0.0.1', port=8000, debug=True)
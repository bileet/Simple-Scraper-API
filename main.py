import httpx, os
from sanic import Sanic, text, json
from bs4 import BeautifulSoup

app = Sanic('Simple_Scraper')

@app.route('/')
async def index(request):
    return json({"success": True})

@app.post('/extract')
async def extract(request):
    try:
        # Getting URL to scrape
        url = request.args.get('url')

        # Make GET request to the given URL
        req = httpx.get(url)

        # Init BeautifulSoup parser
        soup = BeautifulSoup(req.text, 'html.parser')
    except:

        # If something went wrong
        return json({
            'success': False,
            'error': 'Something went wrong!'
        })

    # Scrape the the website <title>
    title = soup.find('title').getText()

    # Scrape all texts on the website
    texts = []
    for txt in soup.find_all('span') + soup.find_all('p'):
        string = txt.getText()
        if  string not in texts and string.__len__() != 0:
            texts.append(string)

    # Scrape all links on the website
    links = [link.get('href') for link in soup.find_all('a')]

    # Scrape all images on the website
    images = [link.get('src') for link in soup.find_all('img')]

    # Return a success response with scraped data
    return json({
        'success': True,
        'data': {
            'title': title,
            'texts': texts,
            'links': links,
            'images': images
        }
    })

@app.on_response
async def headers(request, response):
    # Allow API calls from any website
    response.headers['Access-Control-Allow-Origin'] = '*'

if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 8080))

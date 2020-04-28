# Broken Links

Sample code that can be used to crawl a website and identify any broken `href` links on the site. The project uses Python3 and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) package for processing the html from a site.

## Running the crawler

1. Download the code
1. Update `maxUrlsToCrawl` in `brokenlinks.py`to a suitable value, so the crawler does not run forever
1. Run `python3 brokenlinks.py` from terminal

Once the process completes, the list of various urls is written in a csv within the same folder as the code, which includes data in following format -
<parentPage>, <link_on_the_page>, <http_status_of_the_link>

Note: The crawler tries to verify external links available on the site, though it does not process any further links available on the external page

The code assumes you have installed Python3, Requests and BeautifulSoup on your machine

## Possible improvements

1. Some websites prevent crawlers from retrieving the page so need to handle that in code
1. Code does not work with SPA sites

## NOTE

The code is provided for learning purpose only. Do not use this to crawl a site that is not controlled/owned by you. Get permission from the website owner before crawling or scraping their site

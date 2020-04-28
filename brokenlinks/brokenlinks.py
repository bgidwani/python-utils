from urllib.parse import urldefrag, urljoin, urlparse

import collections
import bs4
import requests
import time

maxUrlsToCrawl = 5
urlstatuses = list()
currentUrl = ''
sitedomain = ''
crawled = []  # list of pages already crawled
crawledUrlCount = 0
# delay (in seconds) between subsequent request to the site
pauseBetweenRequests = 0.4


def formatUrl(url):
    if url.startswith('http:') or url.startswith('https:'):
        return url
    else:
        return 'http://' + url


def validateUrl(url, currentpage):
    global crawledUrlCount

    if url == '':
        return False

    if crawledUrlCount > maxUrlsToCrawl:
        raise Exception("MAX Urls crawled")

    res = requests.head(url)
    crawled.append((url, res.status_code))

    updateUrlStatus(url, currentpage, res.status_code)

    if not issamedomain(url):
        return False

    if (res.is_permanent_redirect or res.is_redirect):
        return validateUrl(res.headers["location"], "")
    else:
        return url


def updateUrlStatus(url, currentpage, status_code):
    urlstatuses.append((currentpage, url, status_code))


def crawlUrl(url, currentpage):
    global crawledUrlCount
    # read the page
    try:
        urlToCrawl = validateUrl(url, currentpage)
        if urlToCrawl == False:
            return False

        print(" -- Crawling url", urlToCrawl)
        # if Url is valid retrieve the text using GET request
        res = requests.get(urlToCrawl)
        # no need to parse Url's with no html content
        if not res.headers["content-type"].startswith("text/html"):
            print(" *** Skipping", urlToCrawl, res.headers["content-type"])
            return False

        # Parse html using Beautiful Soup
        parsedHtml = bs4.BeautifulSoup(res.text, "html.parser")
        # print(parsedHtml)

        # get the links from this page and add them to the list
        links = getlinks(urlToCrawl, parsedHtml)
        time.sleep(pauseBetweenRequests)

        for link in links:
            if not wasUrlCrawled(link):
                crawledUrlCount += 1
                crawlUrl(link, url)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
        updateUrlStatus(urlToCrawl, "", -99)


def getlinks(pageurl, parsedHtml):
    "Returns a list of links from from this page to be crawled"

    urls = []  # list of links to be crawled
    # iterate over all links on the page
    for a in parsedHtml.select("a[href]"):
        # remove fragment identifiers from href links
        url = urldefrag(a.attrs.get("href"))[0]

        # exclude any empty strings
        if (url and url == '/'):
            continue

        # if it's a relative link, change to absolute
        if (not bool(urlparse(url).netloc)):
            url = urljoin(pageurl, url)

        # no need to crawl links from different domain
        if (issamedomain(url)):
            urls.append(url)
        else:
            # validate the url from other domains since it will not be crawled automatically
            validateUrl(url, pageurl)

    return urls


def issamedomain(link):
    "Determine whether the link points to the same domain."
    link_netloc = urlparse(link).netloc
    link_domain = link_netloc.lower()
    if "." in link_domain:
        link_domain = link_domain.split(
            ".")[-2] + "." + link_domain.split(".")[-1]

    return link_domain == sitedomain


def wasUrlCrawled(url):
    "Determine whether a URL is in a list of crawled URLs"
    http_version = url.replace("https://", "http://")
    https_version = url.replace("http://", "https://")
    link_crawled = False
    for link in crawled:
        if link[0] == http_version or link[0] == https_version:
            link_crawled = True
            break

    return link_crawled


sitetocrawl = input("Enter the site url to identify any broken links: ")
if sitetocrawl == '':
    sitetocrawl = "www.crummy.com"

sitetocrawl = formatUrl(sitetocrawl)

# identify the domain of the site being crawled
sitedomain_netloc = urlparse(sitetocrawl).netloc
sitedomain = sitedomain_netloc.lower()
if "." in sitedomain:
    sitedomain = sitedomain.split(".")[-2] + "." + sitedomain.split(".")[-1]

try:
    crawlUrl(sitetocrawl, "")
except Exception as ex:
    print(ex)

print(" ******** Processed data *********** ")
urlstatuses = sorted(urlstatuses)
fhandle = open("./output.csv", "w")
fhandle.write("Parent Page, Url, HTTP Status\n")
for (parent, url, status) in urlstatuses:
    data = parent + "," + url + "," + str(status) + "\n"
    fhandle.write(data)

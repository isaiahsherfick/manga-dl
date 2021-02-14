from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from urllib.error import HTTPError
from http.client import InvalidURL
from ssl import _create_unverified_context

class AnchorParser(HTMLParser):
    def __init__(self, baseURL = ""):
        # Parent class constructor

        HTMLParser.__init__(self)

        # Set that will contain all hyperlinks found in a webpage
        self.pageLinks = set()

        # The base url of the webpage to parse
        self.baseURL = baseURL

    def getLinks(self):
        return self.pageLinks

    def handle_starttag(slef, tag, attrs):
        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":
                    #handles case of relative/absolute pathing inconsistency
                    absoluteUrl = urljoin(self.baseURL, value)
                    if urlparse(absoluteUrl).scheme in ["http","https"]:
                        self.pageLinks.add(absoluteUrl)


class MyWebCrawler(object):
    def __init__(self, url, maxCrawl=10):
        self.visited = set()
        self.starterUrl = url
        self.max = maxCrawl

        def getVisited(self):
            return self.visited

        def parse():
            try:
                # that gibberish about context is used to ignore cert validation
                #when making the web request
                htmlContent = urlopen(url,
                        context=_create_unverified_context()).read().decode()
                parser = AnchorParser(url)
                parser.feed(htmlContent)
                return parser.getLinks()
            except (HTTPError, InvalidURL, UnicodeDecodeError):
                print("FAILED: {}".format(url))

                #returns an empty set
                return set()

        def crawl():
            urlsToParse = {self.starterUrl}
            while(len(urlsToParse) > 0 and len(self.visited) < self.max):
                nextUrl = urlsToParse.pop()
                if nextUrl not in self.visited:
                    self.visited.add(nectUrl)
                    print("Parsing: {}".format(nextUrl))
                    urlsToParse |= self.parse(nextUrl)



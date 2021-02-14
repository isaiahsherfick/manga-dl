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

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (attribute, value) in attrs:
                if attribute == "href":
                    #handles case of relative/absolute pathing inconsistency
                    absoluteUrl = urljoin(self.baseURL, value)
                    if urlparse(absoluteUrl).scheme in ["http","https"]:
                        if ("https://mangadex.org/chapter" in absoluteUrl) and not ("comments" in absoluteUrl):
                            self.pageLinks.add(absoluteUrl)





class MyWebCrawler(object):
    def __init__(self, url, maxCrawl=10):
        self.visited = set()
        self.chapters = set()
        self.starterUrl = url
        self.max = maxCrawl

    def getVisited(self):
        return self.visited

    def parse(self, url):
        try:
            # that gibberish about context is used to ignore cert validation
            #when making the web request
            htmlContent = urlopen(url,
                    context=_create_unverified_context()).read().decode()
            parser = AnchorParser(url)
            parser.feed(htmlContent)
            for link in parser.getLinks():

            return parser.getLinks()
        except (HTTPError, InvalidURL, UnicodeDecodeError):
            print("FAILED: {}".format(url))

            #returns an empty set
            return set()

    def crawl(self):
        urlsToParse = {self.starterUrl}
        while(len(urlsToParse) > 0 and len(self.visited) < self.max):
            nextUrl = urlsToParse.pop()
            if nextUrl not in self.visited:
                self.visited.add(nextUrl)
                if "chapter/" in nextUrl:
                    self.chapters.add(nextUrl.rpartition('/')[2])
                    print("adding {} to chapters!".format(nextUrl.rpartition('/')[2]))
                print("Parsing: {}".format(nextUrl))
                urlsToParse |= self.parse(nextUrl)

    def sortChapters(self):
        self.chapters = sorted(self.chapters)
        for i in range(len(self.chapters)):
            self.chapters[i] = int(self.chapters[i])
        self.chapters = sorted(self.chapters)
        print("chapters after calling sort: {}".format(self.chapters))
        print("len(chapters)={}".format(len(self.chapters)))

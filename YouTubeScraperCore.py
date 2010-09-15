import sys, urllib, urllib2, re, string, cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
#import YouTubeCore

class YouTubeScraperCore:     
    #===========================================================================
    # __settings__ = sys.modules[ "__main__" ].__settings__
    # __language__ = sys.modules[ "__main__" ].__language__
    # __plugin__ = sys.modules[ "__main__"].__plugin__    
    # __dbg__ = sys.modules[ "__main__" ].__dbg__
    #===========================================================================

    #core = YouTubeCore.YouTubeCore()
    USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
        
    def scrapeTrailersGridFormat (self, page, params = {}):
        get = params.get
                 
        vobjects = []

        list = SoupStrainer(id="popular-column", name="div")
        trailers = BeautifulSoup(page, parseOnlyThese=list)
        
        if (len(trailers) > 0):
            trailer = trailers.div.div
            
            while (trailer != None):
                item ={}
                videoid = trailer.div.a['href']

                if (videoid):
                    if (videoid.find("=") > -1):
                        videoid = videoid[videoid.find("=")+1:]
                    item["videoid"] = videoid
                    item["thumbnail"] = trailer.div.a.span.img['src'] 
                    item["Title"] = trailer.div.a.span.img['title']

                    vobjects.append(item)
                trailer = trailer.findNextSibling(name="div", attrs = { 'class':"trailer-cell *v1" })
        
        print repr(vobjects)
                
        return vobjects
        
    def scrapeTrailersListFormat (self, page, params = {}):
        get = params.get
                 
        vobjects = []

        list = SoupStrainer(id="recent-trailers-container", name="div")
        trailers = BeautifulSoup(page, parseOnlyThese=list)
        
        if (len(trailers) > 0):
            trailer = trailers.div.div
            
            while (trailer != None):
                item ={}
                videoid = trailer.div.div.a['href']

                if (videoid):
                    if (videoid.find("=") > -1):
                        videoid = videoid[videoid.find("=")+1:]
                    item["videoid"] = videoid
                    item["thumbnail"] = trailer.div.div.a.span.img['src'] 
                    item["Title"] = trailer.div.div.a.span.img['title']

                    vobjects.append(item)
                trailer = trailer.findNextSibling(name="div")
        
        print repr(vobjects)
                
        return vobjects

    def _fetchPage(self, feed, params = {}):
        url = urllib2.Request(feed)
        url.add_header('User-Agent', self.USERAGENT);
        
        con = urllib2.urlopen(url);
        page = con.read()
        con.close()
        return page

if __name__ == '__main__':
    scraper = YouTubeScraperCore()
    trailers_url = "http://www.youtube.com/trailers?s=tr"
    
    print "In Theaters"
    url = trailers_url + "it"
    page = scraper._fetchPage(url)
    scraper.scrapeTrailersGridFormat(page)
    
    print " "
    print "Popular"
    url = trailers_url + "p"
    page = scraper._fetchPage(url)
    scraper.scrapeTrailersGridFormat(page)
    
    print " "
    print "Opening Soon"
    url = trailers_url + "os"
    page = scraper._fetchPage(url)
    scraper.scrapeTrailersGridFormat(page)
    
    print " "
    print "Latest"
    url = trailers_url
    page = scraper._fetchPage(url)
    scraper.scrapeTrailersListFormat(page)


    sys.exit(0);
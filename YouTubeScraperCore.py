import sys, urllib, urllib2, re, string, cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import YouTubeCore

class YouTubeScraperCore:     

    __settings__ = sys.modules[ "__main__" ].__settings__
    __language__ = sys.modules[ "__main__" ].__language__
    __plugin__ = sys.modules[ "__main__"].__plugin__    
    __dbg__ = sys.modules[ "__main__" ].__dbg__

    core = YouTubeCore.YouTubeCore()
    USERAGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
    
    urls = {}
    urls['disco_main'] = "http://www.youtube.com/disco" 
    urls['disco_search'] = "http://www.youtube.com/disco?action_search=1&query=%s"
    urls['main'] = "http://www.youtube.com"
    urls['trailers'] = "http://www.youtube.com/trailers?s=tr"
    urls['current_trailers'] = "http://www.youtube.com/trailers?s=trit"
    urls['upcoming_trailers'] = "http://www.youtube.com/trailers?s=tros"
    urls['popular_trailers'] = "http://www.youtube.com/trailers?s=trp"
        
    def scrapeTrailersGridFormat (self, page, params = {}):
        get = params.get
                 
        yobjects = []

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

                    yobjects.append(item)
                trailer = trailer.findNextSibling(name="div", attrs = { 'class':"trailer-cell *vl" })
        
        if (not yobjects):
            return (yobjects, 500)
        
        return (yobjects, 200)
    
    def searchDisco(self, query, params = {}):
        get = params.get
        url = self.urls["disco_search"] % urllib.quote_plus(query)
        print "search url " + url
        page = self._fetchPage(url)
        
        if (page.find("watch?") != -1):
            items = []
            page = page[page.find("/watch?"):page.rfind('"')]
            url = self.urls["main"] + page
            print "search result url " + url
            page = self._fetchPage(url)
            
            list = SoupStrainer(id="quicklist", name="div")
            ajax = BeautifulSoup(page, parseOnlyThese=list)
            if (len(ajax) > 0):
                if (ajax.div["data-active-ajax-url"]):
                    url = self.urls["main"] + ajax.div["data-active-ajax-url"]
                    print "ajax url " + url
                
                page = self._fetchPage(url)
                video_list = SoupStrainer(name="ol")
                videos = BeautifulSoup(page, parseOnlyThese=video_list)
                if (len(videos) > 0):
                    video = videos.li
                    while (video != None):
                        videoid = video.a["href"]
                        if (videoid.find("=") > 0):
                            videoid = videoid[videoid.find("=") +1:videoid.find("&")]
                        items.append(videoid)
                        
                        video = video.findNextSibling(name="li", attrs = { 'class':re.compile("^quicklist-item")})
            
            if (items):
                return self.core._get_batch_details(items)
            else:
                if (self.__dbg__):
                    print self.__plugin__ + " Disco scraper failed, youtube probably changed their layout"    
        return ([], 303)

        
    def scrapeTrailersListFormat (self, page, params = {}):
        get = params.get         
        yobjects = []
        
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
                    item = self.core._get_details(videoid)
                    
                    if (item):
                        item["thumbnail"] = trailer.div.div.a.span.img['src'] 
                        yobjects.append(item)
                        
                trailer = trailer.findNextSibling(name="div")
        if (not yobjects):
            return (yobjects, 500)
        
        return (yobjects, 200)

    def _fetchPage(self, feed, params = {}):
        url = urllib2.Request(feed)
        url.add_header('User-Agent', self.USERAGENT);
        
        con = urllib2.urlopen(url);
        page = con.read()
        con.close()
        return page
    
    def scrapeDiscoTop25(self, params = {}):
        get = params.get
        url = self.urls["disco_main"]
        page = self._fetchPage(url, params)
        list = SoupStrainer(name="div", attrs = {"class":"popular-message"})
        popular = BeautifulSoup(page, parseOnlyThese=list)
        result = []
        if (len(popular) > 0):
            videos = self.urls["main"] + popular.a["onclick"]
            if (videos.find("&quot;") > 0):
                videos = videos[videos.find("&quot;"):videos.rfind("])")]
                videos = videos.replace("&quot;","")
                videos = videos.replace(" ","")
                items = videos.split(",")
                return self.core._get_batch_details(items)

        return ("Scraper failed", 500)
        
    def scrapeDiscoTopArtist(self, params = {}):
        get = params.get
        url = self.urls["disco_main"]
        page = self._fetchPage(url, params)
        list = SoupStrainer(name="div", attrs = {"class":"popular-artists"})
        popular = BeautifulSoup(page, parseOnlyThese=list)
        if (len(popular)):
            yobjects = []
            artists = popular.findAll(attrs={"class":"popular-artist-row"})
            for artist in artists:
                item = {}
                item["search"] = artist.contents[0]
                item["Title"] = artist.contents[0]
                item["thumbnail"] = "discoball"
                item["path"] = get("path")
                item["action"] = "disco_search"
                yobjects.append(item)
                
        return (yobjects, 200)
    
    def scrapeTrailers(self, params = {}):
        get = params.get
        if (get("scraper") in self.urls):
            url = self.urls[get("scraper")]
        else :
            url = self.urls["trailers"]
        page = self._fetchPage(url, params)
        if (get("scraper") == "latest_trailers"):
            return self.scrapeTrailersListFormat(page, params)
        else:
            return self.scrapeTrailersGridFormat(page, params)
        
    def scrape(self, params = {}):
        get = params.get
        if (get("scraper") == "disco_top_25"):
            return self.scrapeDiscoTop25(params)
        if (get("scraper") == "disco_top_artist"):
            return self.scrapeDiscoTopArtist(params)
        if (get("scraper", "").find("trailers") > -1):
            return self.scrapeTrailers(params)
    
if __name__ == '__main__':

    sys.exit(0);
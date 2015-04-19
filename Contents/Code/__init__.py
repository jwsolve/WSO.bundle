######################################################################################
#
#	Watchseries-online.ch - v1.00
#
######################################################################################

TITLE = "Watch Series Online"
PREFIX = "/video/wso"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_NEXT = "icon-next.png"
ICON_MOVIES = "icon-movies.png"
ICON_SERIES = "icon-series.png"
ICON_QUEUE = "icon-queue.png"
BASE_URL = "http://watchseries-online.ch"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_MOVIES)
	VideoClipObject.art = R(ART)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
	HTTP.Headers['Host'] = "watchseries-online.ch"
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	return Shows()

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/shows")	
def Shows():

	oc = ObjectContainer()
	oc.add(InputDirectoryObject(key = Callback(Search), title='Search', summary='Search WSO', prompt='Search for...'))
	#html = HTML.ElementFromURL(BASE_URL + '/2005/07/index.html', cacheTime = CACHE_1HOUR)
	#for each in html.xpath("//div[@class='ddmcc']/ul/ul/li"):
	#	try:
	#		title = each.xpath("./a/text()")[0]
	#		url = each.xpath("./a/@href")[0]
	#		thumb = ""
	#	except:
	#		continue

	#	oc.add(DirectoryObject(
	#		key = Callback(ShowEpisodes, title = title, url = url),
	#			title = title,
	#			thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
	#			)
	#	)
	return oc

######################################################################################
@route(PREFIX + "/showepisodes")	
def ShowEpisodes(title, url):

	oc = ObjectContainer(title1 = title)
	html = HTML.ElementFromURL(url, cacheTime = CACHE_1HOUR)

	for each in html.xpath("//span[@class='PostHeader']"):
		title = each.xpath("./a/text()")[0]
		url = each.xpath("./a/@href")[0]
		thumb = ""
		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
				)
		)
	for each in html.xpath("//a[@class='prev']"):
		try:
			title = "Previous"
			url = each.xpath("./@href")[0]
			oc.add(DirectoryObject(
				key = Callback(ShowEpisodes, title = title, url = url),
					title = title,
					thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
					)
			)
		except:
			continue
	for each in html.xpath("//a[@class='next']"):
		try:
			title = "Next"
			url = each.xpath("./@href")[0]
			oc.add(DirectoryObject(
				key = Callback(ShowEpisodes, title = title, url = url),
					title = title,
					thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
					)
			)
		except:
			continue
	return oc

######################################################################################
@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page = HTML.ElementFromURL(url, cacheTime = CACHE_1HOUR)
	title = page.xpath("//span[@class='PostHeader']/a/text()")[0]
	url = url
	thumb = ""

	oc.add(VideoClipObject(
		title = title,
		thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png'),
		url = url
		)
	)	
	
	return oc

####################################################################################################
@route(PREFIX + "/search")
def Search(query):

	oc = ObjectContainer(title2='Search Results')
	html = HTML.ElementFromURL(BASE_URL + '?s=%s' % String.Quote(query, usePlus=True))

	for each in html.xpath("//span[@class='PostHeader']"):
		title = each.xpath("./a/text()")[0].strip('\n')
		url = each.xpath("./a/@href")[0]
		thumb = ""
		oc.add(DirectoryObject(
			key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
				)
		)
	for each in html.xpath("//a[@class='prev']"):
		try:
			title = "Previous"
			url = each.xpath("./@href")[0]
			oc.add(DirectoryObject(
				key = Callback(ShowEpisodes, title = title, url = url),
					title = title,
					thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
					)
			)
		except:
			continue
	for each in html.xpath("//a[@class='next']"):
		try:
			title = "Next"
			url = each.xpath("./@href")[0]
			oc.add(DirectoryObject(
				key = Callback(ShowEpisodes, title = title, url = url),
					title = title,
					thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-series.png')
					)
			)
		except:
			continue
	return oc

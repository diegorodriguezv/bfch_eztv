import chanutils.torrent
from chanutils import select_all, select_one, get_attr
from chanutils import get_doc, post_doc, get_json
from chanutils import get_text, get_text_content, replace_entity, byte_size
from playitem import TorrentPlayItem, ShowMoreItem, PlayItemList

#_SEARCH_URL = "https://eztv.ch/search/"
_SEARCH_URL = "http://eztvapi.re/shows/1?keywords="

_FEEDLIST = [
  {'title':'Latest', 'url':'https://eztv.ch'},
  {'title':'Popular', 'url':'http://eztvapi.re/shows/1'},
]

def name():
  return 'EZTV'

def image():
  return 'icon.png'

def description():
  return "EZTV Torrents Channel (<a target='_blank' href='https://eztv.ch'>https://eztv.ch</a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  if idx > 0:
    data = get_json(_FEEDLIST[idx]['url'])
    return _extract_showlist(data)
  else:
    doc = get_doc(_FEEDLIST[idx]['url'], proxy=True)
    return _extract_html(doc)

def search(q):
  url = _SEARCH_URL + q
  data = get_json(url)
  return _extract_showlist(data)

def showmore(imdb_id):
  data = get_json('http://eztvapi.re/show/' + imdb_id)
  return _extract_show(data)

def _extract_html(doc):
  rtree = select_all(doc, 'tr.forum_header_border')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a.epinfo')
    title = get_text(el)
    img = '/img/icons/film.svg'
    el = select_one(l, 'a.magnet')
    url = get_attr(el, 'href')
    results.add(TorrentPlayItem(title, img, url))
  return results

def _extract_showlist(data):
  results = PlayItemList()
  for r in data:
    title = r['title']
    img = r['images']['poster']
    url = r['imdb_id']
    subtitle = "Year: " + r['year'] + ", "
    subtitle = subtitle + "Seasons: " + str(r['num_seasons']) + ", "
    subtitle = subtitle + "Rating: " + str(r['rating']['percentage']) + "%"
    synopsis = '<a target="_blank" href="http://www.imdb.com/title/' + r['imdb_id'] + '/">View on IMDB</a>'
    results.add(ShowMoreItem(title, img, url, subtitle, synopsis))
  return results

def _extract_show(data):
  results = PlayItemList()
  img = data['images']['poster']
  rtree = data['episodes'] 
  for r in rtree:
    title = r['title']
    url = r['torrents']['0']['url']
    subtitle = "Season: " + str(r['season']) + ", Episode: " + str(r['episode'])
    synopsis = r['overview']
    results.add(TorrentPlayItem(title, img, url, subtitle, synopsis))
  return results

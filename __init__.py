import chanutils.torrent
from chanutils import select_all, select_one, get_attr, post_doc
from chanutils import get_doc, get_json, series_season_episode
from chanutils import get_text, get_text_content, replace_entity, byte_size
from playitem import TorrentPlayItem, ShowMoreItem, PlayItemList

_BASE_URL = "https://eztv.ag"
_SEARCH_URL = _BASE_URL + "/search/"

_FEEDLIST = [
  {'title':'Latest', 'url':'https://eztv.ag'},
  {'title':'All Shows', 'url':'https://eztv.ag/showlist/rating/'},
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
  doc = get_doc(_FEEDLIST[idx]['url'], proxy=False)
  if idx > 0:
    return _extract_showlist(doc)
  else:
    return _extract_html(doc)

def search(q):
  q = q.replace(' ', '-')
  doc = get_doc(_SEARCH_URL + q, proxy=False)
  return _extract_html(doc)

def showmore(show_url):
  doc = get_doc(_BASE_URL + show_url, proxy=False)
  return _extract_html(doc)

def _extract_showlist(doc):
  rtree = select_all(doc, 'tr[name="hover"]')
  img = None
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a.thread_link')
    title = get_text(el)
    url = get_attr(el, 'href')
    el = select_one(l, 'b')
    rating = get_text(el)
    subtitle = "Rating: " + rating
    item = ShowMoreItem(title, img, url, subtitle)
    results.add(item)
  return results

def _extract_html(doc):
  rtree = select_all(doc, 'tr.forum_header_border[name="hover"]')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a.epinfo')
    title = get_text(el)
    img = '/img/icons/film.svg'
    el = select_one(l, 'a.magnet')
    url = get_attr(el, 'href')
    if url is None:
      continue
    subs = series_season_episode(title)
    results.add(TorrentPlayItem(title, img, url, subs=subs))
  return results

def _extract_show(data):
  results = PlayItemList()
  img = data['images']['poster']
  series = data['title']
  rtree = data['episodes'] 
  for r in rtree:
    title = r['title']
    url = r['torrents']['0']['url']
    subtitle = "Season: " + str(r['season']) + ", Episode: " + str(r['episode'])
    synopsis = r['overview']
    subs = {'series':series, 'season':r['season'], 
            'episode':r['episode']}
    results.add(TorrentPlayItem(title, img, url, subtitle, synopsis, subs=subs))
  return results

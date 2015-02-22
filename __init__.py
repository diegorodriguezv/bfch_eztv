import chanutils.torrent
from chanutils import get_doc, post_doc, select_all, select_one, get_attr
from chanutils import get_text, get_text_content, replace_entity, byte_size
from playitem import TorrentPlayItem, PlayItemList

_SEARCH_URL = "https://eztv.ch/search/"

_FEEDLIST = [
  {'title':'Latest', 'url':'https://eztv.ch'},
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
  doc = get_doc(_FEEDLIST[idx]['url'], proxy=True)
  return _extract(doc)

def search(q):
  payload = {'SearchString1':q, 'SearchString':'', 'search':'Search'}
  doc = post_doc(_SEARCH_URL, payload)
  return _extract(doc)

def _extract(doc):
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

import requests
import json
import functools

class cache(object):

  def __init__(self, fn):
    self.fn = fn
    self._cache = {}
    functools.update_wrapper(self, fn)

  def __call__(self, *args, **kwargs):
    key = str(args) + str(kwargs)
    if key in self._cache:
      ret = self._cache[key]
    else:
      ret = self._cache[key] = self.fn(*args, **kwargs)

    return ret

  def clear_cache(self):
    self._cache = {}


def _wiki_request(params):
  '''
  Make a request to the Wikipedia API using the given search parameters.
  Returns a parsed dict of the JSON response.
  '''
  global RATE_LIMIT_LAST_CALL
  global USER_AGENT

  params['format'] = 'json'
  if not 'action' in params:
    params['action'] = 'query'

  headers = {
    'User-Agent': USER_AGENT
  }

  if RATE_LIMIT and RATE_LIMIT_LAST_CALL and \
    RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT > datetime.now():

    # it hasn't been long enough since the last API call
    # so wait until we're in the clear to make the request

    wait_time = (RATE_LIMIT_LAST_CALL + RATE_LIMIT_MIN_WAIT) - datetime.now()
    time.sleep(int(wait_time.total_seconds()))

  r = requests.get(API_URL, params=params, headers=headers)

  if RATE_LIMIT:
    RATE_LIMIT_LAST_CALL = datetime.now()

  return r.json()

def page(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
  '''
  Get a WikipediaPage object for the page with title `title` or the pageid
  `pageid` (mutually exclusive).
  Keyword arguments:
  * title - the title of the page to load
  * pageid - the numeric pageid of the page to load
  * auto_suggest - let Wikipedia find a valid page title for the query
  * redirect - allow redirection without raising RedirectError
  * preload - load content, summary, images, references, and links during initialization
  '''

  if title is not None:
    if auto_suggest:
      results, suggestion = search(title, results=1, suggestion=True)
      try:
        title = suggestion or results[0]
      except IndexError:
        # if there is no suggestion or search results, the page doesn't exist
        raise PageError(title)
    return WikipediaPage(title, redirect=redirect, preload=preload)
  elif pageid is not None:
    return WikipediaPage(pageid=pageid, preload=preload)
  else:
    raise ValueError("Either a title or a pageid must be specified")

@cache
def summary(title, sentences=0, chars=0, auto_suggest=True, redirect=True):
  '''
  Plain text summary of the page.
  .. note:: This is a convenience wrapper - auto_suggest and redirect are enabled by default
  Keyword arguments:
  * sentences - if set, return the first `sentences` sentences (can be no greater than 10).
  * chars - if set, return only the first `chars` characters (actual text returned may be slightly longer).
  * auto_suggest - let Wikipedia find a valid page title for the query
  * redirect - allow redirection without raising RedirectError
  '''

  # use auto_suggest and redirect to get the correct article
  # also, use page's error checking to raise DisambiguationError if necessary
  page_info = page(title, auto_suggest=auto_suggest, redirect=redirect)
  title = page_info.title
  pageid = page_info.pageid

  query_params = {
    'prop': 'extracts',
    'explaintext': '',
    'titles': title
  }

  if sentences:
    query_params['exsentences'] = sentences
  elif chars:
    query_params['exchars'] = chars
  else:
    query_params['exintro'] = ''

  request = _wiki_request(query_params)
  summary = request['query']['pages'][pageid]['extract']

  return summary

summary('Water')
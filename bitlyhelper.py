import urllib.request
import json

TOKEN = "2702f6f265be750dcad2b6057e498ec22c9f13e3"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class BitlyHelper:
	def shorten_url(self, longurl):
		try:
			url = ROOT_URL+ SHORTEN.format(TOKEN, longurl)
			response = urllib.request.urlopen(url).read()
			jr = json.loads(response)
			return jr['data']['url']
		except Exception as e:
			print (e)

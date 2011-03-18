"""
A dinky little script which scrapes logo image URLs out of a few news sites' HTML.

Extremely verbose, so's it can function as a teaching aid.
"""

from pyquery import PyQuery as pq
import re
import urllib2
import webbrowser

urls = [
	'http://cnn.com',
	'http://nytimes.com',
	'http://wired.com',
]

header_re = re.compile('header|hdr|logo')


def get_header_image_from_url(url):
	# open the URL, and parse its HTML using PyQuery
	html = pq(urllib2.urlopen(url).read())

	# get all <img> elements from the page's HTML source
	images = html('img')

	header_img_candidates = []
	for img in images:
		# do any of the image's attributes (src="", alt="", etc.) contain a string like "header", "hdr", etc?
		matching_image_attributes = [v for k, v in img.attrib.iteritems() if header_re.findall(v)]

		# does the image have alt text?
		image_has_alt_text = bool(img.attrib.get('alt'))

		if matching_image_attributes and image_has_alt_text:
			# based on the heuristics we're using, it's likely that this guy could be a header/logo image
			header_img_candidates.append(img)

	if header_img_candidates:
		# header images are usually found at the beginning of a page's HTML
		header_img = header_img_candidates[0]

		# where's the image located?
		src = header_img.attrib.get('src')
		if src:
			if src[0] == '/':
				# src is relative url (like '/images/header.png'), prepend the domain to create a full URL
				src = url + src

			# okay, we're pretty sure we found the header image, let's see what it looks like
			webbrowser.open_new(src)


for url in urls:
	get_header_image_from_url(url)

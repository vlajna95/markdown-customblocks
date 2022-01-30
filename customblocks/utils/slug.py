import re
import unicodedata
import functools
from urllib.parse import quote

RE_TAGS = re.compile(r'</?[^>]*>', re.UNICODE)
RE_INVALID_SLUG_CHAR = re.compile(r'[^\w\- ]', re.UNICODE)
RE_SEP = re.compile(r' ', re.UNICODE)
RE_ASCII_LETTERS = re.compile(r'[A-Z]', re.UNICODE)


def _uslugify(text, sep="_", case="lower", percent_encode=False, normalize='NFC'):
	"""Unicode slugify (`utf-8`)."""

	# Normalize, Strip html tags, strip leading and trailing whitespace, and lower
	slug = RE_TAGS.sub('', unicodedata.normalize(normalize, text)).strip()
	if case == 'lower':
		slug = slug.lower()
	elif case == 'lower_ascii':
		def lower(m):
			"""Lowercase character."""
			return m.group(0).lower()
		slug = RE_ASCII_LETTERS.sub(lower, slug)
	elif case == 'fold':
		slug = slug.casefold()
	# Remove non word characters, non spaces, and non dashes, and convert spaces to underscores.
	slug = RE_SEP.sub(sep, RE_INVALID_SLUG_CHAR.sub('', slug))
	return quote(slug.encode('utf-8')) if percent_encode else slug


def slugify(text, **kwargs):
	"""Configurable slugify."""

	sep = kwargs.get("sep", "_")
	case = kwargs.get("case", "lower_ascii")
	percent_encode = kwargs.get("percent_encode", False)
	normalize = kwargs.get("normalize", "NFC")
	return _uslugify(text, sep, case, percent_encode, normalize)
	# return functools.partial(_uslugify, sep=sep, case=case, percent_encode=percent, normalize=normalize)


"""
non_url_safe = ['"', '#', '$', '%', '&', '+', ',', '/', ':', ';', '=', '?', '@', '[', '\\', ']', '^', '`', '{', '|', '}', '~', "'"]
translate_table = {ord(char): u"" for char in non_url_safe}
translate_table["

def slugify(text):
	text = text.translate(translate_table)
	text = u"_".join(text.split())
	return text
"""
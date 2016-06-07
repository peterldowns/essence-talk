# coding: utf-8
import re


def to_sentences(text):
  return _sentence_splitter.split(text)

def is_stopword(word):
  return word.lower() in stopwords

def clean(text):
  """ Get rid of any non-alphabetic character and clean up whitespace. """
   # Remove everything that isn't an alphabet character (only interested
   # in words, not numbers or punctuation).
  text = re.sub(r'[^a-zA-Z]', ' ', text)
  # Collapse whitespace in any amount or type (tabs, newlines, etc.) into
  # a single space.
  text = re.sub(r'\s+', ' ', text)
  return text.strip()

def to_words(text):
  return clean(text.lower()).split()

# The ~100 most common words in the english language (which will be ignored in
# the analysis), taken from
# http://www.duboislc.org/EducationWatch/First100Words.html
stopwords = set("""mr mrs ms dr the of and a to in is you that it he was for
on are as with his they i at be this have from or one had by word but not what
all were we when your can said there use an each which she do how their if will
up other about out many then them these so some her would make like him into
time has look two more write go see number no way could people my than first
water been call who oil its now find long down day did get come made may part
am let""".split())

# A simple regex for splitting text into sentences, ignoring some common
# abbreviations, numbers, and other phrases that also use a '.' to mean
# something other than the end of a sentence. In my experience this works well
# enough to compare favorably with the NLTK sentence splitter.
_sentence_splitter = re.compile(
  ur'''(?<!\d)
       (?<![A-Z]\.)
       (?<!\.[a-z]\.)
       (?<!\.\.\.)
       (?<!etc\.)
       (?<![Mm]r\.)
       (?<![Pp]rof\.)
       (?<![Dd]r\.)
       (?<![Mm]rs\.)
       (?<![Mm]s\.)
       (?<![Mm]z\.)
       (?<![Mm]me\.)
       (?:
           (?<=[.!?])|
           (?<=[.!?]['"“”\(\)\[\]])
       )
       [\s]+?
       (?=[^a-z0-9])''', re.VERBOSE)

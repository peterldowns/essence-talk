# coding: utf-8
import re
from collections import Counter

# The ~100 most common words in the english language (which will be ignored in
# the analysis), taken from
# http://www.duboislc.org/EducationWatch/First100Words.html
_stopwords = set("""mr mrs ms dr the of and a to in is you that it he was for
on are as with his they i at be this have from or one had by word but not what
all were we when your can said there use an each which she do how their if will
up other about out many then them these so some her would make like him into
time has look two more write go see number no way could people my than first
water been call who oil its now find long down day did get come made may part
am let""".split())

def is_stopword(word):
  return word.lower() in _stopwords

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

def clean(text):
  """ Get rid of any non-alphabetic character and clean up whitespace. """
   # Remove everything that isn't an alphabet character (only interested
   # in words, not numbers or punctuation).
  text = re.sub(r'[^a-zA-Z]', ' ', text)
  # Collapse whitespace in any amount or type (tabs, newlines, etc.) into
  # a single space.
  text = re.sub(r'\s+', ' ', text)
  return text.strip()

def to_sentences(text):
  return _sentence_splitter.split(text)

def to_words(text):
  return clean(text).split()


class Text(object):
  def get_results(self):
    # Returns a list of tuples (absolute_score, relative_score, sentence) in
    # descending score order.
    for sentence in self.sorted_sentences:
      score = self.scores[sentence]
      yield (score, score/self.highest_s_score, sentence)

  def __init__(self, input_text):
    self.inputstr = input_text
    if not isinstance(self.inputstr, unicode):
        self.inputstr = self.inputstr.decode('utf8')

    # Step 1: split the input into sentences.
    self.sentences = to_sentences(self.inputstr.strip())

    # Count each unique word's frequency in the input text.
    self.words = to_words(self.inputstr)
    self.word_weights = Counter()
    for word in self.words:
        # Don't count frequencies for stop words.
        if is_stopword(word):
            continue
        self.word_weights[word] += 1

    # The number of times a word has appeared in the text is its raw
    # weight. Modify these weights by certain conditions not based on
    # appearance count.
    for word in self.word_weights:
        # Modify proper noun weights (but not ALL_CAPS words)
        if word.istitle() and not word.isupper():
            self.word_weights[word] *= 1.2

    # Assign each individual sentence a weight/score based on the weights
    # of the words of which they are comprised.
    lengths = []
    self.scores = {}
    for s in self.sentences:
        sentence = clean(s)
        # Keep track of each sentence length so we can figure out an
        # average length later.
        lengths.append(len(sentence.split()))
        s_sum = 0.0 # Sum of the weights of the words in this sentence.
        s_words = 0 # Number of words in the sentence.
        for s_word in sentence.split():
            # This works because the Counter object returns 0 if a key
            # doesn't exist. Stop-words removed earlier will have a value
            # of 0.
            s_sum += self.word_weights[s_word]
            s_words += 1

        # Sentence scores are normalized by length; if it's a word-less
        # 'sentence' (because of our regex-based splitting algorithm) give
        # it a value of 0.
        self.scores[s] = s_sum/s_words if s_words else 0

    self.av_length = sum(lengths)/len(lengths)

    # Despite earlier normalization, sentence scores do depend on length.
    for sentence in self.sentences:
        length = len(clean(sentence).split())
        if length < self.av_length/1.5: # punish short self.sentences
            try:
                self.scores[sentence] = float(self.scores[sentence])/3
            except: pass
        elif length > self.av_length*1.2: # reward longer self.sentences
            try:
                self.scores[sentence] = self.scores[sentence]*3
            except: pass

    self.sorted_sentences = sorted(
            self.scores.keys(),
            key=lambda k: self.scores[k],
            reverse=True)
    self.highest_s_score = self.scores[self.sorted_sentences[0]]

    self.sorted_words = sorted(
            self.word_weights.keys(),
            key=lambda key: self.word_weights[key],
            reverse=True)
    self.highest_w_score = self.word_weights[self.sorted_words[0]]

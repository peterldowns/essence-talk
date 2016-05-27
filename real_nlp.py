# coding: utf-8

from common import *
from gensim import interfaces, utils, corpora, models, matutils

"""
class MagnitudeModel(interfaces.TransformationABC):
  def __init__(self, corpus):
    self.corpus = corpus
    self.initialize(corpus)

  def initialize(self, corpus):
    self.mags = {}
    for docno, bow in enumerate(corpus):
      self.mags[docno] = sum((
"""


class MagModel(interfaces.TransformationABC):
  def __init__(self): pass

  def __getitem__(self, bow, eps=1e-12):
    is_corpus, bow = utils.is_corpus(bow)
    if is_corpus:
      return self._apply(bow)

    return sum(v*v for _, v in bow) # L2 norm



# http://radimrehurek.com/gensim/tut2.html#available-transformations
class SimpleCountModel(interfaces.TransformationABC):
  """ Words that show up more often are more important. """
  # Derived from
  # https://github.com/piskvorky/gensim/blob/develop/gensim/models/tfidfmodel.py
  def __init__(self, corpus, normalize=True):
    self.normalize = normalize

    self.initialize(corpus)

  def initialize(self, corpus):
    self.corpus_counts = {} # word : total count in all documents
    for docno, bow in enumerate(corpus):
      for term_id, _ in bow:
        self.corpus_counts[term_id] = self.corpus_counts.get(term_id, 0.0) + 1.0

  def __getitem__(self, bow, eps=1e-12):
    is_corpus, bow = utils.is_corpus(bow)
    if is_corpus:
      return self._apply(bow)

    vector = [(term_id, self.corpus_counts.get(term_id, 0.0))
              for term_id, _ in bow]

    if self.normalize is True:
      vector = matutils.unitvec(vector)
    elif self.normalize:
      vector = self.normalize(vector)

    # make sure there are no explicit zeroes in the vector (must be sparse)
    result = [(term_id, weight)
             for term_id, weight in vector if abs(weight) > eps]
    return result


class Text(object):
  def __init__(self, input_text):
    if not isinstance(input_text, unicode):
      input_text = input_text.decode('utf8')

    self.raw_sentences = raw_sentences = to_sentences(input_text.strip())
    self.tokenized = tokenized = map(to_words, raw_sentences)
    print tokenized[0]
    self.tokenized_to_raw = tokenized_to_raw = {
        ' '.join(bag_of_words):raw_sentences[i] for i, bag_of_words in enumerate(tokenized)}

    self.dictionary = dictionary = corpora.Dictionary(tokenized)
    stop_ids = [dictionary.token2id[stopword] for stopword in list(stopwords) if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    dictionary.compactify()

    bow_corpus = map(dictionary.doc2bow, tokenized)
    self.bow_corpus = bow_corpus

    count_model = SimpleCountModel(bow_corpus, normalize=True)
    self.count_model = count_model
    count_corpus = count_model[bow_corpus]
    self.count_corpus = count_corpus

    svd_model = models.lsimodel.LsiModel(count_corpus, id2word=dictionary, num_topics=3)
    self.svd_model = svd_model
    svd_corpus = svd_model[count_corpus]
    self.svd_corpus = svd_corpus

    mag_model = MagModel()
    self.mag_model = mag_model
    mag_corpus = mag_model[svd_corpus]
    self.mag_corpus = mag_corpus

    sentence_to_doc_no = {s:i for i, s in enumerate(raw_sentences)}
    self.sorted_sentences = sorted_sentences = sorted(
        raw_sentences,
        key=lambda k: self.mag_corpus[sentence_to_doc_no[k]],
        reverse=True)
    max_score = self.mag_corpus[sentence_to_doc_no[self.sorted_sentences[0]]]

    for i, sentence in enumerate(sorted_sentences[:20]):
      score = self.mag_corpus[sentence_to_doc_no[sentence]]
      rel = score / max_score
      print score, rel, sentence, '\n', sentence_to_doc_no[sentence]

    #sorted([(v, doc_no) for doc_no, v in enumerate(text.mag_corpus)])








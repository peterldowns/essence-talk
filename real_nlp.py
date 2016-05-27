# coding: utf-8
from gensim import interfaces, utils, corpora, models, matutils

from common import *


class Text(object):
  def __init__(self, input_text):
    if not isinstance(input_text, unicode):
      input_text = input_text.decode('utf8')

    # Convert the raw text into a list of sentences.
    raw_sentences = to_sentences(input_text.strip())
    # Convert each sentence into a list of cleaned words.
    tokenized = map(to_words, raw_sentences)
    #self.tokenized_to_raw = tokenized_to_raw = {
    #    ' '.join(bag_of_words): raw_sentences[i]
    #    for i, bag_of_words in enumerate(tokenized)}

    # Calculate statistics on how often the words appear.
    dictionary = corpora.Dictionary(tokenized)
    stop_ids = [dictionary.token2id[stopword]
                for stopword in list(stopwords)
                if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_ids)
    dictionary.compactify()

    # Convert each sentence from a list of tokenized words to a list of
    # references to the dictionary's words (just changing internal
    # representation).
    bow_corpus = map(dictionary.doc2bow, tokenized)

    # Convert each sentence to a list of (word, word_count)
    count_model = SimpleCountModel(bow_corpus, normalize=True)
    count_corpus = count_model[bow_corpus]

    # Convert each sentence to a vector in 10 distinct topics, not of words.
    svd_model = models.lsimodel.LsiModel(
        count_corpus, id2word=dictionary, num_topics=10)
    svd_corpus = svd_model[count_corpus]

    # Convert each sentence to its magnitude in the 10-topic space.
    mag_model = MagnitudeModel(L1=True)
    mag_corpus = mag_model[svd_corpus]

    # Sort the original sentences by this latest score.
    sentence_to_doc_no = {s:i for i, s in enumerate(raw_sentences)}
    sorted_sentences = sorted(
        raw_sentences,
        key=lambda k: mag_corpus[sentence_to_doc_no[k]],
        reverse=True)
    max_score = mag_corpus[sentence_to_doc_no[sorted_sentences[0]]]

    # Make these structures available for further use.
    self.raw_sentences = raw_sentences
    self.tokenized = tokenized
    self.dictionary = dictionary
    self.bow_corpus = bow_corpus
    self.count_model = count_model
    self.count_corpus = count_corpus
    self.svd_model = svd_model
    self.svd_corpus = svd_corpus
    self.mag_model = mag_model
    self.mag_corpus = mag_corpus
    self.sentence_to_doc_no = sentence_to_doc_no
    self.sorted_sentences = sorted_sentences
    self.max_score = max_score

  def get_results(self):
    # Generates tuples (absolute_score, relative_score, sentence) in descending
    # score order.
    for sentence in self.sorted_sentences:
      score = self.mag_corpus[self.sentence_to_doc_no[sentence]]
      yield (score, score/self.max_score, sentence)


# http://radimrehurek.com/gensim/tut2.html#available-transformations
class SimpleCountModel(interfaces.TransformationABC):
  """ Words that show up more often are more important. """
  # Derived from
  # https://github.com/piskvorky/gensim/blob/develop/gensim/models/tfidfmodel.py
  def __init__(self, corpus, normalize=False):
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


class MagnitudeModel(interfaces.TransformationABC):
  def __init__(self, L1=True):
    self.L1 = L1

  def __getitem__(self, vec, eps=1e-12):
    is_corpus, vec = utils.is_corpus(vec)
    if is_corpus:
      return self._apply(vec)

    if self.L1:
      score = sum( v  for _, v in vec) / len(vec) if vec else 0
    else:
      score = sum(v*v for _, v in vec) / len(vec) if vec else 0
    return score

# coding: utf-8
import re
from collections import Counter

from common import *


class Text(object):
  def __init__(self, input_text):
    if not isinstance(input_text, unicode):
      input_text = input_text.decode('utf8')

    # Step 1: split the input into sentences.
    sentences = to_sentences(input_text.strip())

    # Count each unique word's frequency in the input text.
    word_weights = Counter()
    for word in to_words(input_text):
      # Don't count frequencies for stop words.
      if is_stopword(word):
        continue
      word_weights[word] += 1

    # The number of times a word has appeared in the text is its raw
    # weight. Modify these weights by certain conditions not based on
    # appearance count.
    for word in word_weights:
      # Modify proper noun weights (but not ALL_CAPS words)
      if word.istitle() and not word.isupper():
        word_weights[word] *= 1.2

    # Assign each individual sentence a weight/score based on the weights
    # of the words of which they are comprised.
    lengths = []
    average_length = 0.0
    scores = {}
    for i, raw_sentence in enumerate(sentences):
      s_clean = clean(raw_sentence)
      s_words = s_clean.split()
      s_length = len(s_words)

      # Update the average length of all sentences based on the length of this
      # sentence.
      average_length = float(average_length * i + s_length) / (i + 1)

      # Sum the weights of the words in this sentence. This is the basic
      # concept of a sentence's score.
      s_sum = 0.0
      for s_word in s_words:
        s_sum += word_weights[s_word]

      # Sentence scores are normalized by length; if the sentence has no words
      # (possible because of our very naive sentence splitting trick), give it
      # a value of 0.
      scores[raw_sentence] = float(s_sum)/s_length if s_length else 0.0

    # Despite earlier normalization, the final sentence scores do depend on
    # length.
    for raw_sentence in sentences:
      s_length = len(clean(raw_sentence).split())
      if s_length < (average_length / 1.5): # punish short sentences
        scores[raw_sentence] /= 3
      elif s_length > (average_length * 1.2): # reward longer sentences
        scores[raw_sentence] *= 3

    self.sentences = sentences # ["sentence", ...]
    self.scores = scores # {"sentence": 3.52, ...}
    self.word_weights = word_weights # {"word": 5.1}
    self.sorted_sentences = sorted(
            scores.keys(),
            key=lambda k: scores[k],
            reverse=True) # ["most important sentence", ..., "least important"]
    self.highest_sentence_score = scores[self.sorted_sentences[0]] # 9.1
    self.average_sentence_length = average_length # 5.18
    self.sorted_words = sorted(
            word_weights.keys(),
            key=lambda key: word_weights[key],
            reverse=True) # ["most important word", ..., "least important"]
    self.highest_word_score = word_weights[self.sorted_words[0]] # 51.6

  def get_results(self):
    # Generates tuples (absolute_score, relative_score, sentence) in descending
    # score order.
    for sentence in self.sorted_sentences:
      score = self.scores[sentence]
      yield (score, score/self.highest_sentence_score, sentence)



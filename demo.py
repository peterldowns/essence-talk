#!/usr/bin/env python
# coding: utf-8
import re
from itertools import islice

import bookshrink
import real_nlp
import markov
from common import to_words


def demo_markov(demo_text):
  words = to_words(demo_text)
  ngrams = markov.calc_up_to_ngram(words, 3)

  pause()
  print "------ Walking (1-deep) ... "
  _ = markov.stochastic_walk(words, 20, 1, ngrams=ngrams)
  print ""

  pause()
  print "------ Walking (2-deep) ... "
  _ = markov.stochastic_walk(words, 30, 2, ngrams=ngrams)
  print ""

  pause()
  print "------ Walking (3-deep) ... "
  _ = markov.stochastic_walk(words, 50, 3, ngrams=ngrams)
  print ""

  return ngrams


def demo_bookshrink(demo_text):
  text = bookshrink.Text(demo_text)
  for absolute, relative, sentence in islice(text.get_results(), 0, 20):
    print absolute, relative, sentence
  return text


def demo_svd(demo_text):
  text = real_nlp.Text(demo_text)
  return text


_store = {}
def cached_reader(filename):
  def read():
    content = _store.get(filename)
    if content:
      return content
    with open(filename, 'r') as fin:
      content = _store[filename] = fin.read()
    return content
  return read

# Text files for the demo
Bible = cached_reader('./texts/thebible.txt')
Union = cached_reader('./texts/obamastateofunion2011.txt')
Quixote = cached_reader('./texts/donquixote.txt')
MLK = cached_reader('./texts/ihaveadream.txt')
Mao = cached_reader('./texts/mao_clean.txt')

def pause(text=None):
  _ = raw_input((text or '>') + ' ')
  return

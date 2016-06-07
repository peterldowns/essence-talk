#!/usr/bin/env python
# coding: utf-8
"""
Little tools and helpers designed to be used in a live demo, for which I
recommend IPython. Start with `from demo import *` and  you'll have a nice
vocabulary for exploring the problem space.

Example usage:

>>> bible = LoadBible()
>>> mlk = LoadMLK()
>>> _ = demo_markov(mlk)
>>> _ = demo_markov(bible)
>>> bs_res = bookshrink.Text(mlk)
>>> matrix_res = real_nlp.Text(mlk)
>>> write_html_results(bs_res, matrix_res, count=10)
# now visit http://localhost:8080/ to see a comparison between the Bookshrink
# method and the SVD-related method.
"""

import re
from itertools import islice
from mustache import template

from essence import bookshrink
from essence import real_nlp
from essence import markov
from essence.common import to_words

# Helpers for reading text files at most once and returning the results.
_store = {}
def _cached_reader(filename):
  def read():
    content = _store.get(filename)
    if content:
      return content
    with open(filename, 'r') as fin:
      content = _store[filename] = fin.read()
    return content
  return read

LoadBible = _cached_reader('./texts/thebible.txt')
LoadUnion = _cached_reader('./texts/obamastateofunion2011.txt')
LoadQuixote = _cached_reader('./texts/donquixote.txt')
LoadMLK = _cached_reader('./texts/ihaveadream.txt')
LoadMao = _cached_reader('./texts/mao_clean.txt')
LoadClass = _cached_reader('./texts/americaclass.txt')


# Helpers for showing different types of analysis on the raw text from one of
# the example text files. `demo_text` is supposed to be a string, ideally the
# output from one of the Load* helpers.
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
  print_results(text, 10)
  return text

def demo_svd(demo_text):
  text = real_nlp.Text(demo_text)
  print_results(text, 10)
  return text


# Helpers for preinting results
def print_svd_topics(model):
  for i, desc in model.show_topics():
    print i, desc

def print_results(text, count=20):
  # `text` is a bookshrink.Text or real_nlp.Text object.
  for absolute, relative, sentence in islice(text.get_results(), 0, count):
    print absolute, relative, sentence


def write_html_results(bs, svd, count=5):
  @template('comparison.tpl')
  def render_comparison(data):
    return data, {}

  def res2dict(restup):
    return {
        'absolute': restup[0],
        'relative': '{:.2f}'.format(restup[1]),
        'sentence': restup[2],
      }

  html = render_comparison({
      'bs': [res2dict(res) for res in islice(bs.get_results(), 0, count)],
      'svd': [res2dict(res) for res in islice(svd.get_results(), 0, count)],
    })
  with open('index.html', 'w') as fout:
    fout.write(unicode(html).encode(errors='xmlcharrefreplace'))

def pause(text=None):
  _ = raw_input((text or '>') + ' ')
  return

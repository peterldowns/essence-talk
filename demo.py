#!/usr/bin/env python
# coding: utf-8
import re
from itertools import islice
from mustache import template

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
  print_results(text, 10)
  return text


def demo_svd(demo_text):
  text = real_nlp.Text(demo_text)
  print_results(text, 10)
  return text

# --------------------------------------


def print_results(text, count=20):
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


def pause(text=None):
  _ = raw_input((text or '>') + ' ')
  return


# Text files for the demo
LoadBible = cached_reader('./texts/thebible.txt')
LoadUnion = cached_reader('./texts/obamastateofunion2011.txt')
LoadQuixote = cached_reader('./texts/donquixote.txt')
LoadMLK = cached_reader('./texts/ihaveadream.txt')
LoadMao = cached_reader('./texts/mao_clean.txt')
LoadClass = cached_reader('./texts/americaclass.txt')

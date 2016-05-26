#!/usr/bin/env python
# coding: utf-8
import bookshrink
import real_nlp
from itertools import islice


def demo_bookshrink():
  demo_text = open('./texts/obamastateofunion2011.txt', 'r').read()
  text = bookshrink.Text(demo_text)
  for absolute, relative, sentence in islice(text.get_results(), 0, 20):
    print absolute, relative, sentence
  return text


def demo_svd():
  demo_text = open('./texts/obamastateofunion2011.txt', 'r').read()
  text = real_nlp.Text(demo_text)
  return text


if __name__ == '__main__':
  _ = demo_bookshrink()

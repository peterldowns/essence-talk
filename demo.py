#!/usr/bin/env python
# coding: utf-8
import bookshrink
from itertools import islice


def demo_bookshrink():
  demo_text = open('./texts/ihaveadream.txt', 'r').read()
  text = bookshrink.Text(demo_text)
  for absolute, relative, sentence in islice(text.get_results(), 0, 20):
    print absolute, relative, sentence
  return text


def demo_svd():
  pass


if __name__ == '__main__':
  _ = demo_bookshrink()

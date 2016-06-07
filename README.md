# Finding the Essence with Natural Language Processing
This repository contains code / notes / slides from a presentation I gave in late May 2016 to a small group of programmers in Bishkek, Kyrgyzstan.
My aim was to give a quick overview of some NLP techniques, starting from very simple (using [Markov chains](https://en.wikipedia.org/wiki/Markov_chain) to generate language-like text) and gradually getting more complex.
The main focus was [the code](https://github.com/peterldowns/bookshrink) behind [Bookshrink](http://bookshrink.com), a tool that uses simple word tokenization and frequency counting to pick important sentences out of a book or paper. The underlying algorithm was described in detail and its results were analyzed.
Then, the same algorithm was described in terms of more modern NLP techniques, and an additional technique ([dimensionality reduction with Principle Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis)) was added in to the mix. These results were compared against the results from the more naive algorithm, and differences were discussed.

The talk was given as a combination of slides and live demonstration using [IPython](http://ipython.org/). All of the relevant code for the demo is included in this repository.

# Installing Dependencies
This talk involves a comparison of some very naive, simple code with some much more computationally complex code, provided by the [`gensim`](http://radimrehurek.com/gensim/index.html) package. This can be slightly tricky to install,  but you should be able to make it work without too many problems by following [Gensim's installation instructions](http://radimrehurek.com/gensim/install.html). The only other dependency is [my `mustache`](https://github.com/peterldowns/python-mustache) library, which you can install with `pip`:

```bash
$ pip install -r requirements.txt
```

# Talk outline

*(more or less. these were some notes I wrote down before hand to help guide the presentation, but it didn't go exactly as planned.)*

- Hi, who am I?
  - Student at MIT, Computer Science + considering masters in Artificial Intelligence
  - Love to program, check out my github
    - My website is mostly blog posts I wrote when I was in highschool, don't bother
  - I know Kainar from working for Locu, a company that structured data in SF
- Markov Chains: first programming project
  - Demo on some texts
- Why is this interesting?
  - Basic statistics getting closer to "language"
  - words are just arbitrary symbols. Each word could be replaced by a unique emoji and the code would all run the same. This should work for other languages (try this at home?)
- Now, project with biggest impact on my life: bookshrink
  - "Find the Essence"
  - How do you think this might work?
  - Description of how it works
    - For every word, count how many times it shows up. This is the number of points each word has. Don't include very common words.
    - Make Proper Nouns worth slightly more.
    - Sentence Score = (Sum of scores of words in sentence) / number of words in sentence
    - Make slightly longer sentences worth more, slightly shorter sentences worth less (fixed penalty cutoff, not sliding)
  - If you don't believe me that this works, know this:
    - Got me in to MIT
    - I've talked about this at length in every job interview I've ever had
    - Maybe 400 lines of code total, very simple idea, definitely worth
- What are some smarter techniques?
- Dimensionality Reduction: SVD, PCA, LSI, LSA
  - M = U S V^
  - M = words x sentences
  - U = words x IDEAS
  - S = strength of IDEAS
  - V^ = IDEAS x sentences
  - Show comparison
- Norms, L1 vs L2
- Why is the SVD result not stable?

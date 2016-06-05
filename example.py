from demo import *

bible = LoadBible()
mlk = LoadMLK()

_ = demo_markov(mlk)
_ = demo_markov(bible)

bs_res = bookshrink.Text(mlk)
matrix_res = real_nlp.Text(mlk)
write_html_results(bs_res, matrix_res, count=10)
# http://localhost:8080/

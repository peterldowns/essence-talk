from demo import *

bible = LoadBible()
mlk = LoadMLK()

_ = demo_markov(mlk)
_ = demo_markov(bible)

state_of_union = LoadUnion()
bs_res = bookshrink.Text(state_of_union)
matrix_res = real_nlp.Text(state_of_union)
write_html_results(bs_res, matrix_res, count=10)
# http://localhost:8080/

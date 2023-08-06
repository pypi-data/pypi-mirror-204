from getdata import *

linear_example = get_chapter_1()
eigen_example = get_chapter_2()
f, f_str = get_chapter_3()

A = linear_example['S1.2']['A']
print(A)
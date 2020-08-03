# -*- coding: utf-8 -*-
# @Project ：content_analysis2
# @Time    : 2020-08-02 23:33
# @Author  : honywen
# @FileName: test.py
# @Software: PyCharm

import numpy as np
a = np.array([[1, 5, 5, 2],
              [9, 6, 2, 8],
              [3, 7, 9, 1]])
print(np.sum(a, axis=0))
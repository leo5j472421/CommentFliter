import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+'\libsvm-3.20\python')
from svmutil import *

y, x = svm_read_problem("Output-bow.txt")
m = svm_train(y[0:10000],x[0:10000], '-t 0 -c 1')
svm_save_model('libsvm.model', m)

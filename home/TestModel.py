from svmutil import *

y, x = svm_read_problem("Output-bow.txt")
m = svm_load_model('libsvm.model')
p_label, p_acc, p_val = svm_predict(y[10000:20000], x[10000:20000], m)

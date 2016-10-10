import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+'\libsvm-3.20\python')
from svmutil import *
from Comment import *
from Dictionary import *

def LabAndComment():
    o = open('feedback.txt','r',encoding='utf-8-sig')
    LabelAndComments = [] ;
    while True :
        c = o.readline()
        if ( c == "" ):
            break
        label = c[0]
        c = c[1:]
        comment = ""
        b = True
        while b : # readTheComment
            if ( "!!!endofcommend!!!" in c ):
                b = False
                c=c.replace("!!!endofcommend!!!","")
            comment += c + " "
            if ( b ) :
              c = o.readline()
        c=""
        b= True
        title=""
        while b : # readTheComment
            if ( "!!!endoftitle!!!" in c ):
                b = False
                c=c.replace("!!!endoftitle!!!","")
            title += c + " "
            if ( b ) :
              c = o.readline()
        c=""
        title=""
        time = o.readline()
        LabelAndComment=[label,comment,title,time]
        LabelAndComments.append(LabelAndComment)
    return LabelAndComments
def OutFile() :
  comments = LabAndComment()
  dictionary = Dictionary()
  dictionary.loadDictionary()
  i = len(comments)
  totext = ""

  for lac in comments:
      comment = Comment(lac[1])
      comment.flag = lac[0]
      text = comment.BagOfWords(dictionary)
      totext += text

  with open("Feedback-bow.txt", "w") as text_file:
    text_file.write(totext)

def ModelData():
    o = open('libsvm.model','r')
    out = open('model.txt','w')
    for a in range(9) : o.readline()
    while True :
      lines = o.readline()
      if ( lines == "" ):
          break
      line = lines.split(' ')
      if ( float(line[0]) >= 0 ):
          line[0] = '1'
      else:
          line[0] ='0'
      out.write(" ".join(str(x) for x in line))
    fb = open('Feedback-bow.txt','r')
    out.write(fb.read())
    out.close()
def UpdateModel():
  o = open('model.txt','r')
  lines = len(o.readlines())
  y, x = svm_read_problem("model.txt")
  line1 = lines/2
  line2 = lines - line1
  print( line1 + line2)
  m = svm_train(y[0:int(line1)],x[0:int(line2)], '-t 0 -c 1')
  svm_save_model('libsvm1.model', m)

UpdateModel()
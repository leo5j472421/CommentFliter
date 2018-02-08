#!python3
# -*- coding: utf8 -*-
#coding: utf8
from home.models import *
import datetime
import os,sys
#sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
#sys.setdefaultencoding('UTF8')
#print(sys.getdefaultencoding())
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+'/libsvm-3.20/python')
#print(BASE_DIR+'/libsvm-3.20/python')
from svmutil import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import  render_to_response
from bs4 import BeautifulSoup
from django.shortcuts import render
from Dictionary import *
from Comment import *
import requests
import json

def Database(video_name,video_id,all_comments,machine_num):
    try :
      Comments.objects.get(video_id=video_id)
      OComment= Comments.objects.get(video_id=video_id) 
      Comments.objects.filter(video_id=video_id).update(all_comments=int(OComment.all_comments)+int(all_comments),machine_num=int(OComment.machine_num)+int(machine_num),time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),click=OComment.click+1)
    except :
      Comments.objects.create(video_name=video_name,video_id=video_id,all_comments=all_comments,machine_num=machine_num,time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),click=1)
    

def home(request):
    comments = Comments.objects.all() 
    return render_to_response('home.html', locals())
    #return render_to_response('home.html')
def table(request):
    comments = Comments.objects.all() 
    comments = comments[::-1]
    return render_to_response('table.html', locals())
        
def magic(request):
    return render_to_response('magic.html')

    
def OneLine(string):
    s = ""
    for a in string :
        if a != '\n' :
            s += a
    return s
    
def back(request) :
    error = True 
    if request.GET['youtube_address'] == 'Search the video you like...' :
        error = True 
    else :
        error = False
    
    if error :
      return render_to_response('home.html', locals())
  
    if request.GET['youtube_address'] != '' and request.GET['youtube_address'] != ' ' :
        #get name of video
        url = str('https://www.youtube.com/watch?v='+request.GET['youtube_address'])
        url = url.replace(' ','')
        html = requests.get(url)
        soup = BeautifulSoup(html.text)
        video_name = soup.find_all("span", attrs={"id": "eow-title"})[0].text
        video_name = OneLine(video_name)
        url = url.replace('/watch?v=','/embed/')
        
        #get comments
        #ID = str(request.GET['youtube_address']).split('=')[1]
        ID = request.GET['youtube_address']
        r=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&order=relevance&textFormat=plainText&videoId={ID}&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID))
        t = json.loads(r.text)
        try :
          commentss = [[item['snippet']['topLevelComment']['snippet']['authorDisplayName'],item['snippet']['topLevelComment']['snippet']['textDisplay'],item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],item['snippet']['topLevelComment']['snippet']['authorChannelUrl']] for item in t['items']]
          comments=MachineOrNot(commentss)
        except :
          return render_to_response('youtube.html', locals())
        machine_num = 0 
        for a in comments:
          if (a['Machine']):
            machine_num += 1  
        try :
            PageToken=t['nextPageToken']
            more = True 
        except :
            pageToken='null'
            more = False
        Database(video_name,ID,len(comments),machine_num)
        return render_to_response('youtube.html', locals())
    else:
        return HttpResponseRedirect('/home/')

def MachineOrNot( comments ):
    dictionary = Dictionary()
    dictionary.loadDictionary()
    CommentAndSpam=[]
    for text in comments :
      get_text = text[1]
      #print(get_text)
      comment = Comment(get_text)
      comment = comment.BagOfWords(dictionary)
      comment = comment.split(' ')
      comment = comment[1:-1]
      #print(comment)
      bow = {}
      for word in comment:
        temp = word.split(':')
        bow[int(temp[0])] = float(temp[1])

      m = svm_load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)),'libsvm.model'))
      p_label, p_acc, p_val = svm_predict([1], [bow], m)
      if p_acc[0] == 0:
          CommentAndSpam.append({ 'UserName' : text[0],'Text':text[1],'Machine':False,'ProfileUrl':text[2],'UserUrl':text[3]})
      else:
          CommentAndSpam.append({ 'UserName' : text[0],'Text':text[1],'Machine':True,'ProfileUrl':text[2],'UserUrl':text[3]})
          #CommentAndSpam.append([text[0],text[1],True,text[2],text[3]])
    return CommentAndSpam
    
    
def LoadMoreComments(request):
    PageToken = request.GET['PageToken']
    ID = request.GET['ID']
    #print('callNotM')
    print(ID)
    print('~~'+PageToken)
    
    try :
      r=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&order=relevance&textFormat=plainText&pageToken={PageToken}&videoId={ID}&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID,PageToken=PageToken))
      t = json.loads(r.text)
      commentss = [[item['snippet']['topLevelComment']['snippet']['authorDisplayName'],item['snippet']['topLevelComment']['snippet']['textDisplay'],item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],item['snippet']['topLevelComment']['snippet']['authorChannelUrl']] for item in t['items']]
      comments=MachineOrNot(commentss)
      
    except:
      print(t)
    machine_num = 0 
    for a in comments:
      if (a['Machine']):
        machine_num += 1
    Database('name',ID,len(comments),machine_num)
    try:
      PageToken=t['nextPageToken']
    except:
      PageToken='null'
    return render_to_response('LoadMoreComments.html', locals())

def LoadMoreVideos(request):
    PageToken = request.GET['PageToken']
    ID = request.GET['ID']
    #print('callNotM')
    print(PageToken)
    try :
      r=requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=30&order=viewCount&pageToken={PageToken}&q={ID}&type=video&videoDefinition=high&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID,PageToken=PageToken))
      t = json.loads(r.text)
      videos=[]
      for a in t['items']:
        if( a['id']['kind']=='youtube#video'):
            video={'id':a['id']['videoId'],'title':a['snippet']['title'],'picture':a['snippet']['thumbnails']['high']['url'],'description':a['snippet']['description']}
            videos.append(video)
    except:
      HttpResponse("")
    try:
      PageToken=t['nextPageToken']
    except:
      PageToken='null'
    return render_to_response('LoadMoreVideos.html', locals())
   
def Feedback(request):
    print('FB')
    print(request.GET)
    '''j = json.loads(request.GET)
    label = j['label']
    text = j['text']
    video = j[video]
    print(text)'''
    label = request.GET['label']
    if ( label == 'true' ):
        l = '1'
    else:
        l = '0'
    text = request.GET['text']
    print( text+ '~~~~~~~~~~~~~~~~~~~~~` ' )
    #text = unicode( request.GET['text'] , "utf-8")
    video = request.GET['video']
    text = str(text).encode('utf-8').decode('utf-8-sig')
    answer = l + ' ' + text + ' !!!endofcommend!!!\n' + video + '!!!endoftitle!!!\nTime: ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(answer)
    o = open(BASE_DIR+'/home/feedback.txt','a',encoding='utf-8-sig')
    o.write(answer+'\n')
    o.close()
    return HttpResponse('Successful')
    
def Search(request):
        ID = NoWSpace(request.GET['youtube_address'])

        r=requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&q={ID}&order=viewCount&maxResults=30&relevanceLanguage=fr&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID))
        t = json.loads(r.text)
        videos=[]
        for a in t['items']:
          if( a['id']['kind']=='youtube#video'):
            try:
              video={'id':a['id']['videoId'],'title':a['snippet']['title'],'picture':a['snippet']['thumbnails']['high']['url'],'description':a['snippet']['description']}
              videos.append(video)
            except:
              print('error url')
        try :
            PageToken=t['nextPageToken']
            more = True
        except :
            pageToken='null'
        return render_to_response('index.html', locals())
        
def hot(request):
        try :
          ID = NoWSpace(request.GET['ID'])
        except:
          ID = 'US'
        r=requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&chart=mostPopular&regionCode={ID}&maxResults=50&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID))
        t = json.loads(r.text)
        videos=[]
        for a in t['items']:
          if( a['kind']=='youtube#video'):
            video={'id':a['id'],'title':a['snippet']['title'],'picture':a['snippet']['thumbnails']['high']['url'],'description':a['snippet']['description']}
            videos.append(video)
        try :
            PageToken=t['nextPageToken']
            more = True
        except :
            pageToken='null'
        return render_to_response('index.html', locals())
        
def NoWSpace(String):
    String=String.replace('$','%24')
    String=String.replace('-','%2D')
    String=String.replace('_','%5F')
    String=String.replace('.','%2E')
    String=String.replace('+','%2B')
    String=String.replace('!','%21')
    String=String.replace('*','%2A')
    String=String.replace('%','%25')
    String=String.replace('"','%22')
    String=String.replace("'","%27")
    String=String.replace('(','%28')
    String=String.replace(')','%29')
    String=String.replace(';','%3B')
    String=String.replace('/','%2F')
    String=String.replace('?','%3F')
    String=String.replace(':','%3A')
    String=String.replace('@','%40')
    String=String.replace('=','%3D')
    String=String.replace('$','%26')
    String=String.replace('|','%7C')
    String=String.replace('#','%23')
    return String.replace(' ','+')
#Search('angelina+guitar')
    

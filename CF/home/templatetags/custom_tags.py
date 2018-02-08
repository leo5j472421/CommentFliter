from django import template
from bs4 import BeautifulSoup
import requests
import json
register = template.Library()
def percentage(a,b):
    try :
        return round(a*100/b,2)
    except :
        return 0.00  
register.filter('percentage', percentage)

def cutt(value, arg):
    """Removes all values of arg from the given string"""
    print('ss')
    return value + arg
register.filter('cutt', cutt)
def GetMoreComments(PageToken,ID):
    r=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&textFormat=plainText&videoId={ID}&pageToken={PageToken}&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID,PageToken=PageToken))
    t = json.loads(r.text)
    commentss = [[item['snippet']['topLevelComment']['snippet']['authorDisplayName'],item['snippet']['topLevelComment']['snippet']['textDisplay'],item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl'],item['snippet']['topLevelComment']['snippet']['authorChannelUrl']] for item in t['items']]
    comments.extend(MachineOrNot(commentss))
    return comments
register.filter('GetMoreComments', GetMoreComments)

def extend(a,b):
    print(a)
    print(b)
    a.extend(b)
    print(a)
    return a
register.filter('extend', extend)

def NextPageToken(PageToken,ID):
    print('callsuc')
    r=requests.get('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&maxResults=100&textFormat=plainText&videoId={ID}&pageToken={PageToken}&key=AIzaSyAZqRuapzU5PE0wsV1dBWuQL2ePRP3DjaI'.format(ID= ID,PageToken=PageToken))
    t = json.loads(r.text)
    try:
      PageToken=t['nextPageToken']
    except:
      PageToken='null'
    return PageToken
register.tag(NextPageToken)
class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            print(template.VariableDoesNotExist)
            value = ""
        context[self.var_name] = value
        return u""

def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)

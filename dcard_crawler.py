'''

API	URL
看板資訊(meta)	http://dcard.tw/_api/forums
文章資訊(meta)	http://dcard.tw/_api/forums/{看板名稱}/posts
文章內文	http://dcard.tw/_api/posts/{文章編號}
文章內引用連結	http://dcard.tw/_api/posts/{文章編號}/links
文章內留言	http://dcard.tw/_api/posts/{文章編號}/comments

＊文章資訊(meta) 與 文章內留言 預設使用熱門度 (popularity) 作為排序，而且一次請求 (request) 中只回應 30 筆。

想要讓這兩項使用 時間 排序，可在 GET 參數中加入 popular=false
欲取得更多的 文章資訊(meta)，可以使用 before={某文章編號}來獲得早於 #{某文章編號} 的另外 30 筆 資訊。
欲取得更多的 文章內留言，可以使用 after={某樓層} 來獲得大於 #{某樓層} 的另外 30 筆 留言。

'''

import _thread
import time
import requests
import numpy as np
from lxml import etree
import time
url = 'https://www.dcard.tw/f/whysoserious/p'


def get_article(post_num):
    
    
    #print(post_num)
    urla = 'http://dcard.tw/_api/posts/{post_num}'
    urlb = 'http://dcard.tw/_api/posts/{post_num}/comments'
    comments = []
    param =  {}


    Q = requests.get( urla.format(post_num=str(post_num)) ).json()
    
    try:
        if Q['forumAlias'] != 'whysoserious':
            #print(Q['forumAlias'])
            return
    except:
        return
    
    
    article = Q['content']
    
    
    Q = requests.get( (urlb).format(post_num=str(post_num)), param).json()
    
    #這邊有小問題 會影響效率 也爬不到90樓以後的東西
    #總之這邊是弄留言的
    for i in range(0,3):
        Q = requests.get( (urlb).format(post_num=str(post_num)),param).json()
        param['after'] = param.get('after',0)+len(Q)
        comments += Q
       # print(Q)
    
    for x in comments:
        
        '''
        --------------------------------------------------------
        
        變數改這邊~~~ 就可以找了
        
        {  
        "id":"6d872423-6530-4cd4-abe3-d35245e47137",
        "anonymous":true,
        "postId":226104349,
        "createdAt":"2018-03-22T08:28:07.650Z",
        "updatedAt":"2018-03-22T08:28:07.650Z",
        "floor":13,
        "content":"白帽 那個搜尋器\n\n是不是因為多了話題\n\n格式跑掉惹OAO)\n\n我搜校系都搜不到東西\"> <)\n\n\n\n-麥",
        "likeCount":0,
        "withNickname":false,
        "hiddenByAuthor":false,
        "gender":"M",
        "school":"國立清華大學",
        "host":false,
        "liked":false,
        "reportReason":"",
        "currentMember":false,
        "hidden":false,
        "inReview":false
        }

        --------------------------------------------------------
        '''
        
        sth,sth1,schoolname,gender = '很高很高的山','','交通大學','M'
        
        #print("----------------------")
        try:
            if(article.find('sth')!=-1):
                print(article)
            
            if( (x['school'].find(schoolname)!=-1 and x['gender'] == gender) or x['content'].find(sth1)!=-1 ):
                print(x['floor'],x['content'],x['school'], post_num)
        except:
            pass
    
    
def partition(a,b,post):
    pa = time.time()

    print('@@',a,b)

    for c in range(a,b):
        try:
            get_article(post[c])
        except:
            pass
    
    pb = time.time()
    print('time: ', pb-pa)



def get_forum_post(forum_name, deep):
    url = 'http://dcard.tw/_api/forums/{x}/posts'.format(x=str(forum_name))
    
    param =  {}
    Q = requests.get( url , param).json()
    result = []
    
    for i in range(0,deep):
        Q = requests.get( url , param).json()
        result = result + [x['id'] for x in Q]
        param['before'] = int(result[-1])
        
    return result



page_deep = 100                         #要翻幾層
post = get_forum_post('whysoserious', page_deep)
print(post,len(post))
thread_num = 15                         #線程數

    

p = np.linspace(0,page_deep*30-1,thread_num)


for i in range(0,thread_num-1):
    _thread.start_new_thread( partition, (int(p[i]) , int(p[i+1]) , post ) )



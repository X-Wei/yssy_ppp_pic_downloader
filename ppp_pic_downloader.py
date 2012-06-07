#! /usr/bin/python 
# -*- coding: utf-8 -*- 
import sys, os, string, re, urllib, urllib2, cookielib, socket

def pic_download(url):
    content=session.open(url).read().decode('gb2312','ignore').encode('UTF-8')#解决中文乱码问题
    content=re.findall(r'<tr><td>(.*)',content)[0]
    sp=content.split('<tr><td>')
    socket.setdefaulttimeout(2)#设定超时时间
    for ln in sp:
        try:
            num=re.findall(r'(.*)<td>.?<td>',ln)[0]
            ln=re.findall(r'bbstcon(.*)html',ln)
            if len(ln)==1:
                url='https://bbs.sjtu.edu.cn/'+'bbstcon'+ln[0]+'html'
                postsession=session.open(url)
                postctnt=postsession.read().decode('gb2312','ignore').encode('UTF-8')#the encoding problem is solved!!!
                post_title=num+'_'+re.findall(r'<title>(.*)-',postctnt)[0]
                print post_title
                if not os.path.isdir(download_dir+'/'+post_title):
                    os.mkdir(download_dir+'/'+post_title)
                picurls=re.findall(r'IMG SRC=\"(.*)\" onload',postctnt)
                for pu in picurls:#pu=picurl
                    pu=pu if 'http' in pu else 'https://bbs.sjtu.edu.cn/'+pu
                    pn=pu.split('/')[-1]
                    if os.path.exists(download_dir+'/'+post_title+'/'+pn): print pn, 'already exists!'
                    else:
                        path=download_dir+'/'+post_title+'/'+pn
                        urllib.urlretrieve(pu,path)
                        print pn,'saved!'
                postsession.close()
        except:
            info=sys.exc_info()  
            print info[0],":",info[1]  
            continue
    print 'DONE~'

if __name__ == '__main__':
    download_dir = 'yssy_ppp'
    if not os.path.isdir(download_dir): os.mkdir(download_dir)
    session = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    ctnt=session.open('https://bbs.sjtu.edu.cn/bbstdoc,board,PPPerson.html').read().decode('gb2312','ignore').encode('UTF-8')
    num=filter(str.isdigit, re.findall(r'<a href=(.*)>上一页</a> <a',ctnt)[0])#看看一共有几页帖子
    print num, 'pages...'
    pic_download('https://bbs.sjtu.edu.cn/bbstdoc,board,PPPerson.html')#只下载最近一页的帖子. 若把以下几行注释去掉, 则会下载所有的帖子: 注意, 会很慢, 下载量很大!
    #~ for i in range(1,int(num)+1):#如果只想下载最近几页的, 只需把1改成比num小一些的数字
        #~ print i
        #~ pic_download('https://bbs.sjtu.edu.cn/bbstdoc,board,PPPerson,page,'+str(i)+'.html')
        #~ print '\n\n'
    os.system('''find yssy_ppp/ -type f | perl -ne 'chomp;unlink "$_" if -T $_' ''')#删除不是图片的那些文件(有些比较老的帖子 下载不下来, 或者下载下来的不是图片)
    os.system('rmdir yssy_ppp/*')#删除空文件夹
    print 'DONE FINALLY!!!'
    raw_input('press any key to exit...')

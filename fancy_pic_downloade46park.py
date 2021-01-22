import re
import requests
from bs4 import BeautifulSoup
import os


def gethttp(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except:
        print('error loading webpage')

def pagecollector(url, linkntitle):
    html = gethttp(url)
    soup = BeautifulSoup(html, 'html.parser')
    pagelist = soup.find_all('a', {'href': re.compile(r'index.php\?app=forum&act=threadview&tid=.*.*')})
    for each in pagelist:
        if '动态图' in each.text:
            link = each.attrs['href']
            title = each.text
            linkntitle.append((link, title))
    return linkntitle

def picsorter(linkntitle, url, root):
    for page in linkntitle:
        piclist = []
        link = page[0]
        title = page[1]
        subroot = root + title + '/'
        if not os.path.exists(subroot):
            os.mkdir(subroot)
        else:
            continue
        suburl = url.replace('index.php', '') + link
        html = gethttp(suburl)
        soup = BeautifulSoup(html, 'html.parser')
        pics = soup.find_all('img')
        #pics = re.findall(r'https//www.*jpg', soup)
        for each in pics:
            try:
                #print(each)
                # pic = each.attrs['mydatasrc']    #to download pic files
                pic = each.attrs['src']    #to download pic files
                #pic = re.findall(r'http://.*.gif', each)
                #print(pic)
                piclist.append(pic)
            except:
                print('skip')
                continue
        print('page {} loaded, pic list grabbed, total number of pic is {}:'.format(title, len(piclist)))
        downloader(subroot, piclist)
    return piclist


def downloader(root, piclist):
    for pic in piclist:
        try:
            name = pic.split('/')[-1]
            path = root + name
            if not os.path.exists(path):
                r = requests.get(pic)
                with open(path, 'wb') as f:
                    f.write(r.content)
                print('{} is downloaded!'.format(name))
            '''
            else:
                yourchoice = input('do you want to overwrite? y/n')
                if yourchoice.lower() == 'y':
                    r = requests.get(pic)
                    with open(path, 'wb+') as f:
                        f.write(r.content)
                    print('{} is overwritten!',format(name))
                else:
                    print('nothing be done!')
            '''
        except:
            continue

def main():
    url = "https://club.6parkbbs.com/enter1/index.php"
    root = "C://Users/Vincent/PycharmProjects/crawling/funnypics/"
    linkntitle = []
    pagecollector(url, linkntitle)
    picsorter(linkntitle, url, root)
    #downloader(root, piclist)
    print('everything is finished')

main()
'''
url = "https://club.6parkbbs.com/enter1/index.php"
print(pagecollector(url))
'''
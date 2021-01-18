##扒取北美新冠病毒感染人数

import re
import requests
from bs4 import BeautifulSoup

def gethttp(url):
    try:
        r = requests.get(url, timeout = 30, headers = {'User-Agent' : 'Mozilla/5.0'})
        #r.encoding = r.apparent_encoding
        #print(r.request.headers)
        #print(r.status_code)
        r.raise_for_status()
        print(r.text)
        return r.text
    except:
        print('error loading the website')

def createlist(outlist, html):
    soup = BeautifulSoup(html, 'html.parser')
    #stat = soup.find('div', {'class': 'jsx-2186057076 state-table'}).find_all('div', {'class':'jsx-2186057076 stat row'})
    #stat = soup.find('div', {'class': re.compile('jsx-\d* state-table')}).find_all('div', {'class': re.compile('jsx-\d* stat row')})
    #print(soup)
    stat2 = soup.find('div', {'class': re.compile('jsx-\d* state-table')})
    print(stat2)
    for i in range(len(stat)):
        span = stat[i].find_all('span')
        name = span[0].text
        infected = span[1].text.split('+')[0]
        death = span[2].text
        deathrate = span[3].text
        outlist.append([name, infected, death, deathrate])

def printlist(outlist, path):

    with open(path, 'w', encoding='utf-8') as f:    ###need encoding = 'utf-8', otherwise cannot save to local file
        template = '{0:^10}\t{1:^10}\t{2:^10}\t{3:^10}\t{4:^10}\n'
        f.write(template.format('排名', '州', '感染人数', '死亡', '死亡率', chr(12288)))
        #f.write('sss')
        print(template.format('排名', '州', '感染人数', '死亡', '死亡率', chr(12288)))
        rank = 0
        for i in range(len(outlist)):
            rank += 1
            #f.write('ddd')
            f.write(template.format(rank, outlist[i][0], outlist[i][1], outlist[i][2], outlist[i][3]))
            print(template.format(rank, outlist[i][0], outlist[i][1], outlist[i][2], outlist[i][3], chr(12288)))
        f.close()

def main():
    url = 'https://coronavirus.1point3acres.com/'
    root = "C://Users/Vincent/PycharmProjects/crawling/"
    path = root + '0405cov19_update' + '.txt'
    html = gethttp(url)
    outlist = []
    createlist(outlist, html)
    printlist(outlist, path)
    print("done, file saved as" + path)

main()
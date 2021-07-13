from bs4 import BeautifulSoup
import re
import os
import requests

#CONFIG
#quality = 360P or 480P or 720P or 1080P
URL_PATTERN = 'https://streamani.net/videos/{}-episode-{}' #General URL pattern for every anime on genoanime
def init(): #init function

    string = "welcome to streamani.net batch downloader / link generator. \n"
    string += "by default it fetches at 1080P\n"
    string += "link example: \n"
    string += "https://streamani.net/videos/boku-no-hero-academia-5th-season-dub-episode-13 \n"

    return string 

def getlink(): #get the anime link
    return input("Enter Link to the first episode of your Anime Series : ")  #User Enters URL

def getstart(): #get the anime start
    start = int(input("Enter Episode Number to start with : "))
    if start <= 0:
        start = 1
    return start

def getend(): #get the anime end
    end = int(input("Enter Episode Number to end with : "))
    return end
def getquality():
    quality = 0
    quality = int(input("quality:(360p=1|480p=2|720p=3|1080p=4|default=PRESS ENTER)") or 0 )
    valid = [0,1,2,3,4]
    if quality in valid :
        return quality
    else :
        return getquality()
def getfiletype():
    filetype = 0
    filetype = int(input("filetype:(m3u8=1|mp4=0|default=PRESS ENTER)") or 0 )
    valid = [0,1]
    if filetype in valid :
        return filetype
    else :
        return getfiletype()
def formatname(animelink):
    animename = animelink.split("/")  #splits link by /
    animearr = animename[4].split("-")
    animearr.pop()
    animearr.pop()
    animename = "-".join(animearr)
    return (animename)

def dl():
    print(init())
    animelink = getlink()
    start = getstart()
    end = getend()
    quality =  getquality()
    filetype = getfiletype()
    main(animelink, start,end, quality, filetype)

ajax_parse = lambda dt: (
    dt.get('source', [{}])[0].get('file'), dt.get('source', [{}])[0].get('label'), dt.get('source', [{}])[0].get('type'), 
    dt.get('source_bk', [{}])[0].get('file'), dt.get('source_bk', [{}])[0].get('label'), dt.get('source_bk', [{}])[0].get('type'))
def main(alink, startt, endd, quality, filetype):
    start = int(startt)
    end = int(endd)
    animename = formatname(alink)
    quality = {
        0: 0,
        1: "360P",
        2: "480P",
        3: "720P",
        4: "1080P"
    }.get(quality)
    try:
        filename = "{}.txt".format(animename)
        f = open(filename)
        f.close()
        os.remove(filename)
    except:
        #do nothing i don't care
        dummy = "dummy"

    longstring = ""
    end=end+1 # Increased by 1 for range function
    # session = requests.Session()
    for episode in range(start,end):
        url = URL_PATTERN.format(animename,episode)
        srcCode = requests.get(url)
        soup = BeautifulSoup(srcCode.content,'html.parser')
        #get link from GenoAnime A
        if quality == 0 :
            dl_wrapper = soup.find_all('iframe')
            dl_wrapper = str(dl_wrapper).split('"')
            link =("https:"+dl_wrapper[11])
            links = []
            srcCode = requests.get('%s' % link.replace('streaming', 'loadserver'))
            for urls in re.finditer(r"(?<=sources:\[{file: ')[^']+", srcCode.text):
                links.append(urls.group(0))
            if filetype == 0 :    
                f = open('{}.txt'.format(animename), "a") #opens file with name of "test.txt"
                f.write(str(links[0])+"\n")             
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[0])
            else :  
                f = open('{}.txt'.format(animename), "a") #opens file with name of "test.txt"
                f.write(str(links[1])+"\n")
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[1])

        else :
            dl_wrapper = soup.find_all('iframe')
            dl_wrapper = str(dl_wrapper).split('"')
            link =("https:"+dl_wrapper[11])
            # with session.get('%s' % link.replace('streaming', 'ajax')) as response:
            response = requests.get('%s' % link.replace('streaming', 'ajax'))
            content = response.json()

            if content == 404:
                print("[ERROR:streamani.net:(Sorry, Links multiquanlity temporary disable.)]")
                links=[]
                srcCode = requests.get('%s' % link.replace('streaming', 'loadserver'))
                for urls in re.finditer(r"(?<=sources:\[{file: ')[^']+", srcCode.text):
                    links.append(urls.group(0))
            else:
                s1, l1, t1, s2, l2, t2 =  ajax_parse(content)        
                links = [{'quality': "%s [%s]" % (l1, t1), 'stream_url': s1}] + ([{'quality': "%s [%s]" % (l2, t2), 'stream_url': s2}] if s2 else [])

            if filetype == 0 :    
                f = open('{}.txt'.format(animename), "a") #opens file with name of "test.txt"
                f.write(str(links[0])+"\n")             
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[0])
            else :  
                f = open('{}.txt'.format(animename), "a") #opens file with name of "test.txt"
                f.write(str(links[1])+"\n")
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[1])
    return longstring


#print(init())

#print(main())

#forget deleting the file for now



def success(alink):
    animename = formatname(alink)
    print("----- -----------------------------------------------------")
    print("success. you can copy the links here or from {}.txt in this folder".format(animename))
    print("----------------------------------------------------------")




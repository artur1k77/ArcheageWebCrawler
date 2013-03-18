from bs4 import BeautifulSoup
import urllib

from django.utils import timezone
from inout_manager.models import *

def getSoup(url) :
    f= urllib.urlopen(url)
    s = f.read()
    f.close()
    return BeautifulSoup(s)
    

def getExpedInfo(expedId) : 
    soup = getSoup("http://play.archeage.com/expeditions/HIRAMAKAND/"+str(expedId))
    expedInfoDiv = soup.find("div", {"class","exped_info"}) 
    if(expedInfoDiv is None):
        print("cannot find info div")
    #else:
        #print type(expedInfoDiv).__name__
        #print(expedInfoDiv)
    count = expedInfoDiv.find("em", {"class", "count"})
    print(count.text)

class MemberInfo : 
    def __init__(self, name, classType, level) : 
        self.name = name
        self.classType = classType
        self.level = level
        
    def __repr(self) :
        return "name=%s, classType=%s, level=%d" % (self.name, self.classType, self.level)

class ExpedInfo : 
    def __init__(self, name, id) : 
        self.name = name
        self.id = id

    def __repr__(self) : 
        return "{name=%s, id=%d}" % (self.name.encode('utf8'), self.id)


def getAllExpedList() :
    """ return list of instances of ExpedInfo """
    allExpedInfo = []
    currPageNum = 1
    while True :
        listFromPage = getExpedListFromPage(currPageNum)
        # currPageNum limit should be configured. 
        if (len(listFromPage) < 1) or  currPageNum > 1 :
            break
        #print "page=%d, num=%d" % (currPageNum, len(listFromPage))
        allExpedInfo = allExpedInfo + listFromPage
        currPageNum += 1
    return allExpedInfo
    

def getExpedListFromPage(pageNum) :
    """ return list of instances of EpxedInfo """
    expedList = []
    soup = getSoup("http://play.archeage.com/exps/all?page="+str(pageNum)+"&expeditionType=MANUFACTURE&gameServer=HIRAMAKAND&searchType=EXPEDITION_NAME")
    expedInfoList = soup.find("ul", {"class","lst"}).findAll("div", {"class", "exped_info"})
    #print expedInfoList
    for expedInfo in expedInfoList:
        nameSpan = expedInfo.find("span", {"class","name"})
        link = expedInfo.find("a") 
        expedId = link["href"].split('/')[3]
        expedList.append(ExpedInfo(nameSpan.text, int(expedId)))
        #print expedId
        
        """
        print link["href"]
        print expedId
        print nameSpan.text
        """
    return expedList
    

def getExpedMemberInfo(expedId): 
    soup = getSoup("http://play.archeage.com/expeditions/HIRAMAKAND/"+str(expedId)+"/members")
    expedMemberTable = soup.find("tbody").findAll("tr")
    for memberRow in expedMemberTable :
        memberInfo = memberRow.findAll("td")
        print memberInfo[1]
        print MemberInfo(memberInfo[1].find("a").text, memberInfo[3].text, memberInfo[2].text).text()


def startCrawling():
    currTime = timezone.now()    
    #update exped
    crawledList = getAllExpedList()
    for crawled in crawledList:
        if not Expedtion.objects.filter(exped_id=crawled.id).exists():
            Expedition(name=crawled.name, exped_id=crawled.id).save()
    # get all members of the expeditions in the server.
    expedIdList = Expedition.objects.all().values('exped_id')
    for id in expedIdList:
        getExpedMemberInfo(id)

            

    # only in crawled. new player
     

    # only in db. out of expedtion.
    
    #update member

def run():
    getAllExpedList()

#getExpedInfo(1005)
#getExpedMemberInfo(1005)
#getExpedList()
#getExpedListFromPage(2)


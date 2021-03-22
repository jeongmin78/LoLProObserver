# 일정시간마다 페이지 탐색 or 등록한 소환사 탐색
# slcak으로 알림 전송
# 소환사명 챔피언 플레이중!
# 관전링크: https://www.op.gg/spectate/pro/

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from slacker import Slacker
import time, calendar

slack = Slacker('xoxb-1595915662211-1619557823728-5XHiUijip8NwZqz1Md2TkqvC')

def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    slack.chat.post_message('#jeongmin-stock', strbuf)

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


if __name__ == '__main__': 
    try:
        printlog('탐색할 팀명', 'DRX')

        while True:
            url = "https://www.op.gg/spectate/pro/"
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html5lib')

            summonerList = soup.find_all('div',{'class':'Content'})
            summonerInfoList = soup.find_all('div',{'class':'Footer'})

            for summoner, summonerInfo in zip(summonerList, summonerInfoList):
                summonerName = summoner.find(attrs={'class':'SummonerName'})
                championNmae = summoner.find(attrs={'class':'ChampionName'})
                teamName =  summonerInfo.find(attrs={'class':'TeamName'})
                summonerUrl = summonerInfo.a['href']
                
                if (teamName.get_text() == "DRX"):
                    dbgout('소속팀: ' + teamName.get_text())
                    dbgout('소환사명: ' + summonerName.get_text())
                    dbgout(championNmae.get_text() + ' 플레이 중')
                    dbgout('관전링크: '+ summonerUrl)
                #print("소속팀: " , teamName.get_text())
                #print("소환사명: " , summonerName.get_text())
                #print(championNmae.get_text() , "플레이 중")
                #print("관전링크: ", summonerUrl)
            time.sleep(10)

    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')
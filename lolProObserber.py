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

def player_register():
    global pro_player_list

    url = "https://www.op.gg/spectate/list/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    summonerList = soup.find_all('div',{'class':'SummonerName'})

    for summoner in summonerList:
        pro_player_list.append(summoner.get_text())
    #print(pro_player_list)

def observe(name, time):
    
    url = "https://www.op.gg/spectate/pro/"
    html = requests.get(url).text
    soup2 = BeautifulSoup(html, 'html5lib')

    global alarm_list
    if name in alarm_list: #알람 보냈고
        if time in game_time_list: #같은 게임 중이면 알람 보내지 않도록 함수 종료
            return False
    else:
        #dbgout('소속팀: ' + team_name.get_text())
        dbgout('소환사명: ' + name)
        #dbgout(champion_nmae.get_text() + ' 플레이 중')
        #dbgout('관전링크: '+ summoner_url)

if __name__ == '__main__': 
    
    try:

        observing_list = []
        alarm_list = []
        pro_player_list = []
        game_time_list = []

        player_register()

        n = True
        while n:
            user_name = input("프로게이머 소환사명을 입력하세요: ")
            if user_name not in pro_player_list:
                print("등록되지 않은 소환사입니다.")
            else:
                observing_list.append(user_name)
                print("옵저빙 목록에 추가되었습니다.")
                print(observing_list)
                question = input("소환사 등록을 종료하고 옵저빙을 시작할까요?(y/n)")
                if question == 'y':
                    print("옵저빙 시작")
                    n = False
            
        while True:

            print(observing_list)

            url = "https://www.op.gg/spectate/pro/"
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html5lib')

            summoner_list = soup.find_all('div',{'class':'Content'})
            summonerinfo_list = soup.find_all('div',{'class':'Footer'})
            
            for summoner, summoner_info in zip(summoner_list, summonerinfo_list):
                summoner_name = summoner.find(attrs={'class':'SummonerName'})
                champion_nmae = summoner.find(attrs={'class':'ChampionName'})
                game_time = summoner.find(attrs={'class':'GameTime'})
                team_name =  summoner_info.find(attrs={'class':'TeamName'})
                summoner_url = summoner_info.a['href']
                
                summoner_name = summoner_name.get_text()
                game_time = game_time.get_text()

                #game_time_list.append(game_time)
                #print(summoner_name)

                if summoner_name in observing_list:
                    print(summoner_name)
                    if [summoner_name,game_time] not in alarm_list: #한번 알람 가면 같은 알람 x
                        observe(summoner_name, game_time)
                        alarm_list.append([summoner_name,game_time])
                
            print(alarm_list)

            time.sleep(10)

    except Exception as ex:
        print('`main -> exception! ' + str(ex) + '`')



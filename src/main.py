from datetime import datetime
from service.network_crawl import NetworkCrawl
from service.data_manage import DataManage


class main:
    def __init__(self):
        self.getRound() # 회차번호 구하기

        회차리스트 = self.readRound() # 회차번호 읽어들이기

        for 회차 in 회차리스트:
            회차번호 = 회차[0]
            회차날짜 = 회차[1]
            print(회차번호)
            self.getData(회차번호, 회차날짜) # 회차값 저장


    def readRound(self):
        데이터베이스 = DataManage('localhost', 'root', 'passworld', 'DHLOTTERY', 'ROUND_INFORMATION')
        
        
        회차리스트 = 데이터베이스.읽기(조건="round > '1156'") # 마지막 날짜 1156회
        
        데이터베이스.연결종료()
        return 회차리스트


    def getRound(self):
        클라이언트 = NetworkCrawl('https://m.dhlottery.co.kr/gameResult.do?method=byWin')
        결과 = 클라이언트.크롤링()

        옵션 = 결과.find_all('option')

        데이터베이스 = DataManage('localhost', 'root', 'passworld', 'DHLOTTERY', 'ROUND_INFORMATION')
        
        for option in 옵션:
            if 'value' in option.attrs:
                회차 = option['value']
                날짜_str = option.get_text(strip=True).split('(')[1].split('일')[0].strip()
                
                if '일' not in 날짜_str:
                    날짜_str += '일'

                try:
                    날짜 = datetime.strptime(날짜_str, '%Y년 %m월 %d일').date()
                except ValueError:
                    print(f"Invalid date format: {날짜_str}")
                    continue

                데이터 = {
                    'round': 회차,
                    'date': 날짜
                }
                
                데이터베이스.생성(데이터)

        데이터베이스.연결종료()
        print('작업완료')

    def getData(self, 회차번호, 회차날짜):
        클라이언트 = NetworkCrawl('https://m.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=' + 회차번호)
        결과 = 클라이언트.크롤링()

        당첨숫자 = []
        for ball in 결과.find_all('span', class_='ball'):
            if ball.text.strip() != "+":
                당첨숫자.append(ball.text.strip())

        보너스번호 = 당첨숫자[-1]
        번호 = 당첨숫자[:-1]

        데이터베이스 = DataManage('localhost', 'root', 'passworld', 'DHLOTTERY', 'DATA')

        데이터 = {
            'round': 회차번호,
            'number1': 번호[0],
            'number2': 번호[1],
            'number3': 번호[2],
            'number4': 번호[3],
            'number5': 번호[4],
            'number6': 번호[5],
            'bonusNumber': 보너스번호,
            'date': 회차날짜
        }

        데이터베이스.생성(데이터)
        데이터베이스.연결종료()




if __name__ == "__main__":
    main()
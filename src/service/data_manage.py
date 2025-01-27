import mysql.connector


class DataManage:
    def __init__(self, 호스트, 사용자, 비밀번호, 데이터베이스, 테이블):
        self.db = mysql.connector.connect(
            host = 호스트,
            user = 사용자,
            password = 비밀번호,
            database = 데이터베이스
        )
        self.table = 테이블
        self.cursor = self.db.cursor()

    def 읽기(self, 조건=None):
        sql = f"SELECT * FROM {self.table}"

        if 조건:
            sql += f" WHERE {조건}"

        try:
            self.cursor.execute(sql)
            결과 = self.cursor.fetchall()
            return 결과
        except Exception as e:
            print(f"오류 발생: {e}")
            return []

    def 생성(self, 데이터):
        컬럼 = ', '.join(데이터.keys())
        값 = ', '.join(f"'{v}'" for v in 데이터.values())

        sql = f"INSERT INTO {self.table} ({컬럼}) VALUES ({값})"

        try:
            self.cursor.execute(sql)
            self.db.commit()
            print('데이터 입력 완료 :   ', 데이터)
        except Exception as e:
            print(e)
            self.db.rollback()

    def 연결종료(self):
        self.cursor.close()
        self.db.close()
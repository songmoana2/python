import os
import sys
import pymysql # MySQL데이터베이스를 사용하기 위한 라이브러리를 등록함
config = {                  # MySQL데이터베이스를 사용하기 위해 환경변수를 딕셔너리로 생성함. 
    'host' : '127.0.0.1',   # MySql 이 동작하는 ipv4주소 
    'user' : 'root',        # MySql 설치할 때 정한 계정 
    'passwd' : 'root1234',  # MySql 설치할 때 정한 비밀번호
    'database' : 'test_db', # MySql 설치할 때 처음 생성한 데이터베이스 -> test_db
    'port' : 3306,          # MySql이 응용프로그램과 통신할 때 사용하는 포트번호 리터럴이 아닌 정수값으로 써야함
    'charset' : 'utf8',     # 한글을 사용하겠다는 설정 
    'use_unicode' : True    # 한글을 사용하겠다는 설정 
    }
#--------------------------------------------------------------------------------------------------------------

def join():   # product 테이블과 sales 테이블 연동
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        sql = '''select p.pCode,p.unitPrice,p.pName,p.discountRate,s.sCode,s.Qty,s.serial_no,s.Amt 
                from product p inner join sales s 
                on p.pCode = s.sCode;'''
        cursor.execute(sql)

    except Exception as e :
            print('db 연동 실패 : ', e)
            conn.rollback() # 실행 취소 
    finally:
        cursor.close()
        conn.close()
    #
#--------------------------------------------------------------------------------------------------------------
def salCreate() : # 판매 데이터 입력
    try :
        conn = pymysql.connect(**config)    # 딕셔너리 config를 인수로 사용하여 conn 객체를 만듬.
        cursor = conn.cursor()              # conn 객체로부터 cursor() 메소드를 호출하여 cursor 참조변수를 만듬.
        #
        while True:
            os.system('cls')
            print("<<<판매 내역 등록입니다>>>")
            print()
        
            in_sCode = input("등록할 판매 상품의 코드를 입력하세요 : ")  
            if in_sCode != '' :
                sql = f"select unitPrice from product where pCode = '{in_sCode}'" # in_sCode 와 일치하는 코드를 product 테이블에서 찾아 unitPrice 값을 출력한다.
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows == ():
                    print()
                    new_product = input("존재하지않는 코드입니다. 상품을 등록하겠습니까? (y/n) : ")
                    print()
                    if new_product == 'y' or new_product == 'Y':
                        in_pName = input("상품명을 입력하세요 : ")
                        in_UnitPrice = int(input("상품 가격을 입력하세요 : "))
                        in_discountRate = int(input("할인율을 입력하세요 : "))
                        sql = f"insert into product(pCode,pName,UnitPrice,discountRate) values('{in_sCode}','{in_pName}',{in_UnitPrice},{in_discountRate})"
                        cursor.execute(sql)
                        conn.commit()
                        print()
                        print("상품 등록을 성공했습니다.")
                        print()
                        os.system('pause')
                        continue
                    else:
                        print('상품등록을 종료합니다.')
                        print()
                        break
                        
                else:
                    rows1 = rows[0] # 튜플안에 있는 값 추출
                    rows2 = rows1[0]
                    iValue = userInput() # 수량 필터
                    sql = f"select discountRate from product where pCode = '{in_sCode}'"
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    in_Amt = int(iValue) * int(rows2) * ((100 - int(rows[0][0]))/100) # 총 가격 = 수량 * 판매가
                    #
                    sql = f"insert into sales(sCode, Qty, Amt) values('{in_sCode}',{iValue},{in_Amt})" 
                    cursor.execute(sql)
                    conn.commit()
                    print()
                    print("판매 상품등록을 성공했습니다.")
                    print()
                    break
        else :
            print("판매 상품 등록을 위해 코드를 입력해 주세요")
    except Exception as e :
        print('오류 : ', e)
        conn.rollback() # 실행 취소 
    finally:
        cursor.close()
        conn.close()
#--------------------------------------------------------------------------------------------------------------
def salReadAll() : # 조회 (전체)
    os.system('cls')
    print("                <<<판매 내역 조회>>>                       ")
    gf1 = salFind(2)
    rows = gf1.salfind()
    print()
    print("시리얼넘버--상품코드--상품명--개별가격--수량--할인율--총 가격")
    print()
    for row in rows : 
        print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6])) 
#--------------------------------------------------------------------------------------------------------------
class salFind : # 조회 (조건)
    def __init__(self,find_sel,find_in_data=''):   
        #print('\n',sel)        
        self.read_sel = find_sel 
        if find_sel == 3 or find_sel == 5 or find_sel == 6:  # 판매 코드 이용
            self.find_sql = "select * from sales where sCode =" + f"'{find_in_data}'"
        elif find_sel == 4 : # 상품명 이용
            self.find_sql = "select * from product where pName =" + f"'{find_in_data}'"
        elif find_sel == 7 : # 시리얼 넘버 이용
            self.find_sql = "select * from sales where serial_no =" + f"'{find_in_data}'"
        else: 
            self.find_sql = "select serial_no, sCode ,pName, unitPrice, Qty, discountRate, Amt from sales,product where sCode = pCode"

    def salfind(self) :
        try :
            conn = pymysql.connect(**config)    # 딕셔너리 config를 인수로 사용하여 conn 객체를 만듬.
            cursor = conn.cursor()              # conn 객체로부터 cursor() 메소드를 호출하여 cursor 참조변수를 만듬.
            cursor.execute(self.find_sql)
            return cursor.fetchall()    # select 쿼리문의 실행 결과를 return함
                                        # 쿼리의 실행결과가 없으면 요소의 갯수가 0인 리스트가 반환됨
        except Exception as e :
            print('db 연동 실패 : ', e)
            conn.rollback() # 실행 취소 
        finally:
            cursor.close()
            conn.close()
    #
#--------------------------------------------------------------------------------------------------------------
class salRead : # input을 받아 조회 (코드, 상품명, 시리얼넘버)
    def __init__(self,read_sel):            
        self.read_sel = read_sel
        if read_sel == '코드' :  
            self.read_sql = "select * from sales where sCode ="
        elif read_sel == '상품명' : 
            self.read_sql = "select * from product where pName ="
        elif read_sel == '시리얼넘버' :
            self.read_sql = "select * from sales where serial_no ="
        else :
            self.read_sql = "select serial_no, sCode ,pName, unitPrice, Qty, discountRate, Amt from sales,product where sCode = pCode"
    def salReadOne(self) :
        try :
            conn = pymysql.connect(**config)    # 딕셔너리 config를 인수로 사용하여 conn 객체를 만듬.
            cursor = conn.cursor()              # conn 객체로부터 cursor() 메소드를 호출하여 cursor 참조변수를 만듬.
            #
            rows = []
            os.system('cls')
 
            if self.read_sel == '코드' :
                print("<<판매 내역 조회({})입니다.>>>".format(self.read_sel))
                print()
                in_sCode = input("조회할 "+self.read_sel+"를 입력하세요 : ")
                sql = self.read_sql + f"'{in_sCode}'"
            elif self.read_sel == '상품명' : 
                print("<<<판매 내역 조회({})입니다.>>>".format(self.read_sel))
                print()
                in_sCode = input("조회할 "+self.read_sel+"를 입력하세요 : ")
                sql = self.read_sql + f"'{in_sCode}'"
            elif self.read_sel == '시리얼넘버':
                print("<<판매 내역 조회({})입니다.>>>".format(self.read_sel))
                print()
                in_sCode = input("조회할 "+self.read_sel+"를 입력하세요 : ")
                sql = self.read_sql + f"'{in_sCode}'"
            else :
                in_sCode = ''
                sql = self.read_sql
            cursor.execute(sql)
            rows = cursor.fetchall()

            if len(rows) > 0 : # 입력값과 같은 값이 있을 때
                if self.read_sel == '코드':
                    sql = f"select serial_no, sCode, pName, unitPrice, Qty, discountRate, Amt from sales, product where sCode = '{in_sCode}'and sCode = pCode"
                elif self.read_sel == '상품명':
                    sql = f"select serial_no, sCode, pName, unitPrice, Qty, discountRate, Amt from sales, product where pName = '{in_sCode}'and sCode = pCode"
                elif self.read_sel == '시리얼넘버':
                    sql = f"select serial_no, sCode, pName, unitPrice, Qty, discountRate, Amt from sales, product where serial_no = '{in_sCode}'and sCode = pCode"
                cursor.execute(sql)
                rows = cursor.fetchall()
                os.system('cls')
                print("            <<<판매 내역 조회({})>>>                       ".format(self.read_sel))
                print()
                print("시리얼넘버--상품코드--상품명--개별가격--수량--할인율--총 가격")
                print()
                for row in rows:
                    print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                print()
            else: # 입력값과 같은 값이 없을 때
                print()
                print("조회결과 입력한 {}에 맞는 판매 내역이 없습니다.".format(self.read_sel))
                print()      
        except Exception as e :
            print('db 연동 실패 : ', e)
            conn.rollback() # 실행 취소 
        finally:
            cursor.close()
            conn.close()
#--------------------------------------------------------------------------------------------------------------
def salDelete() : # 삭제 (시리얼넘버)
    os.system('cls')
    print("<<<판매상품 목록 조회입니다>>>")
    gf1 = salFind(2)
    rows = gf1.salfind()
    for row in rows :
        print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    try :
        conn = pymysql.connect(**config)    # 딕셔너리 config를 인수로 사용하여 conn 객체를 만듬.
        cursor = conn.cursor()              # conn 객체로부터 cursor() 메소드를 호출하여 cursor 참조변수를 만듬.
        print()
        print("<<<삭제할 판매 상품의 시리얼넘버를 입력하세요>>>")
        print()
        in_serial_no = input('삭제할 시리얼넘버 입력 : ')
        sql = f"select * from sales where serial_no = '{in_serial_no}'"
        cursor.execute(sql) # sql문 실행 
        rows = cursor.fetchall()
        if rows :
            sql = f"delete from sales where serial_no = '{in_serial_no}'"
            cursor.execute(sql) # sql문 실행
            conn.commit() 
            print()
            print('삭제 성공했습니다.')
            #os.system("pause")
        else :
            print()
            print('삭제 실패했습니다.')
            #os.system("pause")
    except Exception as e :
        print('db 연동 실패 : ', e)
        conn.rollback() # 실행 취소 
    finally:
        cursor.close()
        conn.close()
    print()
    print("<<<상품 목록 조회입니다>>>")
    gf1 = salFind(2)
    rows = gf1.salfind()
    for row in rows :
        print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    #
#--------------------------------------------------------------------------------------------------------------
def salUpdate() : # 수정 (시리얼넘버)
    os.system('cls')
    print("<<<판매상품 목록 조회입니다>>>")
    gf1 = salFind(2)
    rows = gf1.salfind()
    for row in rows :
        print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    print()
    print("<<<판매 상품 수정입니다>>>")
    print()
    in_serial_no = input('수정할 판매 상품의 시리얼넘버를 입력하세요 : ') 
    up1 = salFind(7,in_serial_no)
    rows = up1.salfind()
    #
    try :
        conn = pymysql.connect(**config)    # 딕셔너리 config를 인수로 사용하여 conn 객체를 만듬.
        cursor = conn.cursor()              # conn 객체로부터 cursor() 메소드를 호출하여 cursor 참조변수를 만듬.
        if rows : # select 쿼리 실행결과가 있는 경우
            print()
            print("<<<판매 상품 시리얼넘버 조회결과입니다>>>")
            print()
            sql = f"select serial_no, sCode, pName, unitPrice, Qty, discountRate, Amt from sales, product where serial_no = '{in_serial_no}'and sCode = pCode"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows : # 
                print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            print()
            yesNo = input('수정하시겠습니까>(y/n) : ')
            if yesNo == "y" or yesNo == "Y":
                os.system("cls")
                print("<<<수정할 내용을 입력하세요.>>>")
                print()
                in_sCode = input("상품 코드를 입력하세요 : ")

                # 
                sql = f"select unitPrice from product where pCode = '{in_sCode}'" # in_sCode 와 일치하는 코드를 product 테이블에서 찾아 unitPrice 값을 출력한다.
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows == ():
                    print()
                    print("상품코드 오류입니다.")
                    print()
                else:
                    rows1 = rows[0]
                    rows2 = rows1[0]
                    iValue = userInput()  # 상품 수량 
                    in_Amt = int(iValue) * int(rows2) * ((100-row[5])/100) # 수량 * 단가 * ((100-할인율)/100)
                    # print(in_Amt) 
                    sql = f"update sales set sCode = '{in_sCode}', Qty = {iValue}, Amt = {in_Amt} where serial_no = {in_serial_no}"
                    cursor.execute(sql) # sql문 실행
                    conn.commit() 
                    print()
                    print("<<<수정을 완료했습니다>>>")
                    print()
                    sql = f"select serial_no, sCode, pName, unitPrice, Qty, discountRate, Amt from sales, product where serial_no = '{in_serial_no}'and sCode = pCode"
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    print("<<<판매 상품 수정 결과입니다>>>")
                    print()
                    print("시리얼넘버--상품코드--상품명--개별가격--수량--할인율--총 가격")
                    print()
                    for row in rows : # 
                        print("{:<7}{:<10}{:ㅤ<7}{:<7}{:<7}{:<7}{:<10}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                    print()
            else:  
                print()  
                print("<<<수정을 취소했습니다.>>>")
                print()
        else : # select 쿼리 실행결과가 없는 경우
            print('수정할 시리얼넘버가 없습니다.')
            pass
    except Exception as e :
        print('db 연동 실패 : ', e)
        conn.rollback() # 실행 취소 
    finally:
        cursor.close()
        conn.close()
#--------------------------------------------------------------------------------------------------------------
def userInput(): # 입력(수량)
    ui1 = InputFilter()
    #
    while True: # 상품 수량
        if ui1.setQty(input("상품 수량을 입력하세요 : ")) :
            in_Qty = ui1.Qty
            break
        else:
            continue
    #
    return in_Qty
#--------------------------------------------------------------------------------------------------------------
class InputFilter : # 입력필터(수량)
    def __init__(self):   
        self.inputValueFilter_result = False
        self.Qty = 0
    #
    def setQty(self, Qty) : # 수량 필터링
        if Qty == 0 : # 수량이 0이나 음수일때
            print("수량 "+str(Qty)+" 의 정보는 부정확합니다.")
            self.inputValueFilter_result = False
        else:
            self.inputValueFilter_result = True
            self.Qty = Qty
        return self.inputValueFilter_result
    #
#--------------------------------------------------------------------------------------------------------------
if __name__ == "__main__" : # 상품관리 선택
    while True:
        join()
        os.system('cls')
        print("---상품관리---")
        print("상품    등록 : 1 ")
        print("상품목록조회 : 2 ")
        print("코드별  조회 : 3 ")
        print("상품명별조회 : 4 ")
        print("상품    수정 : 5 ")
        print("상품    삭제 : 6 ")
        print("시리얼  조회 : 7 ")
        print("상품관리종료 : 9 ")
        print()
        sel = int(input("작업을 선택하세요 : "))
        print()
        if sel == 1 :
            salCreate()
            os.system("pause")
        elif sel == 2 :
            salReadAll()
            print()
            os.system("pause")
        elif sel == 3 :
            r3 = salRead('코드')
            r3.salReadOne()
            os.system("pause")
        elif sel == 4 :
            r4 = salRead('상품명')
            r4.salReadOne()
            os.system("pause")
        elif sel == 5 :
            salUpdate()
            os.system("pause")
        elif sel == 6 :
            salDelete()
            print()
            os.system("pause")
        elif sel ==7 :
            r7 = salRead('시리얼넘버')
            r7.salReadOne()
            os.system("pause")
        elif sel == 9 :
            print("상품관리를 종료합니다. ")
            print()
            os.system("pause")
            os.system('cls')
            sys.exit(0)
        else :
            print("잘못 선택했습니다. ")
            os.system("pause")
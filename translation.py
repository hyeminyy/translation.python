import pytesseract
import cv2
import os
import sys
import urllib.request
import json
import PyQt5
import operator
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

#변경사항
transUI = "C:/Users/smj03/Desktop/PyProject/untitled/Translator.ui" #UI 저장 경로
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract' # r'C:\Program Files\Tesseract-OCR\tesseract'
client_id = "RLT9wm9Y4A_g5xSuiTro"
client_secret = "UD5AnRXX1Y"

language=["ko","en","zh-cn","zh-cn","ja","es","fr","ru","vi","th","id","de","it"] #언어 배열
lan_count=[0,0,0,0,0,0,0,0,0,0,0,0,0] #각 언어 글자 수 세기
maxValue=lan_count[0] #글자수 카운터 배열의 첫값을 우선 max로 설정
maxindex=0 #글자수 카운터 배열에서 가장 큰 값을 가지는 인덱스를 저장할 변수

class MyWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(transUI, self)

        F_cb = self.From_comboBox
        T_cb = self.To_comboBox

        self.img_pushButton.clicked.connect(self.imgtxt) #p_pushButton = 사진 선택 버튼.
                                                      #connect는 버튼과 imgtxt 함수 연결
        self.save_pushButton.clicked.connect(self.savefile) #save_pushButton = 파일 저장 버튼
        self.tr_pushButton.clicked.connect(self.translate) #tr_pushButton = 번역 버튼

        F_cb.addItem("한국어(KO)") #0
        F_cb.addItem("영어(EN)")  # 1
        F_cb.addItem("중국어 간체(zh-CN)") #2
        F_cb.addItem("중국어 번체(zh-CN)") #3
        F_cb.addItem("일본어(JA)") #4
        F_cb.addItem("스페인어(ES)") #5
        F_cb.addItem("프랑스어(FR)") #6
        F_cb.addItem("러시아어(RU)") #7
        F_cb.addItem("베트남(VI)") #8
        F_cb.addItem("태국어(TH)") #9
        F_cb.addItem("인도네시아어(ID)") #10
        F_cb.addItem("독일어(DE)") #11
        F_cb.addItem("이탈리아어(IT)") #12

        T_cb.addItem("한국어(KO)")  # 0
        T_cb.addItem("영어(EN)")
        T_cb.addItem("중국어 간체(zh-CN)")
        T_cb.addItem("중국어 번체(zh-CN)")
        T_cb.addItem("일본어(JA)")
        T_cb.addItem("스페인어(ES)")
        T_cb.addItem("프랑스어(FR)")
        T_cb.addItem("러시아어(RU)")
        T_cb.addItem("베트남(VI)")
        T_cb.addItem("태국어(TH)")
        T_cb.addItem("인도네시아어(ID)")
        T_cb.addItem("독일어(DE)")
        T_cb.addItem("이탈리아어(IT)")

        ##print(T_cb.currentIndex())


    def imgtxt(self): #imgtxt 함수 : 파일 열고 사진 속 텍스트 출력

        fname=QFileDialog.getOpenFileName(self)
        image = cv2.imread(fname[0], cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        warped = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 21)

        file = open("test.txt", 'w', -1, "utf-8")
        file.write(pytesseract.image_to_string(warped, lang='kor+eng'))
        file.close()
        self.img_textEdit.clear()
        textfile = open("test.txt", 'r', -1, "utf-8")
        text = textfile.read()
        self.img_textEdit.setText(text)  # img_textEdit (사진 텍스트창)에 사진 속 글 출력

    def savefile(self): #savefile 함수 : 사진 텍스트 창에서 글 편집 후 savefile.txt에 저장
        file=open("savefile.txt", 'w', -1, "utf-8")
        savetext=self.img_textEdit.toPlainText()
        file.write(savetext)
        file.close()

        file_2 = open("savefile.txt", 'r', -1, "utf-8")
        #자동으로 FROM 언어 정하기
        while True:
            line = file_2.readline()
            if not line: break

            line = line.strip()
            if (len(line) == 0):
                continue
            else:
                encText = urllib.parse.quote(line)
                from_lan = ''

                data = "query=" + encText
                url = "https://openapi.naver.com/v1/papago/detectLangs"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    #print(response_body.decode('utf-8'))
                    trans_text = json.loads(response_body.decode('utf-8')) #문자열을 python 타입으로 변경
                    from_lan = trans_text['langCode']
                    for i in range(0,13):
                        if (language[i]==from_lan):
                            lan_count[i]+=1

                else:
                    print("Error Code:" + rescode)

        file_2.close()  #savefile.txt닫아준다.

        maxindex, maxValue=max(enumerate(lan_count),key=operator.itemgetter(1))

        self.From_comboBox.setCurrentIndex(maxindex)



    def translate(self): #translate 함수 : savefile.txt를 번역 후 trans_textEdit (번역 텍스트창)에 출력
        file_2 = open("savefile.txt", 'r', -1, "utf-8")
        file_3 = open("result.txt", 'w', -1, "utf-8")
        ##line = file_2.readline()
        ##print(line.strip())

        while True:
            line = file_2.readline()
            if not line: break

            line = line.strip()
            if (len(line) == 0):
                file_3.write('\n')
            else:
                ### file_3.write("1"+'\n')

                encText = urllib.parse.quote(line)
                srcLang = language[self.From_comboBox.currentIndex()]
                tarLang = language[self.To_comboBox.currentIndex()]

                data = "query=" + encText
                url = "https://openapi.naver.com/v1/papago/detectLangs"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if (rescode == 200):
                    response_body = response.read()
                    ##print(response_body.decode('utf-8'))
                    trans_text = json.loads(response_body.decode('utf-8'))
                    currentLang = trans_text['langCode']

                    if (srcLang!= currentLang): #From 언어로 선택하지 않은 언어는 해석 안함
                        file_3.write(line + '\n')
                    elif ((srcLang==currentLang)and(srcLang != tarLang)): #From 언어와 같고, To언어와 다를시 번역
                        url = "https://openapi.naver.com/v1/papago/n2mt"

                        data = "source={}&target={}&text=".format(srcLang, tarLang) + encText
                        request = urllib.request.Request(url)
                        request.add_header("X-Naver-Client-Id", client_id)
                        request.add_header("X-Naver-Client-Secret", client_secret)
                        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                        rescode = response.getcode()
                        if (rescode == 200):
                            response_body = response.read()
                            data = response_body.decode('utf-8')
                            data = json.loads(data)
                            trans_text = data['message']['result']['translatedText']
                            file_3.write(trans_text + '\n')
                        else:
                            print("Error Code:" + rescode)
                    else: # 위 모두 해당 안하면 번역 안 함
                        file_3.write(line + '\n')
                else:
                    print("Error Code:" + rescode)

        file_2.close()
        file_3.close()
        self.trans_textEdit.clear()
        transfile = open("result.txt", 'r', -1, "utf-8")
        trans = transfile.read()
        self.trans_textEdit.setText(trans)

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MyWindow()
    window.show()
    app.exec_()

cv2.waitKey(0)
cv2.destroyAllWindows()
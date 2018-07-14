import sys
import time
import json
import getpass
import codecs

import re
from PTTLibrary import PTT
from uao import Big5UAOCodec

import tkinter as tk

# def insert_point():
#     var = e.get()
#     t.insert('insert',var)

class APP:
    def __init__(self,win):
        self.ID = ''
        self.Password = ''
        self.count = 0
        self.PTTBot = ''
        self.postIndex = 0
        self.broad = 'test'
        self.hint = []
        self.question = []
        win.title("ThinkTempo")
        win.geometry('250x410')
        self.IDlabel=tk.Label(win, text="ID:")   #建立標籤物件
        self.PWlabel=tk.Label(win, text="Password:")   #建立標籤物件
        self.boardlabel=tk.Label(win, text="Board:")   #建立標籤物件
        self.PostIDlabel=tk.Label(win, text="PostID:")   #建立標籤物件
        self.hintlabel=tk.Label(win, text="Hint Players")   #建立標籤物件
        self.hint1label=tk.Label(win, text="ID 1:")   #建立標籤物件
        self.hint2label=tk.Label(win, text="ID 2:")   #建立標籤物件
        self.hint3label=tk.Label(win, text="ID 3:")   #建立標籤物件
        self.questionlabel=tk.Label(win, text="Questions")   #建立標籤物件

        self.Q1label=tk.Label(win, text="Q1")   #建立標籤物件
        self.Q2label=tk.Label(win, text="Q2")   #建立標籤物件
        self.Q3label=tk.Label(win, text="Q3")   #建立標籤物件
        self.Q4label=tk.Label(win, text="Q4")   #建立標籤物件
        self.Q5label=tk.Label(win, text="Q5")   #建立標籤物件
        self.Q6label=tk.Label(win, text="Q6")   #建立標籤物件
        self.Q7label=tk.Label(win, text="Q7")   #建立標籤物件
        self.Q8label=tk.Label(win, text="Q8")   #建立標籤物件
        self.Q9label=tk.Label(win, text="Q9")   #建立標籤物件
        self.Q10label=tk.Label(win, text="Q10")   #建立標籤物件
        self.Q11label=tk.Label(win, text="Q11")   #建立標籤物件
        self.Q12label=tk.Label(win, text="Q12")   #建立標籤物件
        self.Q13label=tk.Label(win, text="Q13")   #建立標籤物件
        self.Q14label=tk.Label(win, text="Q14")   #建立標籤物件
        self.Q15label=tk.Label(win, text="Q15")   #建立標籤物件
        self.Q16label=tk.Label(win, text="Q16")   #建立標籤物件
        self.Q17label=tk.Label(win, text="Q17")   #建立標籤物件
        self.Q18label=tk.Label(win, text="Q18")   #建立標籤物件
        self.Q19label=tk.Label(win, text="Q19")   #建立標籤物件
        self.Q20label=tk.Label(win, text="Q20")   #建立標籤物件
        # label.pack()       #顯示元件
        self.button=tk.Button(win, text="PLAY", command=self.GUIlogin)
        #self.playbutton=tk.Button(win, text="PLAY", command=self.GUIlogin)
        self.text = tk.Text(win,height=1,width=24)
        self.password_input = tk.Entry(win,show='*',width=21)
        self.boardtext = tk.Text(win,height=1,width=24)
        self.boardtext.insert(1.0,"Test")
        self.PostIDtext = tk.Text(win,height=1,width=24)
        self.hintID1text = tk.Text(win,height=1,width=24)
        self.hintID2text = tk.Text(win,height=1,width=24)
        self.hintID3text = tk.Text(win,height=1,width=24)

        self.Qtext = []
        for i in range(20):
            self.Qtext.append(tk.Text(win,height=1,width=10))
        self.Qtext[0].insert(1.0,"題目1")
        self.IDlabel.grid(column=0,row=0)

        self.text.grid(column=1,row=0,columnspan=3)
        self.PWlabel.grid(column=0,row=1)
        self.password_input.grid(column=1,row=1,columnspan=3)
        self.boardlabel.grid(column=0,row=2)
        self.boardtext.grid(column=1,row=2,columnspan=3)
        self.PostIDlabel.grid(column=0,row=3)
        self.PostIDtext.grid(column=1,row=3,columnspan=3)
        self.hintlabel.grid(column=1,row=4)
        self.hint1label.grid(column=0,row=5)
        self.hint2label.grid(column=0,row=6)
        self.hint3label.grid(column=0,row=7)
        self.hintID1text.grid(column=1,row=5,columnspan=3)
        self.hintID2text.grid(column=1,row=6,columnspan=3)
        self.hintID3text.grid(column=1,row=7,columnspan=3)
        self.questionlabel.grid(column=1,row=8)

        self.Q1label.grid(column=0,row=9)
        self.Q2label.grid(column=2,row=9)
        self.Q3label.grid(column=0,row=10)
        self.Q4label.grid(column=2,row=10)
        self.Q5label.grid(column=0,row=11)
        self.Q6label.grid(column=2,row=11)
        self.Q7label.grid(column=0,row=12)
        self.Q8label.grid(column=2,row=12)
        self.Q9label.grid(column=0,row=13)
        self.Q10label.grid(column=2,row=13)
        self.Q11label.grid(column=0,row=14)
        self.Q12label.grid(column=2,row=14)
        self.Q13label.grid(column=0,row=15)
        self.Q14label.grid(column=2,row=15)
        self.Q15label.grid(column=0,row=16)
        self.Q16label.grid(column=2,row=16)
        self.Q17label.grid(column=0,row=17)
        self.Q18label.grid(column=2,row=17)
        self.Q19label.grid(column=0,row=18)
        self.Q20label.grid(column=2,row=18)
        r=-1
        for i in range(20):
            if i%2 == 0:c=1
            else:c=3
            if i%2==0:r+=1
            self.Qtext[i].grid(column=c,row=r+9)

        self.button.grid(column=1,row=19)
        # self.playbutton.grid(column=1,row=4)
        #self.x.configure(state=NORMAL)

    def clickOK(self):
        self.count=self.count + 1
        self.IDlabel.configure(text="Click OK " + str(self.count) + " times")
    def GUIlogin(self):
        self.Password = self.password_input.get()
        self.ID = self.text.get("1.0",'end-1c')
        self.postIndex = self.PostIDtext.get("1.0",'end-1c')
        self.board = self.boardtext.get("1.0",'end-1c')

        if self.hintID1text.get("1.0",'end-1c') != '' : self.hint.append(self.hintID1text.get("1.0",'end-1c'))        
        if self.hintID2text.get("1.0",'end-1c') != '' : self.hint.append(self.hintID2text.get("1.0",'end-1c'))
        if self.hintID3text.get("1.0",'end-1c') != '' : self.hint.append(self.hintID3text.get("1.0",'end-1c'))
        for i in range(20):
            if self.Qtext[i].get("1.0",'end-1c') != '' :
                self.question.append(self.Qtext[i].get("1.0",'end-1c'))
        self.PTTlogin()
        #t.insert('insert',var)
    def PTTlogin(self):
        self.PTTBot = PTT.Library(self.ID, self.Password, kickOtherLogin=False, _LogLevel=PTT.LogLevel.DEBUG)
        ErrCode = self.PTTBot.login()
        self.Tempo()
    def Tempo(self):
        try:
            #self.thinkTempoStartGame(['題目1', '題目2'], self.postIndex, self.board)
            self.thinkTempoStartGame(self.question, self.postIndex, self.board)
        except Exception as e:
            print(e)
            self.PTTBot.Log('接到例外 啟動緊急應變措施')
        self.PTTBot.logout()

    def DetectAndEditPost(self,postIndex, board='turtlesoup'):
        ErrCode, Post = self.PTTBot.getPost(board, PostIndex=postIndex)
        if ErrCode != PTT.ErrorCode.Success:
            self.PTTBot.Log('使用文章編號取得文章詳細資訊失敗 錯誤碼: ' + str(ErrCode))

        editMsg = ""
        for Push in Post.getPushList():
            print(Push.getAuthor() + ':' + Push.getContent())
            if '[指令]' in Push.getContent():
                editMsg = Push.getAuthor() + '使用了指令' + Push.getContent().replace('[指令]', '')

        self.PTTBot.gotoBoard(board)
        self.PTTBot.gotoArticle(postIndex)
        self.PTTBot.editArticle(editMsg)
    def SendMail(self,id, title, content):
        ErrCode = self.PTTBot.mail(id, title, content, 0)
        if ErrCode == PTT.ErrorCode.Success:
            self.PTTBot.Log('寄信給 ' + id + ' 成功')
        else:
            self.PTTBot.Log('寄信給 ' + id + ' 失敗')

    def Push(self,board, postIndex, msg):
        HOST_PUSH_PREFIX = '============'

        ErrCode = self.PTTBot.push(board, PTT.PushType.Push, HOST_PUSH_PREFIX + msg, PostIndex=postIndex)
        if ErrCode == PTT.ErrorCode.Success:
            self.PTTBot.Log('使用文章編號: 推文成功')
            return True
        elif ErrCode == PTT.ErrorCode.ErrorInput:
            self.PTTBot.Log('使用文章編號: 參數錯誤')
            return False
        elif ErrCode == PTT.ErrorCode.NoPermission:
            self.PTTBot.Log('使用文章編號: 無發文權限')
            return False
        else:
            self.PTTBot.Log('使用文章編號: 推文失敗')
            return False

    def getPostPushList(self,board, postIndex, skipNumberOfPushes = 0):
        self.PTTBot.Log('取得推文清單, 於:' + board + ', index:' + str(postIndex) + ', skip:' + str(skipNumberOfPushes))
        ErrCode, Post = self.PTTBot.getPost(board, PostIndex=postIndex)
        if ErrCode != PTT.ErrorCode.Success:
            self.PTTBot.Log('使用文章編號取得文章詳細資訊失敗 錯誤碼: ' + str(ErrCode))

        pushList = Post.getPushList()
        self.PTTBot.Log('推文數量:' + str(len(pushList)))
        self.PTTBot.Log('skip後推文數量:' + str(len(pushList[skipNumberOfPushes:])))
        return pushList[skipNumberOfPushes:]

    def CheckCommandInPustList(self,command, pushList):
        self.PTTBot.Log('檢查指令:' + command)
        count = 0
        for Push in pushList:
            author = Push.getAuthor()
            content = Push.getContent()
            self.PTTBot.Log('檢查推文:' + content + '  ' + command + '!')
            found = re.search(command, content)
            count += 1
            if found != None:
                return found, author, count
        return None, None, len(pushList)

    def CheckCommandInArticle(self,board, postIndex, command, skipNumberOfPushes = 0):
        self.PTTBot.Log('開始檢查文章指令')
        pushList = self.getPostPushList(board, postIndex, skipNumberOfPushes)
        self.PTTBot.Log('取得推文列表')
        return CheckCommandInPustList(command, pushList)

    def CheckAnsInArticle(self,board, postIndex, answer, skipNumberOfPushes = 0):
        pushList = self.getPostPushList(board, postIndex, skipNumberOfPushes)
        # skip pushCheckedCount pushes
        count = 0
        for Push in pushList: 
            author = Push.getAuthor()
            content = Push.getContent()
            found = re.search(r'\*(.+)', content)
            count += 1
            if found != None:
                guess = found.group(1)
                if guess == answer:
                    return author, guess, count
        return None, None, len(pushList)
    def thinkTempoStartGame(self,questions, postIndex, board='test'):

        #hintPlayers = db.search(query.key == 'hintPlayers')[0]['value']
        #hintPlayers = ['st1009']
        hintPlayers = self.hint
        self.PTTBot.Log('讀取提示列表: ' + ','.join(hintPlayers))
        scoreMap = {}
        answerCheckedIndex = 0
        self.PTTBot.Log('遊戲準備開始')
        self.Push(board, postIndex, '遊戲準備開始!!!!')
        round = 0
        for question in questions:
            round += 1
            self.PTTBot.Log('遊戲第' + str(round) + '開始')
            
            self.Push(board, postIndex, '準備寄送題目')
            self.PTTBot.Log('寄送題目')
            for hintPlayer in hintPlayers:
                self.SendMail(hintPlayer, '聯想tempo題目' + str(round), question)
            
            
            self.Push(board, postIndex, '題目已寄送')
            time.sleep(10)
            self.Push(board, postIndex, '提示開始')

            roundComplete = False
            while(not roundComplete):
                self.PTTBot.Log('檢查答案')
                author, guess, checkedIndex = self.CheckAnsInArticle(board, postIndex, question, answerCheckedIndex)
                answerCheckedIndex += checkedIndex
                if author != None:
                    if author not in scoreMap:
                        scoreMap[author] = 1
                    else:
                        scoreMap[author] = scoreMap[author] + 1
                    self.Push(board, postIndex, '恭喜' + author + ':' + question + ' 答對(' + str(scoreMap[author]) + '分)')
                    roundComplete = True
                time.sleep(3)
        
        self.Push(board, postIndex, '遊戲結束，感謝大家!')


if __name__ == '__main__':
    print('Welcome to PTT Library v ' + PTT.Version + ' Demo')
    if len(sys.argv) == 2:
        if sys.argv[1] == '-ci':
            print('CI test run success!!')
            sys.exit()
    
    win = tk.Tk()
    APP=APP(win)
    win .mainloop()

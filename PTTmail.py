import sys
import time
import json
import getpass
import codecs

import re
from PTTLibrary import PTT
from uao import Big5UAOCodec

import tkinter as tk
class APP:
    def __init__(self,win):
        self.ID = ''
        self.Password = ''
        self.count = 0
        self.PTTBot = ''
        self.postIndex = 0

        self.recipient = ''
        self.title = ''
        self.content = ''
        
        win.title("Sent Mail")
        win.geometry('350x400')
        self.IDlabel=tk.Label(win, text="ID:")   #建立標籤物件
        self.PWlabel=tk.Label(win, text="Password:")   #建立標籤物件
        self.relabel=tk.Label(win, text="收件人:")   #建立標籤物件
        self.esclabel=tk.Label(win, text="指令:")   #建立標籤物件
        self.titlelabel=tk.Label(win, text="標題:")   #建立標籤物件
        self.contentlabel=tk.Label(win, text="內容:")   #建立標籤物件

        # label.pack()       #顯示元件
        self.button=tk.Button(win, text="Sent!", command=self.GUIlogin)
        #self.playbutton=tk.Button(win, text="PLAY", command=self.GUIlogin)
        self.text = tk.Text(win,height=1,width=24)
        self.password_input = tk.Entry(win,show='*',width=24)
        self.re_input = tk.Text(win,height=1,width=24)
        self.esc_input = tk.Text(win,height=1,width=24)
        self.title_input = tk.Text(win,height=1,width=24)
        self.content_input = tk.Text(win,height=5,width=24)

        self.IDlabel.grid(column=0,row=0)

        self.text.grid(column=1,row=0,columnspan=3)
        self.PWlabel.grid(column=0,row=1)
        self.password_input.grid(column=1,row=1,columnspan=3)
        self.relabel.grid(column=0,row=2)
        self.re_input.grid(column=1,row=2,columnspan=3)
        #self.esclabel.grid(column=0,row=3)
        #self.esc_input.grid(column=1,row=3,columnspan=3)
        self.titlelabel.grid(column=0,row=3)
        self.title_input.grid(column=1,row=3,columnspan=3)
        self.contentlabel.grid(column=0,row=4)
        self.content_input.grid(column=1,row=4,columnspan=3,rowspan=5)
        # r=-1
        # for i in range(20):
        #     if i%2 == 0:c=1
        #     else:c=3
        #     if i%2==0:r+=1
        #     self.Qtext[i].grid(column=c,row=r+9)

        self.button.grid(column=2,row=19)
    def GUIlogin(self):
        self.Password = self.password_input.get()
        self.ID = self.text.get("1.0",'end-1c')
        self.recipient = self.re_input.get("1.0",'end-1c')
        self.title = self.title_input.get("1.0",'end-1c')
        self.content = self.content_input.get("1.0",'end-1c')
        # print(self.recipient.split('@'))
        self.PTTlogin()
    def PTTlogin(self):
        self.PTTBot = PTT.Library(self.ID, self.Password, kickOtherLogin=False, _LogLevel=PTT.LogLevel.DEBUG)
        ErrCode = self.PTTBot.login()
        for id_num in self.recipient.split('@'):
            self.SendMail(id_num,self.title,self.content)
    def SendMail(self,id, title, content):
        ErrCode = self.PTTBot.mail(id, title, content, 0)
        if ErrCode == PTT.ErrorCode.Success:
            self.PTTBot.Log('寄信給 ' + id + ' 成功')
        else:
            self.PTTBot.Log('寄信給 ' + id + ' 失敗')
if __name__ == '__main__':
    print('Welcome to PTT Library v ' + PTT.Version + ' Demo')
    if len(sys.argv) == 2:
        if sys.argv[1] == '-ci':
            print('CI test run success!!')
            sys.exit()
    
    win = tk.Tk()
    APP=APP(win)
    win .mainloop()
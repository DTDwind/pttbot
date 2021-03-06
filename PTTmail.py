import sys
import time
import json
import getpass
import codecs

import re
from PTTLibraryQ import PTT
from uao import Big5UAOCodec

import tkinter as tk
from tkinter import messagebox
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
        self.esc = ''
        win.title("Sent Mail")
        win.geometry('600x220')
        self.IDlabel=tk.Label(win, text="ID:")   #建立標籤物件
        self.PWlabel=tk.Label(win, text="Password:")   #建立標籤物件
        self.relabel=tk.Label(win, text="收件人:")   #建立標籤物件
        self.esclabel=tk.Label(win, text="指令:")   #建立標籤物件
        self.titlelabel=tk.Label(win, text="標題:")   #建立標籤物件
        self.contentlabel=tk.Label(win, text="內容:")   #建立標籤物件
        #self.backuplabel=tk.Label(win, text="自存底搞")   #建立標籤物件
        # label.pack()       #顯示元件
        self.Preview_button=tk.Button(win, text="預覽", command=self.Preview)
        self.button=tk.Button(win, text="Sent!", command=self.GUIlogin)
        #self.playbutton=tk.Button(win, text="PLAY", command=self.GUIlogin)
        self.text = tk.Text(win,height=1,width=68)
        self.password_input = tk.Entry(win,show='*',width=68)
        self.re_input = tk.Text(win,height=1,width=68)
        self.esc_input = tk.Text(win,height=1,width=68)
        self.title_input = tk.Text(win,height=1,width=68)
        self.content_input = tk.Text(win,height=5,width=68)
        self.var1 = tk.IntVar()
        self.backup_input = tk.Checkbutton(win, text='自存底搞', variable=self.var1, onvalue=1, offvalue=0)
        
        self.IDlabel.grid(column=0,row=0)

        self.text.grid(column=1,row=0,columnspan=5)
        self.PWlabel.grid(column=0,row=1)
        self.password_input.grid(column=1,row=1,columnspan=5)
        self.relabel.grid(column=0,row=2)
        self.re_input.grid(column=1,row=2,columnspan=5)
        self.esclabel.grid(column=0,row=3)
        self.esc_input.grid(column=1,row=3,columnspan=5)
        self.titlelabel.grid(column=0,row=4)
        self.title_input.grid(column=1,row=4,columnspan=5)
        self.contentlabel.grid(column=0,row=5)
        self.content_input.grid(column=1,row=5,columnspan=5,rowspan=5)
        self.backup_input.grid(column=0,row=11)
        self.Preview_button.grid(column=1,row=11)
        # r=-1
        # for i in range(20):
        #     if i%2 == 0:c=1
        #     else:c=3
        #     if i%2==0:r+=1
        #     self.Qtext[i].grid(column=c,row=r+9)

        self.button.grid(column=3,row=11)
    def Preview(self):
        self.recipient = self.re_input.get("1.0",'end-1c')
        self.title = self.title_input.get("1.0",'end-1c')
        self.content = self.content_input.get("1.0",'end-1c')
        self.esc = self.esc_input.get("1.0",'end-1c')
        i = 0
        esc_content = self.esc.split('@')
        escape_content = ''
        for id_num in self.recipient.split('@'):
            if i < len(esc_content): escape_content = self.content.replace('[指令]', esc_content[i])
            else :escape_content = self.content
            i +=1
            tk.messagebox.showinfo(title=id_num,message=escape_content)#提示信息对话窗
        
        
    def GUIlogin(self):
        self.Password = self.password_input.get()
        self.ID = self.text.get("1.0",'end-1c')
        self.recipient = self.re_input.get("1.0",'end-1c')
        self.title = self.title_input.get("1.0",'end-1c')
        self.content = self.content_input.get("1.0",'end-1c')
        self.esc = self.esc_input.get("1.0",'end-1c')

        self.PTTlogin()
    def PTTlogin(self):
        if self.PTTBot == '':
            self.PTTBot = PTT.Library(self.ID, self.Password, kickOtherLogin=False, _LogLevel=PTT.LogLevel.DEBUG)
            ErrCode = self.PTTBot.login()
        esc_content = self.esc.split('@')
        i = 0
        # print(esc_content)
        escape_content = ''
        for id_num in self.recipient.split('@'):
            if i < len(esc_content): escape_content = self.content.replace('[指令]', esc_content[i])
            else :escape_content = self.content
            i +=1
            self.SendMail(id_num,self.title,escape_content)
        #self.PTTBot.logout()
    def SendMail(self,id, title, content):
        # 第一個參數是你想寄信的鄉民 ID
        # 第二個參數是信件標題
        # 第三個參數是信件內容
        # 第四個參數是簽名檔選擇 0 不加簽名檔
        # 第五個參數是是否自存底搞 1存
        ErrCode = self.PTTBot.mail(id, title, content, 0,self.var1.get())
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
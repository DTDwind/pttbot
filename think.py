import sys
import time
import json
import getpass
import codecs

import re
from tinydb import TinyDB, Query
from PTTLibrary import PTT
from uao import Big5UAOCodec
#from PTTLibrary import Big5uao

# 如果你想要自動登入，建立 account.json
# 然後裡面填上 {"ID":"YourID", "Password":"YourPW"}

BoardList = ['Wanted', 'Gossiping', 'Test', 'NBA', 'Baseball', 'LOL', 'C_Chat']

PTTBot = None
ResPath = './OldBug/'

def SendMail(id, title, content):
    ErrCode = PTTBot.mail(id, title, content, 0)
    if ErrCode == PTT.ErrorCode.Success:
        PTTBot.Log('寄信給 ' + id + ' 成功')
    else:
        PTTBot.Log('寄信給 ' + id + ' 失敗')

def Push(board, postIndex, msg):
    HOST_PUSH_PREFIX = '============'

    ErrCode = PTTBot.push(board, PTT.PushType.Push, HOST_PUSH_PREFIX + msg, PostIndex=postIndex)
    if ErrCode == PTT.ErrorCode.Success:
        PTTBot.Log('使用文章編號: 推文成功')
        return True
    elif ErrCode == PTT.ErrorCode.ErrorInput:
        PTTBot.Log('使用文章編號: 參數錯誤')
        return False
    elif ErrCode == PTT.ErrorCode.NoPermission:
        PTTBot.Log('使用文章編號: 無發文權限')
        return False
    else:
        PTTBot.Log('使用文章編號: 推文失敗')
        return False

def writeJsonFile(dictObj):
    with open('data.json', 'w') as outputFile:
        json.dump(dictObj, outputFile)

def getPostPushList(board, postIndex, skipNumberOfPushes = 0):
    PTTBot.Log('取得推文清單, 於:' + board + ', index:' + str(postIndex) + ', skip:' + str(skipNumberOfPushes))
    ErrCode, Post = PTTBot.getPost(board, PostIndex=postIndex)
    if ErrCode != PTT.ErrorCode.Success:
        PTTBot.Log('使用文章編號取得文章詳細資訊失敗 錯誤碼: ' + str(ErrCode))

    pushList = Post.getPushList()
    PTTBot.Log('推文數量:' + str(len(pushList)))
    PTTBot.Log('skip後推文數量:' + str(len(pushList[skipNumberOfPushes:])))
    return pushList[skipNumberOfPushes:]

def CheckCommandInPustList(command, pushList):
    PTTBot.Log('檢查指令:' + command)
    count = 0
    for Push in pushList:
        author = Push.getAuthor()
        content = Push.getContent()
        PTTBot.Log('檢查推文:' + content + '  ' + command + '!')
        found = re.search(command, content)
        count += 1
        if found != None:
            return found, author, count
    return None, None, len(pushList)

def CheckCommandInArticle(board, postIndex, command, skipNumberOfPushes = 0):
    PTTBot.Log('開始檢查文章指令')
    pushList = getPostPushList(board, postIndex, skipNumberOfPushes)
    PTTBot.Log('取得推文列表')
    return CheckCommandInPustList(command, pushList)

def CheckAnsInArticle(board, postIndex, answer, skipNumberOfPushes = 0):
    pushList = getPostPushList(board, postIndex, skipNumberOfPushes)
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

# 聯想tempo遊戲前準備
def thinkTempoPreparation(postIndex, board='turtlesoup'):
    # var init
    HINT_PLAYER_NUMBER = 1  # 提示人數
    GUESS_PLAYER_NUMBER = 3  # 猜題人數(尚未使用)

    PATTERN_REG_HINT = r'\[報名提示\]' # 報名提示指令
    PATTERN_REG_GUESS = r'\[報名猜題\]' # 報名猜題指令(尚未使用)

    # 接受報名
    guessPlayers = []
    hintPlayers = []
    guessPlayerNameMap = {}
    hintPlayerNameMap = {}

    gamePrepared = False
    pushHasCheckedHintRegister = 0
    pushHasCheckedGuessRegister = 0
    
    # 持續檢查報名狀況
    while(not gamePrepared):
        PTTBot.Log('檢查報名')
        # 檢查提示報名
        found, author, checkedIndex = CheckCommandInArticle(board, postIndex, PATTERN_REG_HINT, pushHasCheckedHintRegister)
        PTTBot.Log('已檢查推文數' + str(checkedIndex))
        PTTBot.Log('檢查報名提示完成')
        if found != None:
            PTTBot.Log(author + '報名了提示')
            if (author not in hintPlayers):
                if (len(hintPlayers) == HINT_PLAYER_NUMBER):
                    Push(board, postIndex, author + '報名了提示失敗，人數已滿')
                else:
                    hintPlayers.append(author)
                    Push(board, postIndex, author + '報名了提示成功')
        else:
            PTTBot.Log('未發現報名提示推文')
        pushHasCheckedHintRegister += checkedIndex

        # 檢查猜題報名
        # found, author, checkedIndex = CheckCommandInArticle(board, postIndex, PATTERN_REG_GUESS, pushHasCheckedGuessRegister)
        # if found != None:
        #     PTTBot.Log(author + '報名了猜題')
        #     if (author not in guessPlayers):
        #         if (len(guessPlayers) == GUESS_PLAYER_NUMBER):
        #             Push(board, postIndex, author + '報名了猜題失敗，人數已滿')
        #         else:
        #             guessPlayers.append(author)
        #             Push(board, postIndex, author + '報名了猜題成功')
        #     else:
        #         PTTBot.Log('未發現報名猜題推文')
        # pushHasCheckedGuessRegister += checkedIndex
        
        
        time.sleep(4)

        if len(hintPlayers) == HINT_PLAYER_NUMBER:
            gamePrepared = True
    
    PTTBot.Log('遊戲報名準備完成')
    Push(board, postIndex, '已達報名人數、遊戲報名準備完成')
    
    db = TinyDB('db.json')
    query = Query()
    if len(db.search(query.key == 'hintPlayers')) == 0:
        db.insert({'key': 'hintPlayers','value': hintPlayers})
    else:
        db.update({'key': 'hintPlayers','value': hintPlayers})


    #開始遊戲
    # 推文 遊戲開始!
    # for question in questions:
    #     for hintPlayer in hintPlayers:
            # 寄送 question 給 hintPlayer
        # wait 30 secs

        # 推文 ══════════╡ 提示開始 ╞══════════
        # wait HINT_TIME
        # 推文 ══════════╡ 提示結束 ╞══════════
            # roundComplete = False
            # while(not roundComplete):
                # 取得新的推文
                # if 推文為答題者第一次回答 and 正確  
                #   roundComplete = True
                #   推文  =========答體者: 答案 答對! [比數]
def thinkTempoStartGame(questions, postIndex, board='turtlesoup'):

    PTTBot.Log('讀取報名資料')
    db = TinyDB('db.json')
    query = Query()
    hintPlayers = db.search(query.key == 'hintPlayers')[0]['value']
    # hintPlayers = ['提示id1', '提示id2', '提示id3']
    PTTBot.Log('讀取提示列表: ' + ','.join(hintPlayers))

    scoreMap = {}

    answerCheckedIndex = 0

    PTTBot.Log('遊戲準備開始')
    Push(board, postIndex, '遊戲準備開始!!!!')
    round = 0
    for question in questions:
        round += 1
        PTTBot.Log('遊戲第' + str(round) + '開始')
        
        Push(board, postIndex, '準備寄送題目')
        PTTBot.Log('寄送題目')
        for hintPlayer in hintPlayers:
            SendMail(hintPlayer, '聯想tempo題目' + str(round), question)
        
        
        Push(board, postIndex, '題目已寄送')
        time.sleep(10)
        Push(board, postIndex, '提示開始')

        roundComplete = False
        while(not roundComplete):
            PTTBot.Log('檢查答案')
            author, guess, checkedIndex = CheckAnsInArticle(board, postIndex, question, answerCheckedIndex)
            answerCheckedIndex += checkedIndex
            if author != None:
                if author not in scoreMap:
                    scoreMap[author] = 1
                else:
                    scoreMap[author] = scoreMap[author] + 1
                Push(board, postIndex, '恭喜' + author + ':' + question + ' 答對(' + str(scoreMap[author]) + '分)')
                roundComplete = True
            time.sleep(3)
    
    Push(board, postIndex, '遊戲結束，感謝大家!')
    if len(db.search(query.key == 'scores')) == 0:
        db.insert({'key': 'scores','value': scoreMap})
    else:
        db.update({'key': 'scores','value': scoreMap})


def DetectAndEditPost(postIndex, board='turtlesoup'):
    ErrCode, Post = PTTBot.getPost(board, PostIndex=postIndex)
    if ErrCode != PTT.ErrorCode.Success:
        PTTBot.Log('使用文章編號取得文章詳細資訊失敗 錯誤碼: ' + str(ErrCode))

    editMsg = ""
    for Push in Post.getPushList():
        print(Push.getAuthor() + ':' + Push.getContent())
        if '[指令]' in Push.getContent():
            editMsg = Push.getAuthor() + '使用了指令' + Push.getContent().replace('[指令]', '')

    PTTBot.gotoBoard(board)
    PTTBot.gotoArticle(postIndex)
    PTTBot.editArticle(editMsg)

if __name__ == '__main__':
    print('Welcome to PTT Library v ' + PTT.Version + ' Demo')

    if len(sys.argv) == 2:
        if sys.argv[1] == '-ci':
            print('CI test run success!!')
            sys.exit()

    try:
        with open('Account.json') as AccountFile:
            Account = json.load(AccountFile)
            ID = Account['ID']
            Password = Account['Password']
    except FileNotFoundError:
        ID = input('請輸入帳號: ')
        Password = getpass.getpass('請輸入密碼: ')
    
    #PTTBot = PTT.Library(ID, Password,)
    PTTBot = PTT.Library(ID, Password, kickOtherLogin=False, _LogLevel=PTT.LogLevel.DEBUG)
    ErrCode = PTTBot.login()
    PTTBot.Log(ErrCode)
    if ErrCode != PTT.ErrorCode.Success:
        PTTBot.Log('登入失敗')
        PTTBot.Log(ErrCode)
        sys.exit()
    
    PTTBot.Log('登入成功! 準備進行動作...')
    try:
        #thinkTempoPreparation(340, 'test')
        thinkTempoStartGame(['題目1', '題目2'], 340, 'test')
        pass
    except Exception as e:
        print(e)
        PTTBot.Log('接到例外 啟動緊急應變措施')
    # 請養成登出好習慣
    PTTBot.logout()
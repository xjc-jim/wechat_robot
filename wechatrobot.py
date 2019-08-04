import itchat
import time
import requests
from itchat.content import *

KEY = '9978272a14e54******866104bb47135'  # 你需要用自己的API号替换掉
LIST = []                                 # 用来存放已经有过对话的联系人
MEDIA = []
start = 1
num = 0

def get_response(msg):
    # 这里我们构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'   # 这是API接口网址，不要变
    data = {
        'key'    : KEY,                               # 这个KEY就是上面已经赋值的KEY，就这样不用改
        'info'   : msg,                               # 这是我们要发出去的消息，属于文本消息
        'userid' : 'wechat-robot',                    # wechat-robot这个名字可以随便取，注意加引号
    }
    try:
        r = requests.post(apiUrl, data=data).json()
       
                               # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
                               # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
                               # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
                               # 将会返回一个None
        return

            
def wechat():
    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def reply(msg):    
        nickName0 = itchat.search_friends()['NickName']        #自己的昵称
        try:
            nickName1 = itchat.search_friends(userName=msg['FromUserName'])['NickName']     #对方昵称，try...except...保证nickName1为空时不抛出异常
        except:
            return
        
        global start          #是全局变量得以修改
        if nickName1 == nickName0 and msg.text == 'turn off':     # 对话中出现turn off,则机器人关闭，当然这并不是终止程序运行
            start = 0
            msg.user.send('机器人已关闭！')
        if nickName1 == nickName0 and msg.text == 'turn on':      # 对话中出现turn on,则启动机器人
            start = 1
            msg.user.send('机器人已启动！')

        def delay():
            msg.user.send('等待回复...')
            time.sleep(3)
                    
        if nickName1 != nickName0 and start == 1:
            if msg['Type'] == TEXT or msg['Type'] == MAP or msg['Type'] == CARD or msg['Type'] == NOTE or msg['Type'] == SHARING or msg['Type'] == PICTURE or msg['Type'] == RECORDING or msg['Type'] == ATTACHMENT or msg['Type'] == VIDEO:    
                t0 = time.localtime()[5]              #列表的第5个是秒
                
                while msg.FromUserName not in LIST:       #程序启动后，每与一个人联系，就将此人的名称保存在列表LIST中
                    t1 = time.localtime()[5]
                    if t1 - t0 > 10:
                        msg.user.send('等待超时，程序介入')
                        time.sleep(1)
                        msg.user.send('你好！我是微信机器人助手小夏同学（这个名字自己改，一般与图灵机器人的名字相同），我的主人在2019年4月16日使用python与核心类库itchat及图灵机器人API开发了我，我在主人无法及时回复时介入对话并执行简单任务，我不会搜集任何信息，谢谢合作！')
                        LIST.append(msg.FromUserName)      #保存在LIST中
                        break
                    
                time.sleep(2)
                
                global num
                
                if msg['Type'] == TEXT and num < 101:
                    num = num + 1
                    reply = get_response(msg['Text'])      # 使用图灵机器人回答
                    defaultReply = '信息分类——%s: %s' % (msg.type, msg.text)
                    return reply or defaultReply     #reply优先，异常时才是后者

                if msg['Type'] == TEXT and num == 101:
                    delay()
                    msg.user.send('信息分类——%s: %s' % (msg.type, msg.text))
                                
                if msg['Type'] == MAP or msg['Type'] == CARD or msg['Type'] == NOTE or msg['Type'] == SHARING:
                    delay()
                    msg.user.send('信息分类——%s: %s' % (msg.type, msg.text))
                                
                if msg['Type'] == PICTURE or msg['Type'] == RECORDING or msg['Type'] == ATTACHMENT or msg['Type'] == VIDEO:
                    delay()
                    msg.user.send('信息分类——%s:%s' % (msg.type, msg.fileName))
                                                                      # 上面是输出信息分类
                if msg.type == MAP:                                   # 地图位置信息
                    msg.user.send('哦，我的小宝贝，原来你在这里！')
                                
                if msg.type == CARD:                                  # 名片信息
                    msg.user.send('哇哦，这位优秀的人士是？')
                                
                if msg.type == NOTE:                                  # 当你被拉黑或是加了新朋友后对话框中出现的灰色提示语
                    msg.user.send('谢谢你的通知啦！')
                                
                if msg.type == SHARING:                               # 朋友分享
                    msg.user.send('你的分享可真不错！受益匪浅！')
                                
                if msg.type == PICTURE or msg.type == VIDEO:          # 对方发送的图片与视频会被自动保存在程序文件所在的位置
                    MEDIA.append(msg.fileName)
                    msg.download(MEDIA[-1])
                    msg.user.send('你发送的图片视频将被我自动下载至当前路径')
                                
                if msg.type == RECORDING:                             # 语音信息
                    msg.user.send('虽然我听不懂你的话，但是我依然觉得你的声音是世界上最甜的！')
                    time.sleep(5)
                    msg.user.send('如果你无聊，可以和我聊天呀，嘻嘻嘻嘻！')
                    
                 
    @itchat.msg_register(FRIENDS)
    def add_friend(msg):                                              # 自动允许添加新朋友
        msg.user.verify()
        msg.user.send('你好！Nice to meet you!')

    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):                                              # 群聊中被人@
        if msg.isAt:
            msg.user.send(u'@%s\u2005I received: 神马问题？' %        #itchat中@的固定格式
            msg.actualNickName)


while True:
    wechat()
    itchat.auto_login(hotReload=True)
    itchat.run(True)                                                  # itchat启动

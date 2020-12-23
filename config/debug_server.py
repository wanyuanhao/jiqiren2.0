import socket
from config import Headers
import threading



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8888))
#最大链接数量
server.listen(5)
# 等待链接
print('服务端已启动==》等待链接')
client,address=server.accept()

while True:
    #接受客户端的询问，设置内容长度

    data = client.recv(1024).decode('utf-8')
    print('接受客户端询问的内容是： ',data)
    # 如果客户端发送的内容是close则关闭连接
    if data == 'close':
        print('服务端关闭连接')
        server.close()
        break
    elif data == 'token':
        result = Headers.Headers.token('wanyuanhao')
        print(result)
        client.send(result.encode('utf-8'))

    # 如果客户端发送的内容不是close,则回复客户端的问题
    recv_data = input('请输入回复内容： ')
    client.send(recv_data.encode('utf-8'))
    print('等待客户端的回应。。。')


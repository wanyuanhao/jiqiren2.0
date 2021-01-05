import socket


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('客户端已启动')
client.connect(('127.0.0.1', 8888))
print('客户端已链接到服务端')

# 如果发送的内容是close，则关闭链接，并且把close传到服务端
# 如果不是close则保持链接

while True:
    data = input('请输入咨询的内容')
    client.send(data.encode('utf-8'))
    if data == 'close':
        print('客户端关闭连接')
        client.close()
        break
    print('等待服务端回应。。。')
    # 接受内容的长度
    # recv_data = client.recv(1024).decode('utf-8')
    recv_data = []
    while True:
        data1 = client.recv(1024).decode('utf-8')
        if data1:
            recv_data.append(data1)
        else:
            break
    print('服务端回复的内容是： ',recv_data)

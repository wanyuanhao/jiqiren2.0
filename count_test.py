from config.Headers import Headers
from module.kehuguanli.CustomerList import CustomerList

path = open('d:/zhanghao1.txt', encoding='utf-8')
users = path.readlines()
# users = ['wanyuanhao','top2']
username = []
conut = 0
for i in users:
    user = i.strip('\n').strip(',')
    username.append(user)
    headers = Headers().token(user)
    if "登录报错" in headers:
        pass
    else:
        conut += 1
        result = CustomerList().customerlist_tab_count(headers)
        print('{0}、账号：({1})\n列表统计：{2}'.format(conut,user, result['data']))
        chudan_count = CustomerList().chudan_count(headers)
        print('出单总数：{0}'.format(chudan_count['data']))
        zhanbai_count = CustomerList().zhanbai_count(headers)
        print('战败总数：{0}'.format(zhanbai_count['data']))
        employeeid = CustomerList().get_empolyeeid(headers)
        agent_count = CustomerList().agent_count(headers,employeeid)
        print("业务员总数：{0}".format(agent_count))
        juese_count = CustomerList().role_count(headers,employeeid)
        print("角色总数：{0}".format(juese_count))
        call_count = CustomerList().call_count(headers)
        print('通话记录总数：{}'.format(call_count))

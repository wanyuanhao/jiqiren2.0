from config.Headers import Headers
from module.kehuguanli.kehuliebiao import kehuliebiao

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
        result = kehuliebiao().kehuliebiao_tab_count(headers)
        print('{0}、账号：({1})\n列表统计：{2}'.format(conut,user, result['data']))
        chudan_count = kehuliebiao().chudan_count(headers)
        print('出单总数：{0}'.format(chudan_count['data']))
        zhanbai_count = kehuliebiao().zhanbai_count(headers)
        print('战败总数：{0}'.format(zhanbai_count['data']))
        employeeid = kehuliebiao().get_empolyeeid(headers)
        agent_count = kehuliebiao().agent_count(headers,employeeid)
        print("业务员总数：{0}".format(agent_count))
        juese_count = kehuliebiao().juese_count(headers,employeeid)
        print("角色总数：{0}".format(juese_count))
        call_count = kehuliebiao().call_count(headers)
        print('通话记录总数：{}'.format(call_count))

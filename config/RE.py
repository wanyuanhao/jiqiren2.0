import re
# 正则
s = 'hello world'
result = re.match('hello',s)
print(result)

result1 = re.findall('s',s)
print(result1)
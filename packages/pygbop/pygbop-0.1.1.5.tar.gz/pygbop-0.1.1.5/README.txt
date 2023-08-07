
Gbop平台Python客户端

from pygbop import GbopApiClient, Method

client = GbopApiClient(access_key='xxxxxxxx', secret_key='xxxxxxxx-xxxx-xxxx-xxxx',
                       base_url='hello.api-dev.test.xxx.com')

print('=============GET=============')
params = {
    'params1': '123',
    'params3': ['s', 'w', 'k'],
    'params2': '321',
}
res = client.execute(Method.GET, '/api/v1/hello', params)
print(res.decode('utf-8'))

print('=============POST=============')
data = {'params3': 'testA', 'params4': 'testB'}
res = client.execute(Method.POST, '/api/v1/demo', data=data)
print(res.decode('utf-8'))

print('=============POST2=============')
params = {'params3': 'testA', 'params4': 'testB'}
res = client.execute(Method.POST, '/api/v1/demo', params=params, data=data)
print(res.decode('utf-8'))
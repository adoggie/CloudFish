#coding:utf-8
__author__ = 'zhangbin'


import swiftclient as sw

"""
curl -X POST -d '{"auth”: {"passwordCredentials":{"username": "admin", "password": "605ab45d701f4256"}}}' -H "Content-type: application/json" http://172.16.10.249:5000/v2.0/tokens | python -mjson.tool

http://docs.openstack.org/developer/python-swiftclient/client-api.html#examples

"""

_authurl = 'http://172.16.10.249:5000/v2.0/'
_authurl = 'http://172.16.10.60:5000/v2.0/'
_auth_version = '2'
# _auth_version = '1'
_user = 'admin'
_key = '605ab45d701f4256'
_key = '111111'
_tenant_name = 'admin'

conn = sw.client.Connection(
    authurl=_authurl,
    user=_user,
    key=_key,
    tenant_name=_tenant_name,
    auth_version=_auth_version
)

# print conn.token
#headers,containers = conn.get_account()

# print conn.get_auth()
#overview,files = conn.get_container("cc01")
#for f in files :
#    print f

# print conn.get_object("cc01",u'\u80d6\u5b50-cap.jpg')
# print conn.get_object("cc01",u'f01/swift.conf')
print conn.put_container("0021")

headers,containers = conn.get_account()
print containers

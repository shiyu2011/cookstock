#!/usr/bin/env python
print('If you get error "ImportError: No module named \'six\'" install six:\n'+\
    '$ sudo pip install six');
print('To enable your free eval account and get CUSTOMER, YOURZONE and ' + \
    'YOURPASS, please contact sales@brightdata.com')
import sys
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
    import random
    username = 'brd-customer-hl_2e3eba81-zone-residential_proxy1'
    password = 'kixnymcnl9sr'
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@brd.superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler = request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = request.build_opener(proxy_handler)
    print('Performing request')
    print(opener.open('https://geo.brdtest.com/mygeo.json').read())
if sys.version_info[0]==3:
    import urllib.request
    import random
    username = 'brd-customer-hl_2e3eba81-zone-residential_proxy1'
    password = 'kixnymcnl9sr'
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@brd.superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler = urllib.request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = urllib.request.build_opener(proxy_handler)
    print('Performing request')
    print(opener.open('https://geo.brdtest.com/mygeo.json').read())
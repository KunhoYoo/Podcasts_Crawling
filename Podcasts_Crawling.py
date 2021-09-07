import requests
import json
import os
import re
from itertools import count

cnt = 0
stop = False
for offset in count(0):
    ch_url = 'http://www.podbbang.com/_m_api/podcasts/****/episodes'
    params = {
        'offset': offset,
    }
    
    html = requests.get(ch_url, params = params)
    print(html)
    
    result_dict = json.loads(html.text)
    
    tot_count = result_dict['summary']['total_count']
    print(tot_count)
    
    for r in result_dict['data']:
        cnt += 1
        print(cnt)
        
        print(r['id'])
        print(r['title'])
        print(r['enclosure']['url'])
        print(r['enclosure']['length'])
        print(r['duration'])
        print(r['published_at'])
        title = re.sub('[*\|<>?:"/]', '', r['title'])
        mp3_bin = requests.get(r['enclosure']['url']).content
        
        base_filename = os.path.basename(r['enclosure']['url'])
        filename = '{}_{}_{}'.format(r['id'], title, base_filename)
        print(filename)
        
        with open(filename, 'wb') as f:
            f.write(mp3_bin)  
        
        print(cnt)
        
        if cnt >= tot_count:
            stop = True
            break
        
    if stop:
        break

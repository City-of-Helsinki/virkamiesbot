# -*- coding: utf-8 -*-
import requests
from django.utils.html import strip_tags, escape


api_url = 'https://dev.hel.fi/paatokset/v1/agenda_item/'

def fetch_decisions():
    policymakers = get_policymaker_ids()
    # policymakers = ["u541000vh1", "u51105100vh1", "u5110510020vh1"]
    filtered_decisions = []
    for pmaker in policymakers:
        payload = {'meeting__policymaker__slug': pmaker,
                   'order_by': 'last_modified_time', 'limit': 1}
        response = requests.get(api_url, params=payload)
        if response.ok:
            decisions = response.json()
            if decisions['meta']['total_count'] > 0:
                for d in decisions['objects']:
                    decision = {'policymaker': d['meeting']['policymaker_name'],
                                'content': strip_tags(d['content'][0]['text']),
                                'districts': districts_to_string(d['issue']['districts']),
                                'permalink': d['permalink']}
                    filtered_decisions.append(decision)

    return filtered_decisions

"""Policymaker ids whose decisions are followed from Open Ahjo API
"""
def get_policymaker_ids():
    ids = ["u541000vh1", "u51105100vh1", "u5110510020vh1", "u5110510050vh1",
           "u5110510040vh1", "u5110510010vh1", "u5110510030vh1",
           "u511051002030vh1", "u511051002020vh1", "u511051002010vh1",
           "u511051005020vh1", "u511051005010vh1", "u511051005030vh1",
           "u511051004010vh1", "u511051004020vh1", "u511051004040vh1",
           "u511051004030vh1", "u511051001030vh1", "u511051001020vh1",
           "u511051001010vh1", "u511051003030vh1", "u511051003030vh3",
           "u511051003020vh1", "u511051003020vh2", "u511051003020vh3",
           "u511051003010vh1", "u511051003010vh3", "u511051003010vh2",
           "u511051003010vh4", "u511051003010vh4", "u5110530020vh1",
           "u5110530010vh1", "u5110530030vh1","u5110530040vh1",
           "u511053002020vh1", "u511053002010vh1", "u511053002030vh1",
           "u511053001030vh1", "u511053001040vh1", "u511053001020vh1",
           "u5110530050vh1", "u511053005050vh1", "u511053003020vh1", 
           "u511053003010vh1", "u511053003050vh1", "u511053003030vh1",
           "u511053003040vh1", "u511053004020vh1", "u511053004010vh1",
           "u511053004010vh2", "u511053004030vh1", "u511053004030vh4",
           "u511053004030vh2", "u511053004030vh3", "u511053004030vh5",
           "u51105200vh1", "u5110520050vh1", "u5110520010vh1",
           "u5110520040vh1", "u5110520020vh1", "u511052005010vh1",
           "u511052005020vh1", "u511052001010vh1", "u511052001020vh1",
           "u511052001030vh1", "u511052001040vh1", "u511052004010vh1",
           "u511052004020vh1", "u511052004060vh1", "u511052004030vh1",
           "u511052004040vh1", "u511052004050vh1", "u511052002040vh1",
           "u511052002050vh1", "u511052002010vh1", "u511052002030vh1",
           "u511052002020vh1", "u511052003020vh1", "u511052003060vh1",
           "u511052003060vh2", "u511052003060vh3", "u511052003060vh4",
           "u511052003040vh1", "u511052003010vh1", "u51105400vh1",
           "u5110540010vh1", "u5110540050vh1", "u511054001010vh1"]
    return ids


def districts_to_string(districts):
    district_string = ''
    for dist in districts:
        if dist['type'] == 'kaupunginosa':
            district_string += ' #%s' % dist['name']
    return district_string.strip()
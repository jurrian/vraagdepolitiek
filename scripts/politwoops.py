import json
import requests
import copy
from datetime import datetime
from dateutil import parser


def load(path):
    with open(path, encoding="utf8") as f:
        return json.load(f)


def save(path, data):
    with open(path, 'wb') as f:
        j = json.dumps(data)
        f.write(j.encode('ascii', 'ignore'))


parties = load('parties.json')

politicians = load('politicians.json')
for politician in politicians:
    politician['party'] = parties[str(politician['party_id'])]

politicians = {x['user_name']: x for x in politicians}

groups = load('groups.json')

filter_groups = [
    'amsterdam',
    'utrecht',
    'den-haag',
    'rotterdam',
    'barendrecht',
    'eerstekamer',
    'meierijstad',
    'provincie-drenthe',
    'provincie-flevoland',
    'provincie-fryslan',
    'provincie-gelderland',
    'provincie-groningen',
    'provincie-limburg',
    'provincie-noord-brabant',
    'provincie-noord-holland',
    'provincie-overijssel',
    'provincie-utrecht',
    'provincie-zeeland',
    'provincie-zuid-holland',
]

filter_parties = {
    1: 'cda',
    386: 'cda-',
    2: 'christenunie',
    3: 'd66',
    4: 'groenlinks',
    80: 'gl',
    5: 'pvda',
    6: 'sp',
    237: 'SP',
    197: 'cu',
    8: 'vvd',
    16: 'pvdd',
    17: 'pvv',
    136: 'sgp',
    284: '50plus',
    638: 'denk',
    634: 'forumvoordemocratie',
    # 39: 'tweede-kamer',
    # 71: 'tweede-kramer',
}

new_groups = dict()
for g in groups:
    group = g['group']

    if group['slug'] in filter_groups:
        resp = requests.get(group['href_json'])
        resp.raise_for_status()
        json_data = resp.json()
        politician_data = json_data['true']['user_names']['data'] + json_data['false']['user_names']['data']
        twitter_handles = {x['label']: None for x in politician_data if x['label'] != 'other'}

        if twitter_handles:
            new_groups[group['slug']] = twitter_handles
        else:
            print("Group {} has no twitter handles".format(group['slug']))


rep_fixture = list()
rep_fixture_template = {'model': 'backend.representative', 'pk': None, 'fields': {}}

org_fixture = list()
org_fixture_template = {'model': 'backend.organization', 'pk': None, 'fields': {}}

# group_politicians = copy.copy(new_groups)
# for group, twitter_handles in new_groups.items():
#    for twitter_handle in twitter_handles.keys():
#        politician = politicians.get(twitter_handle)
#        if politician:
for twitter_handle, politician in politicians.items():
            if politician['party_id'] not in filter_parties.keys():
                continue
            # group_politicians[group][twitter_handle] = politician

            fixture_item = copy.deepcopy(rep_fixture_template)

            if politician['gender'] == 'm':
                fixture_item['fields']['gender'] = 0
            elif politician['gender'] == 'f':
                fixture_item['fields']['gender'] = 1

            if politician['date_of_birth']:
                # Currently none found
                dt = parser.parse(politician['date_of_birth'])
                fixture_item['fields']['birth_date'] = dt.strftime('%Y-%m-%d')

            fixture_item['fields']['first_name'] = politician['first_name'] or politician['screen_name']
            if not fixture_item['fields']['first_name']:
                continue

            if politician['last_name']:
                fixture_item['fields']['last_name'] = politician['last_name']
            fixture_item['fields']['picture'] = politician['avatar']
            fixture_item['fields']['twitter'] = twitter_handle
            fixture_item['fields']['organization'] = [politician['party']['id']]

            if not politician['party']['id'] in [x['pk'] for x in org_fixture]:
                fixture1_item = copy.deepcopy(org_fixture_template)
                fixture1_item['pk'] = politician['party']['id']
                fixture1_item['fields']['name'] = politician['party']['name']
                org_fixture.append(fixture1_item)

            # if group:
            #     i = filter_groups.index(group) + 1000
            #     if i not in [x['pk'] for x in org_fixture]:
            #         fixture2_item = copy.deepcopy(org_fixture_template)
            #         fixture2_item['pk'] = i
            #         fixture2_item['fields']['name'] = group
            #
            #         fixture_item['fields']['organization'].append(i)
            #         org_fixture.append(fixture2_item)

            rep_fixture.append(fixture_item)

save('fixtures.json', org_fixture + rep_fixture)

print('Done')

# [{"model": "backend.representative", "pk": 1, "fields": {"picture": "", "gender": 0,
# "birth_date": "2018-09-18", "user": null, "first_name": "Jurrian", "last_name": "Tromp",
# "email": "jurriantromp@gmail.com", "twitter": "jurrian", "organization": []}}]

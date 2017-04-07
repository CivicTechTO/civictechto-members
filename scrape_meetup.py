import csv
import io
import meetup.api
import os
import requests
import sys

# Meetup attendance counts are no longer available via API
# See: https://groups.google.com/forum/#!topic/meetup-api/S2hTGDLDv4Y

ETHERCALC_SHEET_ID = os.environ.get('ETHERCALC_SHEET_ID', 'civictechto-members')
OUTPUT_TYPE = os.environ.get('CTTO_OUTPUT_TYPE', 'file')
MEETUP_API_KEY = os.environ['MEETUP_API_KEY']

client = meetup.api.Client(MEETUP_API_KEY)

members = []
offset = 0
count = 0
while True:
    response = client.GetMembers({'group_urlname': 'Civic-Tech-Toronto', 'offset': offset})
    members.extend(response.results)
    count += response.meta['count']
    total = response.meta['total_count']
    print('Members fetched: {}/{}'.format(count, total))

    if not response.meta['next']:
        break
    offset += 1

# Zero out attendance for each member
for m in members:
    m.update({'attendance_count': 0})

count = 0
response = client.GetEvents({'group_urlname': 'Civic-Tech-Toronto', 'status': 'past,upcoming'})
events = response.results
count += response.meta['count']
total = response.meta['total_count']
print('Events fetched: {}/{}'.format(count, total))
event_ids = [e['id'] for e in events]

rsvps = []
for i, eid in enumerate(event_ids):
    response = client.GetRsvps({'event_id': eid})
    rsvps.extend(response.results)
    print('Fetched {} RSVPs from event {}/{}'.format(response.meta['count'], i+1, len(event_ids)))

for i, m in enumerate(members):
    for r in rsvps:
        if r['member']['member_id'] == m['id'] and r['response'] == 'yes':
            m['attendance_count'] += 1
    n = i + 1
    if n % 100 == 0:
        print('Processed RSVPs for member {}/{}'.format(n, len(members)))

output = {}
output['file'] = open('members.csv', 'w') # send to file
output['screen'] = sys.stdout # send to screen
output['ethercalc'] = io.StringIO() # send to ethercalc

# Set output type here (hardcoded :/ )
writer = csv.writer(output[OUTPUT_TYPE])

writer.writerow(['name', 'meetup_member_id', 'meetup_attendance_count', 'twitter_url', 'facebook_url'])
for m in members:
    services = m['other_services']
    process_twitter = lambda handle: 'https://twitter.com/{}'.format(handle.replace('@', ''))
    twitter = process_twitter(services['twitter']['identifier']) if ('twitter' in services) else None
    facebook = services['facebook']['identifier'] if ('facebook' in services) else None
    writer.writerow([m['name'], m['id'], m['attendance_count'], twitter, facebook])

if OUTPUT_TYPE == 'ethercalc':
    content = output[OUTPUT_TYPE].getvalue()
    requests.put('https://ethercalc.org/_/{}'.format(ETHERCALC_SHEET_ID), content.encode('utf-8'))

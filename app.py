import csv
import meetup.api
import os
import requests
import string
import sys

# Meetup attendance counts are no longer available via API
# See: https://groups.google.com/forum/#!topic/meetup-api/S2hTGDLDv4Y

MEETUP_API_KEY = os.environ['MEETUP_API_KEY']
client = meetup.api.Client(MEETUP_API_KEY)

base_url = 'https://api.meetup.com'
data = {}
data['urlname'] = 'Civic-Tech-Toronto'
data['event_id'] = 238574683

members_url = '/${urlname}/members'
events_url  = '/${urlname}/events'
rsvps_url   = '/${urlname}/events/${event_id}/rsvps'

def build_url(endpoint, query_params={}):
    url = base_url + string.Template(endpoint).substitute(**data)
    url += '?key={}'.format(MEETUP_API_KEY)
    url += '&page=200'
    for k, v in query_params.items():
        url += '&{}={}'.format(k, v)
    return url

members = []
offset = 0
while True:
    response = client.GetMembers({'group_urlname': 'Civic-Tech-Toronto', 'offset': offset})
    members.extend(response.results)
    if not response.meta['next']:
        break
    per_page = response.meta['count']
    total = response.meta['total_count']
    print('Members fetched: {}/{}'.format(per_page*offset, total))
    offset += 1

# Zero out attendance for each member
for m in members:
    m['attendance_count'] = 0

events = requests.get(build_url(events_url, {'status': 'past,upcoming'}))
print(events.headers)
events = events.json()
event_ids = [e['id'] for e in events]

for eid in event_ids:
    data['event_id'] = eid
    event_rsvps = requests.get(build_url(rsvps_url)).json()
    attending_ids = [rsvp['member']['id'] for rsvp in event_rsvps]
    for m in members:
        if m['id'] in attending_ids:
            m['attendance_count'] += 1

writer = csv.writer(sys.stdout)
writer.writerow(['name', 'meetup_member_id', 'meetup_attendance_count'])
for m in members:
    writer.writerow([m['name'], m['id'], m['attendance_count']])

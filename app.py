import csv
import os
import requests
import string
import sys

# Meetup attendance counts are no longer available via API
# See: https://groups.google.com/forum/#!topic/meetup-api/S2hTGDLDv4Y

MEETUP_API_KEY = os.environ['MEETUP_API_KEY']

base_url = 'https://api.meetup.com'
data = {}
data['urlname'] = 'Civic-Tech-Toronto'
data['event_id'] = 238574683

members_url = '/${urlname}/members'
events_url  = '/${urlname}/events'
rsvps_url   = '/${urlname}/events/${event_id}/rsvps'

def build_url(endpoint):
    url = base_url + string.Template(endpoint).substitute(**data)
    url += '?key={}'.format(MEETUP_API_KEY)
    return url

meetup_members = requests.get(build_url(members_url)).json()

# Zero out attendance for each member
for m in meetup_members:
    m['attendance_count'] = 0

# Start with a single event, but we'll do this for all later
one_event = requests.get(build_url(rsvps_url)).json()
attending_ids = [rsvp['member']['id'] for rsvp in one_event]
for m in meetup_members:
    if m['id'] in attending_ids:
        m['attendance_count'] += 1

writer = csv.writer(sys.stdout)
for m in meetup_members:
    writer.writerow(['name', 'meetup_member_id', 'meetup_attendance_count'])
    writer.writerow([m['name'], m['id'], m['attendance_count']])

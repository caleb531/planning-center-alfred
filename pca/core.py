#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import base64
import json
import os
import urllib2
from gzip import GzipFile
from StringIO import StringIO

# Unique identifier for the workflow
WORKFLOW_UID = 'com.calebevans.planningcenteralfred'


# The base URL for the Planning Center API
API_BASE_URL = 'https://api.planningcenteronline.com'
# The User Agent used for all HTTP requests to the Planning Center APIs
REQUEST_USER_AGENT = 'Planning Center for Alfred (Mozilla/5.0)'
# The number of seconds to wait before timing out an HTTP request to the API
REQUEST_CONNECTION_TIMEOUT = 5


# Build the object for a single result list feedback item
def get_result_list_feedback_item(result):

    item = result.copy()

    item['text'] = result.get('text', {}).copy()
    # Text copied to clipboard when cmd-c is invoked for this result
    item['text']['copy'] = item['text'].get('copy', result['title'])
    # Text shown when invoking Large Type for this result
    item['text']['largetype'] = item['text'].get('largetype', result['title'])

    # Use different args when different modifiers are pressed
    item['mods'] = result.get('mods', {}).copy()
    item['mods']['ctrl'] = item['mods'].get('ctrl', {'arg': result['title']})

    # Icon shown next to result text
    item['icon'] = {
        'path': 'icon.png'
    }
    return item


# Constructs an Alfred JSON string from the given result list
def get_result_list_feedback_str(results):

    return json.dumps({
        'items': [get_result_list_feedback_item(result) for result in results]
    })


# Return the value used for the Authorization header on every API request
def get_authorization_header():

    return '{auth_type} {auth_credentials}'.format(
        auth_type='Basic',
        auth_credentials=base64.standard_b64encode('{id}:{secret}'.format(
            id=os.environ.get('app_id').strip(),
            secret=os.environ.get('app_secret').strip())))


# Fetch data from the Planning Center API
def fetch_data(endpoint_path):

    request_url = API_BASE_URL + endpoint_path
    request = urllib2.Request(request_url, headers={
        'User-Agent': REQUEST_USER_AGENT,
        'Accept-Encoding': 'gzip, deflate',
        'Authorization': get_authorization_header()
    })
    response = urllib2.urlopen(request, timeout=REQUEST_CONNECTION_TIMEOUT)
    url_content = response.read()

    # Decompress response body if gzipped
    if response.info().get('Content-Encoding') == 'gzip':
        str_buf = StringIO(url_content)
        with GzipFile(fileobj=str_buf, mode='rb') as gzip_file:
            url_content = gzip_file.read()

    return json.loads(url_content.decode('utf-8'))

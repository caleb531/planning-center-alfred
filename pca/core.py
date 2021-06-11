#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import json

# Unique identifier for the workflow
WORKFLOW_UID = 'com.calebevans.planningcenteralfred'


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

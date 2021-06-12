#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import pca.core as core


# Convert the given dictionary representation of a Planning Center person to a
# Alfred feedback result dictionary
def get_result_from_person(person):

    return {
        'title': person['name']
    }


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    people = core.fetch_data('/people/v2/people')
    return [get_result_from_person(person['attributes'])
            for person in people['data']]


def main(query_str):

    results = get_result_list(query_str)
    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No people matching \'{}\''.format(query_str),
            'valid': False
        })

    print(core.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))

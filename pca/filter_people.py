#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import pca.core as core


# Convert the given dictionary representation of a Planning Center person to a
# Alfred feedback result dictionary
def get_result_from_person(person):

    return {
        'title': person['attributes']['name'],
        'subtitle': 'View in Planning Center',
        'arg': '{base_url}/AC{person_id}'.format(
            base_url='https://people.planningcenteronline.com/people',
            person_id=person['id'])
    }


# Calculate a numeric score used for sorting
def get_person_sort_order(person, query_str):

    attrs = person['attributes']
    score = 0
    for keyword in query_str.split(' '):
        score += (
            (int(keyword in attrs['name']) * -10) +
            (int(attrs['first_name'].lower().startswith(keyword)) * -100) +
            (int(attrs['last_name'].lower().startswith(keyword)) * -100)
        )
    return score


# Return True if the given Person dictionary matches the given query string
def person_matches_query_str(person, query_str):

    return all(keyword in person['attributes']['name'].lower()
               for keyword in query_str.split(' '))


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    query_str = query_str.lower()

    people = core.fetch_data('/people/v2/people')
    people = sorted(people,
                    key=lambda person: get_person_sort_order(person, query_str))
    results = [get_result_from_person(person) for person in people
               if person_matches_query_str(person, query_str)]

    return results


def main(query_str):

    try:
        results = get_result_list(query_str)
    except Exception as error:
        results = []
        if hasattr(error, 'code') and error.code == 401:
            results.append({
                'title': 'Invalid API Credentals',
                'subtitle': 'The app_id and app_secret variables are missing or incorrect',
                'valid': False
            })
        else:
            print(error, file=sys.stderr)
            results.append({
                'title': 'Script Error',
                'subtitle': str(error),
                'valid': False
            })

    if not results:
        results.append({
            'title': 'No Results',
            'subtitle': 'No people matching \'{}\''.format(query_str),
            'valid': False
        })

    print(core.get_result_list_feedback_str(results))


if __name__ == '__main__':
    main(sys.argv[1].decode('utf-8'))

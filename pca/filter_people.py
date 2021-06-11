#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import sys

import pca.core as core


# Retrieves search resylts matching the given query
def get_result_list(query_str):

    return [
        {
            'title': 'Caleb Evans',
            'subtitle': '(123) 456-7890'
        }
    ]


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

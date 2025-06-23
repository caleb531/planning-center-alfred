#!/usr/bin/env python3
# coding=utf-8

import sys

import pca.core as core


# Convert the given dictionary representation of a Planning Center person to a
# Alfred feedback result dictionary
def get_result_from_person(person):
    return {
        "title": person["attributes"]["name"],
        "subtitle": "View in Planning Center",
        "arg": person["id"],
        "variables": {
            "person_id": person["id"],
            "person_name": person["attributes"]["name"],
            "person_url": "{base_url}/AC{person_id}".format(
                base_url="https://people.planningcenteronline.com/people",
                person_id=person["id"],
            ),
        },
    }


# Retrieves search resylts matching the given query
def get_result_list(query_str):
    query_str = query_str.lower()

    people = core.fetch_data(
        "/people/v2/people",
        params={
            "where[search_name_or_email_or_phone_number]": query_str,
            "where[status]": "active",
        },
    )
    results = [get_result_from_person(person) for person in people]

    return results


def main(query_str):
    results = []
    with core.handle_workflow_errors(results):
        results = get_result_list(query_str)

    if not results:
        results.append(
            {
                "title": "No Results",
                "subtitle": "No people matching '{}'".format(query_str),
                "valid": False,
            }
        )

    print(core.get_result_list_feedback_str(results))


if __name__ == "__main__":
    main(sys.argv[1])

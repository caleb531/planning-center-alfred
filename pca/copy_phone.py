#!/usr/bin/env python3
# coding=utf-8

import json
import os

import pca.core as core


# Return the textual phone number for the person with the given ID
def get_person_phone_number(person_id):
    person_phones = core.fetch_data(
        "/people/v2/people/{id}/phone_numbers".format(id=person_id)
    )

    for phone in person_phones:
        if phone["attributes"]["primary"]:
            return phone["attributes"]["number"]

    # If there is no primary phone, but there is at least one phone number on
    # file, then fall back to the first one
    if person_phones:
        return person_phones[0]["attributes"]["number"]

    # Otherwise, indicate that there's no phone number on file for this person
    return "N/A"


def main(variables):
    person_phone_number = get_person_phone_number(variables["person_id"])
    print(
        json.dumps(
            {
                "alfredworkflow": {
                    "arg": variables["person_id"],
                    "variables": {"person_phone_number": person_phone_number},
                }
            }
        )
    )


if __name__ == "__main__":
    main({"person_id": int(os.environ["person_id"])})

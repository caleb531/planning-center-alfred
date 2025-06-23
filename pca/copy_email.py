#!/usr/bin/env python3
# coding=utf-8

import json
import os

import pca.core as core


# Return the textual email address for the person with the given ID
def get_person_email_addr(person_id):
    person_emails = core.fetch_data(
        "/people/v2/people/{id}/emails".format(id=person_id)
    )

    for email in person_emails:
        if email["attributes"]["primary"]:
            return email["attributes"]["address"]

    # If there is no primary email, but there is at least one email address on
    # file, then fall back to the first one
    if person_emails:
        return person_emails[0]["attributes"]["address"]

    # Otherwise, indicate that there's no email number on file for this person
    return "N/A"


def main(variables):
    person_email_addr = get_person_email_addr(variables["person_id"])
    print(
        json.dumps(
            {
                "alfredworkflow": {
                    "arg": variables["person_id"],
                    "variables": {"person_email_addr": person_email_addr},
                }
            }
        )
    )


if __name__ == "__main__":
    main({"person_id": int(os.environ["person_id"])})

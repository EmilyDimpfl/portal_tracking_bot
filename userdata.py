#!/usr/bin/env python3
"""
module for handling portal hunt data
"""

import json


class PointsData:
    """
    class for managing the portal hunt points data structure, serializing, and deserializing
    """
    data = {}
    filepath = None

    def __init__(self, filepath: str = None):
        """
        reads in data to set up our data structure
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as file_desc:
                raw = file_desc.read()
                data = json.loads(raw)

                # validation:
                # (todo)

                self.data = data
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

        self.filepath = filepath

    def modify_points(self, user: str, delta: int):
        """
        adds or removes points from a user
        """

        points = self.get_points(user)
        self.data[user] = points + delta

        self.save_data(self.filepath)

    def get_points(self, user: str):
        """
        returns the number of points a user has
        """
        try:
            if self.data[user] is not None:
                return self.data[user]
        except KeyError:
            self.data[user] = 0

        return 0

    def save_data(self, filepath: str):
        """
        dumps our data structure to disk
        """

        with open(filepath, 'w', encoding='utf-8') as file_desc:
            output = json.dumps(self.data)

            file_desc.write(output)

    def pretty_print(self):
        """
        pretty prints all of our data
        """
        retstr = ""
        for key, value in self.data.items():
            retstr += str(key) + ": " + str(value) + "\n"

        return retstr

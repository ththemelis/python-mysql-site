"""Η σύνδεση με τη βάση του project. Είναι το db.py του Μαθήματος 17, με έναν μόνο λογαριασμό.

Όλα τα προγράμματα ζητούν τη σύνδεση από εδώ. Η σύνδεση δουλεύει και με το with.
"""

import mysql.connector

import config


def connect():
    """Ανοίγει μια σύνδεση με τη βάση του project και την επιστρέφει."""
    return mysql.connector.connect(
        host=config.HOST,
        user=config.APP_USER,
        password=config.APP_PASSWORD,
        database=config.DATABASE,
    )

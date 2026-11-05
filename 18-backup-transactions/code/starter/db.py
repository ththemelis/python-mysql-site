"""Η σύνδεση με τη βάση. Είναι το db.py του Μαθήματος 17, ΑΜΕΤΑΒΛΗΤΟ.

Όλα τα άλλα προγράμματα ζητούν τη σύνδεση από εδώ. Χωρίς ορίσματα συνδέεσαι ως ο λογαριασμός της εφαρμογής· ένα πρόγραμμα που χρειάζεται άλλον
λογαριασμό τον δίνει ως ορίσματα. Η σύνδεση δουλεύει και με το with.
"""

import mysql.connector

import config


def connect(user=config.APP_USER, password=config.APP_PASSWORD):
    """Ανοίγει μια σύνδεση με τη βάση και την επιστρέφει. Αν δεν πεις ποιος λογαριασμός, συνδέεται ως ο λογαριασμός της εφαρμογής."""
    return mysql.connector.connect(
        host=config.HOST,
        user=user,
        password=password,
        database=config.DATABASE,
    )

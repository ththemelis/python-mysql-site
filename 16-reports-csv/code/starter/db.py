"""Η σύνδεση με τη βάση.

Όλα τα άλλα modules ζητούν τη σύνδεση από εδώ: μόνο εδώ ξέρουμε πώς ανοίγει. Η σύνδεση που επιστρέφεται
δουλεύει και με το with, που την κλείνει αυτόματα στο τέλος.
"""

import mysql.connector

import config


def connect():
    """Ανοίγει μια σύνδεση με τη βάση, με τις ρυθμίσεις του config, και την επιστρέφει."""
    return mysql.connector.connect(
        host=config.HOST,
        user=config.USER,
        password=config.PASSWORD,
        database=config.DATABASE,
    )

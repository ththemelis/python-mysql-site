"""Έλεγχος του Σταδίου 2: δοκιμάζει το queries.py. Δεν χρειάζεται να το συμπληρώσεις."""

from datetime import date
from decimal import Decimal

import mysql.connector

import db
import queries

with db.connect() as connection:
    games = queries.get_games(connection)
    print("Παιχνίδια:", len(games), "| το πρώτο:", games[0]["title"], "-", games[0]["genre_name"])

    print("Αναζήτηση «kart»:")
    for game in queries.search_games(connection, "kart"):
        print("  ", game["id"], game["title"])

    print("Είδη:", len(queries.get_genres(connection)), "| Πλατφόρμες:", len(queries.get_platforms(connection)))
    print("Τίτλος του 9:", queries.find_title(connection, 9), "| του 999:", queries.find_title(connection, 999))

    # Προσθήκη και διαγραφή ενός δοκιμαστικού παιχνιδιού, με δύο πλατφόρμες
    new_id = queries.add_game(connection, "Δοκιμή", 3, 2026, Decimal("1.99"), None, date.today(), [1, 3])
    print("Προστέθηκε με id", new_id, "-", queries.get_platforms_of_game(connection, new_id)["platforms"])
    print("Διαγραφή:", queries.delete_game(connection, new_id), "| ξανά:", queries.delete_game(connection, new_id))

    # Το σφάλμα ξαναπετιέται: ο τίτλος «Mini Golf» υπάρχει ήδη (UNIQUE)
    try:
        queries.add_game(connection, "Mini Golf", 3, 2026, Decimal("1.99"), None, date.today(), [])
    except mysql.connector.IntegrityError as error:
        print("Διπλός τίτλος → IntegrityError", error.errno)

    # Ένα παιχνίδι με κριτικές δεν σβήνεται, και οι πλατφόρμες του μένουν
    try:
        queries.delete_game(connection, 11)
    except mysql.connector.IntegrityError as error:
        print("Διαγραφή του 11 → IntegrityError", error.errno)
    print("Πλατφόρμες του 11:", queries.get_platforms_of_game(connection, 11)["platforms"])
    print("Κριτικές του 9:", len(queries.get_reviews(connection, 9)), "| του 4:", queries.get_reviews(connection, 4)[0]["stars"])

"""Έλεγχος του Σταδίου 2: δοκιμάζει το reports.py. Δεν χρειάζεται να το συμπληρώσεις."""

import db
import reports

with db.connect() as connection:
    rows = reports.games_per_genre(connection)
    print("Είδη:", len(rows), "| πρώτο:", rows[0]["genre"], rows[0]["games_n"], rows[0]["average"],
          "| τελευταίο:", rows[-1]["genre"], rows[-1]["games_n"], rows[-1]["average"])

    rows = reports.ratings_per_game(connection, 1)
    print("Βαθμολογίες (όλες):", len(rows), "| καλύτερο:", rows[0]["title"], rows[0]["average_stars"])

    rows = reports.ratings_per_game(connection, 2)
    print("Βαθμολογίες (τουλάχιστον 2 κριτικές):", len(rows), "| καλύτερο:", rows[0]["title"], rows[0]["average_stars"])

    rows = reports.games_per_platform(connection)
    print("Πλατφόρμες:", len(rows), "| πρώτη:", rows[0]["platform"], rows[0]["games_n"],
          "| τελευταία:", rows[-1]["platform"], rows[-1]["games_n"], rows[-1]["average"])

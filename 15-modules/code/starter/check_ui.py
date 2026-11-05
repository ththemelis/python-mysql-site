"""Έλεγχος του Σταδίου 3: δοκιμάζει το ui.py με ΨΕΥΤΙΚΑ δεδομένα, χωρίς βάση. Δεν χρειάζεται να το συμπληρώσεις."""

from datetime import date
from decimal import Decimal

import ui

fake_games = [
    {"id": 1, "title": "Δοκιμαστικό παιχνίδι", "genre_name": "Παζλ", "release_year": 2026, "price": Decimal("3.5"),
     "added_on": date(2026, 9, 15)},
]
ui.print_games(fake_games)
print()
ui.print_reviews([{"title": "Δοκιμαστικό παιχνίδι", "stars": 4, "comment": None}])
ui.print_platforms({"title": "Δοκιμαστικό παιχνίδι", "platforms": None})

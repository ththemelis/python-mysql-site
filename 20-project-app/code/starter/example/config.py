"""Οι ρυθμίσεις του παραδείγματος «pizzeria» (Μάθημα 20): μία βάση, ένας λογαριασμός.

Ό,τι αλλάζει από υπολογιστή σε υπολογιστή γράφεται εδώ και ΜΟΝΟ εδώ. Ο κωδικός δεν γράφεται εδώ: έρχεται από το config_local.py, που δεν ανεβαίνει στο git.
"""

import os

HOST = os.environ.get("DB_HOST", "localhost")
DATABASE = os.environ.get("DB_NAME", "pizzeria")
APP_USER = "pizzeria_app"

try:
    from config_local import APP_PASSWORD
except ImportError:
    APP_PASSWORD = ""

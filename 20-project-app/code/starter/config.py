"""Οι ρυθμίσεις του project σου (Μάθημα 20). Είναι το config.py του Μαθήματος 19: αν δουλεύεις στον φάκελο του Μαθήματος 19, το έχεις ήδη.

ΑΛΛΑΞΕ το "my_project" στο όνομα της ΔΙΚΗΣ ΣΟΥ βάσης (το ίδιο που έβαλες στο 01-schema.sql). Ο κωδικός δεν γράφεται εδώ: έρχεται από το config_local.py,
που δεν ανεβαίνει στο git.
"""

import os

HOST = os.environ.get("DB_HOST", "localhost")
DATABASE = os.environ.get("DB_NAME", "my_project")
APP_USER = "project_app"

try:
    from config_local import APP_PASSWORD
except ImportError:
    APP_PASSWORD = ""

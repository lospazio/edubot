#!/usr/bin/env python
import os
import sys

def main():
    """Esegui i comandi Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edubot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django non è installato. Assicurati di avere il virtualenv attivo "
            "e Django installato."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

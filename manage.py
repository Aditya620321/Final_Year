#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8000/accounts/register/")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reommend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Start a timer to open the browser shortly after the server starts
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        threading.Timer(1.5, open_browser).start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

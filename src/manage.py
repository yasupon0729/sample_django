#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from vegeket.logger import get_logger

logger = get_logger('manage.py')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegeket.settings')
    try:
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    logger.info("起動しました")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

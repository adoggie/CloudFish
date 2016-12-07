#!/usr/bin/env python


import imp,os
PATH = os.path.dirname(os.path.abspath(__file__))
imp.load_source('init',PATH +'/../../init_script.py')


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lemon.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

#!/usr/bin/env python

"""A wrapper for Django's manage.py that sets up App Engine's paths."""

import os
import sys


gae = '/usr/local/google_appengine'


def main():
    sys.path.insert(0, gae)
    import dev_appserver
    dev_appserver.fix_sys_path()
    # Fix Django version (1.4 -> 1.5).
    for i in xrange(len(sys.path)):
        if sys.path[i].endswith('django-1.4'):
            sys.path[i] = '%s5' % sys.path[i][:-1]
            break

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rerss.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

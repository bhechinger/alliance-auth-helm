#!/usr/bin/env python
import os
import sys
import redis

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myauth.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    REDIS_URL = F"redis://{os.environ.get('AA_REDIS_USERNAME', 'default')}:{os.environ.get('AA_REDIS_PASSWORD', '')}@{os.environ.get('AA_REDIS', 'redis:6379')}/{os.environ.get('AA_REDIS_DB', '0')}"
    r = redis.from_url(REDIS_URL)
    if not r.ping():
        print("unable to ping redis")
        sys.exit(-1)

    {{- $commands := list }}
    {{- with .Values.services }}
    {{- if or .memberaudit.enabled .killtracker.enabled .structuretimers.enabled }}
    {{- $commands = append $commands "eveuniverse_load_data map --no-input"}}
    {{- end }}
    {{- if .marketmanager.enabled }}
    {{- $commands = append $commands "eveuniverse_load_data ships --no-input"}}
    {{- end }}
    {{- if .packagemonitor.enabled }}
    {{- $commands = append $commands "package_monitor_refresh"}}
    {{- end }}
    {{- end }}

    commandList = {{ toJson $commands }}
    if len(sys.argv) > 1 and sys.argv[1] == "reset_locks":
        for command in commandList:
            r.delete("data_load." + command)
        sys.exit(0)

    for command in commandList:
        check = r.get("data_load." + command)
        if check != b'skip':
            r.set("data_load." + command, 'skip')
            print("Running %s" % command)
            execute_from_command_line(sys.argv + command.split())
        else:
            print("Skipping %s" % command)


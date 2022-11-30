{{/* If aa-rss-to-discord is enabled we need aadiscordbot */}}
{{- if and (eq .Values.services.aa_rss_to_discord.enabled true) (eq .Values.services.discordbot.enabled false) }}
    {{- fail "discordbot needs to be enabled before you can enable aa_rss_to_discord!" }}
{{- end }}

{{/* If mailrelay is enabled we need discordproxy, memberaudit and the discord service */}}
{{- if .Values.services.mailrelay.enabled }}
    {{- if or (eq .Values.services.discordproxy.enabled false) (eq .Values.services.memberaudit.enabled false) (eq .Values.services.discord.enabled false) }}
        {{- fail "discord, memberaudit and discordproxy need to be enabled before you can enable mailrelay!" }}
    {{- end }}
{{- end }}

{{/* If any of these services are enabled we need to enable eveuniverse */}}
{{- if and (eq .Values.services.structuretimers.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable structuretimers" }}
{{- end }}
{{- if and (eq .Values.services.structures.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable structures" }}
{{- end }}
{{- if and (eq .Values.services.memberaudit.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable memberaudit" }}
{{- end }}
{{- if and (eq .Values.services.moonmining.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable moonmining" }}
{{- end }}
{{- if and (eq .Values.services.killtracker.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable killtracker" }}
{{- end }}
{{- if and (eq .Values.services.marketmanager.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable marketmanager" }}
{{- end }}
{{- if and (eq .Values.services.blueprints.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable blueprints" }}
{{- end }}
{{- if and (eq .Values.services.buybackprogram.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable buybackprogram" }}
{{- end }}
{{- if and (eq .Values.services.standingsrequests.enabled true) (eq .Values.services.eveuniverse.enabled false) }}
    {{- fail "eveuniverse needs to be enabled before you can enable standingsrequests" }}
{{- end }}

# Every setting in base.py can be overloaded by redefining it here.
from .base import *
import sys

SECRET_KEY = os.environ.get("AA_SECRET_KEY")
SITE_NAME = os.environ.get("AA_SITENAME")
SITE_URL = (
    f"{os.environ.get('PROTOCOL')}"
    f"{os.environ.get('AUTH_SUBDOMAIN')}."
    f"{os.environ.get('DOMAIN')}"
)
CSRF_TRUSTED_ORIGINS = [SITE_URL]

DEBUG = os.environ.get("AA_DEBUG", "").lower() == "true"
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ.get("AA_DB_NAME"),
    'USER': os.environ.get("AA_DB_USER"),
    'PASSWORD': os.environ.get("AA_DB_PASSWORD"),
    'HOST': os.environ.get("AA_DB_HOST"),
    'PORT': os.environ.get("AA_DB_PORT", "3306"),
    'OPTIONS': {"charset": "utf8mb4"},
}

# Register an application at https://developers.eveonline.com for Authentication
# & API Access and fill out these settings. Be sure to set the callback URL
# to https://example.com/sso/callback substituting your domain for example.com
# Logging in to auth requires the publicData scope (can be overridden through the
# LOGIN_TOKEN_SCOPES setting). Other apps may require more (see their docs).

ESI_SSO_CLIENT_ID = os.environ.get("ESI_SSO_CLIENT_ID")
ESI_SSO_CLIENT_SECRET = os.environ.get("ESI_SSO_CLIENT_SECRET")
ESI_SSO_CALLBACK_URL = (f"{os.environ.get('PROTOCOL')}"
                        f"{os.environ.get('AUTH_SUBDOMAIN')}."
                        f"{os.environ.get('DOMAIN')}/sso/callback")
ESI_USER_CONTACT_EMAIL = os.environ.get(
    "ESI_USER_CONTACT_EMAIL")  # A server maintainer that CCP can contact in case of issues.

# By default emails are validated before new users can log in.
# It's recommended to use a free service like SparkPost or Elastic Email to send email.
# https://www.sparkpost.com/docs/integrations/django/
# https://elasticemail.com/resources/settings/smtp-api/
# Set the default from email to something like 'noreply@example.com'
# Email validation can be turned off by uncommenting the line below. This can break some services.
REGISTRATION_VERIFY_EMAIL = False
EMAIL_HOST = os.environ.get("AA_EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("AA_EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("AA_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("AA_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("AA_EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get("AA_DEFAULT_FROM_EMAIL", "")

ROOT_URLCONF = 'myauth.urls'
WSGI_APPLICATION = 'myauth.wsgi.application'
STATIC_ROOT = "/var/www/myauth/static/"
BROKER_URL = F"redis://{os.environ.get('AA_REDIS_USERNAME', 'default')}:{os.environ.get('AA_REDIS_PASSWORD', '')}@{os.environ.get('AA_REDIS', 'redis:6379')}/{os.environ.get('AA_REDIS_DB', '0')}"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('AA_REDIS', 'redis:6379')}/{os.environ.get('AA_REDIS_DB', '0')}",
        "OPTIONS": {
            "PASSWORD": f"{os.environ.get('AA_REDIS_PASSWORD','')}"
        }
    }
}

# Add any additional apps to this list.
INSTALLED_APPS += [
{{- with .Values.services }}
{{- if .autogroups.enabled }}
    'allianceauth.eveonline.autogroups',
{{- end }}
{{- if .discord.enabled }}
    'allianceauth.services.modules.discord',
{{- end }}
{{- if .discordbot.enabled }}
    'aadiscordbot',
{{- end }}
{{- if .eveuniverse.enabled }}
    'eveuniverse',
{{- end }}
{{- if .structures.enabled }}
    'structures',
{{- end }}
{{- if .structuretimers.enabled }}
    'structuretimers',
{{- end }}
{{- if .fittings.enabled }}
    'fittings',
{{- end }}
{{- if .mailrelay.enabled }}
    'mailrelay',
{{- end }}
{{- if .killtracker.enabled }}
    'killtracker',
{{- end }}
{{- if .moonmining.enabled }}
    'moonmining',
{{- end }}
{{- if .memberaudit.enabled }}
    'memberaudit',
{{- end }}
{{- if .aa_rss_to_discord.enabled }}
    'aa_rss_to_discord',
{{- end }}
{{- if .blueprints.enabled }}
    'blueprints',
{{- end }}
{{- if .marketmanager.enabled }}
    'marketmanager',
{{- end }}
{{- if .securegroups.enabled }}
    'securegroups',
{{- end }}
{{- if .buybackprogram.enabled }}
    'buybackprogram',
{{- end }}
{{- if .standingsrequests.enabled }}
    'standingsrequests',
{{- end }}
{{- if .taskmonitor.enabled }}
    'taskmonitor',
{{- end }}
{{- if .celeryanalytics.enabled }}
    'celeryanalytics',
{{- end }}
{{- if .packagemonitor.enabled }}
    'package_monitor',
{{- end }}
{{- if .hrapplications.enabled }}
    'allianceauth.hrapplications',
{{- end }}
{{- if .optimer.enabled }}
    'allianceauth.optimer',
{{- end }}
{{- if .corputils.enabled }}
    'allianceauth.corputils',
{{- end }}
{{- if .fleetpings.enabled }}
    'fleetpings',
{{- end }}
{{- end }}
]

#######################################
# Add any custom settings below here. #
#######################################

LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
              'verbose': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
              },
              'simple': {
                'format': '%(levelname)s %(message)s'
              },
            },
            'handlers': {
              'console': {
                'level': {{ .Values.services.discordbot.logLevel | quote }},  # edit this line to change logging level to console
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
                'formatter': 'verbose',
              },
              'notifications': {  # creates notifications for users with logging_notifications permission
                'level': 'ERROR',  # edit this line to change logging level to notifications
                'class': 'allianceauth.notifications.handlers.NotificationHandler',
                'formatter': 'verbose',
              },
            },
            'loggers': {
              'allianceauth': {
                'handlers': ['console', 'notifications'],
                'level': 'INFO',
              },
              'extensions': {
                'handlers': ['console'],
                'level': 'INFO',
              },
              'django': {
                'handlers': ['console'],
                'level': 'ERROR',
              },
              'esi': {
                'handlers': ['console'],
                'level': 'INFO',
              },
              'groupbot': {
                'handlers': ['console'],
                'level': 'DEBUG',
              },
              'aadiscordbot': {
                'handlers': ['console'],
                'level': 'DEBUG',
              },
              'corptools': {
                'handlers': ['console'],
                'level': 'DEBUG',
              },
              'pinger': {
                'handlers': ['console'],
                'level': 'DEBUG',
              },
              'moons': {
                'handlers': ['console'],
                'level': 'DEBUG',
              },
            }
          }

{{- if .Values.services.discord.enabled }}
# Discord Configuration
# Be sure to set the callback URLto https://example.com/discord/callback/
# substituting your domain for example.com in Discord's developer portal
# (Be sure to add the trailing slash)
DISCORD_GUILD_ID = os.environ.get("DISCORD_GUILD_ID", "")
DISCORD_CALLBACK_URL = f"{SITE_URL}/discord/callback/"
DISCORD_APP_ID = os.environ.get("DISCORD_APP_ID", "")
DISCORD_APP_SECRET = os.environ.get("DISCORD_APP_SECRET", "")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
DISCORD_SYNC_NAMES = os.environ.get("DISCORD_SYNC_NAMES", "").lower() == "true"

CELERYBEAT_SCHEDULE['discord.update_all_usernames'] = {
    'task': 'discord.update_all_usernames',
    'schedule': crontab(minute=0, hour='*/12'),
}
{{- end }}

{{- if .Values.services.discordbot.enabled }}
## Settings for Allianceauth-Discordbot
# Admin Commands
ADMIN_DISCORD_BOT_CHANNELS = [{{- include "print.list" .Values.services.discordbot.ADMIN_DISCORD_BOT_CHANNELS }}]
# Sov Commands
SOV_DISCORD_BOT_CHANNELS = [{{- include "print.list" .Values.services.discordbot.SOV_DISCORD_BOT_CHANNELS }}]
# Adm Commands
ADM_DISCORD_BOT_CHANNELS = [{{- include "print.list" .Values.services.discordbot.ADM_DISCORD_BOT_CHANNELS }}]

DISCORD_BOT_SOV_STRUCTURE_OWNER_IDS = [{{- include "print.list" .Values.services.discordbot.DISCORD_BOT_SOV_STRUCTURE_OWNER_IDS }}]
DISCORD_BOT_MEMBER_ALLIANCES = [{{- include "print.list" .Values.services.discordbot.DISCORD_BOT_MEMBER_ALLIANCES }}]

DISCORD_BOT_ADM_REGIONS = [{{- include "print.list" .Values.services.discordbot.DISCORD_BOT_ADM_REGIONS }}]
DISCORD_BOT_ADM_SYSTEMS = [{{- include "print.list" .Values.services.discordbot.DISCORD_BOT_ADM_SYSTEMS }}]
DISCORD_BOT_ADM_CONSTELLATIONS = [{{- include "print.list" .Values.services.discordbot.DISCORD_BOT_ADM_CONSTELLATIONS }}]

# configure the bots in-built cogs.
DISCORD_BOT_COGS = [
    {{- if .Values.services.discordbot.cogs.about }}
    "aadiscordbot.cogs.about", # about the bot
    {{- end }}
    {{- if .Values.services.discordbot.cogs.admin }}
    "aadiscordbot.cogs.admin", # Discord server admin helpers
    {{- end }}
    {{- if .Values.services.discordbot.cogs.members }}
    "aadiscordbot.cogs.members", # Member lookup commands
    {{- end }}
    {{- if .Values.services.discordbot.cogs.timers }}
    "aadiscordbot.cogs.timers", # timer board integration
    {{- end }}
    {{- if .Values.services.discordbot.cogs.auth }}
    "aadiscordbot.cogs.auth", # return auth url
    {{- end }}
    {{- if .Values.services.discordbot.cogs.sov }}
    "aadiscordbot.cogs.sov", # some sov helpers
    {{- end }}
    {{- if .Values.services.discordbot.cogs.time }}
    "aadiscordbot.cogs.time", # whats the time Mr Eve Server
    {{- end }}
    {{- if .Values.services.discordbot.cogs.eastereggs }}
    "aadiscordbot.cogs.eastereggs", # some "fun" commands from ariel...
    {{- end }}
    {{- if .Values.services.discordbot.cogs.remind }}
    "aadiscordbot.cogs.remind", # very Basic in memory reminder tool
    {{- end }}
    {{- if .Values.services.discordbot.cogs.reaction_roles }}
    "aadiscordbot.cogs.reaction_roles" # auth group integrated reaction roles
    {{- end }}
]

# configure the optional rate limited
# this is a bot_task function and how many / time period
# 100/s equates to 100 per second max
# 10/m equates to 10 per minute or 1 every 6 seconds max
# 60/h equates to 60 per hour or one per minute max
DISCORD_BOT_TASK_RATE_LIMITS = {
    "send_channel_message_by_discord_id": {{ .Values.services.discordbot.rate_limit.send_channel_message_by_discord_id | quote }},
    "send_direct_message_by_discord_id": {{ .Values.services.discordbot.rate_limit.send_direct_message_by_discord_id | quote }},
    "send_direct_message_by_user_id": {{ .Values.services.discordbot.rate_limit.send_direct_message_by_user_id | quote }}
}
{{- end }}

{{- if .Values.services.eveuniverse.enabled }}
# EVE Universe settings
EVEUNIVERSE_LOAD_ASTEROID_BELTS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_ASTEROID_BELTS | toString | title }}
EVEUNIVERSE_LOAD_DOGMAS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_DOGMAS | toString | title }}
EVEUNIVERSE_LOAD_GRAPHICS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_GRAPHICS | toString | title }}
EVEUNIVERSE_LOAD_MARKET_GROUPS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_MARKET_GROUPS | toString | title }}
EVEUNIVERSE_LOAD_MOONS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_MOONS | toString | title }}
EVEUNIVERSE_LOAD_PLANETS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_PLANETS | toString | title }}
EVEUNIVERSE_LOAD_STARGATES = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_STARGATES | toString | title }}
EVEUNIVERSE_LOAD_STARS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_STARS | toString | title }}
EVEUNIVERSE_LOAD_STATIONS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_STATIONS | toString | title }}
EVEUNIVERSE_LOAD_TYPE_MATERIALS = {{ .Values.services.eveuniverse.EVEUNIVERSE_LOAD_TYPE_MATERIALS | toString | title }}
EVEUNIVERSE_TASKS_TIME_LIMIT = {{ .Values.services.eveuniverse.EVEUNIVERSE_TASKS_TIME_LIMIT | toString | title }}
EVEUNIVERSE_USE_EVESKINSERVER = {{ .Values.services.eveuniverse.EVEUNIVERSE_USE_EVESKINSERVER | toString | title }}
{{- end }}

{{- if .Values.services.structures.enabled }}
STRUCTURES_ADD_TIMERS = {{ .Values.services.structures.STRUCTURES_ADD_TIMERS | toString | title }}
STRUCTURES_ADMIN_NOTIFICATIONS_ENABLED = {{ .Values.services.structures.STRUCTURES_ADMIN_NOTIFICATIONS_ENABLED | toString | title }}
STRUCTURES_DEFAULT_TAGS_FILTER_ENABLED = {{ .Values.services.structures.STRUCTURES_DEFAULT_TAGS_FILTER_ENABLED | toString | title }}
STRUCTURES_DEFAULT_LANGUAGE = {{ .Values.services.structures.STRUCTURES_DEFAULT_LANGUAGE | quote }}
STRUCTURES_DEFAULT_PAGE_LENGTH = {{ .Values.services.structures.STRUCTURES_DEFAULT_PAGE_LENGTH }}
STRUCTURES_ESI_DIRECTOR_ERROR_MAX_RETRIES = {{ .Values.services.structures.STRUCTURES_ESI_DIRECTOR_ERROR_MAX_RETRIES }}
STRUCTURES_FEATURE_CUSTOMS_OFFICES = {{ .Values.services.structures.STRUCTURES_FEATURE_CUSTOMS_OFFICES | toString | title }}
STRUCTURES_FEATURE_STARBASES = {{ .Values.services.structures.STRUCTURES_FEATURE_STARBASES | toString | title }}
STRUCTURES_FEATURE_REFUELED_NOTIFICATIONS = {{ .Values.services.structures.STRUCTURES_FEATURE_REFUELED_NOTIFICATIONS | toString | title }}
STRUCTURES_HOURS_UNTIL_STALE_NOTIFICATION = {{ .Values.services.structures.STRUCTURES_HOURS_UNTIL_STALE_NOTIFICATION }}
STRUCTURES_MOON_EXTRACTION_TIMERS_ENABLED = {{ .Values.services.structures.STRUCTURES_MOON_EXTRACTION_TIMERS_ENABLED | toString | title }}
STRUCTURES_NOTIFICATION_DISABLE_ESI_FUEL_ALERTS = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_DISABLE_ESI_FUEL_ALERTS | toString | title }}
STRUCTURES_NOTIFICATION_MAX_RETRIES = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_MAX_RETRIES }}
STRUCTURES_NOTIFICATION_SET_AVATAR = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_SET_AVATAR | toString | title }}
STRUCTURES_NOTIFICATION_SHOW_MOON_ORE = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_SHOW_MOON_ORE | toString | title }}
STRUCTURES_NOTIFICATION_SYNC_GRACE_MINUTES = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_SYNC_GRACE_MINUTES }}
STRUCTURES_NOTIFICATION_WAIT_SEC = {{ .Values.services.structures.STRUCTURES_NOTIFICATION_WAIT_SEC }}
STRUCTURES_PAGING_ENABLED = {{ .Values.services.structures.STRUCTURES_PAGING_ENABLED | toString | title }}
STRUCTURES_REPORT_NPC_ATTACKS = {{ .Values.services.structures.STRUCTURES_REPORT_NPC_ATTACKS | toString | title }}
STRUCTURES_SHOW_FUEL_EXPIRES_RELATIVE = {{ .Values.services.structures.STRUCTURES_SHOW_FUEL_EXPIRES_RELATIVE | toString | title }}
STRUCTURES_SHOW_JUMP_GATES = {{ .Values.services.structures.STRUCTURES_SHOW_JUMP_GATES | toString | title }}
STRUCTURES_STRUCTURE_SYNC_GRACE_MINUTES = {{ .Values.services.structures.STRUCTURES_STRUCTURE_SYNC_GRACE_MINUTES }}
STRUCTURES_TASKS_TIME_LIMIT = {{ .Values.services.structures.STRUCTURES_TASKS_TIME_LIMIT }}
STRUCTURES_TIMERS_ARE_CORP_RESTRICTED = {{ .Values.services.structures.STRUCTURES_TIMERS_ARE_CORP_RESTRICTED | toString | title }}

CELERYBEAT_SCHEDULE['structures_update_all_structures'] = {
    'task': 'structures.tasks.update_all_structures',
    'schedule': crontab(minute='*/30'),
}
CELERYBEAT_SCHEDULE['structures_fetch_all_notifications'] = {
    'task': 'structures.tasks.fetch_all_notifications',
    'schedule': crontab(minute='*/5'),
}
{{- end }}

{{- if .Values.services.structuretimers.enabled }}
STRUCTURETIMERS_MAX_AGE_FOR_NOTIFICATIONS = {{ .Values.services.structuretimers.STRUCTURETIMERS_MAX_AGE_FOR_NOTIFICATIONS }}
STRUCTURETIMERS_NOTIFICATIONS_ENABLED = {{ .Values.services.structuretimers.STRUCTURETIMERS_NOTIFICATIONS_ENABLED | toString | title }}
STRUCTURETIMERS_TIMERS_OBSOLETE_AFTER_DAYS = {{ .Values.services.structuretimers.STRUCTURETIMERS_TIMERS_OBSOLETE_AFTER_DAYS }}
STRUCTURETIMERS_DEFAULT_PAGE_LENGTH = {{ .Values.services.structuretimers.STRUCTURETIMERS_DEFAULT_PAGE_LENGTH }}
STRUCTURETIMERS_PAGING_ENABLED = {{ .Values.services.structuretimers.STRUCTURETIMERS_PAGING_ENABLED | toString | title }}
STRUCTURETIMER_NOTIFICATION_SET_AVATAR = {{ .Values.services.structuretimers.STRUCTURETIMER_NOTIFICATION_SET_AVATAR | toString | title }}

CELERYBEAT_SCHEDULE['structuretimers_housekeeping'] = {
    'task': 'structuretimers.tasks.housekeeping',
    'schedule': crontab(minute=0, hour=3),
}
{{- end }}

{{- if .Values.services.fittings.enabled }}
FITTINGS_AADISCORDBOT_INTEGRATION = {{ .Values.services.fittings.FITTINGS_AADISCORDBOT_INTEGRATION | toString | title }}

CELERYBEAT_SCHEDULE['fittings_update_types'] = {
    'task': 'fittings.tasks.verify_server_version_and_update_types',
    'schedule': crontab(minute=0, hour='12'),
}
{{- end }}

{{- if .Values.services.mailrelay.enabled }}
MAILRELAY_DISCORD_TASK_TIMEOUT = {{ .Values.services.mailrelay.MAILRELAY_DISCORD_TASK_TIMEOUT }}
MAILRELAY_DISCORD_USER_TIMEOUT = {{ .Values.services.mailrelay.MAILRELAY_DISCORD_USER_TIMEOUT }}
MAILRELAY_OLDEST_MAIL_HOURS = {{ .Values.services.mailrelay.MAILRELAY_OLDEST_MAIL_HOURS }}
MAILRELAY_RELAY_GRACE_MINUTES = {{ .Values.services.mailrelay.MAILRELAY_RELAY_GRACE_MINUTES }}

CELERYBEAT_SCHEDULE['mailrelay_forward_new_mails'] = {
    'task': 'mailrelay.tasks.forward_new_mails',
    'schedule': crontab(minute='*/5'),
}
{{- end }}

{{- if .Values.services.killtracker.enabled }}
KILLTRACKER_KILLMAIL_MAX_AGE_FOR_TRACKER = {{ .Values.services.killtracker.KILLTRACKER_KILLMAIL_MAX_AGE_FOR_TRACKER }}
KILLTRACKER_MAX_KILLMAILS_PER_RUN = {{ .Values.services.killtracker.KILLTRACKER_MAX_KILLMAILS_PER_RUN }}
KILLTRACKER_PURGE_KILLMAILS_AFTER_DAYS = {{ .Values.services.killtracker.KILLTRACKER_PURGE_KILLMAILS_AFTER_DAYS }}
KILLTRACKER_WEBHOOK_SET_AVATAR = {{ .Values.services.killtracker.KILLTRACKER_WEBHOOK_SET_AVATAR | toString | title }}
KILLTRACKER_STORING_KILLMAILS_ENABLED = {{ .Values.services.killtracker.KILLTRACKER_STORING_KILLMAILS_ENABLED | toString | title }}

CELERYBEAT_SCHEDULE['killtracker_run_killtracker'] = {
    'task': 'killtracker.tasks.run_killtracker',
    'schedule': crontab(minute='*/1'),
}
{{- end }}

{{- if .Values.services.moonmining.enabled }}
MOONMINING_ADMIN_NOTIFICATIONS_ENABLED = {{ .Values.services.moonmining.MOONMINING_ADMIN_NOTIFICATIONS_ENABLED | toString | title }}
MOONMINING_COMPLETED_EXTRACTIONS_HOURS_UNTIL_STALE = {{ .Values.services.moonmining.MOONMINING_COMPLETED_EXTRACTIONS_HOURS_UNTIL_STALE }}
MOONMINING_REPROCESSING_YIELD = {{ .Values.services.moonmining.MOONMINING_REPROCESSING_YIELD }}
MOONMINING_USE_REPROCESS_PRICING = {{ .Values.services.moonmining.MOONMINING_USE_REPROCESS_PRICING | toString | title }}
MOONMINING_VOLUME_PER_DAY = {{ .Values.services.moonmining.MOONMINING_VOLUME_PER_DAY }}
MOONMINING_DAYS_PER_MONTH = {{ .Values.services.moonmining.MOONMINING_DAYS_PER_MONTH }}
MOONMINING_OVERWRITE_SURVEYS_WITH_ESTIMATES = {{ .Values.services.moonmining.MOONMINING_OVERWRITE_SURVEYS_WITH_ESTIMATES | toString | title }}

CELERYBEAT_SCHEDULE['moonmining_run_regular_updates'] = {
    'task': 'moonmining.tasks.run_regular_updates',
    'schedule': crontab(minute='*/10'),
}
CELERYBEAT_SCHEDULE['moonmining_run_report_updates'] = {
    'task': 'moonmining.tasks.run_report_updates',
    'schedule': crontab(minute=30, hour='*/1'),
}
CELERYBEAT_SCHEDULE['moonmining_run_value_updates'] = {
 'task': 'moonmining.tasks.run_calculated_properties_update',
 'schedule': crontab(minute=30, hour=3)
}
{{- end }}

{{- if .Values.services.memberaudit.enabled }}
APP_UTILS_NOTIFY_THROTTLED_TIMEOUT = {{ .Values.services.memberaudit.APP_UTILS_NOTIFY_THROTTLED_TIMEOUT }}
MEMBERAUDIT_APP_NAME = {{ .Values.services.memberaudit.MEMBERAUDIT_APP_NAME | quote }}
MEMBERAUDIT_DATA_RETENTION_LIMIT = {{ .Values.services.memberaudit.MEMBERAUDIT_DATA_RETENTION_LIMIT }}
MEMBERAUDIT_ESI_ERROR_LIMIT_THRESHOLD = {{ .Values.services.memberaudit.MEMBERAUDIT_ESI_ERROR_LIMIT_THRESHOLD }}
MEMBERAUDIT_BULK_METHODS_BATCH_SIZE = {{ .Values.services.memberaudit.MEMBERAUDIT_BULK_METHODS_BATCH_SIZE }}
MEMBERAUDIT_LOCATION_STALE_HOURS = {{ .Values.services.memberaudit.MEMBERAUDIT_LOCATION_STALE_HOURS }}
MEMBERAUDIT_LOG_UPDATE_STATS = {{ .Values.services.memberaudit.MEMBERAUDIT_LOG_UPDATE_STATS | toString | title }}
MEMBERAUDIT_MAX_MAILS = {{ .Values.services.memberaudit.MEMBERAUDIT_MAX_MAILS }}
MEMBERAUDIT_TASKS_MAX_ASSETS_PER_PASS = {{ .Values.services.memberaudit.MEMBERAUDIT_TASKS_MAX_ASSETS_PER_PASS }}
MEMBERAUDIT_TASKS_TIME_LIMIT = {{ .Values.services.memberaudit.MEMBERAUDIT_TASKS_TIME_LIMIT }}
MEMBERAUDIT_UPDATE_STALE_RING_1 = {{ .Values.services.memberaudit.MEMBERAUDIT_UPDATE_STALE_RING_1 }}
MEMBERAUDIT_UPDATE_STALE_RING_2 = {{ .Values.services.memberaudit.MEMBERAUDIT_UPDATE_STALE_RING_2 }}
MEMBERAUDIT_UPDATE_STALE_RING_3 = {{ .Values.services.memberaudit.MEMBERAUDIT_UPDATE_STALE_RING_3 }}

CELERYBEAT_SCHEDULE['memberaudit_run_regular_updates'] = {
    'task': 'memberaudit.tasks.run_regular_updates',
    'schedule': crontab(minute=0, hour='*/1'),
}
{{- end }}

{{- if .Values.services.aa_rss_to_discord.enabled }}
CELERYBEAT_SCHEDULE["aa_rss_to_discord_fetch_rss"] = {
    "task": "aa_rss_to_discord.tasks.fetch_rss",
    "schedule": crontab(minute="*/5"),
}
{{- end }}

{{- if .Values.services.blueprints.enabled }}
CELERYBEAT_SCHEDULE['blueprints_update_all_blueprints'] = {
    'task': 'blueprints.tasks.update_all_blueprints',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['blueprints_update_all_industry_jobs'] = {
    'task': 'blueprints.tasks.update_all_industry_jobs',
    'schedule': crontab(minute=0, hour='*'),
}
CELERYBEAT_SCHEDULE['blueprints_update_all_locations'] = {
    'task': 'blueprints.tasks.update_all_locations',
    'schedule': crontab(minute=0, hour='*/12'),
}
{{- end }}

{{- if .Values.services.marketmanager.enabled }}
## Settings for AA-MarketManager
MARKETMANAGER_CLEANUP_DAYS_STRUCTURE = {{ .Values.services.marketmanager.MARKETMANAGER_CLEANUP_DAYS_STRUCTURE }}
MARKETMANAGER_CLEANUP_DAYS_ORDER = {{ .Values.services.marketmanager.MARKETMANAGER_CLEANUP_DAYS_ORDER }}
MARKETMANAGER_TASK_PRIORITY_ORDERS = {{ .Values.services.marketmanager.MARKETMANAGER_TASK_PRIORITY_ORDERS }}
MARKETMANAGER_TASK_PRIORITY_STRUCTURES = {{ .Values.services.marketmanager.MARKETMANAGER_TASK_PRIORITY_STRUCTURES }}
MARKETMANAGER_TASK_PRIORITY_BACKGROUND = {{ .Values.services.marketmanager.MARKETMANAGER_TASK_PRIORITY_BACKGROUND }}
MARKETMANAGER_TASK_PRIORITY_WATCH_CONFIGS = {{ .Values.services.marketmanager.MARKETMANAGER_TASK_PRIORITY_WATCH_CONFIGS }}
MARKETMANAGER_WEBHOOK_COLOUR_ERROR = {{ .Values.services.marketmanager.MARKETMANAGER_WEBHOOK_COLOUR_ERROR }}
MARKETMANAGER_WEBHOOK_COLOUR_WARNING = {{ .Values.services.marketmanager.MARKETMANAGER_WEBHOOK_COLOUR_WARNING }}
MARKETMANAGER_WEBHOOK_COLOUR_INFO = {{ .Values.services.marketmanager.MARKETMANAGER_WEBHOOK_COLOUR_INFO }}
MARKETMANAGER_WEBHOOK_COLOUR_SUCCESS = {{ .Values.services.marketmanager.MARKETMANAGER_WEBHOOK_COLOUR_SUCCESS }}
MARKETMANAGER_TYPESTATISTICS_MINIMUM_ORDER_COUNT = {{ .Values.services.marketmanager.MARKETMANAGER_TYPESTATISTICS_MINIMUM_ORDER_COUNT }}

# Market Orders
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_market_orders'] = {
    'task': 'marketmanager.tasks.fetch_public_market_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_character_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_character_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporation_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_corporation_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_structure_orders'] = {
    'task': 'marketmanager.tasks.fetch_all_structure_orders',
    'schedule': crontab(minute=0, hour='*/3'),
}
# Structure Information
CELERYBEAT_SCHEDULE['marketmanager_fetch_public_structures'] = {
    'task': 'marketmanager.tasks.fetch_public_structures',
    'schedule': crontab(minute=0, hour=4),
}
CELERYBEAT_SCHEDULE['marketmanager_update_private_structures'] = {
    'task': 'marketmanager.tasks.update_private_structures',
    'schedule': crontab(minute=0, hour=5),
}
CELERYBEAT_SCHEDULE['marketmanager_fetch_all_corporations_structures'] = {
    'task': 'marketmanager.tasks.fetch_all_corporations_structures',
    'schedule': crontab(minute=0, hour=6),
}
# Watch Configs
CELERYBEAT_SCHEDULE['marketmanager_update_managed_watch_configs'] = {
    'task': 'marketmanager.tasks.update_managed_watch_configs',
    'schedule': crontab(minute=0, hour=2),
}
CELERYBEAT_SCHEDULE['marketmanager_run_all_watch_configs'] = {
    'task': 'marketmanager.tasks.run_all_watch_configs',
    'schedule': crontab(minute=0, hour='*/3'),
}
# Background Tasks
CELERYBEAT_SCHEDULE['marketmanager_update_all_type_statistics'] = {
    'task': 'marketmanager.tasks.update_all_type_statistics',
    'schedule': crontab(minute=0, hour=0, day_of_week=1),
}
# Cleanup
CELERYBEAT_SCHEDULE['marketmanager_garbage_collection'] = {
    'task': 'marketmanager.tasks.garbage_collection',
    'schedule': crontab(minute=0, hour=0),
}
{{- end }}

{{- if .Values.services.buybackprogram.enabled }}
BUYBACKPROGRAM_TRACKING_PREFILL = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_TRACKING_PREFILL | quote }}
BUYBACKPROGRAM_PRICE_SOURCE_ID = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_PRICE_SOURCE_ID }}
BUYBACKPROGRAM_PRICE_SOURCE_NAME = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_PRICE_SOURCE_NAME | quote }}
BUYBACKPROGRAM_PRICE_AGE_WARNING_LIMIT = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_PRICE_AGE_WARNING_LIMIT }}
BUYBACKPROGRAM_PRICE_METHOD = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_PRICE_METHOD | quote }}
BUYBACKPROGRAM_PRICE_JANICE_API_KEY = {{ .Values.services.buybackprogram.BUYBACKPROGRAM_PRICE_JANICE_API_KEY | quote }}

# Buybackprogram price updates
CELERYBEAT_SCHEDULE['buybackprogram_update_all_prices'] = {
    'task': 'buybackprogram.tasks.update_all_prices',
    'schedule': crontab(minute=0, hour='0'),
}

# Buybackprogram contract updates
CELERYBEAT_SCHEDULE['buybackprogram_update_all_contracts'] = {
    'task': 'buybackprogram.tasks.update_all_contracts',
    'schedule': crontab(minute='*/15'),
}
{{- end }}

{{- if .Values.services.standingsrequests.enabled }}
SR_CORPORATIONS_ENABLED = {{ .Values.services.standingsrequests.SR_CORPORATIONS_ENABLED | toString | title }}
SR_NOTIFICATIONS_ENABLED = {{ .Values.services.standingsrequests.SR_NOTIFICATIONS_ENABLED | toString | title }}
SR_OPERATION_MODE = {{ .Values.services.standingsrequests.SR_OPERATION_MODE | quote }}
SR_REQUIRED_SCOPES = {{ .Values.services.standingsrequests.SR_REQUIRED_SCOPES }}
SR_PAGE_CACHE_SECONDS = {{ .Values.services.standingsrequests.SR_PAGE_CACHE_SECONDS }}
SR_STANDINGS_STALE_HOURS = {{ .Values.services.standingsrequests.SR_STANDINGS_STALE_HOURS }}
SR_STANDING_TIMEOUT_HOURS = {{ .Values.services.standingsrequests.SR_STANDING_TIMEOUT_HOURS }}
SR_SYNC_BLUE_ALTS_ENABLED = {{ .Values.services.standingsrequests.SR_SYNC_BLUE_ALTS_ENABLED | toString | title }}
STANDINGS_API_CHARID = {{ .Values.services.standingsrequests.STANDINGS_API_CHARID }}
STR_CORP_IDS = {{ .Values.services.standingsrequests.STR_CORP_IDS }}

# CELERY tasks
CELERYBEAT_SCHEDULE['standings_requests_standings_update'] = {
    'task': 'standings_requests.standings_update',
    'schedule': crontab(minute='*/30'),
}
CELERYBEAT_SCHEDULE['standings_requests_update_associations_api'] = {
    'task': 'standings_requests.update_associations_api',
    'schedule': crontab(minute='30', hour='*/3'),
}
CELERYBEAT_SCHEDULE['standings_requests_validate_requests'] = {
    'task': 'standings_requests.validate_requests',
    'schedule': crontab(minute='0', hour='*/6'),
}
CELERYBEAT_SCHEDULE['standings_requests_purge_stale_data'] = {
    'task': 'standings_requests.purge_stale_data',
    'schedule': crontab(minute='0', hour='*/24'),
}
{{- end }}

{{- if .Values.services.taskmonitor.enabled }}
TASKMONITOR_DATA_MAX_AGE = {{ .Values.services.taskmonitor.TASKMONITOR_DATA_MAX_AGE }}
TASKMONITOR_HOUSEKEEPING_FREQUENCY = {{ .Values.services.taskmonitor.TASKMONITOR_HOUSEKEEPING_FREQUENCY }}
TASKMONITOR_REPORTS_MAX_AGE = {{ .Values.services.taskmonitor.TASKMONITOR_REPORTS_MAX_AGE }}
TASKMONITOR_REPORTS_MAX_TOP = {{ .Values.services.taskmonitor.TASKMONITOR_REPORTS_MAX_TOP }}
{{- end }}

{{- if .Values.services.celeryanalytics.enabled }}
CA_HOUSEKEEPING_DB_BACKLOG = {{ .Values.services.celeryanalytics.CA_HOUSEKEEPING_DB_BACKLOG }}
CA_RESULT_MAX_LEN = {{ .Values.services.celeryanalytics.CA_RESULT_MAX_LEN }}
{{- end }}

{{- if .Values.services.packagemonitor.enabled }}
PACKAGE_MONITOR_EXCLUDE_PACKAGES = {{ .Values.services.packagemonitor.PACKAGE_MONITOR_EXCLUDE_PACKAGES }}
PACKAGE_MONITOR_INCLUDE_PACKAGES = {{ .Values.services.packagemonitor.PACKAGE_MONITOR_INCLUDE_PACKAGES }}
PACKAGE_MONITOR_NOTIFICATIONS_ENABLED = {{ .Values.services.packagemonitor.PACKAGE_MONITOR_NOTIFICATIONS_ENABLED | toString | title }}
PACKAGE_MONITOR_SHOW_ALL_PACKAGES = {{ .Values.services.packagemonitor.PACKAGE_MONITOR_SHOW_ALL_PACKAGES | toString | title }}
PACKAGE_MONITOR_EXCLPACKAGE_MONITOR_SHOW_EDITABLE_PACKAGESUDE_PACKAGES = {{ .Values.services.packagemonitor.PACKAGE_MONITOR_SHOW_EDITABLE_PACKAGES | toString | title }}

CELERYBEAT_SCHEDULE['package_monitor_update_distributions'] = {
    'task': 'package_monitor.tasks.update_distributions',
    'schedule': crontab(minute='*/60'),
}
{{- end }}

{{- if and (eq .Values.services.corputils.enabled true) (eq .Values.services.corputils.autoupdate true) }}
CELERYBEAT_SCHEDULE['update_all_corpstats'] = {
    'task': 'allianceauth.corputils.tasks.update_all_corpstats',
    'schedule': crontab(minute=0, hour="*/6"),
}
{{- end }}

{{- if .Values.services.fleetpings.enabled }}
AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE = {{ .Values.services.fleetpings.AA_FLEETPINGS_USE_DOCTRINES_FROM_FITTINGS_MODULE | toString | title }}
{{- end }}

{{/*
Let's definte all the env variables we need here as we reuse them for each container
*/}}
{{- define "alliance-auth-data.env" -}}
- name: AA_SITENAME
  value: {{ .Values.auth.sitename | quote }}
- name: PROTOCOL
  value: {{ .Values.auth.protocol }}://
- name: AUTH_SUBDOMAIN
  value: {{ .Values.auth.subdomain }}
- name: DOMAIN
  value: {{ .Values.auth.domain }}
- name: AA_DEBUG
  value: '{{ .Values.auth.debug }}'
- name: AA_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ .Values.auth.existingSecret }}
      key: secretKey
- name: AA_DB_NAME
  value: {{ .Values.db.name }}
- name: AA_DB_HOST
  value: {{ .Values.db.host }}
- name: AA_DB_PORT
  value: '{{ .Values.db.port }}'
- name: AA_DB_USER
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.existingSecret }}
      key: username
- name: AA_DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ .Values.db.existingSecret }}
      key: password
- name: AA_EMAIL_HOST
  value: {{ .Values.email.host }}
- name: AA_EMAIL_PORT
  value: '{{ .Values.email.port }}'
- name: AA_EMAIL_USE_TLS
  value: '{{ .Values.email.useTLS}}'
- name: AA_DEFAULT_FROM_EMAIL
  value: {{ .Values.email.defaultFrom}}
- name: AA_EMAIL_HOST_USER
  valueFrom:
    secretKeyRef:
      name: {{ .Values.email.existingSecret }}
      key: username
- name: AA_EMAIL_HOST_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ .Values.email.existingSecret }}
      key: password
- name: ESI_USER_CONTACT_EMAIL
  value: {{ .Values.esi.email }}
- name: ESI_SSO_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ .Values.esi.existingSecret }}
      key: clientId
- name: ESI_SSO_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ .Values.esi.existingSecret }}
      key: clientSecret
- name: AA_REDIS
  value: {{ .Values.redis.host }}:{{ .Values.redis.port }}
- name: AA_REDIS_DB
  value: '{{ .Values.redis.db }}'
- name: AA_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ .Values.redis.existingSecret }}
      key: redis-password
{{- if .Values.services.discord.enabled }}
- name: DISCORD_GUILD_ID
  value: '{{ .Values.services.discord.guildId }}'
- name: DISCORD_APP_ID
  valueFrom:
    secretKeyRef:
      name: {{ .Values.services.discord.existingSecret }}
      key: appId
- name: DISCORD_APP_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ .Values.services.discord.existingSecret }}
      key: appSecret
- name: DISCORD_BOT_TOKEN
  valueFrom:
    secretKeyRef:
      name: {{ .Values.services.discord.existingSecret }}
      key: botToken
{{- end }}
{{- if .Values.services.discordproxy.enabled }}
- name: DISCORD_PROXY_BOT_TOKEN
  valueFrom:
    secretKeyRef:
      name: {{ .Values.services.discordproxy.existingSecret }}
      key: botToken
{{- end }}
{{- end }}
ARG imageTag
FROM registry.gitlab.com/allianceauth/allianceauth/auth:${imageTag}

COPY requirements.txt /
RUN pip install -r /requirements.txt

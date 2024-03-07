# syntax=docker/dockerfile:1
ARG PLONE_VERSION=6
FROM plone/server-builder:${PLONE_VERSION} as builder

WORKDIR /app

# Add local code
COPY . src/plone.edu

# Install local requirements and pre-compile mo files
RUN <<EOT
    set -e
    mv src/plone.edu/requirements-docker.txt ./requirements.txt
    bin/pip install -r requirements.txt
    bin/python /compile_mo.py
    rm -Rf src/ /compile_mo.py compile_mo.log
EOT

FROM plone/server-prod-config:${PLONE_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="ghcr.io/collective/edu" \
      org.label-schema.description="A new Plone Distribution" \
      org.label-schema.vendor="Plone Community"

# Disable MO Compilation
ENV zope_i18n_compile_mo_files=
# Show only our distributions
ENV ALLOWED_DISTRIBUTIONS=edu

COPY --from=builder /app /app

RUN <<EOT
    ln -s /data /app/var
EOT

ARG BUILD_FROM=ghcr.io/home-assistant/aarch64-base-python:3.14-alpine3.22
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

# Set Shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements files
COPY requirements.txt requirements-edge.txt /tmp/

# Setup Base
ARG BUILD_ARCH=aarch64
ARG BUILD_VERSION
ARG HA_CLI_VERSION="5.6.0"

# Edge builds (versioned by a 7 character commit hash) install the latest
# redreactor alpha, everything else installs the stable release
RUN \
    requirements="/tmp/requirements.txt" \
    && if [[ "${BUILD_VERSION:-}" =~ ^[0-9a-f]{7}$ ]]; then \
        requirements="/tmp/requirements-edge.txt"; \
    fi \
    \
    && apk add --no-cache --virtual .build-dependencies \
        gcc=14.2.0-r6 \
        musl-dev=1.2.5-r13 \
        linux-headers=6.14.2-r0 \
    \
    && pip3 install --no-cache-dir -r "${requirements}" \
    \
    && curl -fsSL -o /usr/bin/ha \
        "https://github.com/home-assistant/cli/releases/download/${HA_CLI_VERSION}/ha_${BUILD_ARCH}" \
    \
    && chmod a+x /usr/bin/ha \
    \
    && apk del --no-cache --purge .build-dependencies \
    && rm -fr \
        /tmp/*

# Copy Root Filesystem
COPY rootfs /

# Ensure correct permissions
RUN \
    chmod a+x /etc/s6-overlay/s6-rc.d/redreactor/run \
    && chmod a+x /etc/s6-overlay/s6-rc.d/redreactor/finish

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="MrEditor97 <dev@mreditor97.co.uk>" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="Home Assistant Apps" \
    org.opencontainers.image.authors="MrEditor97 <dev@mreditor97.co.uk>" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/mreditor97/homeassistant-apps" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/master/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}

FROM ubuntu:22.04

ARG RUNNER_VERSION=2.319.1
ARG TARGETARCH=x64

ENV DEBIAN_FRONTEND=noninteractive \
    RUNNER_ALLOW_RUNASROOT=1 \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        git \
        git-lfs \
        gnupg \
        jq \
        libicu70 \
        locales \
        lsb-release \
        openssh-client \
        python3 \
        python3-pip \
        python3-venv \
        rsync \
        sudo \
        unzip \
        wget \
        xz-utils \
        zip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/runner \
    && mkdir -p /actions-runner /workdir \
    && chown -R runner:runner /actions-runner /workdir

USER runner
WORKDIR /actions-runner

RUN curl -fsSL -o /tmp/runner.tar.gz \
        "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${TARGETARCH}-${RUNNER_VERSION}.tar.gz" \
    && tar xzf /tmp/runner.tar.gz -C /actions-runner \
    && rm /tmp/runner.tar.gz \
    && sudo ./bin/installdependencies.sh \
    && sudo rm -rf /var/lib/apt/lists/*

COPY --chown=runner:runner entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh

ENV RUNNER_VERSION=${RUNNER_VERSION}

ENTRYPOINT ["/entrypoint.sh"]

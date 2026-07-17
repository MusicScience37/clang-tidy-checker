FROM registry.gitlab.com/musicscience37projects/docker/my-cpp-env-docker:clang22

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlite3 \
    && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -r /var/lib/apt/lists/*

USER ubuntu

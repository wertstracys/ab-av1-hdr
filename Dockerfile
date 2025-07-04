# Base Image 
FROM fedora:42

# Setup home directory, non interactive shell and timezone
RUN mkdir -p /bot /tgenc && chmod -R 777 /usr /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Havana
ENV TERM=xterm

# Install Dependencies
RUN dnf -qq -y update && dnf -qq -y install aria2 bash curl gcc git jq mediainfo procps-ng psmisc pv python3-devel python3-pip qbittorrent-nox wget xz zstd && dnf clean all && python3 -m pip install --upgrade pip setuptools

# Install latest ffmpeg and ab-av1
RUN wget -q https://github.com/QuickFatHedgehog/FFmpeg-Builds-SVT-AV1-HDR/releases/download/latest/ffmpeg-n7.1-latest-linux64-gpl-7.1.tar.xz && tar -xvf *xz && cp *7.1/bin/* /usr/bin && rm -rf ffmpeg* && \
    wget -q https://github.com/alexheretic/ab-av1/releases/download/v0.10.1/ab-av1-v0.10.1-x86_64-unknown-linux-musl.tar.zst && tar -xvf *zst && cp ab-av1 /usr/bin && rm -rf ab-av1*

# Copy files from repo to home directory
COPY . .

# Install python3 requirements
RUN pip3 install -r requirements.txt && \
    pip cache purge

# Cleanup
RUN rm -rf fonts scripts .env* .git* Dockerfile License *.md requirements.txt srun* update*

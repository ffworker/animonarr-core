FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg wget && rm -rf /var/lib/apt/lists/*

# Optional: install sdl-cli if available/published to PyPI or the environment has it.
# Here we just create a dummy 'sdl' to illustrate; replace with actual installer in legal contexts.
RUN echo '#!/usr/bin/env bash\necho "[SDL stub] Downloading: $@"\nsleep 1\necho "50%"\nsleep 1\necho "100%"' > /usr/local/bin/sdl && chmod +x /usr/local/bin/sdl

WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app
RUN mkdir -p /app/data /app/downloads

ENV ANIMONARR_DB=/app/data/animonarr.db
ENV ANIMONARR_DOWNLOAD_DIR=/app/downloads
ENV ANIMONARR_SDL_PATH=sdl
ENV ANIMONARR_ALLOWED_DOMAINS=archive.org,example.com,localhost,127.0.0.1
ENV ANIMONARR_SCRAPE_INTERVAL_MIN=15
ENV TZ=Europe/Berlin

EXPOSE 8080
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]

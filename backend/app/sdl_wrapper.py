import os, re, subprocess, shlex, time
from urllib.parse import urlparse

ALLOWED_DOMAINS = set([d.strip().lower() for d in os.getenv("ANIMONARR_ALLOWED_DOMAINS", "archive.org,localhost,127.0.0.1").split(",") if d.strip()])

class SDLManager:
    def __init__(self, sdl_path: str = None, download_dir: str = None):
        self.sdl_path = sdl_path or os.getenv("ANIMONARR_SDL_PATH", "sdl")
        self.download_dir = download_dir or os.getenv("ANIMONARR_DOWNLOAD_DIR", "./downloads")

    def _is_allowed(self, url: str) -> bool:
        host = urlparse(url).hostname or ""
        host = host.lower()
        return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)

    def download_episode(self, episode_id: int, url: str, quality: str = "best"):
        if not self._is_allowed(url):
            raise ValueError(f"Blocked URL domain for safety/compliance: {url}")
        job_id = f"ep_{episode_id}_{int(time.time())}"
        # This uses 'sdl' generically; in practice, ensure 'sdl' supports the domain and is legally permissible.
        cmd = f"{shlex.quote(self.sdl_path)} download {shlex.quote(url)} -o {shlex.quote(self.download_dir)} --quality {shlex.quote(quality)}"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return job_id, proc

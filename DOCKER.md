# Docker Hosting

This project is a desktop GUI app, so the container hosts it through noVNC.
After the container starts, the chess window is available in your browser.

## Run With Docker Compose

```powershell
docker compose up -d --build
```

Open:

```text
http://localhost:6080/vnc.html?autoconnect=true&resize=scale
```

View logs:

```powershell
docker compose logs -f chess
```

Stop:

```powershell
docker compose down
```

Rebuild from scratch after Dockerfile or launcher changes:

```powershell
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
```

If the app exits during startup, inspect the display logs:

```powershell
docker compose logs chess
```

## Run With Docker Only

```powershell
docker build -t chess-2 .
docker run -d --name chess-2 -p 6080:6080 --restart unless-stopped chess-2
```

Open:

```text
http://localhost:6080/vnc.html?autoconnect=true&resize=scale
```

Stop and remove:

```powershell
docker stop chess-2
docker rm chess-2
```

## Remote Hosting

On a server, copy or clone the project, then run:

```bash
docker compose up -d --build
```

Expose TCP port `6080` in your firewall or reverse proxy, then open:

```text
http://SERVER_IP:6080/vnc.html?autoconnect=true&resize=scale
```

The noVNC endpoint has no password in this development config. For public
hosting, put it behind a reverse proxy with authentication or only expose it on
a private network.

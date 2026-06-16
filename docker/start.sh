#!/usr/bin/env bash
set -euo pipefail

export DISPLAY="${DISPLAY:-:99}"
export RESOLUTION="${RESOLUTION:-1600x1000x24}"
export APP_ENTRY="${APP_ENTRY:-run_.py}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-x11}"

mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

display_number="${DISPLAY#:}"
display_number="${display_number%%.*}"
lock_file="/tmp/.X${display_number}-lock"
socket_file="/tmp/.X11-unix/X${display_number}"

if [ -f "$lock_file" ]; then
    lock_pid="$(tr -d ' ' < "$lock_file" || true)"
    if [ -n "$lock_pid" ] && kill -0 "$lock_pid" >/dev/null 2>&1; then
        echo "Stopping existing X server on display $DISPLAY with pid $lock_pid." >&2
        kill "$lock_pid" >/dev/null 2>&1 || true
        for _ in $(seq 1 50); do
            if ! kill -0 "$lock_pid" >/dev/null 2>&1; then
                break
            fi
            sleep 0.1
        done
        if kill -0 "$lock_pid" >/dev/null 2>&1; then
            kill -9 "$lock_pid" >/dev/null 2>&1 || true
        fi
    fi
    rm -f "$lock_file" "$socket_file"
fi

Xvfb "$DISPLAY" -screen 0 "$RESOLUTION" -ac +extension GLX +render -noreset >/tmp/xvfb.log 2>&1 &
xvfb_pid=$!

display_ready=false
for _ in $(seq 1 100); do
    if ! kill -0 "$xvfb_pid" >/dev/null 2>&1; then
        echo "Xvfb exited before the app could start." >&2
        cat /tmp/xvfb.log >&2
        exit 1
    fi

    if xdpyinfo -display "$DISPLAY" >/tmp/xdpyinfo.log 2>&1; then
        display_ready=true
        break
    fi

    sleep 0.1
done

if [ "$display_ready" != "true" ]; then
    echo "Timed out waiting for X display $DISPLAY." >&2
    echo "Xvfb log:" >&2
    cat /tmp/xvfb.log >&2
    echo "xdpyinfo log:" >&2
    cat /tmp/xdpyinfo.log >&2
    exit 1
fi

fluxbox >/tmp/fluxbox.log 2>&1 &
fluxbox_pid=$!
x11vnc_pid=
websockify_pid=
x11vnc -display "$DISPLAY" -forever -shared -nopw -listen 0.0.0.0 -rfbport 5900 >/tmp/x11vnc.log 2>&1 &
x11vnc_pid=$!
websockify --web=/usr/share/novnc 0.0.0.0:6080 localhost:5900 >/tmp/websockify.log 2>&1 &
websockify_pid=$!

cleanup() {
    kill "$websockify_pid" "$x11vnc_pid" "$fluxbox_pid" "$xvfb_pid" >/dev/null 2>&1 || true
    rm -f "$lock_file" "$socket_file"
}
trap cleanup EXIT HUP INT TERM

sleep 2
if [ ! -f "$APP_ENTRY" ]; then
    if [ "$APP_ENTRY" != "run.py" ] && [ -f "run.py" ]; then
        APP_ENTRY="run.py"
    else
        echo "App entry file not found: $APP_ENTRY" >&2
        echo "Files in /app:" >&2
        ls -la >&2
        exit 1
    fi
fi

set +e
python "$APP_ENTRY"
app_status=$?
exit "$app_status"

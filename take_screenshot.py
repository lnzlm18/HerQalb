"""
Takes a full-page screenshot using Chrome DevTools Protocol.
Usage: python take_screenshot.py <url> [label]
"""
import subprocess, time, json, sys, os, base64, signal
import urllib.request, urllib.error
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9223
WIDTH = 1440
HEIGHT = 5000  # tall enough for full page

url   = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
label = f"-{sys.argv[2]}" if len(sys.argv) > 2 else ""

# Output path
out_dir = Path(__file__).parent / "temporary screenshots"
out_dir.mkdir(exist_ok=True)
existing = sorted(out_dir.glob("screenshot-*.png"))
nums = []
for f in existing:
    try: nums.append(int(f.stem.split("-")[1]))
    except: pass
n = (max(nums) + 1) if nums else 1
out_path = out_dir / f"screenshot-{n}{label}.png"

# Start Chrome
proc = subprocess.Popen([
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    f"--remote-debugging-port={DEBUG_PORT}",
    f"--window-size={WIDTH},{HEIGHT}",
    "--disable-extensions",
    "--disable-background-networking",
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    # Wait for Chrome to start
    for _ in range(20):
        try:
            urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json/version", timeout=1)
            break
        except:
            time.sleep(0.5)
    else:
        raise RuntimeError("Chrome didn't start")

    # Get WebSocket debugger URL — use existing tab or browser target
    tabs = json.loads(urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json/list").read())
    # Find a page tab (not devtools, not extension)
    page_tabs = [t for t in tabs if t.get("type") == "page"]
    if not page_tabs:
        # Try /json directly
        tabs = json.loads(urllib.request.urlopen(f"http://localhost:{DEBUG_PORT}/json").read())
        page_tabs = [t for t in tabs if t.get("type") == "page"]
    if not page_tabs:
        raise RuntimeError(f"No page tabs found. Available: {[t.get('type') for t in tabs]}")
    ws_url = page_tabs[0]["webSocketDebuggerUrl"]

    # Use websocket via socket
    import socket, hashlib, random, struct, threading

    # Parse ws URL
    host = "localhost"
    port = DEBUG_PORT
    path = ws_url.split(f"ws://{host}:{port}")[1]

    def ws_connect(host, port, path):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        key = base64.b64encode(os.urandom(16)).decode()
        s.send(f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += s.recv(1024)
        return s

    def ws_send(s, msg):
        data = json.dumps(msg).encode()
        n = len(data)
        header = bytearray([0x81])
        mask_key = os.urandom(4)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        header += mask_key
        masked = bytearray(data[i] ^ mask_key[i % 4] for i in range(n))
        s.sendall(bytes(header) + bytes(masked))

    def ws_recv(s):
        def read_exact(n):
            buf = b""
            while len(buf) < n:
                buf += s.recv(n - len(buf))
            return buf
        b0, b1 = read_exact(2)
        masked = (b1 & 0x80) != 0
        length = b1 & 0x7F
        if length == 126: length = struct.unpack(">H", read_exact(2))[0]
        elif length == 127: length = struct.unpack(">Q", read_exact(8))[0]
        mask = read_exact(4) if masked else b""
        payload = bytearray(read_exact(length))
        if masked:
            payload = bytearray(payload[i] ^ mask[i % 4] for i in range(length))
        return json.loads(payload.decode())

    def call(s, method, params=None, id=1):
        ws_send(s, {"id": id, "method": method, "params": params or {}})
        while True:
            msg = ws_recv(s)
            if msg.get("id") == id:
                return msg.get("result", {})

    ws = ws_connect(host, port, path)

    # Navigate
    call(ws, "Page.navigate", {"url": url}, id=1)
    time.sleep(0.5)

    # Wait for load
    for _ in range(30):
        result = call(ws, "Runtime.evaluate", {
            "expression": "document.readyState === 'complete' && document.fonts.ready !== undefined"
        }, id=2)
        if result.get("result", {}).get("value"): break
        time.sleep(0.3)

    # Wait for fonts
    call(ws, "Runtime.evaluate", {
        "expression": "document.fonts.ready"
    }, id=3)

    # Trigger all fade-up animations
    call(ws, "Runtime.evaluate", {
        "expression": "document.querySelectorAll('.fu').forEach(el => el.classList.add('vis'))"
    }, id=4)

    # Short extra wait for render
    time.sleep(1.2)

    # Get full page height
    result = call(ws, "Runtime.evaluate", {
        "expression": "document.body.scrollHeight"
    }, id=5)
    page_height = result.get("result", {}).get("value", HEIGHT)

    # Set viewport to full page
    call(ws, "Emulation.setVisibleSize", {"width": WIDTH, "height": page_height}, id=6)
    call(ws, "Emulation.setDeviceMetricsOverride", {
        "width": WIDTH, "height": page_height, "deviceScaleFactor": 2, "mobile": False
    }, id=7)

    time.sleep(0.5)

    # Capture screenshot
    result = call(ws, "Page.captureScreenshot", {
        "format": "png", "captureBeyondViewport": True,
        "clip": {"x": 0, "y": 0, "width": WIDTH, "height": page_height, "scale": 2}
    }, id=8)

    img_data = base64.b64decode(result["data"])
    out_path.write_bytes(img_data)
    print(f"Screenshot saved → {out_path}")
    ws.close()

finally:
    proc.terminate()
    try: proc.wait(timeout=3)
    except: proc.kill()

"""
Enterprise Hub Portal — skrypt uruchomieniowy.
Uruchamia jednocześnie:
  1) Backend APEX API (Flask) na porcie 5100
  2) Frontend Vite (Vue.js) na porcie 3000

Użycie: python start.py
Zatrzymanie: Ctrl+C
"""

import subprocess
import sys
import os
import signal
import time
import socket

BACKEND_DIR = os.path.join(os.path.dirname(__file__), "backend")
FRONTEND_DIR = os.path.dirname(__file__)
BACKEND_PORT = 5100
FRONTEND_PORT = 3000
processes = []


def print_banner():
    print("""
  ╔══════════════════════════════════════════════════════╗
  ║     Enterprise Hub Portal — uruchamianie...          ║
  ╚══════════════════════════════════════════════════════╝
    """)


def wait_for_port(port, timeout=25):
    """Czeka aż port zacznie nasłuchiwać."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


def cleanup():
    """Zatrzymuje wszystkie procesy."""
    print("\n  ■ Zatrzymywanie procesów...")
    for proc in processes:
        if proc and proc.poll() is None:
            try:
                if sys.platform == "win32":
                    proc.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
    print("  ✓ Wszystkie procesy zatrzymane.\n")


if __name__ == "__main__":
    import atexit
    atexit.register(cleanup)

    print_banner()

    # === 1. Python dependencies ===
    try:
        import flask  # noqa
        import flask_cors  # noqa
    except ImportError as e:
        print(f"  ✗ Brak pakietu: {e.name}")
        print(f"    Zainstaluj: pip install flask flask-cors")
        sys.exit(1)
    print("  ✓ Python dependencies OK")

    # === 2. npm install (if needed) ===
    if not os.path.exists(os.path.join(FRONTEND_DIR, "node_modules")):
        print("  ⚠ Brak node_modules — uruchamiam npm install...")
        npm = "npm.cmd" if sys.platform == "win32" else "npm"
        r = subprocess.run([npm, "install"], cwd=FRONTEND_DIR)
        if r.returncode != 0:
            print("  ✗ npm install nie powiódł się. Uruchom ręcznie: npm install")
            sys.exit(1)
        print("  ✓ npm install gotowy")
    else:
        print("  ✓ node_modules OK")

    # === 3. Uruchom backend APEX API ===
    python = sys.executable
    apex_script = os.path.join(BACKEND_DIR, "apex_api.py")
    if not os.path.exists(apex_script):
        print(f"  ✗ Nie znaleziono {apex_script}")
        sys.exit(1)

    print(f"\n  ▶ Uruchamianie APEX API (Flask :{BACKEND_PORT})...")
    backend = subprocess.Popen(
        [python, apex_script],
        cwd=BACKEND_DIR,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )
    processes.append(backend)

    if wait_for_port(BACKEND_PORT):
        print(f"    ✓ APEX API → http://localhost:{BACKEND_PORT}")
    else:
        print(f"    ⚠ APEX API nie zdążył wystartować (timeout 25s)")

    # === 4. Uruchom frontend ===
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    print(f"  ▶ Uruchamianie frontendu (Vite :{FRONTEND_PORT})...")
    frontend = subprocess.Popen(
        [npm, "run", "dev"],
        cwd=FRONTEND_DIR,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )
    processes.append(frontend)

    if wait_for_port(FRONTEND_PORT):
        print(f"    ✓ Frontend → http://localhost:{FRONTEND_PORT}")
    else:
        print(f"    ⚠ Frontend nie zdążył wystartować (timeout 25s) — sprawdź błędy powyżej")

    print(f"""
  ╔══════════════════════════════════════════════════════╗
  ║     Portal gotowy!                                   ║
  ║     Frontend: http://localhost:{FRONTEND_PORT}              ║
  ║     APEX API: http://localhost:{BACKEND_PORT}                ║
  ║     DDT:      http://localhost:8501                  ║
  ║                                                      ║
  ║     Ctrl+C — zatrzymaj wszystkie procesy             ║
  ╚══════════════════════════════════════════════════════╝
    """)

    # Czekaj aż któryś z procesów zginie lub Ctrl+C
    try:
        while True:
            time.sleep(1)
            if backend.poll() is not None:
                print("\n  ✗ Backend zakończył działanie. Zatrzymuję...")
                break
            if frontend.poll() is not None:
                print("\n  ✗ Frontend zakończył działanie. Zatrzymuję...")
                break
    except KeyboardInterrupt:
        print("\n  ■ Ctrl+C")
    finally:
        cleanup()
        sys.exit(0)

#!/usr/bin/env python3
import http.server
import ssl
import os
import socket
import sys
import logging
import threading
import time
import argparse
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TimeOnlyFormatter(logging.Formatter):
    """Custom formatter to show only HH:MM:SS without date or milliseconds."""
    def formatTime(self, record, datefmt=None):
        return datetime.fromtimestamp(record.created).strftime('%H:%M:%S')

# Setup logging
LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'srv.log'
LOG_HISTORY_FILE = LOG_DIR / 'srv_history.log'
PID_FILE = LOG_DIR / 'srv.pid'

# Rotate logs: append current log to history and start fresh
def rotate_logs():
    """Archive current log to history file and start fresh."""
    if LOG_FILE.exists():
        # Read current log content
        with open(LOG_FILE, 'r') as f:
            current_content = f.read()

        # Append to history if there's content
        if current_content.strip():
            with open(LOG_HISTORY_FILE, 'a') as f:
                # Add separator with timestamp
                f.write(f"\n{'=' * 60}\n")
                f.write(f"Archive from: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'=' * 60}\n")
                f.write(current_content)
                if not current_content.endswith('\n'):
                    f.write('\n')

        # Clear current log
        LOG_FILE.unlink()

# Rotate logs before configuring logging
rotate_logs()

# Configure logging with time-only format
formatter = TimeOnlyFormatter('%(asctime)s - %(message)s')

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

logger = logging.getLogger(__name__)

# Global flag to track if a rebuild is pending
_rebuild_pending = False
_rebuild_lock = threading.Lock()


class LoggingHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that logs to file instead of stderr."""

    def __init__(self, *args, **kwargs):
        # Serve from the output directory
        super().__init__(*args, directory='output', **kwargs)

    def log_message(self, format, *args):
        logger.info(f"{self.address_string()} - {format % args}")


def write_pid():
    """Write process ID to file."""
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

def kill_existing_server():
    """Kill existing server if running."""
    if not PID_FILE.exists():
        return
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists
        try:
            os.kill(pid, 0)  # Signal 0 checks if process exists
        except OSError:
            # Process doesn't exist, just remove stale PID file
            PID_FILE.unlink()
            return
        
        # Process exists, kill it
        logger.info(f"⚠️  Killing existing server (PID: {pid})")
        os.kill(pid, 15)  # SIGTERM
        
        # Wait briefly for graceful shutdown
        time.sleep(0.5)
        
        # Force kill if still running
        try:
            os.kill(pid, 0)
            os.kill(pid, 9)  # SIGKILL
            time.sleep(0.2)
        except OSError:
            pass
        
        PID_FILE.unlink()
        logger.info("✓ Previous server stopped")
        
    except (ValueError, FileNotFoundError) as e:
        logger.warning(f"Could not read PID file: {e}")
        PID_FILE.unlink()


def remove_pid():
    """Remove PID file on shutdown."""
    if PID_FILE.exists():
        PID_FILE.unlink()


def run_build():
    """Run the build script to generate output/index.html."""
    try:
        # Import and run the build script
        from scripts.build import main as build_main
        build_main()
    except Exception as e:
        logger.error(f"❌ Build failed: {e}")


class RebuildEventHandler(FileSystemEventHandler):
    """File watcher that triggers rebuilds on changes."""

    def __init__(self, debounce_seconds=0.5):
        super().__init__()
        self.debounce_seconds = debounce_seconds
        self.last_rebuild_time = 0

    def should_trigger_rebuild(self, event):
        """Determine if this event should trigger a rebuild."""
        # Ignore directory changes
        if event.is_directory:
            return False

        # Only watch .py, .html, .jinja files
        if not any(event.src_path.endswith(ext) for ext in ['.py', '.html', '.jinja']):
            return False

        # Ignore __pycache__ and other generated files
        if '__pycache__' in event.src_path or '.pyc' in event.src_path:
            return False

        return True

    def on_modified(self, event):
        self.trigger_rebuild(event, "modified")

    def on_created(self, event):
        self.trigger_rebuild(event, "created")

    def on_deleted(self, event):
        self.trigger_rebuild(event, "deleted")

    def trigger_rebuild(self, event, action):
        """Trigger a rebuild with debouncing."""
        if not self.should_trigger_rebuild(event):
            return

        global _rebuild_pending

        current_time = time.time()

        # Debounce: only rebuild if enough time has passed
        with _rebuild_lock:
            if current_time - self.last_rebuild_time < self.debounce_seconds:
                _rebuild_pending = True
                return

            self.last_rebuild_time = current_time
            _rebuild_pending = False

        # Log the change
        file_path = Path(event.src_path).relative_to(Path.cwd())
        logger.info(f"📝 Detected change: {file_path} ({action})")

        # Run build
        run_build()


def start_file_watcher(project_root):
    """Start watching for file changes in sketchpy/ and templates/."""
    event_handler = RebuildEventHandler(debounce_seconds=0.5)
    observer = Observer()

    watch_dirs = []
    # Watch the sketchpy directory
    sketchpy_dir = project_root / 'sketchpy'
    if sketchpy_dir.exists():
        observer.schedule(event_handler, str(sketchpy_dir), recursive=True)
        watch_dirs.append('sketchpy/')

    # Watch the templates directory
    templates_dir = project_root / 'templates'
    if templates_dir.exists():
        observer.schedule(event_handler, str(templates_dir), recursive=True)
        watch_dirs.append('templates/')

    logger.info(f"👁️  Watching: {', '.join(watch_dirs)}")
    observer.start()
    return observer


def daemonize(project_root):
    """Fork the process to run in the background."""
    try:
        pid = os.fork()
        if pid > 0:
            # Parent process - print info and exit
            print(f"✓ Server started in background (PID: {pid})")
            print(f"  Access: https://localhost:8007/")
            print(f"  Logs: tail -f {LOG_FILE}")
            print(f"  Stop: kill $(cat {PID_FILE})")
            sys.exit(0)
    except OSError as e:
        logger.error(f"Fork failed: {e}")
        sys.exit(1)

    # Decouple from parent environment
    os.setsid()
    os.umask(0)

    # Second fork to prevent zombie processes
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        logger.error(f"Second fork failed: {e}")
        sys.exit(1)

    # Change back to project root
    os.chdir(project_root)

    # Redirect standard file descriptors to /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, 'r') as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    with open(os.devnull, 'a+') as devnull:
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Start the sketchpy development server')
    parser.add_argument('-b', '--background', action='store_true',
                        help='Run server in background (daemon mode)')
    parser.add_argument('-f', '--foreground', action='store_true',
                        help='Run server in foreground (default)')
    args = parser.parse_args()

    # Default to background mode unless foreground is explicitly requested
    run_in_background = args.background or not args.foreground

    # Change to project root directory first
    project_root = Path(__file__).parent.parent
    kill_existing_server()

    os.chdir(project_root)

    # Daemonize if running in background
    if run_in_background:
        daemonize(project_root)
        # Reconfigure logging after daemonization (only to file now)
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(TimeOnlyFormatter('%(asctime)s - %(message)s'))

        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler]
        )
        # Reinitialize logger
        global logger
        logger = logging.getLogger(__name__)

    # Run initial build
    run_build()

    # Start file watcher
    observer = start_file_watcher(project_root)

    # Generate self-signed certificate if it doesn't exist
    cert_file = 'localhost.pem'
    if not os.path.exists(cert_file):
        logger.info("Generating SSL certificate...")
        os.system(f'openssl req -new -x509 -keyout {cert_file} -out {cert_file} -days 365 -nodes -subj "/CN=localhost" 2>/dev/null')

    PORT = 8007

    # Get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    logger.info(f"🚀 Server: https://localhost:{PORT} (also at https://{local_ip}:{PORT})")

    # Write PID file
    write_pid()

    try:
        httpd = http.server.HTTPServer(('0.0.0.0', PORT), LoggingHTTPRequestHandler)

        # Create SSL context (modern approach)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("⏹️  Stopped")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        raise
    finally:
        observer.stop()
        observer.join()
        remove_pid()


if __name__ == '__main__':
    main()

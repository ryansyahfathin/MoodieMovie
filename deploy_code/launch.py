import subprocess
import sys
import time
import socket
import webbrowser
from pyngrok import ngrok

# === Fungsi: Tunggu sampai port terbuka ===
def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(("localhost", port))
                if result == 0:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False

# === Jalankan Streamlit ===
app_path = r"C:\\Users\\fasya meliala\\OneDrive\\Telkom\\Semester 6\\ROSBD\\DB\\DB\\app.py"
port = 8502  # Ganti jika perlu

streamlit_proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", app_path, f"--server.port={port}"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# === Tunggu sampai port terbuka ===
if wait_for_port(port, timeout=20):
    # === Koneksi ngrok ===
    ngrok.set_auth_token("2xa7lyvnJzZ4BbSvzLuyJGxiTHU_7P3ZiGK2iZ5PvoEW3Ddqc")  # ganti token bila perlu
    public_url = ngrok.connect(port, "http").public_url
    print("🔗 Akses aplikasi:", public_url)

    # === Buka di browser otomatis ===
    webbrowser.open(public_url)
else:
    print(f"❌ Port {port} tidak terbuka. Streamlit mungkin gagal dijalankan.")

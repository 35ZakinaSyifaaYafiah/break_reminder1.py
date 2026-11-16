import tkinter as tk
from tkinter import messagebox
import threading
import time
from datetime import datetime
from plyer import notification
import pywhatkit as kit

# ==================== KONFIGURASI PENGGUNA ====================
# Ganti dengan nomor WhatsApp tujuan (gunakan format kode negara, contoh: "+6281234567890")
WHATSAPP_NUMBER = "+6285748249026" 

# Atur durasi dalam detik (untuk pengujian, bisa diset 30 & 60 detik)
WATER_INTERVAL = 30  # Setiap 30 detik untuk pengingat minum air
BREAK_INTERVAL = 60  # Setiap 60 detik untuk istirahat & pesan WhatsApp
# ==============================================================

class BreakReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Break Reminder - Health Tracker")
        self.root.geometry("420x350")
        self.root.resizable(False, False)
        
        self.is_running = False
        self.reminder_thread = None

        # --- Desain Antarmuka (GUI) ---
        title_label = tk.Label(root, text="🧘‍♂️ Break & Hydration Reminder", font=("Arial", 14, "bold"))
        title_label.pack(pady=15)

        # Status Label
        self.status_var = tk.StringVar(value="Status: Berhenti (Idle)")
        self.label_status = tk.Label(root, textvariable=self.status_var, font=("Arial", 11), fg="red")
        self.label_status.pack(pady=5)

        # Informasi Interval
        info_text = f"• Pengingat Minum Air: Tiap {WATER_INTERVAL} detik\n• Pengingat Istirahat & WA: Tiap {BREAK_INTERVAL} detik"
        self.label_info = tk.Label(root, text=info_text, font=("Arial", 10), fg="gray", justify="left")
        self.label_info.pack(pady=10)

        # Tombol Start
        self.btn_start = tk.Button(root, text="Mulai Reminder", bg="green", fg="white", font=("Arial", 11, "bold"), width=24, command=self.start_reminder)
        self.btn_start.pack(pady=8)

        # Tombol Stop
        self.btn_stop = tk.Button(root, text="Hentikan Reminder", bg="red", fg="white", font=("Arial", 11, "bold"), width=24, command=self.stop_reminder, state=tk.DISABLED)
        self.btn_stop.pack(pady=5)

import time
from datetime import datetime
from plyer import notification
import pywhatkit as kit

# ==================== KONFIGURASI PENGGUNA ====================
# Ganti dengan nomor WhatsApp tujuan (gunakan format negara, misal: "+6281234567890")
WHATSAPP_NUMBER = "+6285748249026" 

# Atur durasi dalam detik (untuk pengujian awal, bisa diset kecil. Contoh: 30 & 60 detik)
# Untuk penggunaan normal harian, ubah ke: 1800 (30 menit) dan 3600 (1 jam)
WATER_INTERVAL = 30   # Setiap 30 detik untuk pengingat minum air
BREAK_INTERVAL = 60   # Setiap 60 detik untuk istirahat & pesan WhatsApp
# ==============================================================

def send_desktop_notification(title, message):
    """Fungsi untuk menampilkan notifikasi pop-up di layar komputer."""
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="Break Reminder",
            timeout=10
        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] NOTIFIKASI: {title}")
    except Exception as e:
        print(f"Gagal memunculkan notifikasi: {e}")

def send_whatsapp_alert(message_text):
    """Fungsi untuk mengirim pesan otomatis ke WhatsApp Web."""
    try:
        now = datetime.now()
        # Menjadwalkan pengiriman pesan 1 menit ke depan agar browser siap
        hour = now.hour
        minute = now.minute + 1
        
        if minute >= 60:
            minute = 0
            hour = (hour + 1) % 24

        print(f"[{datetime.now().strftime('%H:%M:%S')}] WHATSAPP: Menjadwalkan pesan ke {WHATSAPP_NUMBER} pada pukul {hour}:{minute:02d}...")
        
        # Mengirim pesan via pywhatkit (pastikan browser default sudah login WhatsApp Web)
        kit.sendwhatmsg(WHATSAPP_NUMBER, message_text, hour, minute, wait_time=15, tab_close=True)
        print("Pesan WhatsApp berhasil dikirim!")
    except Exception as e:
        print(f"ERROR WHATSAPP: Gagal mengirim pesan. Detail: {e}")

def main():
    print("==================================================")
    print("      APLIKASI BREAK REMINDER BERHASIL DIMULAI    ")
    print("==================================================")
    print(f"[*] Pengingat Minum Air : Setiap {WATER_INTERVAL} detik")
    print(f"[*] Pengingat Istirahat : Setiap {BREAK_INTERVAL} detik")
    print("[*] Tekan 'Ctrl + C' di terminal untuk menghentikan program.\n")
    
    start_time = time.time()
    last_water_check = start_time
    last_break_check = start_time

    try:
        while True:
            current_time = time.time()
            
            # 1. Pengecekan Waktu Minum Air
            if current_time - last_water_check >= WATER_INTERVAL:
                send_desktop_notification(
                    "Waktunya Minum Air! 💧", 
                    "Jaga hidrasi tubuhmu. Ambil segelas air putih sekarang!"
                )
                last_water_check = current_time

            # 2. Pengecekan Waktu Istirahat & WhatsApp
            if current_time - last_break_check >= BREAK_INTERVAL:
                send_desktop_notification(
                    "Waktunya Istirahat & Peregangan! 🧘‍♂️", 
                    "Berdiri sejenak, istirahatkan mata dari layar laptop selama 5 menit."
                )
                
                # Pesan pengingat yang akan dikirim ke WhatsApp
                wa_message = "Halo! Ini adalah pengingat otomatis dari aplikasi Break Reminder Python. Kamu sudah duduk terlalu lama di depan laptop, yuk bangun sejenak untuk peregangan dan minum air! Tetap jaga kesehatan ya! 💪"
                send_whatsapp_alert(wa_message)
                
                last_break_check = current_time

            # Jeda 1 detik untuk efisiensi CPU
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n==================================================")
        print("     Aplikasi Break Reminder telah dihentikan.    ")
        print("==================================================")

if __name__ == "__main__":
    main()

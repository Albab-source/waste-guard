===============================================================================================================================================
FIRST MVP
===============================================================================================================================================
[Sensors] --> (Sensor Temperature / pH / Volume)
       \
        --> [Device IoT] -- publish --> [MQTT Broker]

[Main.py] 
    - subscribe topic sensor/data
    - evaluasi berdasarkan rules.json
    - simpan semua data ke DB melalui [Python Store DB]
    - jika alert:
        → publish topic sensor/alert (opsional jika broker tidak lakukan sendiri)
        → kirim payload ke endpoint webhook: [Webhook Backend (REST API)] → [Auth Token Required]

[Database] 
    - Table: data_temperature
        - id
        - sensorId
        - temperature
        - timestamp
    - Table: data_ph
        - id
        - sensorId
        - ph
        - timestamp
    - Table: data_volume
        - id
        - sensorId
        - volume
        - timestamp
    - Table: sensor_logs
        - id (PK)
        - sensorId
        - topic
        - value
        - status_message (ex: "High pH level")
        - timestamp


[MQTT Broker] 
    - ACL per client (ex: IoT device hanya bisa publish)
    - Listener hanya bisa subscribe dan publish alert

[Webhook Backend / API]
    - Token-based Auth (Bearer)
    - Hanya Python Listener yang boleh POST ke endpoint webhook

[Webhook Backend]
    - menerima alert dari Python Listener 
    - autentikasi dengan token 
    - validasi payload ---------------------------------------------
    - menyimpan ke table sensor_logs 
    - forward notifikasi ke WhatsApp API 
    - opsi broadcast melalui WebSocket ke [Dashboard]

[Webhook Backend] --> [WhatsApp API]
        - mengirim alert
        - retry on failure (3x retry logic) ------------------------#
        - status check (delivery success / failed) -----------------#

[API Backend]
    - GET /sensor-data  → ke database-------------------------------
    - GET /sensor-log     → ke database-----------------------------
    - WebSocket server:
        → menerima push alert dari Webhook--------------------------#
        → broadcast real-time ke client (Dashboard)

[Index Dashboard]
    - GET data via REST API-----------------------------------------
    - Subscribe WebSocket → menerima real-time alert

            [Sidebar]
        ├── Dashboard
        ├── Notification
        ├── Profile
        ├── Sign In / Sign Up / Log Out

        [Dashboard Page]
        ├── Chart Temp Limbah
        ├── Chart pH Limbah
        ├── Chart Volume Limbah
        ├── Table Sensor Data (Normal)
        └── Table Alert Log (terbaru)

        [Notification Page]
        ├── Table All Alerts
        └── Filter & Search

        [Profile Page]
        └── User Info + Settings

        [Real-Time Notification]
        └── Toast / Popup dari WebSocket

        [Login / Sign Up]
        └── Auth Page

===============================================================================================================================================
SECOND MVP
===============================================================================================================================================

# 📋 Rencana Pengembangan Fitur Web Monitoring Limbah

| No  | Fitur                          | Deskripsi                                                                                   | Status     |
|-----|--------------------------------|---------------------------------------------------------------------------------------------|------------|
| 1   | Autentikasi & RBAC             | Sistem login/logout dan pembagian hak akses (admin, teknisi, auditor)                      |Belum    |
| 2   | User Login/Logout              | Form login pengguna dan endpoint logout (clear token/session)                              |Belum    |
| 3   | Role Admin                     | Akses penuh: manajemen pengguna, device, dan konfigurasi sistem                            |Belum    |
| 4   | Role Teknisi                   | Akses dashboard, alert, dan histori sensor                                                 |Belum    |
| 5   | Role Auditor                   | Akses hanya untuk melihat histori dan statistik                                            |Belum    |
| 6   | *Histori Data Sensor*          | Halaman tabel data sensor lengkap                                                          |Belum    |
| 7   | *Filter Histori Data*          | Filter berdasarkan tanggal, device, dan jenis sensor                                       |Belum    |
| 8   | *Export CSV Histori*           | Tombol export data histori ke file CSV                                                     |Belum    |
| 9   | *Monitoring Status Device*     | Penanda online/offline berdasarkan last_seen device                                        |Belum    |
| 10  | *last_seen Device*             | Update otomatis tiap kali device kirim data                                                |Belum    |
| 13  | Catatan Tindakan Alert         | Catatan teknisi atas penanganan alert                                                      |Belum    |
| 11  | Tabel Alert Log                | Menampilkan semua notifikasi peringatan (alert)                                            |Sudah    |
| 12  | Status Alert (dibaca, resolved)| Sistem penanda status alert dan tombol 'resolve'                                           |Belum    |
| 14  | Manajemen Device               | Tambah/edit/hapus device, validasi ID unik dan jenis sensor                                |Sebagian |
| 15  | Form Threshold Dinamis    ---  | Konfigurasi ambang batas sensor tiap device disimpan ke DB                                 |Belum    |
| 16  | Sinkronisasi Threshold ke MQTT | Pengambilan threshold dari DB untuk rule engine Python                                     |Belum    |
| 17  | Notifikasi WhatsApp            | Notifikasi alert via WhatsApp (sudah berjalan)                                             |Sudah    |
| 18  | Channel Telegram/Email         | Tambahan channel notifikasi selain WhatsApp                                                |Opsional |
| 19  | Konfigurasi Channel per Device | Pilihan channel notifikasi per device di backend                                           |Opsional |
| 20  | *Export Data Manual*           | Tombol download data sensor dan log dalam format CSV/ZIP                                   |Belum    |
| 21  | Jadwal Backup Otomatis    ---  | Backup data mingguan otomatis                                                              |Opsional |
| 22  | *Dashboard Ringkasan*          | Widget: total alert, device aktif, rata-rata suhu/pH/volume                                |Belum    |
| 23  | WebSocket Real-time Chart      | Integrasi WebSocket dengan Chart.js untuk data live                                        |Sudah    |
| 24  | Dropdown Filter Device         | Dropdown device untuk memilih data yang ditampilkan di chart/table                         |Sebagian |

> 🔄 *Status "Sudah" berarti sudah berjalan; "Sebagian" artinya ada fitur yang sudah dibuat namun belum lengkap; "Belum" artinya fitur belum ada sama sekali.*
> 🔄 *Fitur Berwarna => Prioritas pengembangan*
> 🔄 *Fitur yang disertai 3 strip(-) => Opsinal namun disarankan untuk dihadirkan*
> 🔄 *Fitur selain du kriteria diatas dan memiliki status belum adatau sebagian memiliki prioritas terakhir, dapat dilakukan jika terdapat waktu tersisa*


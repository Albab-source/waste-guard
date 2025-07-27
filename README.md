# Waste Guardian

![Waste Guardian Banner](https://via.placeholder.com/1200x400?text=Waste+Guardian)

**Waste Guardian** adalah sistem pemantauan limbah waktu nyata yang dirancang untuk membantu perusahaan migas dan industri lainnya dalam melacak dan merespons parameter kualitas air limbah seperti temperatur, pH, volume, dan COD. Proyek ini dibuat untuk submission Devpost Hackathon bertema "Time" dengan menekankan pentingnya pemantauan berbasis waktu dalam menjaga kualitas lingkungan.

## 🕒 About the Project

### 🎯 Apa yang Menginspirasi Kami

Waktu adalah hal krusial dalam pengelolaan limbah. Setiap keterlambatan dalam mendeteksi perubahan parameter bisa berdampak besar bagi lingkungan dan kesehatan. Karena itulah kami membangun sistem yang mengintegrasikan data sensor dan pemantauan waktu nyata untuk memudahkan deteksi dini dan pelaporan historis berbasis waktu.

### 📚 Apa yang Kami Pelajari

* Cara mengintegrasikan sensor (mock/real) dengan dashboard berbasis web
* Perancangan sistem backend REST API menggunakan Node.js dan MySQL
* Filtering dan ekspor data histori berdasarkan waktu, lokasi, dan device
* Validasi status alert limbah berdasarkan ambang batas

### 🛠️ Bagaimana Kami Membangunnya

1. Membuat backend server dengan Node.js dan Express
2. Merancang skema database di MySQL
3. Membuat frontend dengan HTML, CSS, JS + template AdminKit
4. Membuat sistem REST API `/history`, `/alert`, `/devices`, dll
5. Menghubungkan data dari sensor (mocked via Python) ke dashboard
6. Menyediakan fitur filtering historis berbasis tanggal, lokasi, dan device ID

### 🚧 Tantangan

* Menyusun arsitektur schema historis untuk query yang efisien
* Menjaga sinkronisasi antara data sensor dan data alert
* Membuat sistem export data CSV yang dinamis berdasarkan filter

## 🧰 Built With

* Frontend: HTML, CSS, JavaScript, AdminKit
* Backend: Node.js, Express.js
* Database: MySQL (XAMPP)
* Tools: Chart.js, DataTables, Fetch API

## 🌐 Try It Out

* [GitHub Repo](https://github.com/your-username/waste-guardian) *(isi dengan URL kamu nanti)*
* [Live Demo](https://your-link-if-available.com) *(opsional)*

## 🎥 Video Demo

* [Watch on YouTube](https://youtu.be/your-video-link) *(ganti dengan link video kamu)*

## 🪪 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

Dashboard UI is based on the [AdminKit template](https://adminkit.io/) by the AdminKit Authors. It is also licensed under the MIT License.

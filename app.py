from datetime import datetime  # Import modul datetime untuk manipulasi waktu dan tanggal
from flask import Flask, request, send_file, jsonify  # Import modul dari Flask untuk aplikasi web dan HTTP request
import json  # Import modul json untuk pengolahan data JSON
from flask_cors import CORS  # Import CORS untuk mengizinkan akses lintas domain
from flask import Flask, render_template  # Import render_template untuk render file HTML

app = Flask(__name__)  # Membuat objek Flask untuk aplikasi web
CORS(app)  # Aktifkan CORS untuk mengizinkan akses dari domain lain jika diperlukan

# Database simulasi untuk menyimpan data
database = [
    {
        'idx': 101,
        'suhu': 36,
        'humid': 36,
        'kecerahan': 25,
        'timestamp': '2010-09-18 07:23:48'
    },
    {
        'idx': 226,
        'suhu': 36,
        'humid': 36,
        'kecerahan': 27,
        'timestamp': '2011-05-02 12:29:34'
    },
]

# Menentukan nilai idx terbesar dari database untuk menambah idx baru
key = max([data['idx'] for data in database], default=0)

@app.route('/')  # Route untuk halaman utama
def index_html():
    return render_template('index.html')  # Menampilkan file index.html di browser

@app.route('/api/post', methods=['POST'])  # Route untuk menerima data POST
def post_data():
    global key  # Mengakses variabel key secara global
    json_data = request.get_json()  # Mendapatkan data JSON dari request

    # Validasi jika request bukan JSON atau JSON kosong
    if not request.is_json or not json_data:
        return jsonify({'message': 'data is not json'}), 400  # Mengirimkan response error jika data tidak valid

    key += 1  # Menambah nilai key untuk index baru
    data = {
        'idx': key,  # Index data baru
        'suhu': int(json_data['suhu']),  # Suhu yang diterima dari request
        'humid': int(json_data['kelembaban']),  # Kelembaban yang diterima dari request
        'kecerahan': int(json_data['kecerahan']),  # Kecerahan yang diterima dari request
        'timestamp': datetime.now().isoformat()  # Waktu saat data diterima dalam format ISO
    }

    database.append(data)  # Menambahkan data baru ke database

    return jsonify({'message': 'success'}), 200  # Mengirimkan response sukses

@app.route('/api/get', methods=['GET'])  # Route untuk mendapatkan data dengan metode GET
def get_data():
    data_suhu = [data['suhu'] for data in database]  # Mendapatkan daftar suhu dari database
    month_year_max = [
        {
            'month_year': datetime.fromisoformat(data['timestamp']).strftime('%m-%Y')  # Mengambil bulan dan tahun dari timestamp
        } for data in database
    ]

    # Menghitung suhu maksimum, minimum, dan rata-rata
    suhumax = max(data_suhu)
    suhumin = min(data_suhu)
    suhurata = sum(data_suhu) / len(data_suhu)

    data = {
        'suhumax': suhumax,  # Suhu maksimum
        'suhumin': suhumin,  # Suhu minimum
        'suhurata': suhurata,  # Suhu rata-rata
        'nilai_suhu_max_humid_max': database,  # Data lengkap database
        'month_year_max': month_year_max  # Daftar bulan dan tahun untuk setiap data
    }

    return jsonify(data)  # Mengirimkan data dalam format JSON

@app.route('/api/download', methods=['GET'])  # Route untuk mendownload data dalam format JSON
def download_json():
    file_path = "data.json"  # Menentukan nama file untuk data JSON
    with open(file_path, 'w') as f:  # Membuka file untuk menulis
        json.dump(database, f, indent=4)  # Menulis database ke file JSON dengan indentasi

    return send_file(file_path, as_attachment=True, download_name="data.json", mimetype='application/json')  # Mengirimkan file untuk diunduh

if __name__ == '__main__':  # Menjalankan aplikasi Flask
    app.run(host='0.0.0.0', port=5000, debug=True)  # Menjalankan server Flask di alamat 0.0.0.0 dan port 5000

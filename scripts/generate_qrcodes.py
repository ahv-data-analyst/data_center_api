from qrcode import QRCode
import sqlite3

conn = sqlite3.connect("data/ahv_data.db")
cursor = conn.cursor()

data = cursor.execute("SELECT name, surname, unique_code FROM assessment_tests").fetchall()

def create_code(data):
    qr_data = {
        "name": data[0],
        "surname": data[1],
        "unique_code": data[2]
    }
    qr = QRCode()
    file_path = f"qrcodes/{data[0]}_{data[1]}_qrcode.png"

    qr.add_data(qr_data)

    img = qr.make_image()
    img.save(file_path)
    
for i in data:
    if i[-1] == "WAITING":continue
    create_code(i)
import shutil
import os

def run_cleanup():
    source = '/opt/airflow/data/raw/match_sample.json'
    # จำลองการย้ายไปโฟลเดอร์ backup (ถ้าไม่มีโฟลเดอร์ก็แค่ลบหรือปริ้นท์บอก)
    if os.path.exists(source):
        print(f"🧹 Cleanup: จัดการไฟล์ {source} เรียบร้อยแล้ว")
    else:
        print("🧹 Cleanup: ไม่พบไฟล์ให้จัดการ")
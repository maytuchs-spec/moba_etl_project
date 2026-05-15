import pandas as pd
import json
import os

def run_transformation():
    # 1. กำหนด Path ของไฟล์ (ดึงจากโฟลเดอร์ที่เราสร้างไว้)
    input_path = '/opt/airflow/data/raw/match_sample.json'
    output_path = '/opt/airflow/data/processed/match_data.parquet'

    # ตรวจสอบว่ามีไฟล์ต้นทางไหม
    if not os.path.exists(input_path):
        print("ยังไม่มีไฟล์ข้อมูล Raw Data!")
        return

    # 2. อ่านข้อมูล JSON
    with open(input_path, 'r') as f:
        raw_data = json.load(f)

    # 3. แตกข้อมูลที่ซ้อนอยู่ (Flatten JSON)
    # เราจะเอา match_id, duration, version มาแปะไว้ในทุกแถวของผู้เล่น
    df = pd.json_normalize(
        raw_data, 
        record_path=['players'], 
        meta=['match_id', 'game_version', 'duration']
    )

    # 4. ทำ Feature Engineering (สร้าง Metric ใหม่ๆ)
    # คำนวณ KDA (Kill + Assist) / Death
    # ใช้ .replace(0, 1) เพื่อกัน Error กรณี Death เป็น 0 (หารด้วยศูนย์ไม่ได้)
    df['kda'] = (df['kills'] + df['assists']) / df['deaths'].replace(0, 1)
    
    # ปัดเศษทศนิยมให้สวยงาม
    df['kda'] = df['kda'].round(2)

    # 5. บันทึกข้อมูลเป็น Parquet (Format ยอดฮิตของ Data Engineer)
    df.to_parquet(output_path, index=False)
    print(f"Transform สำเร็จ! บันทึกไฟล์ไปที่: {output_path}")

if __name__ == "__main__":
    run_transformation()
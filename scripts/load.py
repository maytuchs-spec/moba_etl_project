import pandas as pd
from sqlalchemy import create_engine

def run_load():
    # 1. ระบุที่อยู่ไฟล์ Parquet
    file_path = '/opt/airflow/data/processed/match_data.parquet'
    
    # 2. อ่านข้อมูลขึ้นมา
    df = pd.read_parquet(file_path)
    
    # 3. เปลี่ยนจาก PostgreSQL มาใช้ SQLite แทน (ไม่ต้องใช้รหัสผ่าน)
    db_url = 'sqlite:////opt/airflow/data/processed/moba_database.db'
    engine = create_engine(db_url)
    
    # 4. โหลดข้อมูลลงตารางชื่อ 'match_statistics'
    df.to_sql('match_statistics', engine, if_exists='append', index=False)
    
    print(f"โหลดข้อมูล {len(df)} แถวลง Database สำเร็จ!")

if __name__ == "__main__":
    run_load()
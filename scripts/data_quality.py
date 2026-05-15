import pandas as pd

def run_dq_check():
    df = pd.read_parquet('/opt/airflow/data/processed/match_data.parquet')
    
    # เช็คว่ามีแถวข้อมูลไหม
    if len(df) == 0:
        raise ValueError("❌ DQ Check Failed: ข้อมูลว่างเปล่า!")
        
    # เช็คว่ามีค่า KDA ติดลบไหม (ซึ่งเป็นไปไม่ได้ในเกม)
    if (df['kda'] < 0).any():
        raise ValueError("❌ DQ Check Failed: พบค่า KDA ติดลบ!")
        
    print("✅ Data Quality Check: ผ่านฉลุย!")
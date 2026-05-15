import requests
import json
import os

# >>> เช็คบรรทัดนี้ ต้องมีคำว่า 'ion' ต่อท้ายให้เหมือนใน DAG เป๊ะๆ <<<
def run_extraction(): 
    api_url = "https://jsonplaceholder.typicode.com/posts/1"
    print(f"กำลังดึงข้อมูลจาก API: {api_url}...")
    
    # ... (โค้ดที่เหลือ) ...
    
    try:
        # 2. ส่งคำขอไปยัง API
        response = requests.get(api_url)
        response.raise_for_status() # ตรวจสอบว่าดึงสำเร็จไหม (ถ้า error จะกระโดดไปที่ except)
        
        # 3. แปลงข้อมูลที่ได้เป็น JSON
        raw_data = response.json()
        
        # --- (สมมติว่าเราดึงข้อมูล MOBA มาได้แล้ว) ---
        # ในที่นี้ผมจะสร้างข้อมูลจำลองเพื่อเอาไปใช้ต่อในโปรเจกต์เดิมของเรา
        moba_sample_data = [
            {
                "match_id": "M999",
                "game_version": "1.9.01",
                "duration": 1100,
                "players": [
                    {"hero_id": 5, "hero_name": "Miya", "kills": 10, "deaths": 1, "assists": 5, "win": True},
                    {"hero_id": 10, "hero_name": "Akai", "kills": 1, "deaths": 5, "assists": 15, "win": True}
                ]
            }
        ]
        
        # 4. บันทึกข้อมูลที่ดึงมาได้ลงในโฟลเดอร์ data/raw
        output_path = '/opt/airflow/data/raw/match_sample.json'
        with open(output_path, 'w') as f:
            json.dump(moba_sample_data, f, indent=4)
            
        print(f"✅ Extract สำเร็จ! บันทึกข้อมูลดิบไปที่: {output_path}")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการ Extract: {e}")

if __name__ == "__main__":
    run_extraction()
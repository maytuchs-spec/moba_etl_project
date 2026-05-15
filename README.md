# 🎮 MOBA E-Sport End-to-End Data Pipeline

## 📌 Project Overview (หัวข้อเรื่องที่ทำ)
โปรเจกต์นี้คือการสร้าง **Automated Data Pipeline** แบบ End-to-End สำหรับจัดการข้อมูลสถิติการแข่งขัน E-Sport (เกมแนว MOBA) โดยแก้ปัญหาการนำข้อมูลดิบจาก API ที่มีความซับซ้อน (Nested JSON) มาผ่านกระบวนการ ETL เพื่อทำความสะอาด คำนวณสถิติสำคัญ (เช่น KDA) และจัดเก็บลงฐานข้อมูล เพื่อนำไปแสดงผลบน Dashboard ให้นักวิเคราะห์และทีมโค้ชนำไปใช้งานต่อได้ทันที

---

## 🏗️ Architecture & Workflow (สถาปัตยกรรมและลำดับการทำงาน)
ระบบถูกออกแบบให้ทำงานอัตโนมัติบน Docker Container โดยมี Workflow เรียงลำดับ 5 ขั้นตอนดังนี้:

1. **Extract:** โหลดข้อมูลการแข่งขันล่าสุดผ่าน API และจัดเก็บเป็นไฟล์ JSON ในรูปแบบ Raw Data
2. **Transform:** ใช้ Pandas แปลงโครงสร้างข้อมูล (Flatten) จาก JSON ให้เป็นแบบตาราง (Relational) และคำนวณ Feature ใหม่ เช่น KDA (Kill/Death/Assist) ก่อนบันทึกเป็นไฟล์ Parquet เพื่อประสิทธิภาพในการอ่าน
3. **Data Quality Check:** ตรวจสอบความถูกต้องของข้อมูล (Validation) เช่น ตรวจหาค่า Null หรือค่าสถิติที่ติดลบ เพื่อป้องกันข้อมูลเน่า (Garbage Data) เข้าสู่ระบบ
4. **Load:** นำข้อมูลที่ผ่านการตรวจสอบแล้ว โหลดเข้าสู่ฐานข้อมูล SQLite
5. **Cleanup:** ลบไฟล์ชั่วคราวที่เกิดระหว่างกระบวนการ เพื่อบริหารพื้นที่จัดเก็บข้อมูลให้มีประสิทธิภาพสูงสุด

---

## 💻 Tech Stack (เทคโนโลยีที่ใช้)
* **Orchestration:** Apache Airflow
* **Data Processing:** Python (Pandas)
* **Storage:** SQLite
* **Data Format:** Parquet, JSON
* **Visualization:** Streamlit, Plotly
* **Infrastructure:** Docker, Docker Compose

---

## 🚀 How to Run (วิธีรันโปรเจกต์)

**1. Clone Repository:**
```bash
git clone [https://github.com/maytuchs-spec/moba_etl_project.git](https://github.com/maytuchs-spec/moba_etl_project.git)
cd moba_etl_project
```

**2. Start the Pipeline Infrastructure:**
รันคำสั่งเพื่อเปิดใช้งาน Airflow และระบบหลังบ้าน
```bash
docker-compose up -d
```

**3. Execute the ETL Pipeline:**
* เข้าไปที่ `http://localhost:8080` (User: `airflow` / Pass: `airflow`)
* กดเปิดใช้งาน (Unpause) และสั่ง Trigger DAG ที่ชื่อ `moba_esport_etl` เพื่อเริ่มกระบวนการดึงและแปลงข้อมูล

---

## 📊 Run Dashboard (วิธีรันแดชบอร์ด)
หลังจากที่ Pipeline ทำงานเสร็จและมีข้อมูลใน Database แล้ว สามารถรัน Dashboard เพื่อดูผลลัพธ์ได้ดังนี้:

1. **รันคำสั่ง Streamlit ผ่าน Docker:**
```bash
docker run -it --rm -p 8501:8501 -v "${PWD}:/app" -w /app python:3.9 bash -c "pip install streamlit pandas plotly sqlalchemy && python -m streamlit run dashboard.py --server.address 0.0.0.0"
```

2. **เข้าดูผลลัพธ์:**
* เปิด Browser ไปที่ `http://localhost:8501`
* คุณจะพบกับหน้าจอสรุปสถิติ Win Rate, KDA และกราฟวิเคราะห์ Performance ของฮีโร่และผู้เล่น

---

## 📂 Project Structure (โครงสร้างโปรเจกต์)
```text
moba_etl_project/
├── dags/
│   └── moba_etl_dag.py        # ไฟล์คุมลำดับงาน (DAG)
├── scripts/                   # ไฟล์สคริปต์การทำงานแยกส่วน
│   ├── extract.py             # ดึงข้อมูลจาก API
│   ├── transform.py           # แปลงข้อมูลและคำนวณ KDA
│   ├── data_quality.py        # ตรวจสอบความถูกต้องของข้อมูล
│   └── load.py                # โหลดข้อมูลลง SQLite
├── data/                      # โฟลเดอร์เก็บไฟล์ JSON และ Parquet
├── moba_database.db           # ฐานข้อมูล SQLite ปลายทาง
├── dashboard.py               # ไฟล์สำหรับรันหน้า Dashboard
├── docker-compose.yml         # การตั้งค่าระบบ Docker
└── README.md                  # เอกสารประกอบโปรเจกต์
```

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow')
from scripts.extract import run_extraction
from scripts.transform import run_transformation
from scripts.data_quality import run_dq_check  # <--- เพิ่ม
from scripts.load import run_load
from scripts.cleanup import run_cleanup       # <--- เพิ่ม

default_args = {
    'owner': 'boss',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'moba_esport_pipeline_V3_Pro',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    # 1. ดึงข้อมูล
    extract_task = PythonOperator(task_id='extract_data', python_callable=run_extraction)

    # 2. แปลงข้อมูล
    transform_task = PythonOperator(task_id='transform_data', python_callable=run_transformation)

    # 3. ตรวจสอบคุณภาพ (เพิ่มเข้ามา)
    dq_task = PythonOperator(task_id='data_quality_check', python_callable=run_dq_check)

    # 4. โหลดลง Database
    load_task = PythonOperator(task_id='load_to_db', python_callable=run_load)

    # 5. ทำความสะอาด (เพิ่มเข้ามา)
    cleanup_task = PythonOperator(task_id='cleanup_files', python_callable=run_cleanup)

    # จัดลำดับการรัน 5 ขั้นตอนรวด!
    extract_task >> transform_task >> dq_task >> load_task >> cleanup_task
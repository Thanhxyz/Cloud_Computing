from sqlalchemy import create_engine, text
import pandas as pd
import os

# 🚀 Kết nối đến PostgreSQL (Cập nhật thông tin của bạn)
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"
engine = create_engine(DATABASE_URL)
# Kết nối đến PostgreSQL
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Kết nối PostgreSQL thành công!")
        
        # Truy vấn bảng `bao_cao_kqkd`
        query = text("SELECT * FROM bao_cao_kqkd")
        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        # Kiểm tra dữ liệu
        if not df.empty:
            print("✅ Dữ liệu đã được truy xuất thành công!")
            print(df.head())  # Hiển thị 5 dòng đầu tiên
        else:
            print("⚠️ Bảng `bao_cao_kqkd` không có dữ liệu.")
except Exception as e:
    print(f"❌ Lỗi kết nối PostgreSQL: {e}")
    print("⚠️ Vui lòng kiểm tra lại cấu hình kết nối.")

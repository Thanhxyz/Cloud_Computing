import pandas as pd
from sqlalchemy import create_engine

# Thay thế bằng Connection String của bạn
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"

# Tạo kết nối đến PostgreSQL
engine = create_engine(DATABASE_URL)

# Danh sách các bảng và file CSV tương ứng
files = {
    "doanh_nghiep": "clean_data/DoanhNghiep_Cleaned.csv",
    "chi_so_tai_chinh": "clean_data/ChiSoTaiChinh_Cleaned.csv",
    "bang_can_doi_ke_toan": "clean_data/BangCanDoiKeToan_Cleaned.csv",
    "bao_cao_kqkd": "clean_data/BaoCaoKetQuaKinhDoanh_Cleaned.csv"
}

# Lặp qua từng file và nhập vào PostgreSQL
for table, file_path in files.items():
    try:
        df = pd.read_csv(file_path)  # Đọc file CSV vào DataFrame
        df.to_sql(table, engine, if_exists="append", index=False)  # Nhập dữ liệu vào PostgreSQL
        print(f"✅ Dữ liệu bảng {table} đã được nhập thành công!")
    except Exception as e:
        print(f"❌ Lỗi khi nhập bảng {table}: {e}")

print("🎉 Hoàn thành nhập dữ liệu!")

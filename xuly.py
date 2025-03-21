import os
import pandas as pd
import numpy as np  # Import numpy để dùng log1p
import psycopg2
from sqlalchemy import create_engine

# Thông tin kết nối PostgreSQL
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"
TABLE_NAME = "bao_cao_kqkd"
OUTPUT_DIR = "data_huanluyen"
OUTPUT_FILE = "data.csv"

# Kết nối đến PostgreSQL
engine = create_engine(DATABASE_URL)
query = f"SELECT * FROM {TABLE_NAME};"

# Đọc dữ liệu vào DataFrame
df = pd.read_sql(query, engine)

# Xử lý dữ liệu
def process_data(df):
    # Chuyển đổi tất cả các cột số sang kiểu số, lỗi sẽ thành NaN
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    
    # Loại bỏ dòng có tất cả giá trị NaN (tức là toàn bộ dữ liệu không hợp lệ)
    df_numeric = df_numeric.dropna(how='all')
    
    # Loại bỏ dòng có ít nhất một giá trị rỗng hoặc bằng 0
    df_numeric = df_numeric.replace(0, np.nan).dropna()
    
    # Loại bỏ các dòng có tất cả giá trị trống (ví dụ như AAA,,,,,,)
    df_numeric = df_numeric.dropna(how='all', axis=1)
    
    # Kiểm tra giá trị âm bất thường
    if 'loinhuansauthue' in df_numeric.columns:
        df_numeric = df_numeric[df_numeric['loinhuansauthue'] > -1e12]  # Loại bỏ doanh nghiệp lỗ quá lớn
    
    # Xử lý outlier bằng IQR
    Q1 = df_numeric.quantile(0.25)
    Q3 = df_numeric.quantile(0.75)
    IQR = Q3 - Q1
    df_numeric = df_numeric[~((df_numeric < (Q1 - 1.5 * IQR)) | (df_numeric > (Q3 + 1.5 * IQR))).any(axis=1)]
    
    # Chuẩn hóa dữ liệu (Log transformation để giảm chênh lệch đơn vị)
    df_numeric = df_numeric.apply(lambda x: np.log1p(x))
    
    # Ghép lại với các cột không phải số
    df_processed = df.copy()
    df_processed[df_numeric.columns] = df_numeric
    
    return df_processed

# Áp dụng xử lý
df_clean = process_data(df)

# Tạo thư mục nếu chưa tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lưu file CSV
df_clean.to_csv(os.path.join(OUTPUT_DIR, OUTPUT_FILE), index=False)

print(f"✅ Dữ liệu đã được xử lý và lưu tại {OUTPUT_DIR}/{OUTPUT_FILE}")
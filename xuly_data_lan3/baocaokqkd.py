import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Đọc dữ liệu từ file CSV
file_path = "clean_data/BaoCaoKetQuaKinhDoanh_Cleaned.csv"
df = pd.read_csv(file_path)

# Chuyển đổi đơn vị về cùng dạng phù hợp
df["doanhthuthuan"] = df["doanhthuthuan"] / 1e12   # Đưa về đơn vị nghìn tỷ
df["loinhuangop"] = df["loinhuangop"] / 1e12       # Đưa về đơn vị nghìn tỷ
df["loinhuanthuan"] = df["loinhuanthuan"] / 1e12   # Đưa về đơn vị nghìn tỷ
df["loinhuantruocthue"] = df["loinhuantruocthue"] / 1e12   # Đưa về đơn vị nghìn tỷ
df["loinhuansauthue"] = df["loinhuansauthue"] / 1e12   # Đưa về đơn vị nghìn tỷ
df["laitrencophieu"] = df["laitrencophieu"] / 1000     # Đưa về đơn vị nghìn đồng/cổ phiếu

# Áp dụng Min-Max Scaling
scaler = MinMaxScaler()
columns_to_scale = df.columns[1:]  # Bỏ cột 'mack'
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Lưu vào thư mục mới
output_dir = "clean_data3"
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
output_file = os.path.join(output_dir, "BaoCaoKetQuaKinhDoanh_Cleaned_3.csv")
df.to_csv(output_file, index=False)

print(f"✅ Dữ liệu đã chuẩn hóa và lưu tại: {output_file}")

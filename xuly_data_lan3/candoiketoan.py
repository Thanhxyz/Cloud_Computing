import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Đọc dữ liệu từ file CSV
file_path = "clean_data/BangCanDoiKeToan_Cleaned.csv"
df = pd.read_csv(file_path)

# Chuyển đổi đơn vị về nghìn tỷ đồng
df["taisannganhan"] = df["taisannganhan"] / 1e12
df["taisandaihan"] = df["taisandaihan"] / 1e12
df["tongtaisan"] = df["tongtaisan"] / 1e12
df["nophaitra"] = df["nophaitra"] / 1e12
df["vonchusohuu"] = df["vonchusohuu"] / 1e12

# Áp dụng Min-Max Scaling
scaler = MinMaxScaler()
columns_to_scale = df.columns[1:]  # Bỏ cột 'mack'
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Lưu vào thư mục mới
output_dir = "clean_data3"
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
output_file = os.path.join(output_dir, "BangCanDoiKeToan_Cleaned_3.csv")
df.to_csv(output_file, index=False)

print(f"✅ Dữ liệu đã chuẩn hóa và lưu tại: {output_file}")

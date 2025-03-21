import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Đọc dữ liệu từ file CSV
file_path = "clean_data/DoanhNghiep_Cleaned.csv"
df = pd.read_csv(file_path)

# Chuyển đổi đơn vị vốn hóa về nghìn tỷ đồng
df["vonhoa"] = df["vonhoa"] / 1e12

# Áp dụng Min-Max Scaling
scaler = MinMaxScaler()
df["vonhoa"] = scaler.fit_transform(df[["vonhoa"]])

# Lưu vào thư mục mới
output_dir = "clean_data3"
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
output_file = os.path.join(output_dir, "DoanhNghiep_Cleaned_3.csv")
df.to_csv(output_file, index=False)

print(f"✅ Dữ liệu đã chuẩn hóa và lưu tại: {output_file}")

import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler

# Đọc dữ liệu
file_path = "clean_data/ChiSoTaiChinh_Cleaned.csv"
df = pd.read_csv(file_path)

# Chuyển đổi đơn vị để chuẩn hóa
df["eps"] = df["eps"] / 1000  # Đưa về nghìn đồng/cổ phiếu
df["roa"] = df["roa"] / 1e12  # Đưa về mức dễ đọc hơn
df["roe"] = df["roe"] / 1e12  # Đưa về mức dễ đọc hơn

# Áp dụng Min-Max Scaling
scaler = MinMaxScaler()
columns_to_scale = df.columns[1:]  # Bỏ cột 'mack' (Mã CK)
df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])

# Lưu vào thư mục mới
output_dir = "clean_data3"
os.makedirs(output_dir, exist_ok=True)  # Tạo thư mục nếu chưa có
output_file = os.path.join(output_dir, "ChiSoTaiChinh_Cleaned_3.csv")
df.to_csv(output_file, index=False)

print(f"✅ Dữ liệu đã chuẩn hóa và lưu tại: {output_file}")

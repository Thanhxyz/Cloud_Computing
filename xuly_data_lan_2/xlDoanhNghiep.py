import pandas as pd

# Đọc file CSV
df = pd.read_csv("DoanhNghiep.csv")

# Chuyển đổi cột 'VonHoa' sang kiểu số để xử lý
# Lưu ý: Nếu có lỗi, có thể cần xử lý dữ liệu dạng text bị lẫn trong cột này
df["VonHoa"] = pd.to_numeric(df["VonHoa"], errors='coerce')

# Lọc bỏ các hàng có VonHoa bằng 0
df_filtered = df[df["VonHoa"] > 0]

# Lưu vào file CSV mới
df_filtered.to_csv("DoanhNghiep_filtered.csv", index=False)

print("Đã lọc và lưu dữ liệu thành công!")
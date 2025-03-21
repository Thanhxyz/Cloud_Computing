import pandas as pd

# Đọc file DoanhNghiep_filtered.csv
df_doanh_nghiep = pd.read_csv("DoanhNghiep_filtered.csv")

# Đọc file ChiSoTaiChinh.csv
df_chiso = pd.read_csv("ChiSoTaiChinh.csv")

# Lọc các dòng trong df_chiso có MaCK thuộc df_doanh_nghiep
df_filtered = df_chiso[df_chiso["MaCk"].isin(df_doanh_nghiep["MaCK"])].copy()

# Lưu kết quả vào file mới
df_filtered.to_csv("ChiSoTaiChinh_filtered.csv", index=False)

print("Đã lọc và lưu dữ liệu thành công!")

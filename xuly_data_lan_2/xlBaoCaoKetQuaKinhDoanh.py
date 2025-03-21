import pandas as pd

# Đọc file DoanhNghiep_filtered.csv
df_doanh_nghiep = pd.read_csv("DoanhNghiep_filtered.csv")

# Đọc file BaoCaoKetQuaKinhDoanh.csv
df_bckqkd = pd.read_csv("BaoCaoKetQuaKinhDoanh.csv")

# Lọc các dòng trong df_bckqkd có MaCK thuộc df_doanh_nghiep
df_filtered = df_bckqkd[df_bckqkd["MaCK"].isin(df_doanh_nghiep["MaCK"])].copy()

# Xóa cột STT nếu tồn tại
if "STT" in df_filtered.columns:
    df_filtered.drop(columns=["STT"], inplace=True)

# Lưu kết quả vào file mới
df_filtered.to_csv("BaoCaoKetQuaKinhDoanh_filtered.csv", index=False)

print("Đã lọc, xóa cột STT và lưu dữ liệu thành công!")
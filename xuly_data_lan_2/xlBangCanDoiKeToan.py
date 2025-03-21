import pandas as pd

# Đọc file DoanhNghiep_filtered.csv
doanh_nghiep_df = pd.read_csv("DoanhNghiep_filtered.csv", header=None, names=["MaCK", "TenCongTy", "SanGiaoDich", "VonHoa"])

# Đọc file BangCanDoiKeToan.csv
bang_can_doi_df = pd.read_csv("BangCanDoiKeToan.csv")

# Lọc dữ liệu chỉ giữ lại các dòng có MaCK trong danh sách doanh nghiệp
filtered_df = bang_can_doi_df[bang_can_doi_df["MaCK"].isin(doanh_nghiep_df["MaCK"])].copy()

# Lưu vào file mới
filtered_df.to_csv("BangCanDoiKeToan_filtered.csv", index=False)

print("Đã lọc và lưu file BangCanDoiKeToan_filtered.csv thành công!")

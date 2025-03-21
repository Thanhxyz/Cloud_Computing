import pandas as pd
import os

# Tạo thư mục lưu dữ liệu sạch nếu chưa tồn tại
output_dir = "clean_data"
os.makedirs(output_dir, exist_ok=True)

# Định nghĩa hàm chuẩn hóa số liệu (loại bỏ dấu phân tách hàng nghìn)
def clean_numeric(value):
    if isinstance(value, str):
        value = value.replace('.', '').replace(',', '.')  # Loại bỏ dấu phân cách hàng nghìn
    try:
        return float(value)
    except ValueError:
        return None  # Nếu lỗi, trả về None để xử lý sau

# Xử lý bảng DoanhNghiep_filtered.csv
df_doanh_nghiep = pd.read_csv("DoanhNghiep_filtered.csv")
df_doanh_nghiep["VonHoa"] = df_doanh_nghiep["VonHoa"].apply(clean_numeric)
df_doanh_nghiep.to_csv(os.path.join(output_dir, "DoanhNghiep_Cleaned.csv"), index=False)

# Xử lý bảng BangCanDoiKeToan_filtered.csv
df_can_doi = pd.read_csv("BangCanDoiKeToan_filtered.csv")
for col in ["TaiSanNganHan", "TaiSanDaiHan", "TongTaiSan", "NoPhaiTra", "VonChuSoHuu"]:
    df_can_doi[col] = df_can_doi[col].apply(clean_numeric)
df_can_doi.to_csv(os.path.join(output_dir, "BangCanDoiKeToan_Cleaned.csv"), index=False)

# Xử lý bảng BaoCaoKetQuaKinhDoanh_filtered.csv
df_kqkd = pd.read_csv("BaoCaoKetQuaKinhDoanh_filtered.csv")
for col in ["DoanhThuThuan", "LoiNhuanGop", "LoiNhuanThuan", "LoiNhuanTruocThue", "LoiNhuanSauThue", "LaiTrenCoPhieu"]:
    df_kqkd[col] = df_kqkd[col].apply(clean_numeric)
df_kqkd.to_csv(os.path.join(output_dir, "BaoCaoKetQuaKinhDoanh_Cleaned.csv"), index=False)

# Xử lý bảng ChiSoTaiChinh_filtered.csv
df_chi_so = pd.read_csv("ChiSoTaiChinh_filtered.csv")
for col in ["EPS", "PE", "PB", "ROA", "ROE", "TangTruongDoanhThuThuan", "TangTruongLoiNhuanGop", "TangTruongTongTaiSan"]:
    df_chi_so[col] = df_chi_so[col].apply(clean_numeric)
df_chi_so.to_csv(os.path.join(output_dir, "ChiSoTaiChinh_Cleaned.csv"), index=False)

print(f"Dữ liệu đã được làm sạch và lưu vào thư mục '{output_dir}/'!")

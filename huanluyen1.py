import psycopg2
import pandas as pd
import joblib
import boto3
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# ✅ Cấu hình AWS S3
AWS_ACCESS_KEY = "AKIA2YICARIK4JD7HOZX"
AWS_SECRET_KEY = "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"
AWS_BUCKET_NAME = "my-hose-data"
S3_FOLDER_CSV = "data_model/"    # 📁 Nơi lưu file CSV
S3_FOLDER_MODELS = "models/"     # 📁 Nơi lưu mô hình

# Khởi tạo S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# ✅ Thông tin kết nối PostgreSQL
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"
TABLE_NAME = "bao_cao_kqkd"  

# ✅ Kết nối và lấy dữ liệu từ PostgreSQL
def get_data_from_postgres():
    conn = psycopg2.connect(DATABASE_URL)
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_data_from_postgres()

# ✅ Tiền xử lý dữ liệu
features = ['doanhthuthuan', 'loinhuangop', 'loinhuanthuan', 'loinhuantruocthue', 'loinhuansauthue', 'laitrencophieu']
df_features = df[features].dropna()

# ✅ Chuẩn hóa dữ liệu
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_features)

# ✅ Tạo mô hình Isolation Forest
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(df_scaled)

# ✅ Lưu mô hình tạm thời
MODEL_FILE = "isolation_forest_model.pkl"
joblib.dump(model, MODEL_FILE)
print(f"✅ Mô hình đã được huấn luyện và lưu tại {MODEL_FILE}")

# ✅ Đẩy mô hình lên AWS S3 (📁 `models/`)
try:
    s3.upload_file(MODEL_FILE, AWS_BUCKET_NAME, S3_FOLDER_MODELS + MODEL_FILE)
    print(f"🚀 Đã upload {MODEL_FILE} lên s3://{AWS_BUCKET_NAME}/{S3_FOLDER_MODELS}{MODEL_FILE}")
except Exception as e:
    print(f"❌ Lỗi khi upload {MODEL_FILE}: {str(e)}")

# ✅ Dự đoán các bất thường
predictions = model.predict(df_scaled)
df['is_anomaly'] = predictions

# ✅ Lọc các doanh nghiệp có báo cáo tài chính bất thường
anomalies = df[df['is_anomaly'] == -1]
ANOMALY_FILE = "anomalous_companies.csv"
anomalies.to_csv(ANOMALY_FILE, index=False)

print("\n🚨 Các doanh nghiệp có báo cáo tài chính bất thường:")
print(anomalies[['mack', 'doanhthuthuan', 'loinhuanthuan', 'loinhuansauthue', 'is_anomaly']])

# ✅ Đẩy file anomalies lên AWS S3 (📁 `data_model/`)
try:
    s3.upload_file(ANOMALY_FILE, AWS_BUCKET_NAME, S3_FOLDER_CSV + ANOMALY_FILE)
    print(f"🚀 Đã upload {ANOMALY_FILE} lên s3://{AWS_BUCKET_NAME}/{S3_FOLDER_CSV}{ANOMALY_FILE}")
except Exception as e:
    print(f"❌ Lỗi khi upload {ANOMALY_FILE}: {str(e)}")

# ✅ Kiểm tra lại mô hình đã lưu từ S3
model_loaded = joblib.load(MODEL_FILE)
predictions_loaded = model_loaded.predict(df_scaled)
print("\n✅ Dự đoán từ mô hình đã tải lại:")
print(predictions_loaded)

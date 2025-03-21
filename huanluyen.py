import os
import boto3
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sqlalchemy import create_engine

# ✅ Cấu hình AWS S3
AWS_ACCESS_KEY = "AKIA2YICARIK4JD7HOZX"
AWS_SECRET_KEY = "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"
AWS_BUCKET_NAME = "my-hose-data"
S3_FOLDER_CSV = "data_model/"
S3_FOLDER_MODELS = "models/"

# Khởi tạo S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# ✅ Thông tin kết nối PostgreSQL
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"
TABLE_NAME = "bao_cao_kqkd"
OUTPUT_FILE = "data.csv"

# ✅ Kết nối đến PostgreSQL và tải dữ liệu
engine = create_engine(DATABASE_URL)
query = f"SELECT * FROM {TABLE_NAME};"
df = pd.read_sql(query, engine)

# ✅ Xử lý dữ liệu
def process_data(df):
    df_numeric = df.apply(pd.to_numeric, errors='coerce')
    df_numeric = df_numeric.dropna(how='all')
    df_numeric.replace(0, np.nan, inplace=True)
    df_numeric.fillna(df_numeric.mean(), inplace=True)
    df_processed = df.copy()
    df_processed[df_numeric.columns] = df_numeric
    return df_processed

df_clean = process_data(df)

# ✅ Lưu file CSV tạm thời
df_clean.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Dữ liệu đã được xử lý và lưu tạm thời tại {OUTPUT_FILE}")

# ✅ Đẩy CSV lên AWS S3 (📁 `data_model/`)
try:
    s3.upload_file(OUTPUT_FILE, AWS_BUCKET_NAME, S3_FOLDER_CSV + OUTPUT_FILE)
    print(f"🚀 Đã upload {OUTPUT_FILE} lên s3://{AWS_BUCKET_NAME}/{S3_FOLDER_CSV}{OUTPUT_FILE}")
except Exception as e:
    print(f"❌ Lỗi khi upload {OUTPUT_FILE}: {str(e)}")

# ✅ Huấn luyện mô hình và upload lên `models/`
def train_and_upload_models(df):
    features = ['doanhthuthuan', 'loinhuangop', 'loinhuanthuan', 'loinhuantruocthue']
    target = 'loinhuansauthue'
    
    df = df.dropna(subset=[target])
    
    if df.empty:
        print("❌ Dữ liệu không đủ để huấn luyện mô hình.")
        return
    
    X = df[features]
    y = df[target]
    
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    y = y.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    if len(X) < 2 or len(y) < 2:
        print("❌ Dữ liệu không đủ để chia train/test.")
        return
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    results = []
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        model_filename = f"{name.replace(' ', '_').lower()}.pkl"
        joblib.dump(model, model_filename)
        
        # ✅ Upload mô hình lên S3 (📁 `models/`)
        try:
            s3.upload_file(model_filename, AWS_BUCKET_NAME, S3_FOLDER_MODELS + model_filename)
            print(f"🚀 Đã upload {model_filename} lên s3://{AWS_BUCKET_NAME}/{S3_FOLDER_MODELS}{model_filename}")
        except Exception as e:
            print(f"❌ Lỗi khi upload {model_filename}: {str(e)}")

        results.append({"model": name, "MAE": mae, "R2": r2})
    
    # ✅ Huấn luyện mô hình Stacking
    estimators = [("lr", models["Linear Regression"]), ("rf", models["Random Forest"])]
    stacking_model = StackingRegressor(estimators=estimators, final_estimator=LinearRegression())
    stacking_model.fit(X_train, y_train)
    y_pred_stack = stacking_model.predict(X_test)
    
    mae_stack = mean_absolute_error(y_test, y_pred_stack)
    r2_stack = r2_score(y_test, y_pred_stack)
    
    stacking_model_filename = "stacking_model.pkl"
    joblib.dump(stacking_model, stacking_model_filename)
    
    # ✅ Upload mô hình Stacking lên S3
    try:
        s3.upload_file(stacking_model_filename, AWS_BUCKET_NAME, S3_FOLDER_MODELS + stacking_model_filename)
        print(f"🚀 Đã upload {stacking_model_filename} lên s3://{AWS_BUCKET_NAME}/{S3_FOLDER_MODELS}{stacking_model_filename}")
    except Exception as e:
        print(f"❌ Lỗi khi upload {stacking_model_filename}: {str(e)}")
    
    results.append({"model": "Stacking Regressor", "MAE": mae_stack, "R2": r2_stack})
    
    best_model = min(results, key=lambda x: x['R2'])
    print(f"🏆 Mô hình tốt nhất: {best_model['model']} với R²={best_model['R2']:.4f}")

train_and_upload_models(df_clean)
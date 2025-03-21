import pandas as pd
from xuly import process_data  # import hàm process_data từ file code của bạn

data = {'doanhthuthuan': [100, 200, 'abc'], 'loinhuangop': [50, 60, 0]}  # Dữ liệu mẫu
df = pd.DataFrame(data)

# Gọi hàm process_data để xử lý dữ liệu
df_processed = process_data(df)

# In kết quả để kiểm tra
print(df_processed)

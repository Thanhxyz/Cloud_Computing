import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib

# 🚀 Tải các mô hình đã huấn luyện
stacking_model = joblib.load('model/stacking_model.pkl')
random_forest_model = joblib.load('model/random_forest.pkl')
linear_regression_model = joblib.load('model/linear_regression.pkl')

# 🎨 Thiết lập giao diện
st.set_page_config(page_title="📊 Dự Báo Lợi Nhuận Doanh Nghiệp", layout="wide")

# 🔥 Tiêu đề chính
st.title("🚀 Dự Báo Lợi Nhuận Sau Thuế Của Doanh Nghiệp")

# 📌 Nhập Dữ Liệu Doanh Nghiệp
doanh_thu = st.number_input("Doanh thu thuần", step=0.01)  
loi_nhuan_huan_op = st.number_input("Lợi nhuận gộp", step=0.01)  
loi_nhuan_thuan = st.number_input("Lợi nhuận thuần", step=0.01)  
loi_nhuan_truoc_thue = st.number_input("Lợi nhuận trước thuế", step=0.01)  

# 📌 Chọn mô hình dự đoán
model_choice = st.selectbox("Chọn mô hình dự đoán", ["Stacking Model", "Random Forest", "Linear Regression"])

# Chọn mô hình
def load_model(model_name):
    model_dict = {
        "Stacking Model": stacking_model,
        "Random Forest": random_forest_model,
        "Linear Regression": linear_regression_model
    }
    return model_dict[model_name]

model = load_model(model_choice)

# Dự đoán khi người dùng nhấn nút
if st.button("Dự Báo Lợi Nhuận Sau Thuế"):
    # Chuẩn bị dữ liệu đầu vào cho mô hình
    input_data = np.array([[doanh_thu, loi_nhuan_huan_op, loi_nhuan_thuan, loi_nhuan_truoc_thue]])
    
    # Dự đoán
    result = model.predict(input_data)
    
    # Hiển thị kết quả
    st.subheader("Dự Báo Lợi Nhuận Sau Thuế:")
    st.write(f"Lợi nhuận sau thuế dự đoán: {result[0]:.2f} VNĐ")
    
    # 📊 Biểu đồ trực quan cho dữ liệu đã nhập
    st.subheader("📊 Biểu Đồ Phân Tích")

    # Biểu đồ Doanh thu, Lợi nhuận gộp, Lợi nhuận thuần
    df_input = pd.DataFrame({
        "Chỉ Số": ["Doanh thu", "Lợi nhuận gộp", "Lợi nhuận thuần"],
        "Giá trị (VNĐ)": [doanh_thu, loi_nhuan_huan_op, loi_nhuan_thuan]
    })

    fig_input = go.Figure()
    fig_input.add_trace(go.Bar(
        x=df_input["Chỉ Số"],
        y=df_input["Giá trị (VNĐ)"],
        marker_color=["blue", "green", "orange"]
    ))
    fig_input.update_layout(title="📊 Biểu Đồ Phân Tích", xaxis_title="Chỉ số", yaxis_title="Giá trị (VNĐ)", template="plotly_white")
    st.plotly_chart(fig_input)

    # 📊 Biểu đồ Lợi nhuận trước thuế và sau thuế
    st.subheader("📈 Biểu Đồ So Sánh Lợi Nhuận Trước và Sau Thuế")

    fig_profit = go.Figure()
    fig_profit.add_trace(go.Bar(
        x=["Lợi nhuận trước thuế", "Lợi nhuận sau thuế"],
        y=[loi_nhuan_truoc_thue, result[0]],
        marker_color=["blue", "green"],
        text=[f"{loi_nhuan_truoc_thue:.2f}", f"{result[0]:.2f}"],
        textposition='outside'
    ))
    fig_profit.update_layout(title="📊 So Sánh Lợi Nhuận Trước & Sau Thuế", xaxis_title="Loại lợi nhuận", yaxis_title="Giá trị (VNĐ)", template="plotly_white")
    st.plotly_chart(fig_profit)

    # 📈 Biểu đồ thể hiện tỷ lệ lợi nhuận gộp và lợi nhuận thuần
    st.subheader("📊 Biểu Đồ Tỷ Lệ Lợi Nhuận Gộp và Lợi Nhuận Thuần")

    df_margin = pd.DataFrame({
        "Chỉ số": ["Lợi nhuận gộp", "Lợi nhuận thuần"],
        "Tỷ lệ (%)": [(loi_nhuan_huan_op / doanh_thu) * 100, (loi_nhuan_thuan / doanh_thu) * 100]
    })

    fig_margin = px.bar(df_margin, x="Chỉ số", y="Tỷ lệ (%)", color="Chỉ số", text="Tỷ lệ (%)", title="📊 Tỷ Lệ Lợi Nhuận Gộp và Lợi Nhuận Thuần")
    st.plotly_chart(fig_margin)

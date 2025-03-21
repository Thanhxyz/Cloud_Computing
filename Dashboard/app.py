import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import joblib

# -----------------------------------
# Phần cấu hình chung (thông tin kết nối, tải mô hình, ...)
# -----------------------------------
st.set_page_config(page_title="📊 Ứng Dụng Phân Tích & Dự Báo Doanh Nghiệp", layout="wide")

# 🚀 Kết nối đến PostgreSQL (Cập nhật thông tin của bạn)
DATABASE_URL = "postgresql://data_owner:npg_lXG4nWhfUk0P@ep-cold-tooth-a1p19dl8-pooler.ap-southeast-1.aws.neon.tech/data?sslmode=require"
engine = create_engine(DATABASE_URL)

# Kiểm tra kết nối thành công
try:
    with engine.connect() as connection:
        st.success("✅ Kết nối PostgreSQL thành công!")
except Exception as e:
    st.error(f"❌ Lỗi kết nối PostgreSQL: {e}")

# 🚀 Tải các mô hình đã huấn luyện cho dự báo
random_forest_model = joblib.load('model/random_forest.pkl')
linear_regression_model = joblib.load('model/linear_regression.pkl')
stacking_model = joblib.load('model/stacking_model.pkl')

# -----------------------------------
# Thiết lập giao diện chung
# -----------------------------------

# Tạo menu lựa chọn chức năng trên sidebar
page = st.sidebar.radio("Chọn chức năng", 
                        ["Phân Tích Doanh Nghiệp", 
                         "Dự Báo Lợi Nhuận Sau Thuế", 
                         "Dự Báo Lợi Nhuận Sau Thuế (Từ DB)"])

# -----------------------------------
# Trang 1: Phân Tích Doanh Nghiệp
# -----------------------------------
if page == "Phân Tích Doanh Nghiệp":
    st.title("🚀 Dashboard Phân Tích Doanh Nghiệp")
    
    # 📌 Load danh sách doanh nghiệp
    query = "SELECT mack, tencongty FROM doanh_nghiep"
    df_companies = pd.read_sql(query, engine)

    # 📌 Chọn mã chứng khoán
    selected_mack = st.selectbox(
        "🔍 Chọn mã chứng khoán",
        df_companies["mack"].tolist(),
        format_func=lambda x: df_companies[df_companies["mack"] == x]["tencongty"].values[0]
    )

    # ✅ Khi người dùng chọn mã chứng khoán
    if selected_mack:
        col1, col2 = st.columns([2, 3])
    
        # 🏢 Thông tin doanh nghiệp
        with col1:
            st.subheader("📌 Thông tin Doanh Nghiệp")
            query_dn = f"SELECT * FROM doanh_nghiep WHERE mack = '{selected_mack}'"
            df_dn = pd.read_sql(query_dn, engine)
            st.dataframe(df_dn)
    
        # 🔥 Chỉ số tài chính quan trọng
        with col2:
            st.subheader("📈 Chỉ Số Tài Chính")
            query_cs = f"SELECT * FROM chi_so_tai_chinh WHERE mack = '{selected_mack}'"
            df_cs = pd.read_sql(query_cs, engine)
    
            if not df_cs.empty:
                col1_metric, col2_metric, col3_metric = st.columns(3)
                col1_metric.metric("EPS", f"{df_cs['eps'].values[0]:,.2f}", "Lợi nhuận trên mỗi cổ phiếu")
                col2_metric.metric("P/E", f"{df_cs['pe'].values[0]:,.2f}", "Giá/Thu nhập")
                col3_metric.metric("P/B", f"{df_cs['pb'].values[0]:,.2f}", "Giá trị sổ sách")
    
        # 🏦 Tabs hiển thị các bảng dữ liệu
        tab1, tab2, tab3, tab4 = st.tabs([ 
            "📊 Chỉ Số Tài Chính", "📈 Tăng Trưởng", "📜 Bảng Cân Đối Kế Toán", "📉 Báo Cáo KQKD"
        ])
    
        # 📊 Biểu đồ Chỉ Số Tài Chính
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=["ROA", "ROE"],
                y=[df_cs["roa"].values[0], df_cs["roe"].values[0]],
                marker_color=["blue", "green"],
                text=[f"{df_cs['roa'].values[0]:,.2f}", f"{df_cs['roe'].values[0]:,.2f}"],
                textposition='outside',
                name="Tỷ suất lợi nhuận"
            ))
            fig.update_layout(title="📈 Chỉ Số ROA & ROE", xaxis_title="Chỉ số", yaxis_title="Giá trị (%)", template="plotly_white")
            st.plotly_chart(fig)
    
        # 📈 Biểu đồ Tăng Trưởng
        with tab2:
            st.subheader("📊 Biểu Đồ Tăng Trưởng")
            query_growth = f"SELECT tangtruongdoanhthuthuan, tangtruongloinhuangop, tangtruongtongtaisan FROM chi_so_tai_chinh WHERE mack = '{selected_mack}'"
            df_growth = pd.read_sql(query_growth, engine)
    
            if not df_growth.empty:
                fig2 = px.line(
                    df_growth.melt(),
                    x="variable",
                    y="value",
                    markers=True,
                    title="📊 Biểu đồ Tăng Trưởng",
                    labels={"variable": "Chỉ số", "value": "Tăng trưởng (%)"}
                )
                st.plotly_chart(fig2)
    
                # 📊 Biểu đồ So Sánh Tăng Trưởng
                fig_growth = px.bar(
                    df_growth.melt(),
                    x="variable",
                    y="value",
                    color="variable",
                    text="value",
                    title="📊 So Sánh Tăng Trưởng Doanh Thu - Lợi Nhuận - Tài Sản"
                )
                st.plotly_chart(fig_growth)
    
        # 📜 Bảng Cân Đối Kế Toán & Biểu đồ
        with tab3:
            query_bc = f"SELECT * FROM bang_can_doi_ke_toan WHERE mack = '{selected_mack}'"
            df_bc = pd.read_sql(query_bc, engine)
            if not df_bc.empty:
                st.subheader("📜 Bảng Cân Đối Kế Toán")
                st.dataframe(df_bc)
    
                fig_bc = go.Figure()
                fig_bc.add_trace(go.Bar(
                    x=["Tài sản ngắn hạn", "Tài sản dài hạn", "Tổng tài sản"],
                    y=[df_bc["taisannganhan"].values[0], df_bc["taisandaihan"].values[0], df_bc["tongtaisan"].values[0]],
                    marker_color=["blue", "green", "orange"],
                    name="Tài sản"
                ))
                fig_bc.add_trace(go.Bar(
                    x=["Nợ phải trả", "Vốn chủ sở hữu"],
                    y=[df_bc["nophaitra"].values[0], df_bc["vonchusohuu"].values[0]],
                    marker_color=["red", "purple"],
                    name="Nợ & Vốn"
                ))
                fig_bc.update_layout(title="📊 Phân Tích Tài Sản - Nợ - Vốn Chủ Sở Hữu", 
                                       xaxis_title="Danh mục", 
                                       yaxis_title="Giá trị (VNĐ)", 
                                       template="plotly_white", 
                                       barmode="group")
                st.plotly_chart(fig_bc)
    
                # 📊 Biểu đồ Cơ cấu Nợ & Vốn Chủ Sở Hữu
                labels = ["Nợ phải trả", "Vốn chủ sở hữu"]
                values = [df_bc["nophaitra"].values[0], df_bc["vonchusohuu"].values[0]]
                fig_pie = px.pie(
                    names=labels, 
                    values=values, 
                    title="📊 Cơ cấu Nợ & Vốn Chủ Sở Hữu",
                    hole=0.3
                )
                st.plotly_chart(fig_pie)
    
        # 📉 Báo Cáo KQKD & Biểu đồ
        with tab4:
            query_kqkd = f"SELECT * FROM bao_cao_kqkd WHERE mack = '{selected_mack}'"
            df_kqkd = pd.read_sql(query_kqkd, engine)
            if not df_kqkd.empty:
                st.subheader("📉 Báo Cáo KQKD")
                st.dataframe(df_kqkd)
    
                fig_kqkd = go.Figure()
                fig_kqkd.add_trace(go.Bar(
                    x=["Doanh thu thuần", "Lợi nhuận gộp", "Lợi nhuận thuần"],
                    y=[df_kqkd["doanhthuthuan"].values[0], df_kqkd["loinhuangop"].values[0], df_kqkd["loinhuanthuan"].values[0]],
                    marker_color=["blue", "green", "orange"],
                    name="Lợi nhuận"
                ))
                fig_kqkd.update_layout(title="📈 Biểu Đồ Doanh Thu - Lợi Nhuận", 
                                         xaxis_title="Chỉ số", 
                                         yaxis_title="Giá trị (VNĐ)", 
                                         template="plotly_white")
                st.plotly_chart(fig_kqkd)
    
                # 📊 Biểu đồ Lợi Nhuận theo giai đoạn
                labels = ["Lợi nhuận trước thuế", "Lợi nhuận sau thuế"]
                values = [df_kqkd["loinhuantruocthue"].values[0], df_kqkd["loinhuansauthue"].values[0]]
                fig_pie_profit = px.pie(names=labels, values=values, 
                                        title="📊 Tỷ Lệ Lợi Nhuận Trước & Sau Thuế", 
                                        hole=0.3)
                st.plotly_chart(fig_pie_profit)

# -----------------------------------
# Trang 2: Dự Báo Lợi Nhuận Sau Thuế (Nhập Thủ Công)
# -----------------------------------
elif page == "Dự Báo Lợi Nhuận Sau Thuế":
    st.title("🚀 Dự Báo Lợi Nhuận Sau Thuế & Phát Hiện Gian Lận")

    # 📌 Nhập Dữ Liệu Doanh Nghiệp
    doanh_thu = st.number_input("Doanh thu thuần", step=0.01)
    loi_nhuan_gop = st.number_input("Lợi nhuận gộp", step=0.01)
    loi_nhuan_thuan = st.number_input("Lợi nhuận thuần", step=0.01)
    loi_nhuan_truoc_thue = st.number_input("Lợi nhuận trước thuế", step=0.01)

    # 📌 Nhập Lợi Nhuận Sau Thuế Thực Tế
    loi_nhuan_sau_thue_thuc_te = st.number_input("Lợi nhuận sau thuế thực tế", step=0.01)

    # 📌 Chọn mô hình dự đoán
    model_choice = st.selectbox("Chọn mô hình dự đoán", ["Random Forest", "Linear Regression", "Stacking Model"])

    def load_model(model_name):
        model_dict = {
            "Random Forest": random_forest_model,
            "Linear Regression": linear_regression_model,
            "Stacking Model": stacking_model
        }
        return model_dict[model_name]

    model = load_model(model_choice)

    def detect_anomaly(predicted, actual, percent_threshold=0.20, absolute_threshold=100_000_000_000):
        difference = abs(predicted - actual)
        percentage_diff = difference / abs(actual) if actual != 0 else 0
        
        if percentage_diff > percent_threshold or difference > absolute_threshold:
            return True, percentage_diff * 100
        else:
            return False, percentage_diff * 100

    if st.button("Dự Báo Lợi Nhuận Sau Thuế"):
        if any(pd.isna(x) for x in [doanh_thu, loi_nhuan_gop, loi_nhuan_thuan, loi_nhuan_truoc_thue, loi_nhuan_sau_thue_thuc_te]):
            st.warning("⚠️ Vui lòng nhập đầy đủ dữ liệu để dự báo!")
        else:
            input_data = np.array([[doanh_thu, loi_nhuan_gop, loi_nhuan_thuan, loi_nhuan_truoc_thue]])
            result = model.predict(input_data)[0]
            is_anomaly, anomaly_percentage = detect_anomaly(result, loi_nhuan_sau_thue_thuc_te)
            
            st.subheader("📊 Kết Quả Dự Báo")
            st.write(f"🔹 **Dự báo lợi nhuận sau thuế:** {result:,.2f} VNĐ")
            st.write(f"🔹 **Thực tế lợi nhuận sau thuế:** {loi_nhuan_sau_thue_thuc_te:,.2f} VNĐ")
            
            if is_anomaly:
                st.warning(f"⚠️ Phát hiện bất thường: Chênh lệch {anomaly_percentage:.2f}%!")
            else:
                st.success("✅ Không có bất thường, dự báo khớp với thực tế.")

            # 📊 Biểu đồ trực quan hóa
            st.subheader("📈 Biểu Đồ Phân Tích")
            
            df = pd.DataFrame({
                "Chỉ Số": ["Doanh thu", "Lợi nhuận gộp", "Lợi nhuận thuần"],
                "Giá trị (VNĐ)": [doanh_thu, loi_nhuan_gop, loi_nhuan_thuan]
            })
            fig = px.bar(df, x="Chỉ Số", y="Giá trị (VNĐ)", color="Chỉ Số", title="📊 So sánh các chỉ số tài chính")
            st.plotly_chart(fig)

            fig_profit = go.Figure()
            fig_profit.add_trace(go.Bar(x=["Lợi nhuận trước thuế", "Lợi nhuận sau thuế (Dự báo)", "Lợi nhuận sau thuế (Thực tế)"],
                                        y=[loi_nhuan_truoc_thue, result, loi_nhuan_sau_thue_thuc_te],
                                        marker_color=["blue", "green", "red"],
                                        text=[f"{loi_nhuan_truoc_thue:,.2f}", f"{result:,.2f}", f"{loi_nhuan_sau_thue_thuc_te:,.2f}"],
                                        textposition='outside'))
            fig_profit.update_layout(title="📊 So Sánh Lợi Nhuận", xaxis_title="Loại lợi nhuận", yaxis_title="Giá trị (VNĐ)")
            st.plotly_chart(fig_profit)

# -----------------------------------
# Trang 3: Dự Báo Lợi Nhuận Sau Thuế (Từ Dữ Liệu PostgreSQL)
# -----------------------------------
elif page == "Dự Báo Lợi Nhuận Sau Thuế (Từ DB)":
    st.title("🚀 Dự Báo Lợi Nhuận Sau Thuế Từ Dữ Liệu PostgreSQL")

    # 📌 Load danh sách doanh nghiệp
    query = "SELECT mack, tencongty FROM doanh_nghiep"
    df_companies = pd.read_sql(query, engine)

    # 📌 Chọn mã chứng khoán
    selected_mack = st.selectbox(
        "🔍 Chọn mã chứng khoán",
        df_companies["mack"].tolist(),
        format_func=lambda x: df_companies[df_companies["mack"] == x]["tencongty"].values[0]
    )

        # 📌 Truy vấn dữ liệu từ PostgreSQL
    if selected_mack:
        query_kqkd = f"SELECT doanhthuthuan, loinhuangop, loinhuanthuan, loinhuantruocthue, loinhuansauthue FROM bao_cao_kqkd WHERE mack = '{selected_mack}'"
        df_kqkd = pd.read_sql(query_kqkd, engine)

        if not df_kqkd.empty:
            # Lấy dữ liệu từ bảng `bao_cao_kqkd`
            doanh_thu = df_kqkd["doanhthuthuan"].values[0]
            loi_nhuan_gop = df_kqkd["loinhuangop"].values[0]
            loi_nhuan_thuan = df_kqkd["loinhuanthuan"].values[0]
            loi_nhuan_truoc_thue = df_kqkd["loinhuantruocthue"].values[0]
            loi_nhuan_sau_thue_thuc_te = df_kqkd["loinhuansauthue"].values[0]

            # Hiển thị dữ liệu
            st.subheader("📌 Dữ Liệu Từ Báo Cáo KQKD")
            st.write(f"- Doanh thu thuần: {doanh_thu:,.2f} VNĐ")
            st.write(f"- Lợi nhuận gộp: {loi_nhuan_gop:,.2f} VNĐ")
            st.write(f"- Lợi nhuận thuần: {loi_nhuan_thuan:,.2f} VNĐ")
            st.write(f"- Lợi nhuận trước thuế: {loi_nhuan_truoc_thue:,.2f} VNĐ")
            st.write(f"- Lợi nhuận sau thuế thực tế: {loi_nhuan_sau_thue_thuc_te:,.2f} VNĐ")

            # 📌 Chọn mô hình dự đoán
            model_choice = st.selectbox("Chọn mô hình dự đoán", ["Random Forest", "Linear Regression", "Stacking Model"])

            def load_model(model_name):
                model_dict = {
                    "Random Forest": random_forest_model,
                    "Linear Regression": linear_regression_model,
                    "Stacking Model": stacking_model
                }
                return model_dict[model_name]

            model = load_model(model_choice)

            def detect_anomaly(predicted, actual, percent_threshold=0.20, absolute_threshold=100_000_000_000):
                difference = abs(predicted - actual)
                percentage_diff = difference / abs(actual) if actual != 0 else 0

                if percentage_diff > percent_threshold or difference > absolute_threshold:
                    return True, percentage_diff * 100
                else:
                    return False, percentage_diff * 100

            if st.button("Dự Báo Lợi Nhuận Sau Thuế"):
                input_data = np.array([[doanh_thu, loi_nhuan_gop, loi_nhuan_thuan, loi_nhuan_truoc_thue]])
                result = model.predict(input_data)[0]
                is_anomaly, anomaly_percentage = detect_anomaly(result, loi_nhuan_sau_thue_thuc_te)

                st.subheader("📊 Kết Quả Dự Báo")
                st.write(f"🔹 **Dự báo lợi nhuận sau thuế:** {result:,.2f} VNĐ")
                st.write(f"🔹 **Thực tế lợi nhuận sau thuế:** {loi_nhuan_sau_thue_thuc_te:,.2f} VNĐ")

                if is_anomaly:
                    st.warning(f"⚠️ Phát hiện bất thường: Chênh lệch {anomaly_percentage:.2f}%!")
                else:
                    st.success("✅ Không có bất thường, dự báo khớp với thực tế.")

                # 📊 Biểu đồ trực quan hóa
                st.subheader("📈 Biểu Đồ Phân Tích")

                df = pd.DataFrame({
                    "Chỉ Số": ["Doanh thu", "Lợi nhuận gộp", "Lợi nhuận thuần"],
                    "Giá trị (VNĐ)": [doanh_thu, loi_nhuan_gop, loi_nhuan_thuan]
                })
                fig = px.bar(df, x="Chỉ Số", y="Giá trị (VNĐ)", color="Chỉ Số", title="📊 So sánh các chỉ số tài chính")
                st.plotly_chart(fig)

                fig_profit = go.Figure()
                fig_profit.add_trace(go.Bar(x=["Lợi nhuận trước thuế", "Lợi nhuận sau thuế (Dự báo)", "Lợi nhuận sau thuế (Thực tế)"],
                                           y=[loi_nhuan_truoc_thue, result, loi_nhuan_sau_thue_thuc_te],
                                           marker_color=["blue", "green", "red"],
                                           text=[f"{loi_nhuan_truoc_thue:,.2f}", f"{result:,.2f}", f"{loi_nhuan_sau_thue_thuc_te:,.2f}"],
                                           textposition='outside'))
                fig_profit.update_layout(title="📊 So Sánh Lợi Nhuận", xaxis_title="Loại lợi nhuận", yaxis_title="Giá trị (VNĐ)")
                st.plotly_chart(fig_profit)
        else:
            st.warning("⚠️ Không tìm thấy dữ liệu cho mã chứng khoán này.")
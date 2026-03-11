import streamlit as st
import time

# Cấu hình giao diện
st.set_page_config(page_title="Mô phỏng Sản xuất", layout="wide")
st.title("🏭 Hệ thống Mô phỏng Rời rạc (DES)")

# Thanh điều khiển bên trái
st.sidebar.header("Cấu hình công đoạn")
p1_time = st.sidebar.slider("Thời gian Process 1 (giây)", 1, 10, 3)
p2_time = st.sidebar.slider("Thời gian Process 2 (giây)", 1, 10, 5)
p3_time = st.sidebar.slider("Thời gian Process 3 (giây)", 1, 10, 2)

# Khởi tạo trạng thái (WIP và Output)
if 'wip' not in st.session_state:
    st.session_state.wip = [0, 0, 0] # [P1, P2, P3]
    st.session_state.output = 0
    st.session_state.start_time = time.time()

# Giao diện chính (Các cột tương ứng với sơ đồ của bạn)
cols = st.columns(5)

with cols[0]:
    st.metric("Input", "∞")
    if st.button("Thêm 1 hàng (Dot)"):
        st.session_state.wip[0] += 1

# Hiển thị các Process và số "Dot"
for i in range(1, 4):
    with cols[i]:
        st.subheader(f"Process {i}")
        # Vẽ các chấm đỏ dựa trên số lượng hàng đang chờ
        dots = "🔴 " * st.session_state.wip[i-1]
        st.write(dots if dots else "Trống")
        
        # Logic nút bấm để giả lập hoàn thành công đoạn
        if st.button(f"Xong P{i}", key=f"btn{i}"):
            if st.session_state.wip[i-1] > 0:
                st.session_state.wip[i-1] -= 1
                if i < 3:
                    st.session_state.wip[i] += 1
                else:
                    st.session_state.output += 1

with cols[4]:
    st.metric("Output", st.session_state.wip[0] + st.session_state.wip[1] + st.session_state.wip[2] + st.session_state.output)
    st.success(f"Đã xong: {st.session_state.output}")

# Tính toán thời gian
elapsed = round(time.time() - st.session_state.start_time, 1)
st.info(f"⏱️ Tổng thời gian vận hành: {elapsed} giây")

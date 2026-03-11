import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Quản lý Dòng chảy Sản xuất", layout="wide")

# Khởi tạo dữ liệu
if 'processes' not in st.session_state:
    st.session_state.processes = {
        'input': {'name': 'Đầu vào', 'time': 0, 'next': 'P1', 'wip': 0},
        'P1': {'name': 'Công đoạn 1', 'time': 5, 'next': 'output', 'wip': 0},
        'output': {'name': 'Đầu ra', 'time': 0, 'next': None, 'wip': 0}
    }
if 'total_out' not in st.session_state:
    st.session_state.total_out = 0

st.title("🏭 Sơ đồ Dòng chảy & Mô phỏng Sản xuất")

# --- KHU VỰC THIẾT KẾ (Sidebar) ---
with st.sidebar:
    st.header("🛠️ Thiết kế quy trình")
    with st.expander("Thêm công đoạn mới"):
        new_id = st.text_input("Mã công đoạn (vd: P2)", "P2")
        new_name = st.text_input("Tên hiển thị", "Kiểm hàng")
        new_time = st.number_input("Thời gian (s)", 1, 100, 5)
        new_next = st.selectbox("Chuyển đến công đoạn:", list(st.session_state.processes.keys()))
        
        if st.button("Thêm vào sơ đồ"):
            st.session_state.processes[new_id] = {
                'name': new_name, 'time': new_time, 'next': new_next, 'wip': 0
            }
            st.rerun()

    if st.button("🗑️ Làm mới sơ đồ"):
        st.session_state.processes = {
            'input': {'name': 'Đầu vào', 'time': 0, 'next': 'output', 'wip': 0},
            'output': {'name': 'Đầu ra', 'time': 0, 'next': None, 'wip': 0}
        }
        st.rerun()

# --- KHU VỰC HIỂN THỊ SƠ ĐỒ ---
st.subheader("📍 Dòng chảy hiện tại")
cols = st.columns(len(st.session_state.processes))

# Vẽ sơ đồ bằng Markdown & CSS đơn giản để không bao giờ lỗi
flow_md = " -> ".join([f"**[{p['name']}]**" for p in st.session_state.processes.values()])
st.markdown(f"**Hướng dòng chảy:** {flow_md}")

for i, (p_id, p_data) in enumerate(st.session_state.processes.items()):
    with cols[i]:
        st.info(f"**{p_data['name']}**")
        st.write(f"⏱️ {p_data['time']}s")
        st.write(f"🔴 WIP: {p_data['wip']}")
        
        if st.button(f"Xong {p_id}", key=f"btn_{p_id}"):
            if p_id == 'input':
                st.session_state.processes[p_id]['wip'] += 1
            elif st.session_state.processes[p_id]['wip'] > 0:
                st.session_state.processes[p_id]['wip'] -= 1
                next_p = p_data['next']
                if next_p in st.session_state.processes:
                    st.session_state.processes[next_p]['wip'] += 1
                if p_id == 'output':
                    st.session_state.total_out += 1

st.divider()
st.metric("Tổng sản phẩm hoàn thành", st.session_state.total_out)

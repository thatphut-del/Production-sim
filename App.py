import streamlit as st
import uuid

st.set_page_config(page_title="CT Block Workflow Studio", layout="wide")

# CSS để giao diện giống Studio chuyên nghiệp
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stButton>button { width: 100%; border-radius: 5px; }
    .process-card {
        padding: 15px; border-radius: 10px; border: 1px solid #ddd;
        background-color: #f9f9f9; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo dữ liệu quy trình
if 'workflow' not in st.session_state:
    st.session_state.workflow = {
        'nodes': {
            'start': {'name': '📦 Load Material', 'time': 0, 'next': 'finish'},
            'finish': {'name': '✅ Finished', 'time': 0, 'next': None}
        }
    }

st.title("🏭 CT Block Workflow Studio")

col_tools, col_canvas = st.columns([1, 3])

# --- TOOLBOX & BLOCK EDITOR ---
with col_tools:
    with st.container(border=True):
        st.subheader("🛠️ Toolbox")
        new_name = st.text_input("Tên công đoạn", "Công đoạn 1")
        new_time = st.number_input("Thời gian (s)", 1, 3600, 10)
        
        if st.button("➕ Thêm Block"):
            node_id = f"node_{uuid.uuid4().hex[:4]}"
            st.session_state.workflow['nodes'][node_id] = {
                'name': new_name, 'time': new_time, 'next': 'finish'
            }
            st.rerun()

    # Editor để sửa kết nối
    with st.container(border=True):
        st.subheader("📝 Block Editor")
        target_node = st.selectbox("Chọn Block để sửa:", list(st.session_state.workflow['nodes'].keys()), 
                                   format_func=lambda x: st.session_state.workflow['nodes'][x]['name'])
        
        if target_node not in ['start', 'finish']:
            new_n = st.text_input("Sửa tên", st.session_state.workflow['nodes'][target_node]['name'])
            new_t = st.number_input("Sửa thời gian (s)", 1, 3600, st.session_state.workflow['nodes'][target_node]['time'])
            st.session_state.workflow['nodes'][target_node]['name'] = new_n
            st.session_state.workflow['nodes'][target_node]['time'] = new_t

        new_connection = st.selectbox("Nối đến Block:", [n for n in st.session_state.workflow['nodes'].keys() if n != target_node])
        if st.button("🔗 Cập nhật kết nối"):
            st.session_state.workflow['nodes'][target_node]['next'] = new_connection
            st.rerun()

# --- CANVAS HIỂN THỊ TRỰC QUAN ---
with col_canvas:
    st.subheader("🎨 Canvas")
    
    # Vẽ sơ đồ bằng mũi tên
    nodes = st.session_state.workflow['nodes']
    current = 'start'
    visited = []
    
    # Tạo giao diện ngang cho dòng chảy
    flow_cols = st.columns(len(nodes) if len(nodes) < 6 else 6)
    
    idx = 0
    temp_node = 'start'
    while temp_node and temp_node not in visited:
        visited.append(temp_node)
        with flow_cols[idx % 6]:
            color = "#e1f5fe" if temp_node == 'start' else "#fff9c4" if temp_node == 'finish' else "#e8f5e9"
            st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; border-radius: 10px; border: 2px solid #333; text-align: center;">
                    <b>{nodes[temp_node]['name']}</b><br>
                    <small>{nodes[temp_node]['time']}s</small>
                </div>
                <div style="text-align: center; font-size: 20px;">⬇️</div>
            """, unsafe_allow_html=True)
        temp_node = nodes[temp_node]['next']
        idx += 1

# --- MÔ PHỎNG & KẾT QUẢ ---
st.divider()
st.subheader("🚀 Mô phỏng và Kết quả")
c1, c2, c3 = st.columns(3)

# Tính tổng Lead Time
total_time = sum(n['time'] for n in nodes.values())
c1.metric("Tổng Lead Time", f"{total_time} giây")
c2.metric("Số lượng Block", len(nodes))
if st.button("▶️ Chạy mô phỏng hệ thống"):
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
    st.success(f"Mô phỏng hoàn tất! Năng suất dự kiến: {round(3600/max(1, total_time), 2)} sản phẩm/giờ")

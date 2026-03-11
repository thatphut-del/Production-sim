import streamlit as st
from streamlit_flow import StreamlitFlow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
import uuid

st.set_page_config(page_title="CT Block Workflow Studio", layout="wide")

# --- KHỞI TẠO DỮ LIỆU ---
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        StreamlitFlowNode('start', (50, 200), {'content': '🚀 Load Material'}, 'input', 'right'),
        StreamlitFlowNode('end', (800, 200), {'content': '🏁 Finished'}, 'output', 'left')
    ]
if 'edges' not in st.session_state:
    st.session_state.edges = []

# --- GIAO DIỆN CHÍNH ---
st.title("🏗️ CT Block Workflow Studio")
st.caption("Xây dựng quy trình sản xuất bằng kéo-thả block và kết nối luồng.")

col_tools, col_canvas = st.columns([1, 3])

# --- TOOLBOX & EDITOR (Bên trái) ---
with col_tools:
    with st.container(border=True):
        st.subheader("Toolbox")
        name = st.text_input("Tên công đoạn", "Công đoạn A")
        t = st.number_input("Thời gian xử lý (s)", 1, 3600, 10)
        
        if st.button("➕ Thêm Block vào Canvas", use_container_width=True):
            new_id = f"node_{uuid.uuid4().hex[:4]}"
            # Tạo node mới với handle cả 2 bên để nối
            new_node = StreamlitFlowNode(new_id, (400, 200), {'content': f"{name}\n({t}s)"}, 'default', 'right', 'left')
            st.session_state.nodes.append(new_node)
            st.rerun()

    with st.container(border=True):
        st.subheader("Mô phỏng")
        sim_time = st.slider("Thời gian chạy (phút)", 1, 60, 10)
        if st.button("▶️ Chạy mô phỏng", type="primary", use_container_width=True):
            st.warning("Tính năng mô phỏng đang tính toán dựa trên các kết nối...")

# --- CANVAS (Chính giữa) ---
with col_canvas:
    st.info("💡 Kéo từ dấu chấm của Block này sang Block kia để tạo luồng sản xuất.")
    
    # Hiển thị Canvas kéo thả
    result = StreamlitFlow(
        key='workflow_canvas',
        nodes=st.session_state.nodes,
        edges=st.session_state.edges,
        enable_node_menu=True,
        enable_edge_menu=True,
        enable_pan_zoom=True,
        height=600
    )

    # Cập nhật thay đổi từ người dùng (kéo thả, nối dây)
    if result:
        st.session_state.nodes = result.nodes
        st.session_state.edges = result.edges

# --- KẾT QUẢ ---
with st.expander("📊 Chi tiết cấu trúc quy trình"):
    st.write(f"Số lượng công đoạn: {len(st.session_state.nodes)}")
    st.write(f"Số lượng kết nối: {len(st.session_state.edges)}")

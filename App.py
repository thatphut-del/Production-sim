import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
import uuid

st.set_page_config(page_title="Sơ đồ Dòng chảy Sản xuất", layout="wide")
st.title("🏭 Thiết kế Quy trình Sản xuất Thông minh")

# Khởi tạo danh sách Node và Mũi tên trong bộ nhớ
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        StreamlitFlowNode("input", (50, 200), {'content': 'Input'}, 'input', 'right'),
        StreamlitFlowNode("output", (600, 200), {'content': 'Output'}, 'output', 'left')
    ]
if 'edges' not in st.session_state:
    st.session_state.edges = []

# Khu vực điều khiển bên trái
with st.sidebar:
    st.header("Cài đặt Công đoạn")
    node_name = st.text_input("Tên công đoạn (vd: P1, May, Cắt)", "P1")
    node_time = st.number_input("Thời gian xử lý (giây)", min_value=1, value=5)
    
    if st.button("Thêm Công đoạn mới"):
        new_id = str(uuid.uuid4())[:8]
        # Tạo node mới nằm ở giữa màn hình
        new_node = StreamlitFlowNode(new_id, (300, 200), {'content': f'{node_name} ({node_time}s)'}, 'default', 'both')
        st.session_state.nodes.append(new_node)
        st.rerun()

    st.divider()
    if st.button("Xóa toàn bộ sơ đồ"):
        st.session_state.nodes = [
            StreamlitFlowNode("input", (50, 200), {'content': 'Input'}, 'input', 'right'),
            StreamlitFlowNode("output", (600, 200), {'content': 'Output'}, 'output', 'left')
        ]
        st.session_state.edges = []
        st.rerun()

# Hiển thị Canvas Kéo thả
st.subheader("Bản vẽ Quy trình (Kéo thả khối và nối các đầu tròn)")
st.info("Hướng dẫn: Nhấn giữ chuột vào chấm tròn ở cạnh khối này và kéo sang chấm tròn của khối khác để tạo mũi tên dòng chảy.")

updated_nodes, updated_edges = streamlit_flow(
    'production_flow',
    st.session_state.nodes,
    st.session_state.edges,
    enable_node_menu=True,
    enable_edge_menu=True,
    enable_pan_zoom=True,
    fit_view=True,
    height=500
)

# Cập nhật lại vị trí nếu người dùng kéo thả
st.session_state.nodes = updated_nodes
st.session_state.edges = updated_edges

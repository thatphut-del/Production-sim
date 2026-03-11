import streamlit as st
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
import uuid

st.set_page_config(page_title="Sơ đồ Dòng chảy", layout="wide")

# Khởi tạo dữ liệu trong session_state nếu chưa có
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        StreamlitFlowNode("input", (50, 200), {'content': 'Đầu vào'}, 'input', 'right'),
        StreamlitFlowNode("output", (600, 200), {'content': 'Đầu ra'}, 'output', 'left')
    ]
if 'edges' not in st.session_state:
    st.session_state.edges = []

st.title("🏭 Thiết kế Quy trình Kéo thả")

with st.sidebar:
    st.header("Thêm Công đoạn")
    name = st.text_input("Tên công đoạn", "Máy 1")
    t = st.number_input("Thời gian (s)", 1, 100, 5)
    
    if st.button("➕ Thêm vào sơ đồ"):
        new_id = f"node_{uuid.uuid4().hex[:4]}"
        new_node = StreamlitFlowNode(new_id, (300, 250), {'content': f"{name} ({t}s)"}, 'default', 'both')
        st.session_state.nodes.append(new_node)
        st.rerun()

    if st.button("🗑️ Xóa hết"):
        st.session_state.nodes = [
            StreamlitFlowNode("input", (50, 200), {'content': 'Đầu vào'}, 'input', 'right'),
            StreamlitFlowNode("output", (600, 200), {'content': 'Đầu ra'}, 'output', 'left')
        ]
        st.session_state.edges = []
        st.rerun()

# Giao diện kéo thả
st.info("💡 Cách nối: Kéo từ chấm tròn của khối này sang khối kia để tạo mũi tên.")

# Gọi component và bắt sự kiện thay đổi
result = streamlit_flow(
    'flow_designer',
    st.session_state.nodes,
    st.session_state.edges,
    enable_node_menu=True,
    enable_edge_menu=True,
    fit_view=True,
    height=500
)

# Quan trọng: Cập nhật lại state khi người dùng thao tác trên canvas
if result:
    st.session_state.nodes, st.session_state.edges = result

import streamlit as st
from streamlit_flow import StreamlitFlow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
import uuid

st.set_page_config(page_title="Sơ đồ Dòng chảy", layout="wide")

# Khởi tạo dữ liệu
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        StreamlitFlowNode(id='input', pos=(50, 200), data={'content': 'Đầu vào'}, node_type='input', source_position='right'),
        StreamlitFlowNode(id='output', pos=(600, 200), data={'content': 'Đầu ra'}, node_type='output', target_position='left')
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
        new_node = StreamlitFlowNode(new_id, (300, 250), {'content': f"{name} ({t}s)"}, 'default', 'right', 'left')
        st.session_state.nodes.append(new_node)
        st.rerun()

    if st.button("🗑️ Xóa hết"):
        st.session_state.nodes = [
            StreamlitFlowNode('input', (50, 200), {'content': 'Đầu vào'}, 'input', 'right'),
            StreamlitFlowNode('output', (600, 200), {'content': 'Đầu ra'}, 'output', 'left')
        ]
        st.session_state.edges = []
        st.rerun()

# Hiển thị Canvas
# Lưu ý: Chữ 'StreamlitFlow' viết hoa S và F
result = StreamlitFlow(
    key='flow_designer',
    nodes=st.session_state.nodes,
    edges=st.session_state.edges,
    enable_node_menu=True,
    enable_edge_menu=True,
    fit_view=True,
    height=500
)

# Cập nhật state
if result:
    st.session_state.nodes, st.session_state.edges = result.nodes, result.edges

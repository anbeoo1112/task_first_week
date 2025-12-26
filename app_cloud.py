"""
VN Document Cloud - Streamlit Web Application
Modern UI for Vietnamese document processing
"""
import streamlit as st
import os
import tempfile
from typing import Dict, Any

from core import DocumentProcessor, CATEGORIES

# ─── Page Configuration ────────────────────────────────────────────────

st.set_page_config(
    page_title="VN Document Cloud",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Modern card styling */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.8) !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
    }
    
    /* Data card */
    .data-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .data-label {
        color: #6c757d;
        font-size: 0.85rem;
        margin-bottom: 0.25rem;
    }
    
    .data-value {
        color: #212529;
        font-size: 1.1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ─── Display Functions (defined first) ─────────────────────────────────

def display_data_item(key: str, value: Any):
    """Display a single data item"""
    label = key.replace("_", " ").title()
    st.markdown(f"""
    <div class="data-card">
        <div class="data-label">{label}</div>
        <div class="data-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def display_data_cards(data: Dict[str, Any]):
    """Display data in nice card format"""
    items = [(k, v) for k, v in data.items() if v]
    
    if not items:
        st.caption("Không có dữ liệu")
        return
    
    # Display in 2 columns
    col1, col2 = st.columns(2)
    mid = len(items) // 2 + len(items) % 2
    
    with col1:
        for key, value in items[:mid]:
            display_data_item(key, value)
    
    with col2:
        for key, value in items[mid:]:
            display_data_item(key, value)


def display_single_result(result: Dict[str, Any]):
    """Display single document processing result"""
    
    if result.get("error"):
        st.error("❌ Lỗi xử lý!")
        st.warning(f"Chi tiết: {result['error']}")
        st.info("💡 Vui lòng chờ 30 giây rồi thử lại nếu là Rate Limit.")
        return
    
    # Success
    st.success("✅ Xử lý thành công!")
    st.markdown("---")
    
    # Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        category = result.get("category")
        cat_info = CATEGORIES.get(category) if category else None
        icon = cat_info.icon if cat_info else "📄"
        st.metric("📁 Nhóm", f"{icon} {category.title() if category else 'N/A'}")
    
    with col2:
        st.metric("📋 Loại văn bản", result.get("doc_type", "Không xác định"))
    
    # Extracted data
    data = result.get("data")
    if data:
        st.markdown("### 📝 Thông tin trích xuất")
        
        # Convert to dict if needed
        if hasattr(data, "model_dump"):
            data = data.model_dump()
        elif hasattr(data, "dict"):
            data = data.dict()
        
        if isinstance(data, dict):
            display_data_cards(data)
            
            with st.expander("🔍 Xem JSON"):
                st.json(data)
    else:
        st.warning("⚠️ Không trích xuất được dữ liệu")


def display_multi_result(result: Dict[str, Any]):
    """Display multi-document processing result"""
    
    if result.get("error"):
        st.error("❌ Lỗi xử lý!")
        st.warning(f"Chi tiết: {result['error']}")
        return
    
    documents = result.get("documents", [])
    
    if not documents:
        st.warning("⚠️ Không phát hiện văn bản nào")
        return
    
    st.success(f"✅ Phát hiện {len(documents)} văn bản!")
    st.markdown("---")
    
    # Display each document
    for i, doc in enumerate(documents):
        with st.expander(f"📄 Văn bản {i + 1}: {doc.get('doc_type', 'Unknown')}", expanded=(i == 0)):
            data = doc.get("data")
            
            if data:
                if isinstance(data, dict):
                    display_data_cards(data)
                else:
                    st.write(data)
            else:
                st.caption("Không có dữ liệu")


# ─── Sidebar ───────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📄 VN Document")
    st.markdown("---")
    
    st.markdown("### ⚡ Công nghệ")
    st.caption("🔹 OCR: Google Document AI")
    st.caption("🔹 LLM: Gemini 2.0 Flash")
    st.caption("🔹 Độ chính xác: Cao")
    
    st.markdown("---")
    st.markdown("### 📋 Văn bản hỗ trợ")
    
    for cat_key, category in CATEGORIES.items():
        with st.expander(f"{category.icon} {cat_key.title()}"):
            for code, (name, _) in category.docs.items():
                st.markdown(f"• {name}")
    
    st.markdown("---")
    
    # Processing mode
    st.markdown("### ⚙️ Chế độ xử lý")
    process_mode = st.radio(
        "Chọn chế độ:",
        options=["single", "multi"],
        format_func=lambda x: "📄 Đơn văn bản" if x == "single" else "📚 Nhiều văn bản",
        help="Đơn: Xử lý 1 loại văn bản\nNhiều: Phát hiện nhiều loại trong 1 file"
    )

# ─── Main Content ──────────────────────────────────────────────────────

st.markdown("# 📄 Trích xuất thông tin văn bản")
st.markdown("##### Nhận dạng và trích xuất thông tin từ giấy tờ Việt Nam")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "📎 Tải lên file (PDF hoặc ảnh)",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Hỗ trợ PDF và các định dạng ảnh phổ biến"
)

if uploaded_file:
    # File info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.info(f"📎 **{uploaded_file.name}**")
    
    with col2:
        st.caption(f"📦 {uploaded_file.size / 1024:.1f} KB")
    
    with col3:
        process_btn = st.button(
            "🚀 Xử lý",
            type="primary",
            use_container_width=True
        )
    
    # Process file
    if process_btn:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        try:
            processor = DocumentProcessor()
            
            with st.spinner("⏳ Đang xử lý với AI..."):
                result = processor.run(tmp_path)
                
                # Debug: show raw result
                # st.json(result)
                
                if result.get("error"):
                    st.error(f"❌ Lỗi: {result['error']}")
                else:
                    documents = result.get("documents", [])
                    
                    if len(documents) == 0:
                        st.warning("⚠️ Không phát hiện văn bản nào")
                    elif len(documents) == 1:
                        # Single document
                        doc = documents[0]
                        display_single_result({
                            "category": doc.get("category"),
                            "doc_type": doc.get("docType"),
                            "data": doc.get("data"),
                            "confidence": doc.get("confidence"),
                            "_debug": doc.get("_debug")
                        })
                    else:
                        # Multiple documents
                        display_multi_result({
                            "documents": [
                                {
                                    "doc_type": d.get("docType"),
                                    "data": d.get("data"),
                                    "confidence": d.get("confidence")
                                }
                                for d in documents
                            ]
                        })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            st.error(f"❌ Lỗi: {str(e)}")
        
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

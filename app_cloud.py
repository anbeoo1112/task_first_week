"""
VN Document Cloud - Streamlit Web Application
FULLY AUTOMATIC - User chỉ cần upload file
"""
import streamlit as st
import os
import tempfile
from typing import Dict, Any, List

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
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        color: white;
    }
    .stMetric label { color: rgba(255,255,255,0.8) !important; }
    .stMetric [data-testid="stMetricValue"] { color: white !important; }
    
    .data-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .data-label { color: #6c757d; font-size: 0.85rem; margin-bottom: 0.25rem; }
    .data-value { color: #212529; font-size: 1.1rem; font-weight: 500; }
    
    .cost-free { color: #28a745; font-weight: bold; }
    .cost-paid { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# ─── Display Functions ─────────────────────────────────────────────────

def displayDataItem(key: str, value: Any):
    """Display a single data item"""
    label = key.replace("_", " ").title()
    st.markdown(f"""
    <div class="data-card">
        <div class="data-label">{label}</div>
        <div class="data-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def displayDataCards(data: Dict[str, Any]):
    """Display data in card format"""
    items = [(k, v) for k, v in data.items() if v and not k.startswith("_")]
    
    if not items:
        st.caption("Không có dữ liệu")
        return
    
    col1, col2 = st.columns(2)
    mid = len(items) // 2 + len(items) % 2
    
    with col1:
        for key, value in items[:mid]:
            displayDataItem(key, value)
    
    with col2:
        for key, value in items[mid:]:
            displayDataItem(key, value)


def displayDebugInfo(doc: Dict[str, Any]):
    """Display debug info"""
    debug = doc.get("_debug", {})
    loader = debug.get("loader", "?")
    vision = debug.get("vision", False)
    pageCount = doc.get("pageCount", 1)
    
    costClass = "cost-paid" if vision else "cost-free"
    costText = "$" if vision else "FREE"
    
    st.caption(f"""
    🔧 Loader: `{loader}` | Vision: `{vision}` | 
    Pages: `{pageCount}` | Cost: <span class="{costClass}">{costText}</span>
    """, unsafe_allow_html=True)


def displayDocument(doc: Dict[str, Any], index: int, total: int):
    """Display a single document result"""
    docType = doc.get("docType", "Unknown")
    category = doc.get("category", "")
    catInfo = CATEGORIES.get(category) if category else None
    icon = catInfo.icon if catInfo else "📄"
    pageCount = doc.get("pageCount", 1)
    
    title = f"{icon} {docType}"
    if pageCount > 1:
        title += f" ({pageCount} trang)"
    
    expanded = (index == 0)  # Mở văn bản đầu tiên
    
    with st.expander(title, expanded=expanded):
        displayDebugInfo(doc)
        
        # Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📁 Nhóm", category.title() if category else "N/A")
        with col2:
            confidence = doc.get("confidence")
            st.metric("🎯 Độ tin cậy", f"{confidence}/10" if confidence else "N/A")
        
        # Data
        data = doc.get("data")
        if data:
            st.markdown("#### 📝 Thông tin trích xuất")
            if isinstance(data, dict):
                displayDataCards(data)
                with st.expander("🔍 JSON"):
                    st.json(data)
        else:
            st.warning("Không trích xuất được dữ liệu")


def displayResults(result: Dict[str, Any]):
    """Display processing results"""
    
    if result.get("error"):
        st.error("❌ Lỗi xử lý!")
        st.warning(f"Chi tiết: {result['error']}")
        st.info("💡 Vui lòng chờ 30 giây rồi thử lại nếu là Rate Limit.")
        return
    
    documents = result.get("documents", [])
    
    if not documents:
        st.warning("⚠️ Không phát hiện được văn bản nào")
        return
    
    # Summary
    st.success(f"✅ Phát hiện {len(documents)} văn bản!")
    
    # Display each document
    st.markdown("---")
    for i, doc in enumerate(documents):
        displayDocument(doc, i, len(documents))


# ─── Sidebar ───────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📄 VN Document")
    st.markdown("---")
    
    st.markdown("### 📋 Văn bản hỗ trợ")
    
    for catKey, category in CATEGORIES.items():
        with st.expander(f"{category.icon} {catKey.title()}"):
            for code, (name, _) in category.docs.items():
                st.markdown(f"• {name}")

# ─── Main Content ──────────────────────────────────────────────────────

st.markdown("# 📄 Trích xuất thông tin văn bản")
st.markdown("##### Upload file → Hệ thống tự động nhận diện và trích xuất")

st.markdown("---")

# File uploader
uploadedFile = st.file_uploader(
    "📎 Tải lên file (PDF, ảnh, hoặc Excel)",
    type=["pdf", "png", "jpg", "jpeg", "xlsx", "xls"],
    help="Hỗ trợ PDF, ảnh, và Excel (mỗi sheet = 1 văn bản)"
)

if uploadedFile:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.info(f"📎 **{uploadedFile.name}**")
    
    with col2:
        st.caption(f"📦 {uploadedFile.size / 1024:.1f} KB")
    
    with col3:
        processBtn = st.button("🚀 Xử lý tự động", type="primary", use_container_width=True)
    
    if processBtn:
        fileExt = os.path.splitext(uploadedFile.name)[1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=fileExt) as tmp:
            tmp.write(uploadedFile.getvalue())
            tmpPath = tmp.name
        
        try:
            processor = DocumentProcessor()
            
            with st.spinner("⏳ Đang xử lý tự động với AI..."):
                result = processor.run(tmpPath)
                displayResults(result)
        
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")
        
        finally:
            if os.path.exists(tmpPath):
                os.remove(tmpPath)

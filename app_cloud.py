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

# ─── Styling ───────────────────────────────────────────────────────────

def loadCustomCss():
    """Load custom CSS styles"""
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

# ─── Display Components ────────────────────────────────────────────────

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
            displayDataItem(key, value)
    
    with col2:
        for key, value in items[mid:]:
            displayDataItem(key, value)

# ─── Result View Controllers ───────────────────────────────────────────

def displaySingleResult(result: Dict[str, Any]):
    """Display single document processing result"""
    # Success message
    st.success("✅ Xử lý thành công!")
    st.markdown("---")
    
    # Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        category = result.get("category")
        catInfo = CATEGORIES.get(category) if category else None
        icon = catInfo.icon if catInfo else "📄"
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
            displayDataCards(data)
            
            with st.expander("🔍 Xem JSON"):
                st.json(data)
    else:
        st.warning("⚠️ Không trích xuất được dữ liệu")


def displayMultiResult(result: Dict[str, Any]):
    """Display multi-document processing result"""
    documents = result.get("documents", [])
    
    st.success(f"✅ Phát hiện {len(documents)} văn bản!")
    st.markdown("---")
    
    # Display each document
    for i, doc in enumerate(documents):
        with st.expander(f"📄 Văn bản {i + 1}: {doc.get('doc_type', 'Unknown')}", expanded=(i == 0)):
            data = doc.get("data")
            
            if data:
                if isinstance(data, dict):
                    displayDataCards(data)
                else:
                    st.write(data)
            else:
                st.caption("Không có dữ liệu")

def handleDisplayResults(result: Dict[str, Any]):
    """Central logic to route result to correct display"""
    if result.get("error"):
        st.error("❌ Lỗi xử lý!")
        st.warning(f"Chi tiết: {result['error']}")
        return

    documents = result.get("documents", [])
    
    if len(documents) == 0:
        st.warning("⚠️ Không phát hiện văn bản nào")
        return

    # Logic chọn View hiển thị
    if len(documents) == 1:
        # Chế độ xem đơn
        doc = documents[0]
        displaySingleResult({
            "category": doc.get("category"),
            "doc_type": doc.get("docType"),
            "data": doc.get("data"),
            "confidence": doc.get("confidence"),
            "_debug": doc.get("_debug")
        })
    else:
        # Chế độ xem đa văn bản
        displayMultiResult({
            "documents": [
                {
                    "doc_type": d.get("docType"),
                    "data": d.get("data"),
                    "confidence": d.get("confidence")
                }
                for d in documents
            ]
        })

# ─── Main Application ──────────────────────────────────────────────────

def main():
    loadCustomCss()
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("## 📄 Document Extractor")

        
        for catKey, category in CATEGORIES.items():
            with st.expander(f"{category.icon} {catKey.title()}"):
                for code, (name, _) in category.docs.items():
                    st.markdown(f"• {name}")
        
    
    # --- Main Content ---
    st.markdown("# 📄 Document Extractor")
    st.markdown("##### Nhận dạng và trích xuất thông tin từ giấy tờ")
    st.markdown("---")

    uploadedFile = st.file_uploader(
        "📎 Tải lên file (PDF hoặc ảnh)",
        type=["pdf", "png", "jpg", "jpeg"],
        help="Hỗ trợ PDF và các định dạng ảnh phổ biến"
    )

    if uploadedFile:
        # Info bar
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.info(f"📎 **{uploadedFile.name}**")
        with col2:
            st.caption(f"📦 {uploadedFile.size / 1024:.1f} KB")
        with col3:
            processBtn = st.button("🚀 Xử lý", type="primary", use_container_width=True)
        
        # Process Action
        if processBtn:
            fileExt = os.path.splitext(uploadedFile.name)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=fileExt) as tmp:
                tmp.write(uploadedFile.getvalue())
                tmpPath = tmp.name
            
            try:
                processor = DocumentProcessor()
                with st.spinner("⏳ Đang xử lý với AI..."):
                    # Gọi pipeline với chế độ xử lý đã chọn
                    result = processor.run(tmpPath)
                    # Hiển thị kết quả
                    handleDisplayResults(result)
                    
            except Exception as e:
                import traceback
                traceback.print_exc()
                st.error(f"❌ Lỗi: {str(e)}")
            finally:
                if os.path.exists(tmpPath):
                    os.remove(tmpPath)

if __name__ == "__main__":
    main()

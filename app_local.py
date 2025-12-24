import streamlit as st
import os
import tempfile

from core.local_processor import LocalProcessor

# Page config
st.set_page_config(
    page_title="VN Document - Local",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Phân loại Giấy tờ Việt Nam")
st.markdown("*Chạy Local với Ollama + Tesseract (Miễn phí)*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Thông tin")
    
    st.success("✅ Chế độ Local")
    st.caption("**Model:** `qwen2.5:3b`")
    st.caption("**OCR:** Tesseract")
    st.caption("**Chi phí:** Miễn phí 100%")
    
    st.divider()
    
    st.markdown("### 📋 Văn bản hỗ trợ:")
    
    with st.expander("🪪 Giấy tờ tùy thân"):
        st.markdown("- CCCD / CMND")
        st.markdown("- Hộ chiếu")
        st.markdown("- Giấy khai sinh")
    
    with st.expander("🚗 Giấy tờ phương tiện"):
        st.markdown("- Bằng lái xe")
        st.markdown("- Đăng ký xe")
        st.markdown("- Đăng kiểm")
    
    with st.expander("💰 Giấy tờ tài chính"):
        st.markdown("- Hóa đơn VAT")
        st.markdown("- Biên lai")
        st.markdown("- Hợp đồng")

# Main content
st.divider()

# Upload file
uploaded_file = st.file_uploader(
    "📤 Upload file (PDF hoặc ảnh)",
    type=["pdf", "png", "jpg", "jpeg"],
)

if uploaded_file:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info(f"📄 **{uploaded_file.name}**")
        st.caption(f"Kích thước: {uploaded_file.size / 1024:.1f} KB")
    
    with col2:
        process_btn = st.button("🚀 Xử lý", type="primary", use_container_width=True)

# Xử lý
if uploaded_file and process_btn:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    try:
        processor = LocalProcessor()
        
        with st.spinner("🔍 Đang xử lý..."):
            result = processor.run(tmp_path)
        
        st.success("✅ Xử lý thành công!")
        st.divider()
        
        # Kết quả
        icons = {"identity": "🪪", "vehicle": "🚗", "finance": "💰"}
        names = {"identity": "Tùy thân", "vehicle": "Phương tiện", "finance": "Tài chính"}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cat = result.get("category")
            st.metric("📁 Nhóm", f"{icons.get(cat, '📄')} {names.get(cat, 'N/A')}")
        
        with col2:
            st.metric("📋 Loại", result["classification"])
        
        with col3:
            if result["confidence"]:
                st.metric("🎯 Độ tin cậy", f"{result['confidence']}/10")
        
        # Dữ liệu trích xuất
        if result["data"]:
            st.markdown("### 📄 Thông tin trích xuất")
            
            data = result["data"]
            col1, col2 = st.columns(2)
            items = list(data.items())
            mid = len(items) // 2
            
            with col1:
                for k, v in items[:mid]:
                    if v:
                        st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")
            
            with col2:
                for k, v in items[mid:]:
                    if v:
                        st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")
            
            with st.expander("📋 JSON"):
                st.json(result["data"])
        else:
            st.warning("Không trích xuất được dữ liệu")
                        
    except Exception as e:
        st.error(f"❌ Lỗi: {str(e)}")
        st.info("💡 Kiểm tra: Ollama đang chạy? (`ollama serve`)")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

# Footer
st.divider()
st.caption("🏠 VN Document | Local Mode | Ollama + Tesseract")

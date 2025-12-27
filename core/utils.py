import os
from typing import Optional, List, Dict, Any
from core.classifications import CLASSIFICATION_TREE

def countPages(filePath: str) -> int:
    """Đếm số trang của file (PDF hoặc ảnh)."""
    ext = os.path.splitext(filePath)[1].lower()
    if ext == '.pdf':
        try:
            import fitz
            doc = fitz.open(filePath)
            n = len(doc)
            doc.close()
            return n
        except Exception:
            pass
    return 1

def findCategory(docTypeName: str) -> Optional[str]:
    """Tìm category (nhóm) dựa trên doc_type_name."""
    for node in CLASSIFICATION_TREE.nodes:
        if hasattr(node, 'children'):
            for child in node.children:
                if child.name == docTypeName:
                    return node.name
    return None

def sanitizePageGroups(groups, maxPages: int) -> None:
    """
    Phát hiện và sửa lỗi 'ảo giác' số trang của Splitter.
    Ví dụ: Tài liệu chỉ có 2 trang nhưng Splitter nhận diện trang 3.
    Hàm này sẽ kẹp (clamp) số trang lại trong khoảng hợp lệ.
    """
    for group in groups:
        if not hasattr(group, 'pages') or not group.pages:
            continue
        
        originalPages = list(group.pages)
        sanitizedPages = []
        modified = False
        
        for p in group.pages:
            # Splitter dùng 1-based index
            if p > maxPages:
                # Nếu trang vượt quá thực tế, gán bằng trang cuối cùng
                sanitizedPages.append(maxPages)
                modified = True
            else:
                sanitizedPages.append(p)
        
        if modified:
            # Loại bỏ trùng lặp và giữ nguyên thứ tự
            group.pages = list(dict.fromkeys(sanitizedPages))
            print(f"   🔧 Sửa lỗi số trang: {originalPages} -> {group.pages}")

def makeSuccessResponse(
    category: Optional[str] = None, 
    docType: Optional[str] = None, 
    data: Any = None, 
    confidence: Optional[float] = None, 
    loader: str = "?", 
    vision: bool = False
) -> Dict:
    """Tạo response thành công chuẩn hóa."""
    return {"documents": [{
        "category": category, 
        "docType": docType, 
        "data": data,
        "confidence": confidence, 
        "_debug": {"loader": loader, "vision": vision}
    }], "error": None}

def makeErrorResponse(msg: str) -> Dict:
    """Tạo response lỗi chuẩn hóa."""
    return {"documents": [], "error": msg}

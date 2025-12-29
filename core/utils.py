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

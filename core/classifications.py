from typing import Dict, Optional, Type, List
from extract_thinker import Classification, Contract
from extract_thinker.models.classification_node import ClassificationNode
from extract_thinker.models.classification_tree import ClassificationTree
from contracts import IDENTITY_DOCS, VEHICLE_DOCS, FINANCE_DOCS
from contracts.government import GOV_LEGAL_DOCS, GOV_ADMIN_DOCS

# Category metadata for UI
CATEGORY_META = {
    "identity": ("🪪", "Giấy tờ tùy thân"),
    "vehicle": ("🚗", "Giấy tờ phương tiện"),
    "finance": ("💰", "Giấy tờ tài chính"),
    "gov_legal": ("📜", "Văn bản pháp luật"),
    "gov_admin": ("📋", "Văn bản hành chính"),
}

def _buildNode(name: str, desc: str, docs: Dict) -> ClassificationNode:
    children = []
    for code, item in docs.items():
        if isinstance(item, tuple) or isinstance(item, list):
            displayName, contractClass = item
        else:
            displayName = code
            contractClass = item
            
        children.append(ClassificationNode(
            name=displayName,
            classification=Classification(name=displayName, description=f"{desc}: {displayName}", 
            contract=contractClass)
        ))
    return ClassificationNode(
        name=name,
        classification=Classification(name=name, description=desc),
        children=children
    )

# Dựng cây phân loại CÂN BẰNG
CLASSIFICATION_TREE = ClassificationTree(nodes=[
    # Identity: 3 docs
    _buildNode("identity", "Giấy tờ tùy thân: CCCD, hộ chiếu, thẻ sinh viên", IDENTITY_DOCS),
    
    # Vehicle: 1 doc
    _buildNode("vehicle", "Giấy tờ phương tiện: bằng lái xe, đăng ký xe", VEHICLE_DOCS),
    
    # Finance: 1 doc
    _buildNode("finance", "Giấy tờ tài chính: hóa đơn, hợp đồng, bill", FINANCE_DOCS),
    
    # Government chia thành 2 nhóm
    _buildNode("gov_legal", "Văn bản quy phạm pháp luật: Luật, Pháp lệnh, Nghị định, Thông tư", GOV_LEGAL_DOCS),
    _buildNode("gov_admin", "Văn bản hành chính: Nghị quyết, Lệnh, Văn bản chỉ đạo điều hành", GOV_ADMIN_DOCS),
    
    # Other
    ClassificationNode(
        name="Other",
        classification=Classification(name="Other", description="Giấy tờ khác không thuộc các loại trên")
    ),
])

# Hàm tìm kiếm hợp đồng
def getContractForDocType(categoryName: str, docTypeName: str) -> Optional[Type[Contract]]:
    for node in CLASSIFICATION_TREE.nodes:
        if node.name == categoryName:
            if node.children:
                for child in node.children:
                    if child.name == docTypeName:
                        return child.classification.contract
    return None

# Định nghĩa các loại giấy tờ cho UI display (sidebar)
class Category:
    def __init__(self, name: str, icon: str, docs: Dict):
        self.name = name
        self.icon = icon
        self.docs = docs

CATEGORIES = {
    "identity": Category("identity", "🪪", IDENTITY_DOCS),
    "vehicle": Category("vehicle", "🚗", VEHICLE_DOCS),
    "finance": Category("finance", "💰", FINANCE_DOCS),
    "gov_legal": Category("gov_legal", "📜", GOV_LEGAL_DOCS),
    "gov_admin": Category("gov_admin", "📋", GOV_ADMIN_DOCS),
}

# Hàm lấy danh sách các loại giấy tờ (Flat List)
def getClassificationsList() -> List[Classification]:
    result = []
    for node in CLASSIFICATION_TREE.nodes:
        if node.children:
            for child in node.children:
                result.append(child.classification)
        else:
            result.append(node.classification)
    return result

# Hàm lấy cây phân loại (Tree) - Dùng cho Tree Classification
def getClassificationsTree() -> ClassificationTree:
    return CLASSIFICATION_TREE

# Helper: In cây để debug
def printTree():
    """In cấu trúc cây để kiểm tra"""
    print("📊 Classification Tree:")
    for node in CLASSIFICATION_TREE.nodes:
        icon = CATEGORY_META.get(node.name, ("📄", ""))[0]
        count = len(node.children) if node.children else 0
        print(f"  {icon} {node.name}: {count} loại")
        if node.children:
            for child in node.children:
                print(f"      └── {child.name}")

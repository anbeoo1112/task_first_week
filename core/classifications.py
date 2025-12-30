from typing import Dict, Optional, Type, List
from extract_thinker import Classification, Contract
from extract_thinker.models.classification_node import ClassificationNode
from extract_thinker.models.classification_tree import ClassificationTree
from contracts import IDENTITY_DOCS, VEHICLE_DOCS, FINANCE_DOCS
from contracts import DOCUMENT_CATEGORIES

# Category metadata for UI
CATEGORY_META = {
    "identity": ("🪪", "Giấy tờ tùy thân"),
    "vehicle": ("🚗", "Giấy tờ phương tiện"),
    "finance": ("💰", "Giấy tờ tài chính"),
}

def _buildNode(name: str, desc: str, docs: Dict) -> ClassificationNode:
    children = [
        ClassificationNode(
            name=displayName,
            classification=Classification(name=displayName, description=f"{desc}: {displayName}", 
            contract=contractClass)
        )
        for code, (displayName, contractClass) in docs.items()
    ]
    return ClassificationNode(
        name=name,
        classification=Classification(name=name, description=desc),
        children=children
    )

# Dựng cây phân loại
CLASSIFICATION_TREE = ClassificationTree(nodes=[
    _buildNode("identity", "Giấy tờ tùy thân: CCCD, hộ chiếu, giấy khai sinh", IDENTITY_DOCS),
    _buildNode("vehicle", "Giấy tờ phương tiện: bằng lái, đăng ký xe, đăng kiểm", VEHICLE_DOCS),
    _buildNode("finance", "Giấy tờ tài chính: hợp đồng, hóa đơn, bill chuyển khoản", FINANCE_DOCS),
    ClassificationNode(
        name="Other",
        classification=Classification(name="Other", description="Giấy tờ khác")
    ),
])

# Hàm tìm kiếm hợp đồng
def getContractForDocType(categoryName: str, docTypeName: str) -> Optional[Type[Contract]]:
    for node in CLASSIFICATION_TREE.nodes:
        if node.name == categoryName:
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


"""Test nhiều ảnh hóa đơn để xem các format khác nhau"""
from core.config import config
import os

loader = config.documentAi.createLoader()

# Test 3 ảnh khác nhau
files = [
    "dataset/finance/invoice/images/X00016469612.jpg",
    "dataset/finance/invoice/images/X00016469672.jpg",
    "dataset/finance/invoice/images/batch1-0513.jpg",
]

for f in files:
    if os.path.exists(f):
        print("=" * 60)
        print(f"FILE: {f}")
        print("=" * 60)
        content = loader.load(f)
        print(content[0]['content'][:1500])  # In 1500 ký tự đầu
        print("\n")

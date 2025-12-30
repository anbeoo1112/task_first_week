import os
import glob
import json
import sys
from core.pipeline import DocumentProcessor

def load_ground_truth(gt_path):
    if not os.path.exists(gt_path):
        return None
    with open(gt_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_data(extracted, expected):
    # Simple strict comparison for now, can be improved
    # Compare only the 'data' fields of documents
    if not extracted or not expected:
        return False
    
    # Check if number of documents matches
    if len(extracted.get('documents', [])) != len(expected.get('documents', [])):
        return False
    
    match_count = 0
    for i, doc in enumerate(expected['documents']):
        ex_doc = extracted['documents'][i]
        
        # Compare docType and category
        if doc.get('docType') != ex_doc.get('docType'):
            print(f"  Mismatch docType: Expected '{doc.get('docType')}', Got '{ex_doc.get('docType')}'")
            return False
            
        # Compare fields
        expected_data = doc.get('data', {})
        extracted_data = ex_doc.get('data', {})
        
        if expected_data is None: expected_data = {}
        if extracted_data is None: extracted_data = {}

        # Check all expected keys
        for key, val in expected_data.items():
            if str(extracted_data.get(key)) != str(val):
                print(f"  Mismatch field '{key}': Expected '{val}', Got '{extracted_data.get(key)}'")
                return False
        match_count += 1
        
    return True

def main():
    input_dir = 'evaluation/inputs'
    gt_dir = 'evaluation/ground_truth'
    
    extensions = ['*.pdf', '*.jpg', '*.jpeg', '*.png']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(input_dir, ext)))
    if not files:
        print("No files found in evaluation/inputs")
        return

    processor = DocumentProcessor()
    
    passed = 0
    failed = 0
    
    print(f"Starting evaluation on {len(files)} files...\n")
    
    for file_path in files:
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        gt_path = os.path.join(gt_dir, base_name + '.json')
        
        print(f"Processing {filename}...")
        
        try:
            result = processor.run(file_path)
            
            if 'error' in result and result['error']:
                print(f"❌ Error during processing: {result['error']}")
                failed += 1
                continue
                
            ground_truth = load_ground_truth(gt_path)
            if not ground_truth:
                print(f"⚠️ No ground truth found for {filename}. Skipping comparison.")
                print(f"Extracted: {json.dumps(result, ensure_ascii=False, indent=2)}")
                continue
                
            is_match = compare_data(result, ground_truth)
            
            if is_match:
                print("✅ PASSED")
                passed += 1
            else:
                print("❌ FAILED (Content mismatch)")
                failed += 1
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            failed += 1
            
    print(f"\nEvaluation Complete.")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(files)}")

if __name__ == "__main__":
    main()

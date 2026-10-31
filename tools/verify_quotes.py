import re
import sys

def verify_quotes(note_path, txt_path):
    with open(note_path, 'r', encoding='utf-8') as f:
        note_content = f.read()
    with open(txt_path, 'r', encoding='utf-8') as f:
        txt_content = f.read()

    # normalize text content by replacing all whitespace with a single space
    clean_txt = ' '.join(txt_content.split())

    # Find quotes in Section 3 Key claims
    m_claims = re.search(r'## 3\. Key claims(.*?)(?=##|\Z)', note_content, re.DOTALL)
    if not m_claims:
        print("No Section 3 found!")
        return False
    
    claims_text = m_claims.group(1)
    quotes = re.findall(r'"([^"\n]+)"', claims_text)
    print(f"Verifying {len(quotes)} verbatim quotes in Section 3 of {note_path}...")
    
    all_ok = True
    for q in quotes:
        clean_q = ' '.join(q.split())
        word_count = len(clean_q.split())
        if word_count > 25:
            print(f"  [FAIL - TOO LONG: {word_count} words] \"{clean_q}\"")
            all_ok = False
            continue
        if clean_q in clean_txt:
            print(f"  [PASS: {word_count} words] \"{clean_q}\"")
        else:
            print(f"  [FAIL - NOT IN TEXT] \"{clean_q}\"")
            all_ok = False
            
    return all_ok

if __name__ == '__main__':
    ok = verify_quotes(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)

import sys

def inspect_paper(txt_path):
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    print(f"Total length: {len(text)} characters")
    print("--- FIRST 1500 CHARACTERS ---")
    print(text[:1500])
    print("--- SEARCH HEADINGS / SECTIONS ---")
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if any(line_clean.lower().startswith(x) for x in ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', 'i. ', 'ii. ', 'iii. ', 'iv. ', 'v. ', 'vi. ', 'section', 'abstract', 'introduction', 'prelimin', 'method', 'experiment', 'evaluat', 'related work', 'conclusion', 'limitation']):
            if len(line_clean) < 60:
                print(f"Line {i}: {line_clean}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        inspect_paper(sys.argv[1])

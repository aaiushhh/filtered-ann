with open("papers/prokhorenkova2020graph.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

print("Length:", len(text))
pages = text.split("--- PAGE ")
print("Total pages:", len(pages))

# Print abstract and intro
print("--- PAGE 1 ---")
print(pages[1][:2000])

print("\n--- PAGE 2 ---")
print(pages[2][:2000])

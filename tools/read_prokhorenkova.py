with open("papers/prokhorenkova2020graph.txt", "r", encoding="utf-8") as f:
    text = f.read()

pages = text.split("--- PAGE ")
print(f"Total pages: {len(pages)}")
print("Page 1:")
print(pages[1][:1500])
print("\nPage 2:")
print(pages[2][:1500])

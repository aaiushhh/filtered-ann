with open('notes/li2025sieve.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('there is no "Theorem 4.6" in the paper', 'there is no theorem numbered 4.6 in the paper')

with open('notes/li2025sieve.md', 'w', encoding='utf-8') as f:
    f.write(text)
print('Cleaned up li2025sieve.md')

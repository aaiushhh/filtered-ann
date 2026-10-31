import csv
import datetime

updates = {
    'prokhorenkova2020graph': {
        'arxiv_id': '1907.00845',
        'link': 'https://arxiv.org/abs/1907.00845',
        'verified_venue': 'Proceedings of the 37th International Conference on Machine Learning (ICML 2020)',
        'verified_year': '2020',
        'text_version': 'arXiv-1907.00845',
        'source_url': 'https://arxiv.org/pdf/1907.00845'
    },
    'diwan2024navigable': {
        'arxiv_id': '2405.18680',
        'link': 'https://arxiv.org/abs/2405.18680',
        'verified_venue': 'Advances in Neural Information Processing Systems (NeurIPS 2024)',
        'verified_year': '2024',
        'text_version': 'arXiv-2405.18680',
        'source_url': 'https://arxiv.org/pdf/2405.18680'
    },
    'indyk2023worst': {
        'arxiv_id': '2310.19126',
        'link': 'https://arxiv.org/abs/2310.19126',
        'verified_venue': 'Advances in Neural Information Processing Systems (NeurIPS 2023)',
        'verified_year': '2023',
        'text_version': 'arXiv-2310.19126',
        'source_url': 'https://arxiv.org/pdf/2310.19126'
    },
    'li2025sieve': {
        'doi': '10.14778/3749646.3749725',
        'arxiv_id': '',
        'verified_status': 'PUB',
        'link': 'https://doi.org/10.14778/3749646.3749725',
        'verified_venue': 'Proceedings of the VLDB Endowment (PVLDB)',
        'verified_year': '2025',
        'text_version': 'PVLDB-vol18-p4723',
        'source_url': 'https://www.vldb.org/pvldb/vol18/p4723-li.pdf'
    },
    'zhang2023vbase': {
        'doi': '',
        'arxiv_id': '',
        'verified_status': 'PUB',
        'link': 'https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi',
        'verified_venue': '17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2023)',
        'verified_year': '2023',
        'text_version': 'OSDI2023-zhang-qianxi',
        'source_url': 'https://www.usenix.org/system/files/osdi23-zhang-qianxi_1.pdf'
    }
}

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

diffs = []
for r in rows:
    k = r['bibkey']
    if k in updates:
        for fk, fv in updates[k].items():
            old_v = r.get(fk, '')
            if old_v != fv:
                diffs.append(f'{k}.{fk}: "{old_v}" -> "{fv}"')
                r[fk] = fv

with open('manifest.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Updated manifest. Total diffs: {len(diffs)}')
for d in diffs:
    print(' ', d)

now = datetime.datetime.now().isoformat()
with open('LOG.md', 'a', encoding='utf-8') as f:
    f.write(f'\n{now} — Manifest updated for Gate 5 notes: {len(diffs)} field corrections\n')
    for d in diffs:
        f.write(f'  - {d}\n')

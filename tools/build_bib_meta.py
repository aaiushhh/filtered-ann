import csv
import json

with open('manifest.csv', 'r', encoding='utf-8') as f:
    manifest = {r['bibkey']: r for r in csv.DictReader(f)}

with open('tools/verification_complete.json', 'r', encoding='utf-8', errors='replace') as f:
    vc = {item['seed']['bibkey']: item for item in json.load(f)}

# Build bib_meta dictionary
bib_meta = {}

# Seed additions from gaps.md
gaps_additions = {
    'gollapudi2023filtereddiskann': {
        'authors': 'Siddharth Gollapudi, Neel Karia, Varun Sivashankar, Ravishankar Krishnaswamy, Nikit Begwani, Swapnil Raz, Yiyong Lin, Yin Zhang, Neelam Mahapatro, Premkumar Srinivasan, Amit Singh, Harsha Vardhan Simhadri',
        'venue': 'Proceedings of the ACM Web Conference 2023 (WWW 2023)',
        'year': '2023',
        'doi': '10.1145/3543507.3583552',
        'status': 'PUB'
    },
    'patel2024acorn': {
        'authors': 'Liana Patel, Peter Kraft, Carlos Guestrin, Matei Zaharia',
        'venue': 'Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)',
        'year': '2024',
        'doi': '10.1145/3654923',
        'status': 'PUB'
    },
    'luo2025tagfiltered': {
        'authors': 'Jiarui Luo, Miao Qiao, Chaoji Zuo, Dong Deng',
        'venue': '2025 IEEE 41st International Conference on Data Engineering (ICDE 2025)',
        'year': '2025',
        'doi': '10.1109/icde65448.2025.00272',
        'status': 'PUB'
    },
    'wu2022hqann': {
        'authors': 'Wei Wu, Junlin He, Yu Qiao, Guoheng Fu, Li Liu, Jin Yu',
        'venue': 'Proceedings of the 31st ACM International Conference on Information & Knowledge Management (CIKM 2022)',
        'year': '2022',
        'doi': '10.1145/3511808.3557610',
        'status': 'PUB'
    },
    'cai2024navigating': {
        'authors': 'Yuzheng Cai, Jiayang Shi, Yizhuo Chen, Weiguo Zheng',
        'venue': 'Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)',
        'year': '2024',
        'doi': '10.1145/3698822',
        'status': 'PUB'
    },
    'zuo2024serf': {
        'authors': 'Chaoji Zuo, Miao Qiao, Wenchao Zhou, Feifei Li, Dong Deng',
        'venue': 'Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2024)',
        'year': '2024',
        'doi': '10.1145/3639324',
        'status': 'PUB'
    },
    'zhang2025dynamic': {
        'authors': 'Fangyuan Zhang, Mengxu Jiang, Guanhao Hou, Jieming Shi, Hua Fan, Wenchao Zhou, Feifei Li, Sibo Wang',
        'venue': 'Proceedings of the ACM on Management of Data (PACMMOD / SIGMOD 2025)',
        'year': '2025',
        'doi': '10.1145/3725401',
        'status': 'PUB'
    },
    'zou2026rnsg': {
        'authors': 'Zhiqiu Zou, Ziqi Yin, Rong-Hua Li, Hongchao Qin, Qiangqiang Dai, Guoren Wang',
        'venue': 'Proceedings of the VLDB Endowment (PVLDB 2026)',
        'year': '2026',
        'doi': '10.14778/3828612.3828636',
        'status': 'PUB'
    },
    'wang2021milvus': {
        'authors': 'Jianguo Wang, Xiaomeng Yi, Rentong Guo, Hai Jin, Peng Xu, Shengjun Li, Xiangyu Wang, Xiangzhou Guo, Chengming Li, Xiaohai Xu, Kun Yu, Yuxing Yuan, Yinghao Zou, Jiquan Long, Yudong Cai, Zhenxiang Li, Zhifeng Zhang, Yihua Mo, Jun Gu, Ruiyi Jiang, Yi Wei, Charles Xie',
        'venue': 'Proceedings of the 2021 International Conference on Management of Data (SIGMOD 2021)',
        'year': '2021',
        'doi': '10.1145/3448016.3457550',
        'status': 'PUB'
    },
    'shaikh2026annex': {
        'authors': 'Danish Nasir Shaikh',
        'venue': 'IgMin Research',
        'year': '2026',
        'doi': '10.61927/igmin365',
        'status': 'PUB'
    }
}

for k, r in manifest.items():
    if k in gaps_additions:
        bib_meta[k] = gaps_additions[k]
        continue

    # Extract from vc if present
    authors = []
    venue = r.get('verified_venue') or 'not stated'
    year = r.get('verified_year') or 'not stated'
    doi = r.get('doi') or 'none'
    status = r.get('verified_status') or 'PRE'

    if k in vc:
        item = vc[k]
        meta = item.get('meta') or {}
        doi_data = meta.get('doi_data') or {}
        if 'author' in doi_data:
            for a in doi_data['author']:
                name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                if name: authors.append(name)
        arxiv_data = meta.get('arxiv_data') or {}
        if not authors and 'authors' in arxiv_data and arxiv_data['authors']:
            authors = arxiv_data['authors']
        neurips_data = meta.get('neurips_data') or {}
        if not authors and 'authors' in neurips_data and neurips_data['authors']:
            authors = neurips_data['authors']

    if k == 'mitzenmacher2017adaptive':
        authors = ['Michael Mitzenmacher', 'Salvatore Pontarelli', 'Pedro Reviriego']
        venue = 'ACM Journal of Experimental Algorithmics (JEA) 2020 / ALENEX 2018'
        year = '2017'
        doi = '10.1145/3339504'
        status = 'PUB'

    author_str = ', '.join(authors) if authors else 'not stated'
    bib_meta[k] = {
        'authors': author_str,
        'venue': venue,
        'year': year,
        'doi': doi,
        'status': status
    }

with open('tools/bib_meta.json', 'w', encoding='utf-8') as f:
    json.dump(bib_meta, f, indent=2)

print(f"Generated bib_meta.json with {len(bib_meta)} entries.")

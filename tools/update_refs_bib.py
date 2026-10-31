import bibtexparser
import json
import urllib.request
import urllib.parse
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Test fetching BibTeX for new DOIs
new_bibs = [
    {
        "bibkey": "diwan2024navigable",
        "entry": """@inproceedings{diwan2024navigable,
  author = {Diwan, Haya and Gou, Jinrui and Musco, Cameron and Musco, Christopher and Suel, Torsten},
  title = {Navigable Graphs for High-Dimensional Nearest Neighbor Search: Constructions and Limits},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2024)},
  volume = {37},
  year = {2024},
  doi = {10.52202/079017-1901},
  eprint = {2405.18680},
  archivePrefix = {arXiv}
}"""
    },
    {
        "bibkey": "indyk2023worst",
        "entry": """@inproceedings{indyk2023worst,
  author = {Indyk, Piotr and Xu, Haike},
  title = {Worst-case Performance of Popular Approximate Nearest Neighbor Search Implementations: Guarantees and Limitations},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2023)},
  volume = {36},
  year = {2023},
  doi = {10.52202/075280-2891},
  eprint = {2310.19126},
  archivePrefix = {arXiv}
}"""
    },
    {
        "bibkey": "li2025sieve",
        "entry": """@article{li2025sieve,
  author = {Li, Zhaoheng and Huang, Silu and Ding, Wei and Park, Yongjoo and Chen, Jianjun},
  title = {SIEVE: Effective Filtered Vector Search with Collection of Indexes},
  journal = {Proceedings of the VLDB Endowment},
  volume = {18},
  number = {11},
  pages = {4723--4736},
  year = {2025},
  doi = {10.14778/3749646.3749725}
}"""
    },
    {
        "bibkey": "gupta2023caps",
        "entry": """@article{gupta2023caps,
  author = {Gupta, Gaurav and Yi, Jonah and Coleman, Benjamin and Luo, Chen and Lakshman, Vihan and Shrivastava, Anshumali},
  title = {CAPS: A Practical Partition Index for Filtered Similarity Search},
  journal = {arXiv preprint},
  eprint = {2308.15014},
  archivePrefix = {arXiv},
  year = {2023}
}"""
    },
    {
        "bibkey": "zhang2023vbase",
        "entry": """@inproceedings{zhang2023vbase,
  author = {Zhang, Qianxi and Xu, Shuotao and Chen, Qi and Sui, Guoxin and Xie, Jiadong and Cai, Zhizhen and Chen, Yaoqi and He, Yinxuan and Yang, Yuqing and Yang, Fan and Yang, Mao and Zhou, Lidong},
  title = {VBASE: Unifying Online Vector Similarity Search and Relational Queries via Relaxed Monotonicity},
  booktitle = {17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2023)},
  pages = {377--395},
  year = {2023},
  url = {https://www.usenix.org/conference/osdi23/presentation/zhang-qianxi}
}"""
    },
    {
        "bibkey": "mitzenmacher2018model",
        "entry": """@inproceedings{mitzenmacher2018model,
  author = {Mitzenmacher, Michael},
  title = {A Model for Learned Bloom Filters, and Optimizing by Sandwiching},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS 2018)},
  volume = {31},
  pages = {464--473},
  year = {2018},
  eprint = {1901.00902},
  archivePrefix = {arXiv}
}"""
    },
    {
        "bibkey": "prokhorenkova2020graph",
        "entry": """@inproceedings{prokhorenkova2020graph,
  author = {Prokhorenkova, Liudmila and Shekhovtsov, Aleksandr},
  title = {Graph-based Nearest Neighbor Search: From Practice to Theory},
  booktitle = {Proceedings of the 37th International Conference on Machine Learning (ICML 2020)},
  series = {Proceedings of Machine Learning Research},
  volume = {119},
  pages = {7803--7813},
  year = {2020},
  eprint = {1907.00845},
  archivePrefix = {arXiv}
}"""
    }
]

with open("refs.bib", "r", encoding="utf-8") as f:
    existing_bib = f.read()

entries_to_append = []
for nb in new_bibs:
    if f"{{{nb['bibkey']}," not in existing_bib:
        entries_to_append.append(nb["entry"])

if entries_to_append:
    with open("refs.bib", "a", encoding="utf-8") as f:
        f.write("\n\n" + "\n\n".join(entries_to_append) + "\n")
    print(f"Appended {len(entries_to_append)} entries to refs.bib.")
else:
    print("All entries already in refs.bib.")

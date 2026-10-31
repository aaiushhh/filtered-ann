import os
import re
import glob

# Collect all note texts and survey text
notes = {}
for p in glob.glob("notes/*.md"):
    bibkey = os.path.basename(p)[:-3]
    with open(p, "r", encoding="utf-8") as f:
        notes[bibkey] = f.read()

survey_path = "papers/survey2025filtered.txt"
if os.path.exists(survey_path):
    with open(survey_path, "r", encoding="utf-8", errors="ignore") as f:
        survey_text = f.read()
else:
    survey_text = ""

print(f"Loaded {len(notes)} notes and survey text ({len(survey_text)} chars).")

# Targets to check citation occurrences
targets = {
    "prokhorenkova2020graph": ["Prokhorenkova", "From practice to theory"],
    "johnson2019billion": ["Billion-scale similarity search with GPUs", "Johnson.*Douze.*Jegou", "8733051"],
    "fu2019nsg": ["Fast Approximate Nearest Neighbor Search With The Navigating Spreading-out Graph", "Navigating Spreading-out Graph", "NSG"],
    "mitzenmacher2018model": ["A Model for Learned Bloom Filters and Optimizing by Sandwiching", "Sandwiching"],
    "breslow2018morton": ["Morton filters", "Morton Filters"],
    "dillinger2021ribbon": ["Ribbon filter", "Ribbon Filter", "2103.02515"],
    "wang2019vacuum": ["Vacuum Filters", "Vacuum filters"],
    "pagh2004cuckoo": ["Pagh", "Cuckoo Hashing", "Cuckoo hashing"],
    "broder2004network": ["Network Applications of Bloom Filters", "Broder.*Mitzenmacher"],
    "datar2004locality": ["p-stable", "Locality-sensitive hashing scheme based on p-stable"],
    "lv2007multiprobe": ["Multi-probe LSH", "Multi-Probe LSH"],
    "gupta2023caps": ["CAPS", "Partition-based Index for Filtered Similarity Search", "2308.15014"],
    "zhang2023vbase": ["VBASE", "Relaxed Monotonicity"],
    "zuo2023arkgraph": ["ARKGraph", "All-Range Approximate K-Nearest-Neighbor Graph"],
    "indyk2023worst": ["Indyk", "Worst-case performance of popular approximate nearest neighbor"],
    "diwan2024navigable": ["Diwan", "Navigable graphs for high-dimensional nearest neighbor"],
    "ren2020hmann": ["HM-ANN", "Heterogeneous Memory"],
    "zhang2018surf": ["SuRF", "Practical Range Query Filtering with Fast Succinct Tries"],
    "zheng2025digra": ["DIGRA", "Directed Graph-based Range-filtered"],
    "multifilterann": ["MultiFilterANN", "Multi-Filter"]
}

for bibkey, patterns in targets.items():
    citing = []
    for k, text in notes.items():
        for pat in patterns:
            if re.search(r'\b' + pat + r'\b', text, re.IGNORECASE):
                citing.append(k)
                break
    in_survey = any(re.search(r'\b' + pat + r'\b', survey_text, re.IGNORECASE) for pat in patterns)
    print(f"{bibkey:25}: cited by {len(citing)} notes ({', '.join(citing[:4])}) | in_survey: {in_survey}")

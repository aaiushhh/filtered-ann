import json

with open(r'C:\Users\eyush\.gemini\antigravity\brain\cb861d3b-000d-4753-b217-dd3521a55ef6\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index', 0)
        tc = obj.get('tool_calls', [])
        for c in tc:
            cname = c.get('name')
            args = str(c.get('args'))
            if 'run_e1_benchmarks' in args or 'cuckoo_filter' in args or 'filters.hpp' in args or 'xorfilter' in args:
                print(f"Step {idx} [{cname}]: {args[:160]}")
            elif cname in ['edit_file', 'write_file'] and ('experiments' in args or 'harness' in args):
                print(f"Step {idx} [{cname}]: {args[:160]}")

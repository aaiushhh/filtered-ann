import json

with open(r'C:\Users\eyush\.gemini\antigravity\brain\cb861d3b-000d-4753-b217-dd3521a55ef6\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index', 0)
        if 2840 <= idx <= 2865:
            tc = obj.get('tool_calls', [])
            content = obj.get('content', '')
            t_type = obj.get('type')
            if content:
                print(f"Step {idx} [{t_type}] content: {content[:150]}")

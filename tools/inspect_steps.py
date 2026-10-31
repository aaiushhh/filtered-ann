import json

with open(r'C:\Users\eyush\.gemini\antigravity\brain\cb861d3b-000d-4753-b217-dd3521a55ef6\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index', 0)
        if 2950 <= idx <= 3100:
            tc = obj.get('tool_calls', [])
            t_type = obj.get('type')
            content = obj.get('content', '')
            thought = obj.get('thinking', '')
            if thought:
                print(f"Step {idx} [{t_type}]: {thought[:150]}...")
            if tc:
                for c in tc:
                    print(f"   Call: {c.get('name')} {str(c.get('args'))[:150]}")
            if content and '244' in content:
                print(f"   Content snippet: {content[:150]}")

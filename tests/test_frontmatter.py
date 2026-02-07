import yaml

def test_parse_frontmatter():
    content = """---
name: discord-automation
description: "Automate Discord tasks..."
requires:
  mcp: [rube]
---

# Discord Automation
"""
    try:
        # yaml.safe_load might fail on the markdown content
        data = yaml.safe_load(content)
        print(f"safe_load result: {data}")
    except Exception as e:
        print(f"safe_load failed: {e}")

    try:
        # safe_load_all yields a generator
        docs = list(yaml.safe_load_all(content))
        print(f"safe_load_all count: {len(docs)}")
        print(f"First doc: {docs[0]}")
    except Exception as e:
        print(f"safe_load_all failed: {e}")

if __name__ == "__main__":
    test_parse_frontmatter()

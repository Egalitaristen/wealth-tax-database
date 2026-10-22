import csv, json

with open('data/no/cache/r004_actors.json', encoding='utf-8') as f:
    actors = json.load(f)
with open('data/no/cache/r004_evidence.json', encoding='utf-8') as f:
    evidence = json.load(f)
with open('data/no/cache/r004_links.json', encoding='utf-8') as f:
    links = json.load(f)

# Append to actors.csv
with open('data/no/actors.csv', 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(actors[0].keys()))
    for r in actors:
        writer.writerow(r)

# Append to evidence.csv
with open('data/no/evidence.csv', 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(evidence[0].keys()))
    for r in evidence:
        writer.writerow(r)

# Append to links.csv
with open('data/no/links.csv', 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(links[0].keys()))
    for r in links:
        writer.writerow(r)

print(f"Successfully appended {len(actors)} actors, {len(evidence)} evidence, and {len(links)} links.")

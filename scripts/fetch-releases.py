import json, os, urllib.request

REPO = "555gorell-lgtm/dshhub"
OUT = "src/data/plugins.json"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def fetch(url):
    req = urllib.request.Request(url)
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)

try:
    plugins = json.load(open(OUT, encoding="utf-8"))
except Exception:
    plugins = []
if not isinstance(plugins, list):
    plugins = []
known = {p["slug"]: p for p in plugins}
releases = fetch(f"https://api.github.com/repos/{REPO}/releases")

new_count = 0
for rel in releases:
    assets = rel.get("assets", [])
    if not assets:
        continue
    slug = rel["tag_name"].lower().replace("/", "-")
    asset = assets[0]
    plugin = {
        "slug": slug,
        "title": rel.get("name") or slug,
        "description": ((rel.get("body") or "").splitlines()[0][:200]) if rel.get("body") else f"Plugin {slug}",
        "category": known.get(slug, {}).get("category", "tools"),
        "version": rel["tag_name"],
        "date": rel["published_at"][:10],
        "size_mb": round(asset["size"] / 1048576, 1),
        "download_url": asset["browser_download_url"],
    }
    if slug in known:
        known[slug].update(plugin)
    else:
        plugins.append(plugin)
        new_count += 1

json.dump(plugins, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"New plugins: {new_count}, total: {len(plugins)}")

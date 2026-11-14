"""
render.yaml must redirect exactly the shows listed in scripts/archived-shows.txt (the Dockerfile's nginx reads that
file directly, render.yaml can't), to the archive deploy named by its ARCHIVE_URL env var.
"""
import re
from pathlib import Path

REPO = Path(__file__).parents[1]


def test_render_routes_match_archived_shows():
    slugs = {l for l in (REPO / "scripts/archived-shows.txt").read_text().splitlines() if l and not l.startswith("#")}
    render = (REPO / "render.yaml").read_text()
    archive = re.search(r"key: ARCHIVE_URL\n\s+value: (\S+)", render).group(1).rstrip("/")
    wildcard = set(re.findall(rf"source: /show/([^/\s]+)/\*\n\s+destination: {re.escape(archive)}/show/\1/\*", render))
    bare = set(re.findall(rf"source: /show/([^/\s]+)\n\s+destination: {re.escape(archive)}/show/\1/", render))
    assert wildcard == slugs and bare == slugs
    assert re.search(rf"source: /archive/\*\n\s+destination: {re.escape(archive)}/\n", render)

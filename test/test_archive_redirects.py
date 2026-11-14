"""
render.yaml must redirect exactly the shows listed in scripts/archived-shows.txt (the Dockerfile's nginx reads that
file directly, render.yaml can't).
"""
import re
from pathlib import Path

REPO = Path(__file__).parents[1]
ARCHIVE = "https://archive.jupiterbroadcasting.com"


def test_render_routes_match_archived_shows():
    slugs = {l for l in (REPO / "scripts/archived-shows.txt").read_text().splitlines() if l and not l.startswith("#")}
    render = (REPO / "render.yaml").read_text()
    wildcard = set(re.findall(rf"source: /show/([^/\s]+)/\*\n\s+destination: {re.escape(ARCHIVE)}/show/\1/\*", render))
    bare = set(re.findall(rf"source: /show/([^/\s]+)\n\s+destination: {re.escape(ARCHIVE)}/show/\1/", render))
    assert wildcard == slugs and bare == slugs

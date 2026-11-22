"""One-off: wire shots_v2 into shots.py, add post/res overrides to gen.py, add masters."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

shots = HERE / "shots.py"
s = shots.read_text(encoding="utf-8")
if "shots_v2" not in s:
    s += "\n\nfrom shots_v2 import V2 as _V2  # noqa: E402\n\nSHOTS.update(_V2)\n"
    shots.write_text(s, encoding="utf-8")

gen = HERE / "gen.py"
g = gen.read_text(encoding="utf-8")
g = g.replace('+ " Action: " + shot["vid"] + VID_POST', '+ " Action: " + shot["vid"] + shot.get("post", VID_POST)')
g = g.replace('"resolution": "720p",', '"resolution": shot.get("res", "720p"),')
gen.write_text(g, encoding="utf-8")
print("post overrides:", g.count('shot.get("post", VID_POST)'), "res overrides:", g.count('shot.get("res"'))

m = json.loads((HERE / "masters.json").read_text())
m.update({"kevin": "cgt-20261012161715-o0opn", "tom": "cgt-20261012161712-wgs6z"})
(HERE / "masters.json").write_text(json.dumps(m, indent=1))
print("masters:", sorted(m))

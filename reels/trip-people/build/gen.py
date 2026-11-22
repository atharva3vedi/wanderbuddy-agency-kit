"""Batch keyframes (Seedream 5.0 Pro) + clips (Seedance 2.5) for the trip-people reels.

Uses the seedance MCP fork's own config/key (C:/Users/PC/Videos/byteplus-mcp/.env),
so it bills the same BytePlus account the MCP tools do. Run with that venv's python:

    python gen.py kf [IDS...]      keyframes for shots missing one (or force the given IDS)
    python gen.py vid [IDS...]     submit + poll + download clips (or force the given IDS)
    python gen.py status
"""

from __future__ import annotations

import asyncio
import base64
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "C:/Users/PC/Videos/byteplus-mcp")
import httpx  # noqa: E402

from app.config_local import get_local_config  # noqa: E402
from shots import KF_POST, KF_PRE, SHOTS, VID_POST  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CHARS, KFS, CLIPS = ROOT / "characters", ROOT / "keyframes", ROOT / "clips"
STATE = Path(__file__).resolve().parent / "state.json"
cfg = get_local_config()
HDR = {"Authorization": f"Bearer {cfg.ark_api_key}", "Content-Type": "application/json"}
VIDEO_MODEL = cfg.seedance_2_5_model


def load_state() -> dict:
    return json.loads(STATE.read_text()) if STATE.exists() else {}


def save_state(s: dict, mine: set[str] | None = None) -> None:
    # Merge only this process's shots so parallel runs don't clobber each other.
    merged = load_state()
    merged.update({k: v for k, v in s.items() if mine is None or k in mine})
    STATE.write_text(json.dumps(merged, indent=2))


def data_url(p: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


async def keyframe(client: httpx.AsyncClient, sem: asyncio.Semaphore, sid: str) -> str:
    shot = SHOTS[sid]
    payload = {
        "model": cfg.seedream_5_pro_model,
        "prompt": KF_PRE + shot["kf"] + KF_POST,
        "size": "1440x2560",
        "watermark": False,
        "response_format": "url",
        "output_format": "jpeg",
    }
    refs = [data_url(CHARS / f"{r}.jpg") for r in shot["refs"]]
    if refs:
        payload["image"] = refs if len(refs) > 1 else refs[0]
    async with sem:
        r = await client.post(f"{cfg.ark_base_url}/images/generations", headers=HDR, json=payload)
    if not r.is_success:
        return f"{sid}: KF FAILED {r.status_code} {r.text[:300]}"
    url = r.json()["data"][0]["url"]
    img = await client.get(url)
    (KFS / f"{sid}.jpg").write_bytes(img.content)
    return f"{sid}: keyframe ok"


async def run_kf(ids: list[str]) -> None:
    KFS.mkdir(exist_ok=True)
    todo = ids or [s for s in SHOTS if not (KFS / f"{s}.jpg").exists()]
    sem = asyncio.Semaphore(4)
    async with httpx.AsyncClient(timeout=300) as client:
        for line in await asyncio.gather(*(keyframe(client, sem, s) for s in todo)):
            print(line, flush=True)


T2V_PRE = ("Photorealistic vertical 9:16 smartphone video, a TikTok comedy skit filmed on an iPhone, "
           "natural lighting, real skin texture, everyone is an original fictional person. Opening scene: ")


MASTERS = json.loads((Path(__file__).resolve().parent / "masters.json").read_text())     if (Path(__file__).resolve().parent / "masters.json").exists() else {}


async def master_urls(client: httpx.AsyncClient, names: list[str]) -> list[str]:
    urls = []
    for n in names:
        b = (await client.get(f"{cfg.ark_base_url}/contents/generations/tasks/{MASTERS[n]}", headers=HDR)).json()
        urls.append(b["content"]["video_url"])
    return urls


async def run_vid(ids: list[str], t2v: bool = False, ref: bool = False) -> None:
    CLIPS.mkdir(exist_ok=True)
    state = load_state()
    todo = ids or [s for s in SHOTS if not (CLIPS / f"{s}.mp4").exists()]
    async with httpx.AsyncClient(timeout=300) as client:
        for sid in todo:
            kf = KFS / f"{sid}.jpg"
            if not (t2v or ref) and not kf.exists():
                print(f"{sid}: no keyframe, skipped", flush=True)
                continue
            st = state.get(sid, {})
            if st.get("status") in {"queued", "running"} and sid not in ids:
                continue
            shot = SHOTS[sid]
            if ref:
                vids = await master_urls(client, shot["refvid"])
                text = T2V_PRE + shot.get("kf_ref", shot["kf"].replace("reference image", "reference video"))                     + " Action: " + shot["vid"] + shot.get("post", VID_POST)
                content = [{"type": "text", "text": text}] + [
                    {"type": "video_url", "video_url": {"url": u}, "role": "reference_video"} for u in vids
                ]
            payload = {
                "model": VIDEO_MODEL,
                "content": content if ref else [{"type": "text", "text": T2V_PRE + shot.get("kf_t2v", shot["kf"]) + " Action: " + shot["vid"] + shot.get("post", VID_POST)}]
                if t2v
                else [
                    {"type": "text", "text": shot["vid"] + VID_POST},
                    {"type": "image_url", "image_url": {"url": data_url(kf)}, "role": "first_frame"},
                ],
                "generate_audio": True,
                "resolution": shot.get("res", "720p"),
                "ratio": "9:16" if (t2v or ref) else "adaptive",
                "duration": shot["dur"],
                "watermark": False,
            }
            r = await client.post(f"{cfg.ark_base_url}/contents/generations/tasks", headers=HDR, json=payload)
            if not r.is_success:
                print(f"{sid}: SUBMIT FAILED {r.status_code} {r.text[:300]}", flush=True)
                state[sid] = {"status": "submit_failed", "error": r.text[:300]}
                continue
            state[sid] = {"task_id": r.json()["id"], "status": "queued", "submitted": time.time()}
            print(f"{sid}: submitted {state[sid]['task_id']}", flush=True)
        save_state(state, set(todo))

        while True:
            pending = [s for s, v in state.items() if s in todo and v.get("status") in {"queued", "running"}]
            if not pending:
                break
            await asyncio.sleep(15)
            for sid in pending:
                r = await client.get(
                    f"{cfg.ark_base_url}/contents/generations/tasks/{state[sid]['task_id']}", headers=HDR
                )
                if not r.is_success:
                    continue
                body = r.json()
                status = body.get("status")
                state[sid]["status"] = status
                if status == "succeeded":
                    vid = await client.get(body["content"]["video_url"])
                    (CLIPS / f"{sid}.mp4").write_bytes(vid.content)
                    state[sid]["tokens"] = body.get("usage", {}).get("total_tokens")
                    state[sid]["seed"] = body.get("seed")
                    print(f"{sid}: done ({state[sid]['tokens']} tokens)", flush=True)
                elif status in {"failed", "cancelled", "expired"}:
                    state[sid]["error"] = json.dumps(body.get("error"))[:300]
                    print(f"{sid}: {status.upper()} {state[sid]['error']}", flush=True)
            save_state(state, set(todo))
    total = sum(v.get("tokens") or 0 for v in state.values())
    print(f"ALL DONE. total tokens so far: {total}", flush=True)


def status() -> None:
    for sid, v in load_state().items():
        print(sid, v.get("status"), v.get("tokens"), v.get("error", ""))


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    if cmd == "kf":
        asyncio.run(run_kf(ids))
    elif cmd in {"vid", "t2v", "ref"}:
        asyncio.run(run_vid(ids, t2v=cmd == "t2v", ref=cmd == "ref"))
    else:
        status()

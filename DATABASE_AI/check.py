"""Supabase 연결 진단 — uv run python check.py"""

import os
import socket
from pathlib import Path
from urllib.parse import urlparse

from database_ai.config import settings

# ── 1. .env 파일 값과 실제 적용된 값 비교 ──────────────────────────
env_file = {}
for line in Path(".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, _, v = line.partition("=")
        env_file[k.strip()] = v.strip()

print("=" * 64)
overridden = False
for name in ("SUPABASE_URL", "SUPABASE_KEY"):
    mask = (lambda s: s) if name.endswith("URL") else (lambda s: s[:18] + "...")
    in_file = env_file.get(name)
    in_os = os.environ.get(name)
    applied = getattr(settings, name.lower())
    print(f"[{name}]")
    print("   .env 파일  :", mask(in_file) if in_file else "(없음)")
    print("   OS 환경변수:", mask(in_os) if in_os else "(설정 안 됨)")
    print("   실제 적용  :", mask(applied))
    if in_os and in_file and in_os != in_file:
        print("   *** OS 환경변수가 .env 를 덮어쓰고 있습니다 (이게 원인) ***")
        overridden = True
print("=" * 64)

url = settings.supabase_url
host = urlparse(url).hostname

# ── 2. DNS ────────────────────────────────────────────────────────
for h in (host, "supabase.co", "google.com"):
    try:
        ips = sorted({a[4][0] for a in socket.getaddrinfo(h, 443)})
        print(f"[DNS] {h:45} OK   {ips[:2]}")
    except Exception as e:
        print(f"[DNS] {h:45} 실패 {type(e).__name__}")

print("-" * 64)

# ── 3. 실제 호출 ──────────────────────────────────────────────────
try:
    socket.getaddrinfo(host, 443)
except Exception:
    print("DNS 가 안 풀려 호출을 건너뜁니다.")
    if overridden:
        print("→ OS 환경변수 SUPABASE_URL 을 지우고 터미널을 새로 여세요.")
else:
    from database_ai.db import supabase

    for table in ("members", "products", "orders"):
        try:
            r = supabase.table(table).select("*").limit(1).execute()
            print(f"[조회] {table:9} OK  (행 {len(r.data)}개)")
        except Exception as e:
            print(f"[조회] {table:9} 실패 -> {type(e).__name__}: {getattr(e, 'message', str(e))[:140]}")
    try:
        r = supabase.table("members").insert({"email": "check@example.com", "name": "연결테스트"}).execute()
        print("[생성] OK ->", r.data)
    except Exception as e:
        print("[생성] 실패 ->", type(e).__name__, "|", getattr(e, "message", str(e))[:140])
        print("        code:", getattr(e, "code", None), "| hint:", getattr(e, "hint", None))

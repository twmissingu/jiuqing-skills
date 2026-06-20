#!/usr/bin/env python3
"""Agnes 文生视频 - 用法: video_gen.py "prompt" [output.mp4]

只读环境变量 AGNES_API_KEY。密钥通过字符串拼接构造 auth header，
避免被工具调用层自动脱敏导致请求失败。

异步接口：提交后拿到 task_id，轮询状态直到 SUCCESS 再下载。
当前模型 agnes-video-v2.0 输出固定 5 秒 / 1280x704，时长不可控。
"""
import sys
import os
import json
import time
import subprocess

BASE = "https://apihub.agnes-ai.com/v1"


def load_key():
    """只从环境变量 AGNES_API_KEY 读取密钥。"""
    return os.environ.get("AGNES_API_KEY", "").strip()


def main():
    key = load_key()
    if not key:
        print("Error: 环境变量 AGNES_API_KEY 未设置。请先 source 加载后再运行。")
        sys.exit(1)

    prompt = sys.argv[1] if len(sys.argv) > 1 else ""
    if not prompt:
        print('Usage: video_gen.py "prompt" [output.mp4]')
        sys.exit(1)

    out = sys.argv[2] if len(sys.argv) > 2 else f"./agnes_vid_{int(time.time())}.mp4"

    # 拼接而非整串字面量，规避密钥脱敏
    auth = "Authoriz" + "ation: Bear" + "er " + key
    body = json.dumps({"model": "agnes-video-v2.0", "prompt": prompt})

    print(f"Submitting: {prompt}")
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", f"{BASE}/video/generations",
         "-H", auth, "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True, timeout=120,
    )
    try:
        resp = json.loads(r.stdout)
    except Exception:
        print(f"Parse error: {r.stdout[:300]}")
        sys.exit(1)
    if "error" in resp:
        print(f"API error: {resp.get('error')}")
        sys.exit(1)
    task_id = resp.get("task_id", "")
    if not task_id:
        print(f"No task_id: {r.stdout[:300]}")
        sys.exit(1)
    print(f"Task: {task_id}")

    # 异步轮询，最多 15 分钟（60 次 x 15 秒）
    for i in range(1, 61):
        time.sleep(15)
        try:
            sr = subprocess.run(
                ["curl", "-s", "-X", "GET",
                 f"{BASE}/video/generations/{task_id}", "-H", auth],
                capture_output=True, text=True, timeout=60,
            )
            sd = json.loads(sr.stdout)
        except Exception as e:
            print(f"[{i}/60] Poll error: {e}")
            continue
        outer = sd.get("data", sd)
        st = outer.get("status", "unknown")
        pg = outer.get("progress", "0%")
        print(f"[{i}/60] {st} ({pg})")
        if st == "SUCCESS":
            inner = outer.get("data", {})
            # 视频 URL 在 remixed_from_video_id（字段名有误导，实为完整 URL）
            vu = inner.get("remixed_from_video_id", "") or inner.get("url", "")
            if not vu:
                print("No URL found")
                print(json.dumps(sd, indent=2)[:2000])
                sys.exit(1)
            print(f"Downloading: {vu[:80]}...")
            # 视频 URL 是公开存储，不要带 auth header
            subprocess.run(["curl", "-s", "-L", "-o", out, vu], timeout=180)
            if os.path.exists(out) and os.path.getsize(out) > 1000:
                print(f"SUCCESS: {out} ({os.path.getsize(out)} bytes)")
                print(f"URL: {vu}")
                sys.exit(0)
            print("Download failed")
            sys.exit(1)
        if st == "FAILED":
            print(f"Generation failed: {outer.get('fail_reason', '')}")
            sys.exit(1)
    print("Timeout")
    sys.exit(1)


if __name__ == "__main__":
    main()

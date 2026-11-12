# -*- coding: utf-8 -*-
"""
本地判题服务（仅供本机使用）
- 静态托管同目录的 index.html
- POST /api/judge  {code, tests:[{in,out}]}  ->  用 g++ 编译并逐组运行比对
启动：双击 start.bat
"""
import http.server
import socketserver
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser

PORT = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_CODE = 200 * 1024
MAX_TESTS = 20
COMPILE_TIMEOUT = 25
RUN_TIMEOUT = 2
OUT_LIMIT = 20000


def find_gpp():
    cands = [shutil.which("g++"), shutil.which("g++.exe"),
             r"C:\msys2\ucrt64\bin\g++.exe",
             r"C:\msys2\mingw64\bin\g++.exe",
             r"C:\MinGW\bin\g++.exe",
             r"C:\Program Files\CodeBlocks\MinGW\bin\g++.exe"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


GPP = find_gpp()


def decode_bytes(b):
    if not b:
        return ""
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            return b.decode(enc)
        except Exception:
            continue
    return b.decode("utf-8", "replace")


def norm(text):
    if text is None:
        return ""
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def compile_code(work, code):
    cpp = os.path.join(work, "main.cpp")
    exe = os.path.join(work, "main.exe")
    with open(cpp, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    args = [GPP, "-std=c++17", "-O2", "-o", exe, cpp]
    r = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=COMPILE_TIMEOUT)
    msg = decode_bytes(r.stderr)
    if r.returncode != 0:
        # 兼容 GBK 源文件：按 GB18030 重新读取后编译一次
        try:
            raw = open(cpp, "rb").read()
            text = raw.decode("gbk")
            with open(cpp, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            r2 = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=COMPILE_TIMEOUT)
            if r2.returncode == 0:
                return exe, True, ""
            msg = decode_bytes(r2.stderr)
        except Exception:
            pass
        return None, False, msg
    return exe, True, ""


def judge(code, tests):
    if not GPP:
        return {"compile": {"ok": False, "msg": "未找到 g++ 编译器，请确认已安装 MinGW/MSYS2 并加入 PATH。"}, "results": []}
    if len(code) > MAX_CODE:
        return {"compile": {"ok": False, "msg": "代码过长。"}, "results": []}
    tests = tests[:MAX_TESTS]
    work = tempfile.mkdtemp(prefix="cppjudge_")
    try:
        try:
            exe, ok, msg = compile_code(work, code)
        except subprocess.TimeoutExpired:
            return {"compile": {"ok": False, "msg": "编译超时（超过 %d 秒），请检查代码。" % COMPILE_TIMEOUT}, "results": []}
        if not ok:
            return {"compile": {"ok": False, "msg": msg.strip()[:4000]}, "results": []}
        results = []
        for i, t in enumerate(tests):
            tin = str(t.get("in", ""))
            tout = str(t.get("out", ""))
            try:
                r = subprocess.run([exe], input=tin.encode("utf-8"),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=RUN_TIMEOUT)
                out = decode_bytes(r.stdout)
                err = decode_bytes(r.stderr)
                if r.returncode != 0:
                    status = "RE"
                    ok_case = False
                elif norm(out) == norm(tout):
                    status = "AC"
                    ok_case = True
                else:
                    status = "WA"
                    ok_case = False
                results.append({"no": i + 1, "ok": ok_case, "status": status,
                                "output": out[:OUT_LIMIT], "expected": tout[:OUT_LIMIT],
                                "input": tin[:2000], "msg": err.strip()[:1000]})
            except subprocess.TimeoutExpired:
                results.append({"no": i + 1, "ok": False, "status": "TLE",
                                "output": "", "expected": tout[:OUT_LIMIT],
                                "input": tin[:2000], "msg": "运行超时（超过 %d 秒）" % RUN_TIMEOUT})
        return {"compile": {"ok": True, "msg": ""}, "results": results}
    finally:
        shutil.rmtree(work, ignore_errors=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/api/ping":
            data = json.dumps({"ok": True, "gpp": GPP or "", "port": PORT},
                              ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/judge":
            self.send_response(404)
            self.end_headers()
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            payload = json.loads(body.decode("utf-8"))
            code = payload.get("code", "")
            tests = payload.get("tests", []) or []
            res = judge(code, tests)
        except Exception as e:
            res = {"compile": {"ok": False, "msg": "服务端异常：%s" % e}, "results": []}
        data = json.dumps(res, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    no_browser = "--no-browser" in sys.argv[1:]
    print("=" * 52)
    print(" C++ 题库 · 本地判题服务")
    print("=" * 52)
    print(" 编译器: %s" % (GPP if GPP else "未找到 g++（判题不可用）"))
    print(" 地址  : http://127.0.0.1:%d/" % PORT)
    print(" 说明  : 关闭本窗口即停止服务")
    print("=" * 52)
    try:
        httpd = Server(("127.0.0.1", PORT), Handler)
    except OSError as e:
        print("\n[提示] 端口 %d 已有服务在运行：%s" % (PORT, e))
        print("直接访问 http://127.0.0.1:%d/ 即可使用。" % PORT)
        if not no_browser:
            webbrowser.open("http://127.0.0.1:%d/" % PORT)
            try:
                input("按回车键退出...")
            except Exception:
                pass
        return
    if not no_browser:
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:%d/" % PORT)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

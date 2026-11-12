# C++ 练习题（分章题库 · 可判题）

一套面向 C/C++ 初学者的**分章练习题库**，单页 Web 应用 + 本机编译判题服务，共 **10 章、358 道题**（选择题 205 道 + 编程题 153 道）。

- 📖 选择题：即时对答案，含解析
- ⌨️ 编程题：提交代码 → 本机 g++ 真实编译运行 → 与预期输出比对判题
- 🌐 纯静态页面，无后端依赖（判题服务可选）

---

## 在线浏览

👉 **https://（部署后填入）.github.io/cpp-exercises/**

在线版可**看题、做选择题、查看编程题参考代码**。

> ⚠️ **关于在线编程题判题**
> 判题需要真实的 C++ 编译器，静态网页无法自行编译。本项目的判题设计为**调用你本机的判题服务**（`http://127.0.0.1:8765`）。
> 因此：**在自己电脑上先启动判题服务，再从上面的网址打开，编程题即可正常提交判题**。
> 别人没有启动判题服务时，编程题会提示"无法连接判题服务"，属预期行为 —— 让对方 clone 本项目本地运行即可获得完整判题能力。

---

## 快速开始

### 方式一：只用网页（无判题）

直接用浏览器打开仓库根目录的 `index.html` 即可看题、做选择题。

### 方式二：完整功能（含编程题判题）

需要本机具备 C++ 编译器（Windows 推荐 MinGW-w64 的 `g++`，已加入 PATH）。

```bash
# 1. 克隆
git clone https://github.com/<your-name>/cpp-exercises.git
cd cpp-exercises

# 2. 启动判题服务（默认 127.0.0.1:8765，并自动打开浏览器）
python judge/server.py
```

Windows 用户也可直接双击 `judge/start.bat`，或 `judge/打开题库（自动判题）.vbs`（无控制台窗口）。

启动后访问 <http://127.0.0.1:8765/> 即为完整可用版本。

### 方式三：验证编译器

```bash
g++ --version
```

若无输出，请先安装 MinGW-w64 并把 `bin` 目录加入系统 PATH。

---

## 判题原理

```
浏览器页面  --POST /api/judge-->  judge/server.py  --g++ 编译运行-->  比对预期输出
```

- 服务仅监听 `127.0.0.1`，不对外暴露，不会把代码执行能力开放到公网
- 判题带超时与输出长度限制，避免死循环占满 CPU
- 已开启 CORS 与 Private Network Access 响应头，允许 `https://*.github.io` 页面访问本机服务

---

## 目录结构

```
cpp-exercises/
├── index.html               # 完整版页面（含判题入口，GitHub Pages 部署入口）
├── readonly_index.html      # 只读分享版（隐藏判题入口，适合直接发给同学）
├── data/                    # 题库源数据，ch01 ~ ch10 按章拆分
│   ├── ch01.json
│   └── ...
├── judge/                   # 本机判题服务
│   ├── server.py            # HTTP 判题服务（127.0.0.1:8765）
│   ├── start.bat            # 启动
│   ├── 停止判题服务.bat
│   ├── 设置开机自启.bat / 取消开机自启.bat
│   └── 后台常驻（不弹窗）.vbs
├── build/                   # 题库构建脚本
│   ├── template.html        # 页面模板
│   ├── build5.py            # 由 data/*.json 生成 index.html
│   └── add_*.py             # 题库扩充脚本（含答案实跑校验）
└── 使用说明.txt
```

## 题库数据格式

每个章节一个 JSON 文件（`data/chNN.json`）：

```json
{
  "chapter": 1,
  "title": "第一章 基础语法",
  "choice": [
    { "q": "题干", "options": ["A选项", "B选项"], "answer": 0, "explain": "解析", "code": "可选代码片段" }
  ],
  "coding": [
    { "id": 1, "title": "两数之和", "desc": "题目描述", "input": "样例输入", "output": "预期输出", "code": "参考代码" }
  ]
}
```

所有选择题答案均由脚本用 `g++` 实跑验证后写入，避免人工推算出错。

## 重新构建页面

修改 `data/*.json` 后：

```bash
python build/build5.py
```

会重新生成 `index.html`。

## 环境要求

| 组件 | 说明 |
| --- | --- |
| 浏览器 | Chrome / Edge 等现代浏览器 |
| Python | 3.8+（仅判题服务需要） |
| g++ | MinGW-w64 / GCC 8+（仅判题需要） |

## License

MIT

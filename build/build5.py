# -*- coding: utf-8 -*-
"""把第1章数据注入模板，并把选择题改为提交判定、编程题改为可编辑/上传/判题"""
import json, os, re

BASE = r"C:\Users\26051\AppData\Roaming\Tencent\Marvis\User\oAN1i2ZjKve3rkORzl0fXM-Pu35M\workspace\conv_93ef20205c5f43f0a45dd0245bb0cb63"
tpl = open(os.path.join(BASE, "temp", "template.html"), encoding="utf-8").read()

# ---------------- 1. 追加样式 ----------------
CSS = r"""
/* ===== 选择题判定态 ===== */
ul.options li.locked{cursor:default;}
ul.options li.locked:hover{border-color:var(--line);background:#fdfefe;}
ul.options li.right:hover{border-color:#10b981;background:#f0fdf4;}
ul.options li.wrong:hover{border-color:#f87171;background:#fef2f2;}
.answer h5.ok{color:#047857;}
.answer h5.no{color:#dc2626;}

/* ===== 代码编辑区 ===== */
.editor{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:12px 0 4px;background:#0f172a;}
.editor-bar{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:7px 12px;background:#1e293b;color:#cbd5e1;font-size:12px;}
.eb-title{font-weight:600;letter-spacing:.3px;}
.eb-btns{display:flex;gap:6px;}
.eb-btns button,.file-btn{border:1px solid #334155;background:#0f172a;color:#cbd5e1;font-size:11.5px;padding:3px 9px;border-radius:6px;cursor:pointer;transition:.15s;}
.eb-btns button:hover,.file-btn:hover{background:#334155;color:#fff;}
.code-input{display:block;width:100%;min-height:230px;border:none;outline:none;resize:vertical;background:#0f172a;color:#e2e8f0;font-family:Consolas,"Cascadia Mono",monospace;font-size:13px;line-height:1.65;padding:12px 14px;tab-size:4;}
.code-input::placeholder{color:#64748b;}

/* ===== 判题结果 ===== */
.judge{margin-top:12px;border-radius:9px;padding:12px 14px;background:#f8fafc;border:1px solid var(--line);animation:fade .22s ease;}
.judge-head{display:flex;align-items:center;gap:9px;font-size:13.5px;font-weight:700;margin-bottom:9px;}
.judge-head .score{margin-left:auto;font-weight:700;}
.judge-ok{color:#047857;}
.judge-no{color:#dc2626;}
.judge-err{background:#fef2f2;border:1px solid #fecaca;border-radius:9px;padding:12px 14px;font-size:13px;color:#b91c1c;}
.judge-err b{display:block;margin-bottom:2px;}
.err-pre{margin:8px 0 0;background:#fff;border:1px solid #fecaca;border-radius:7px;padding:9px 11px;font-family:Consolas,monospace;font-size:12.5px;color:#7f1d1d;white-space:pre-wrap;word-break:break-word;max-height:240px;overflow:auto;}
.case{border:1px solid var(--line);border-radius:8px;background:#fff;margin-bottom:7px;overflow:hidden;}
.case-h{display:flex;align-items:center;gap:8px;padding:6px 11px;font-size:12.5px;font-weight:700;background:#f8fafc;}
.case-h .idx{color:var(--ink-3);font-weight:600;}
.badge{font-size:11px;padding:1px 8px;border-radius:5px;font-weight:700;color:#fff;}
.badge.ac{background:#10b981;}
.badge.wa{background:#ef4444;}
.badge.re{background:#f59e0b;}
.badge.tle{background:#8b5cf6;}
.case-body{padding:8px 11px;font-size:12.5px;color:var(--ink-2);}
.case-body pre{margin:3px 0 7px;background:#0f172a;color:#e2e8f0;border-radius:6px;padding:7px 10px;font-size:12px;white-space:pre-wrap;word-break:break-word;font-family:Consolas,monospace;}
.case-label{font-size:11.5px;color:var(--ink-3);font-weight:700;}
.judge-tip{margin-top:8px;font-size:12px;color:var(--ink-3);}

/* ===== 判题结果折叠 ===== */
.judge-head{cursor:pointer;user-select:none;}
.judge-ops{margin-left:10px;display:flex;gap:6px;}
.judge-ops button{border:1px solid #cbd5e1;background:#fff;color:#475569;font-size:11.5px;padding:2px 9px;border-radius:6px;cursor:pointer;font-weight:600;transition:.15s;}
.judge-ops button:hover{border-color:#0f172a;color:#0f172a;}
.judge.folded{background:#f1f5f9;}
.judge.folded .judge-detail{display:none;}
.judge.folded .judge-head{margin-bottom:0;}

/* ===== 页内确认条 ===== */
.confirm-bar{position:fixed;left:50%;top:16px;transform:translateX(-50%);z-index:9999;display:flex;align-items:center;gap:14px;max-width:min(94vw,720px);padding:11px 14px;background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:0 14px 36px rgba(15,23,42,.18);font-size:13.5px;color:var(--ink);animation:fade .18s ease;}
.confirm-bar .cb-msg{line-height:1.55;}
.confirm-bar .cb-btns{display:flex;gap:8px;flex-shrink:0;}
.confirm-bar button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:5px 13px;font-size:13px;cursor:pointer;color:var(--ink-2);white-space:nowrap;transition:.15s;}
.confirm-bar button:hover{border-color:#94a3b8;color:var(--ink);}
.confirm-bar button.ok{background:#dc2626;border-color:#dc2626;color:#fff;}
.confirm-bar button.ok:hover{background:#b91c1c;}
.confirm-bar button.alt{background:#0f172a;border-color:#0f172a;color:#fff;}
.confirm-bar button.alt:hover{background:#1e293b;}
"""
assert "/* 响应式 */" in tpl
tpl = tpl.replace("/* 响应式 */", CSS + "\n/* 响应式 */", 1)

# ---------------- 2. 侧边说明 ----------------
old_foot = """    <div class="side-foot">
      答案默认隐藏，点击「查看答案」后才显示。<br>
      标记为「已掌握」的题目会记录在本机浏览器，刷新不丢失。
    </div>"""
new_foot = """    <div class="side-foot">
      选择题：选好后点「提交答案」，系统直接判定对错并给出解析。<br>
      编程题：在编辑区写代码或上传 .cpp，点「提交判题」用 5 组数据实测比对。<br>
      <b>标注说明</b>：<span class="tag-mark tag-exam">常考</span> 高频考试题型 ·
      <span class="tag-mark tag-mistake">易错</span> 常见陷阱 ·
      <span class="tag-mark tag-hard">难题</span> 综合/嵌套类。<br>
      右上角「只看重点题」可只显示带标注的题目。<br>
      判题需先双击 start.bat 启动本地服务；直接双击 index.html 时其余功能仍可用。
    </div>"""
assert old_foot in tpl
tpl = tpl.replace(old_foot, new_foot, 1)

# ---------------- 3. 替换选择题/编程题渲染函数 ----------------
NEW_RENDER = r"""function tagMark(q){
  const t = q.tag || [];
  if (!t.length) return '';
  const cls = {'常考':'tag-exam','易错':'tag-mistake','难题':'tag-hard'};
  return t.map(x => '<span class="tag-mark ' + (cls[x] || 'tag-exam') + '">' + x + '</span>').join('');
}

const QMAP = {};
DATA.forEach(c => {
  (c.choice || []).forEach(q => QMAP[q.id] = q);
  (c.coding || []).forEach(q => QMAP[q.id] = q);
});

function choiceHTML(q, idx, chapColor){
  const L = ['A','B','C','D','E','F'];
  const st = progress[q.id] || {};
  const opts = q.options.map((o, i) =>
    '<li data-opt="' + i + '"><b>' + L[i] + '</b><span>' + o + '</span></li>'
  ).join('');
  return '<article class="card' + (st.mastered ? ' is-mastered' : '') + '" data-qid="' + q.id + '" style="--chap-color:' + chapColor + '">' +
    '<div class="card-head">' +
      '<span class="tag-no">第 ' + (idx + 1) + ' 题</span>' +
      '<span class="tag-type">选择题</span>' +
      levelTag(q.level || 1) +
      tagMark(q) +
      '<span class="qid">' + q.id + '</span>' +
    '</div>' +
    '<div class="q-body">' + q.q + '</div>' +
    (q.code ? codeBlock(q.pre ? (q.pre + '\n\nint main()\n{\n' + q.code + '\n}') : q.code, false) : '') +
    '<ul class="options">' + opts + '</ul>' +
    '<div class="actions">' +
      '<button class="primary" data-act="submit">提交答案</button>' +
      '<button data-act="retry" hidden>重做</button>' +
      '<button class="btn-master' + (st.mastered ? ' on' : '') + '" data-act="master">标记已掌握</button>' +
    '</div>' +
    '<div class="answer" hidden></div>' +
  '</article>';
}

function codingHTML(q, idx, chapColor){
  const st = progress[q.id] || {};
  const hasTests = !!(q.tests && q.tests.length);
  const samples = q.samples.map((s, i) =>
    '<div class="sample">' +
      '<div class="sample-h">输入样例 ' + (i + 1) + '</div>' +
      '<pre>' + (s.in === '' ? '（无输入）' : esc(s.in)) + '</pre>' +
      '<div class="sample-h">输出样例 ' + (i + 1) + '</div>' +
      '<pre>' + esc(s.out) + '</pre>' +
    '</div>'
  ).join('');
  return '<article class="card' + (st.mastered ? ' is-mastered' : '') + '" data-qid="' + q.id + '" style="--chap-color:' + chapColor + '">' +
    '<div class="card-head">' +
      '<span class="tag-no">第 ' + (idx + 1) + ' 题</span>' +
      '<span class="tag-type">编程题</span>' +
      levelTag(q.level || 2) +
      tagMark(q) +
      (q.tags ? q.tags.map(t => '<span class="tag-type">' + esc(t) + '</span>').join('') : '') +
      '<span class="qid">' + q.id + '</span>' +
    '</div>' +
    '<h3 class="q-title">' + esc(q.title) + '</h3>' +
    '<div class="section"><h4>问题描述</h4><p>' + q.desc + '</p></div>' +
    '<div class="section"><h4>输入形式</h4><p>' + q.input + '</p></div>' +
    '<div class="section"><h4>输出形式</h4><p>' + q.output + '</p></div>' +
    '<div class="samples">' + samples + '</div>' +
    '<div class="editor">' +
      '<div class="editor-bar">' +
        '<span class="eb-title">代码编辑区 · C++</span>' +
        '<div class="eb-btns">' +
          '<label class="file-btn">上传 .cpp<input type="file" accept=".cpp,.cc,.cxx,.c,.txt" hidden data-act="upload"></label>' +
          '<button data-act="clear">清空</button>' +
        '</div>' +
      '</div>' +
      '<textarea class="code-input" spellcheck="false" placeholder="// 在这里写你的 C++ 代码，或点右上角「上传 .cpp」载入本地文件"></textarea>' +
    '</div>' +
    '<div class="actions">' +
      '<button class="primary" data-act="judge"' + (hasTests ? '' : ' disabled') + '>提交判题</button>' +
      (hasTests ? '' : '<span class="tag-type">本题暂无判题数据</span>') +
      '<button data-act="hint">查看思路提示</button>' +
      '<button data-act="answer">查看参考代码</button>' +
      '<button class="btn-master' + (st.mastered ? ' on' : '') + '" data-act="master">标记已掌握</button>' +
    '</div>' +
    '<div class="judge" hidden></div>' +
    '<div class="hint" hidden><h5>思路提示</h5><p>' + q.hint + '</p></div>' +
    '<div class="answer" hidden><h5>参考代码（C 语言）</h5>' + codeBlock(q.code, true) + '</div>' +
  '</article>';
}

"""
start = tpl.index("function choiceHTML(")
end = tpl.index("function renderContent(){")
tpl = tpl[:start] + NEW_RENDER + tpl[end:]

# ---------------- 4. 替换 bindCards ----------------
NEW_BIND = r"""const JUDGE_URL = (location.protocol === 'file:') ? 'http://127.0.0.1:8765/api/judge' : '/api/judge';

/* ---- 页内确认条：替代原生 confirm，避免被浏览器拦截导致点了没反应 ---- */
let confirmBar = null;
function closeConfirm(){
  if (confirmBar){ confirmBar.remove(); confirmBar = null; }
}
function showConfirm(msg, actions){
  closeConfirm();
  const wrap = document.createElement('div');
  wrap.className = 'confirm-bar';
  const m = document.createElement('span'); m.className = 'cb-msg'; m.textContent = msg;
  const bw = document.createElement('span'); bw.className = 'cb-btns';
  (actions || [{text:'确定', cls:'ok'}, {text:'取消'}]).forEach(a => {
    const b = document.createElement('button');
    b.textContent = a.text;
    if (a.cls) b.className = a.cls;
    b.addEventListener('click', () => { closeConfirm(); if (a.fn) a.fn(); });
    bw.appendChild(b);
  });
  wrap.appendChild(m); wrap.appendChild(bw);
  document.body.appendChild(wrap);
  confirmBar = wrap;
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeConfirm(); });
const CODE_KEY = 'cpp_code_v1';
let codeStore = {};
try { codeStore = JSON.parse(localStorage.getItem(CODE_KEY) || '{}') || {}; } catch(e){ codeStore = {}; }
function saveCode(qid, text){
  codeStore[qid] = text;
  try { localStorage.setItem(CODE_KEY, JSON.stringify(codeStore)); } catch(e){}
}

function renderChoiceAnswer(card, q, picked, expand){
  const L = ['A','B','C','D','E','F'];
  const ok = picked === q.answer;
  card.querySelectorAll('ul.options li').forEach((li, i) => {
    li.classList.remove('picked');
    li.classList.add('locked');
    li.classList.toggle('right', i === q.answer);
    li.classList.toggle('wrong', i === picked && i !== q.answer);
  });
  const box = card.querySelector('.answer');
  box.innerHTML =
    '<h5 class="' + (ok ? 'ok' : 'no') + '">' + (ok ? '回答正确' : '回答错误') + '</h5>' +
    '<div class="ans-line">你的选择：' + L[picked] + '　正确答案：<b>' + L[q.answer] + '</b></div>' +
    '<div class="explain">' + q.explain + '</div>';
  if (expand) box.hidden = false;
}

function syncJudgeToggle(box){
  const tg = box.querySelector('[data-act="judge-toggle"]');
  if (tg) tg.textContent = box.classList.contains('folded') ? '展开明细' : '收起明细';
}
function toggleJudge(box){
  box.classList.toggle('folded');
  syncJudgeToggle(box);
}
function bindJudgeOps(box){
  const tg = box.querySelector('[data-act="judge-toggle"]');
  if (tg) tg.addEventListener('click', ev => { ev.stopPropagation(); toggleJudge(box); });
  const cl = box.querySelector('[data-act="judge-close"]');
  if (cl) cl.addEventListener('click', ev => { ev.stopPropagation(); box.hidden = true; box.innerHTML = ''; box.classList.remove('folded'); });
  const hd = box.querySelector('.judge-head');
  if (hd) hd.addEventListener('click', () => toggleJudge(box));
  syncJudgeToggle(box);
}

function renderJudge(box, res){
  box.hidden = false;
  box.classList.remove('folded');
  if (!res){
    box.innerHTML = '<div class="judge-err"><b>无法连接本地判题服务</b>' +
      '<div style="font-weight:400;margin-top:4px;">请双击与 index.html 同目录的 start.bat 启动服务窗口，然后刷新本页再提交。若只是练习、不需要自动判题，可继续直接使用本页面。</div></div>';
    return;
  }
  if (!res.compile || !res.compile.ok){
    box.innerHTML = '<div class="judge-err"><b>编译未通过</b><pre class="err-pre">' + esc((res.compile && res.compile.msg) || '未知错误') + '</pre></div>';
    return;
  }
  const rs = res.results || [];
  const pass = rs.filter(r => r.ok).length;
  const allOk = rs.length > 0 && pass === rs.length;
  const label = {AC:'通过', WA:'答案不符', RE:'运行错误', TLE:'超时'};
  let html = '<div class="judge-head"><span class="' + (allOk ? 'judge-ok' : 'judge-no') + '">' +
    (allOk ? '全部用例通过' : '存在未通过用例') + '</span><span class="score">' + pass + ' / ' + rs.length + '</span>' +
    '<span class="judge-ops"><button data-act="judge-toggle">收起明细</button><button data-act="judge-close">关闭</button></span></div>';
  html += '<div class="judge-detail">';
  rs.forEach(r => {
    html += '<div class="case"><div class="case-h"><span class="idx">用例 ' + r.no + '</span>' +
      '<span class="badge ' + String(r.status || 'wa').toLowerCase() + '">' + (label[r.status] || r.status) + '</span></div>' +
      '<div class="case-body">' +
        '<div class="case-label">输入</div><pre>' + (r.input ? esc(r.input) : '（无输入）') + '</pre>' +
        '<div class="case-label">期望输出</div><pre>' + esc(r.expected) + '</pre>' +
        '<div class="case-label">你的输出</div><pre>' + (r.output ? esc(r.output) : '（无输出）') + '</pre>' +
        (r.msg ? '<div class="case-label">错误信息</div><pre>' + esc(r.msg) + '</pre>' : '') +
      '</div></div>';
  });
  html += '<div class="judge-tip">判题方式：每组数据都实际运行你的程序再比对输出，忽略行末空格与末尾空行。点结果标题栏可收起或展开明细。</div>';
  html += '</div>';
  box.innerHTML = html;
  if (allOk) box.classList.add('folded');
  bindJudgeOps(box);
  syncJudgeToggle(box);
}

async function submitJudge(card, q, btn){
  const ta = card.querySelector('.code-input');
  const box = card.querySelector('.judge');
  const code = (ta.value || '').trim();
  if (!code){ toast('请先在代码编辑区写入代码，或上传 .cpp 文件'); return; }
  if (!q.tests || !q.tests.length){ toast('本题暂无判题数据'); return; }
  const old = btn.textContent;
  btn.disabled = true; btn.textContent = '判题中…';
  try {
    const resp = await fetch(JUDGE_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({code: code, tests: q.tests})
    });
    const res = await resp.json();
    renderJudge(box, res);
    if (res.compile && res.compile.ok){
      const pass = (res.results || []).filter(r => r.ok).length;
      if (pass === q.tests.length){
        if (!progress[q.id]) progress[q.id] = {};
        progress[q.id].ac = true; progress[q.id].seen = true;
        saveProgress(); updateProgress();
        toast('全部 ' + q.tests.length + ' 组用例通过');
      } else {
        toast('通过 ' + pass + ' / ' + q.tests.length + ' 组用例');
      }
    } else {
      toast('编译未通过，见下方错误信息');
    }
  } catch(e){
    renderJudge(box, null);
  } finally {
    btn.disabled = false; btn.textContent = old;
  }
}

function bindCards(root){
  root.querySelectorAll('.card').forEach(card => {
    const qid = card.dataset.qid;
    const q = QMAP[qid] || {};
    const answerBox = card.querySelector('.answer');
    const hintBox = card.querySelector('.hint');
    const btnAns = card.querySelector('[data-act="answer"]');
    const btnHint = card.querySelector('[data-act="hint"]');
    const btnMaster = card.querySelector('[data-act="master"]');

    /* ---- 选择题：提交判定 ---- */
    if (q.options && q.answer !== undefined){
      const opts = card.querySelectorAll('ul.options li');
      const btnSubmit = card.querySelector('[data-act="submit"]');
      const btnRetry = card.querySelector('[data-act="retry"]');
      const st = progress[qid] || {};
      const submitted = (st.picked !== undefined && st.picked !== null);
      if (submitted) renderChoiceAnswer(card, q, st.picked, false);
      if (btnSubmit){
        if (submitted){ btnSubmit.textContent = '已提交'; btnSubmit.disabled = true; }
        if (btnRetry && submitted) btnRetry.hidden = false;
        btnSubmit.addEventListener('click', () => {
          const cur = progress[qid] || {};
          if (cur.picked !== undefined && cur.picked !== null){ toast('本题已提交，点「重做」可重新作答'); return; }
          const sel = card.querySelector('ul.options li.picked');
          if (!sel){ toast('请先选择一个选项'); return; }
          const picked = parseInt(sel.dataset.opt, 10);
          if (!progress[qid]) progress[qid] = {};
          progress[qid].picked = picked;
          progress[qid].correct = (picked === q.answer);
          progress[qid].seen = true;
          saveProgress(); updateProgress();
          renderChoiceAnswer(card, q, picked, true);
          btnSubmit.textContent = '已提交'; btnSubmit.disabled = true;
          if (btnRetry) btnRetry.hidden = false;
          toast(picked === q.answer ? '回答正确' : '回答错误，看看解析');
        });
      }
      if (btnRetry){
        btnRetry.addEventListener('click', () => {
          if (progress[qid]){ delete progress[qid].picked; delete progress[qid].correct; }
          saveProgress(); updateProgress();
          card.querySelectorAll('ul.options li').forEach(li => li.classList.remove('picked','right','wrong','locked'));
          const box = card.querySelector('.answer');
          if (box){ box.hidden = true; box.innerHTML = ''; }
          if (btnSubmit){ btnSubmit.textContent = '提交答案'; btnSubmit.disabled = false; }
          btnRetry.hidden = true;
        });
      }
      opts.forEach(li => {
        li.addEventListener('click', () => {
          const cur = progress[qid] || {};
          if (cur.picked !== undefined && cur.picked !== null){ toast('本题已提交，点「重做」可重新作答'); return; }
          opts.forEach(x => x.classList.remove('picked'));
          li.classList.add('picked');
        });
      });
    }

    /* ---- 编程题：编辑器 / 上传 / 判题 ---- */
    const ta = card.querySelector('.code-input');
    if (ta){
      if (codeStore[qid]) ta.value = codeStore[qid];
      ta.addEventListener('input', () => saveCode(qid, ta.value));
      ta.addEventListener('keydown', e => {
        if (e.key === 'Tab'){
          e.preventDefault();
          const s = ta.selectionStart, en = ta.selectionEnd;
          ta.value = ta.value.slice(0, s) + '    ' + ta.value.slice(en);
          ta.selectionStart = ta.selectionEnd = s + 4;
          saveCode(qid, ta.value);
        }
      });
      const clearBtn = card.querySelector('[data-act="clear"]');
      if (clearBtn) clearBtn.addEventListener('click', () => {
        const doClear = () => { ta.value = ''; saveCode(qid, ''); toast('已清空本题代码'); };
        if (!ta.value.trim()){ doClear(); return; }
        showConfirm('确定清空本题已写的代码吗？清空后不可恢复。', [
          { text: '确定清空', cls: 'ok', fn: doClear },
          { text: '取消' }
        ]);
      });
      const up = card.querySelector('[data-act="upload"]');
      if (up) up.addEventListener('change', async e => {
        const f = e.target.files && e.target.files[0];
        if (!f) return;
        const buf = await f.arrayBuffer();
        let text = '';
        try { text = new TextDecoder('utf-8', {fatal:true}).decode(buf); }
        catch(err1){
          try { text = new TextDecoder('gbk').decode(buf); }
          catch(err2){ text = new TextDecoder('utf-8').decode(buf); }
        }
        e.target.value = '';
        const apply = () => { ta.value = text; saveCode(qid, text); toast('已载入 ' + f.name); };
        if (ta.value.trim()){
          showConfirm('编辑区已有代码，是否用「' + f.name + '」覆盖？', [
            { text: '覆盖', cls: 'alt', fn: apply },
            { text: '取消' }
          ]);
        } else apply();
      });
      const judgeBtn = card.querySelector('[data-act="judge"]');
      if (judgeBtn) judgeBtn.addEventListener('click', () => submitJudge(card, q, judgeBtn));
    }

    /* ---- 公共：答案折叠 / 已掌握 ---- */
    if (btnAns){
      if (progress[qid] && progress[qid].seen){
        btnAns.textContent = hintBox ? '收起参考代码' : '收起答案';
        btnAns.classList.remove('primary');
      }
      btnAns.addEventListener('click', () => {
        const open = !answerBox.hidden;
        answerBox.hidden = open;
        btnAns.textContent = open ? (btnHint ? '查看参考代码' : '查看答案') : (btnHint ? '收起参考代码' : '收起答案');
        btnAns.classList.toggle('primary', open);
        if (!open) markSeen(qid);
      });
    }
    if (btnHint){
      btnHint.addEventListener('click', () => {
        const open = !hintBox.hidden;
        hintBox.hidden = open;
        btnHint.textContent = open ? '查看思路提示' : '收起思路提示';
      });
    }
    if (btnMaster){
      btnMaster.addEventListener('click', () => {
        if (!progress[qid]) progress[qid] = {};
        const now = !progress[qid].mastered;
        progress[qid].mastered = now;
        if (now) progress[qid].seen = true;
        saveProgress();
        updateProgress();
        btnMaster.classList.toggle('on', now);
        card.classList.toggle('is-mastered', now);
        if (!now) markSeenToBtn(card);
        toast(now ? '已标记为已掌握' : '已取消标记');
      });
    }

    /* ---- 代码复制 ---- */
    const copyBtn = card.querySelector('.copy-btn');
    if (copyBtn){
      copyBtn.addEventListener('click', () => {
        const pre = copyBtn.parentElement;
        const text = pre.innerText.replace(/^复制代码\s*/, '');
        copyText(text);
      });
    }
  });
}

"""
bs = tpl.index("function bindCards(root){")
be = tpl.index("function markSeenToBtn(card){")
tpl = tpl[:bs] + NEW_BIND + tpl[be:]

# ---------------- 5. 全部展开：跳过空的答案区 ----------------
old_expand = "  document.querySelectorAll('#content .answer, #content .hint').forEach(el => el.hidden = false);"
new_expand = "  document.querySelectorAll('#content .answer, #content .hint').forEach(el => { if (el.innerHTML.trim()) el.hidden = false; });"
assert old_expand in tpl
tpl = tpl.replace(old_expand, new_expand, 1)

# ---------------- 6. 注入数据 ----------------
dd = os.path.join(BASE, "temp", "data3")
files = sorted(f for f in os.listdir(dd) if f.startswith("ch") and f.endswith(".json"))
SHORT = {"1": "概述", "2": "数据类型", "3": "顺序结构", "4": "选择结构", "5": "循环结构",
         "6": "函数", "7": "数组", "8": "指针", "9": "结构体", "10": "文件"}
chaps = []
for f in files:
    c = json.load(open(os.path.join(dd, f), encoding="utf-8"))
    cid = c["id"]
    c["short"] = SHORT.get(cid, c["name"])
    c["name"] = "第 %s 章 %s" % (cid, c["name"])
    chaps.append(c)
chaps.sort(key=lambda x: int(x["id"]))
data_str = json.dumps(chaps, ensure_ascii=False, indent=1).replace("</", "<\\/")
assert "/*__DATA__*/[]" in tpl
tpl = tpl.replace("/*__DATA__*/[]", data_str, 1)

out = os.path.join(BASE, "output", "index.html")
open(out, "w", encoding="utf-8").write(tpl)
print("written", out, len(tpl), "chars")

# 语法检查
m = re.search(r"<script>([\s\S]*)</script>", tpl)
js = m.group(1)
tmpjs = os.path.join(BASE, "temp", "check2.js")
open(tmpjs, "w", encoding="utf-8").write(js)
import subprocess
r = subprocess.run(["node", "--check", tmpjs], capture_output=True, text=True)
print("node check rc=", r.returncode)
print(r.stderr[:1200])

# -*- coding: utf-8 -*-
"""第1-5章追加 易错/难题/常考 型选择题（带 code 的逐题用 gcc 实跑校验输出）"""
import json, os, re, subprocess, tempfile

BASE = r"C:\Users\26051\AppData\Roaming\Tencent\Marvis\User\oAN1i2ZjKve3rkORzl0fXM-Pu35M\workspace\conv_93ef20205c5f43f0a45dd0245bb0cb63"
DATA = os.path.join(BASE, "temp", "data3")
TMP = os.path.join(BASE, "temp", "verify")
os.makedirs(TMP, exist_ok=True)
GCC = r"C:\msys2\ucrt64\bin\gcc.exe"

QUIZ = {}

# ---------------- 第1章 概述 ----------------
QUIZ["ch01"] = [
 dict(level="mid", tag=["常考"],
  q="下列关于 C 程序执行过程的说法，正确的是：",
  code=None, options=[
   "程序总是从源文件中的第一个函数开始执行",
   "程序总是从 main 函数开始执行，main 可以放在源文件的任意位置",
   "main 函数必须写在所有其它函数之前，否则不能调用",
   "一个 C 程序里允许出现多个 main 函数"], answer=1,
  explain="C 程序总是从 main 开始执行，与 main 在源文件中的书写位置无关；一个程序有且仅有一个 main。"),

 dict(level="hard", tag=["易错"],
  q="关于 C 语言注释，下列说法正确的是：",
  code=None, options=[
   "/* ... */ 注释可以嵌套使用，内层注释同样生效",
   "/* ... */ 注释不能嵌套；注释不是语句，在编译前就被替换为一个空格",
   "注释会在运行时被当作语句执行，只是不产生输出",
   "// 单行注释必须顶格书写才有效"], answer=1,
  explain="注释不能嵌套：外层 /* 遇到第一个 */ 就结束，后面的 */ 会引发语法错误。注释在编译预处理阶段被替换为空格，不参与编译。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int add(int a, int b)
{
    return a + b;
}
int main()
{
    printf("%d", add(2, 3) * 2);
    return 0;
}""",
  options=["10", "7", "5", "编译错误"], answer=0, expect="10",
  explain="函数调用 add(2,3) 得到 5，再乘 2 得 10。函数的定义位置不影响调用（本例函数定义在调用之前，无需额外声明）。"),
]

# ---------------- 第2章 基本数据类型 ----------------
QUIZ["ch02"] = [
 dict(level="hard", tag=["易错", "常考"],
  q="int 为 32 位、short 为 16 位时，下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    short a = 32767;
    a = a + 1;
    printf("%d", a);
    return 0;
}""",
  options=["32768", "-32768", "0", "32767"], answer=1, expect="-32768",
  explain="short 占 16 位，最大值为 32767。加 1 后按补码回绕变成 -32768，这就是整型溢出，不会报错也不会变成更大正数。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a = 3, b = 2;
    printf("%d,%.2f", a / b, (double)a / b);
    return 0;
}""",
  options=["1,1.50", "1.5,1.50", "1,1.00", "1.5,1.5"], answer=0, expect="1,1.50",
  explain="两个 int 相除只做整数除法，小数被截断得 1；强制类型转换后有一个 double 参与运算，才按浮点除法得 1.50。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    char c = 'a';
    printf("%c,%d,%c", c, c, c - 32);
    return 0;
}""",
  options=["a,97,A", "a,a,97", "97,97,65", "A,65,A"], answer=0, expect="a,97,A",
  explain="字符按 ASCII 码存储，%c 输出字符本身、%d 输出其编码值；同一个变量用不同格式符输出会得到不同结果。'a'=97，减 32 得 65 即 'A'。"),

 dict(level="hard", tag=["易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    printf("%d,%d,%d,%d", -7 / 2, -7 % 2, 7 / -2, 7 % -2);
    return 0;
}""",
  options=["-3,-1,-3,1", "-4,-1,-4,1", "-3,-1,3,1", "-3,1,-3,-1"], answer=0, expect="-3,-1,-3,1",
  explain="C 的整数除法向零取整，-7/2 得 -3（不是 -4）；取余结果符号与被除数相同：-7%2=-1，7%-2=1。"),

 dict(level="hard", tag=["难题", "易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    double x = 0.1, y = 0.2;
    printf("%d", (x + y) == 0.3);
    return 0;
}""",
  options=["1", "0", "0.3", "编译错误"], answer=1, expect="0",
  explain="0.1 和 0.2 无法用二进制浮点精确表示，相加后与 0.3 存在极小误差，因此相等比较为假。浮点数判断相等要用 fabs(x-y)<1e-6 这类方式。"),
]

# ---------------- 第3章 顺序结构 ----------------
QUIZ["ch03"] = [
 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    printf("[%5d][%05d]", 42, 42);
    return 0;
}""",
  options=["[   42][00042]", "[42   ][42   ]", "[%5d][%05d]", "[42][42]"], answer=0, expect="[   42][00042]",
  explain="%5d 是宽度 5 的右对齐输出，左边补空格；%05d 中 0 表示左补零。宽度修饰只改变显示形式，不改变数值。"),

 dict(level="mid", tag=["易错", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int x = 5;
    printf("%.2f", x / 2.0);
    return 0;
}""",
  options=["2.50", "2.00", "2", "2.5%"], answer=0, expect="2.50",
  explain="x/2.0 中 2.0 是 double，x 自动转换为 double，得 2.5；%.2f 保留两位小数输出 2.50。若写成 x/2 则整数除法得 2，再按 %f 输出是错误用法。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    printf("%d,%d,%d", '\\n', 'A', '0');
    return 0;
}""",
  options=["10,65,48", "92,65,0", "10,97,48", "换行,65,48"], answer=0, expect="10,65,48",
  explain="'\\n' 是转义字符，编码为 10；'A' 为 65；字符 '0' 的编码是 48，与数字 0 完全不同。"),

 dict(level="hard", tag=["易错", "难题"],
  q="从键盘输入 7 8 后回车，下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a, b;
    int n = scanf("%d%d", &a, &b);
    printf("%d,%d,%d", n, a, b);
    return 0;
}""",
  stdin="7 8\n",
  options=["2,7,8", "1,7,8", "0,0,0", "2,8,7"], answer=0, expect="2,7,8",
  explain="scanf 的返回值是成功读入的数据个数，本例读入两个整数故返回 2；两个 %d 之间无需在格式串里写空格，输入时用空格或回车分隔即可。"),
]

# ---------------- 第4章 选择结构 ----------------
QUIZ["ch04"] = [
 dict(level="hard", tag=["易错", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a = 0, b = 1, x = 0;
    if (a > 0)
        if (b > 0) x = 1;
        else       x = 2;
    printf("%d", x);
    return 0;
}""",
  options=["0", "1", "2", "编译错误"], answer=0, expect="0",
  explain="else 与最近的未配对 if 结合，else 属于内层 if。外层条件 a>0 为假，整个 if 语句被跳过，x 仍为 0。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int n = 2;
    switch (n)
    {
        case 1: printf("A");
        case 2: printf("B");
        case 3: printf("C"); break;
        default: printf("D");
    }
    return 0;
}""",
  options=["B", "BC", "ABC", "BCD"], answer=1, expect="BC",
  explain="case 只是入口标签，没有 break 就会继续往下执行（fall through）。本题从 case 2 进入，依次输出 B、C，遇 break 才跳出。"),

 dict(level="hard", tag=["易错", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i = 0;
    if (i++ && i++) { }
    printf("%d", i);
    return 0;
}""",
  options=["0", "1", "2", "3"], answer=1, expect="1",
  explain="&& 具有短路特性：左边 i++ 先用 0 参与判断，判断为假后右边的 i++ 根本不会执行。因此 i 只自增一次，结果为 1。"),

 dict(level="hard", tag=["难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a = 1, b = 3, c = 2;
    printf("%d", a > b ? a : b > c ? b : c);
    return 0;
}""",
  options=["1", "2", "3", "0"], answer=2, expect="3",
  explain="条件运算符右结合，等价于 a>b ? a : (b>c ? b : c)。a>b 为假，取后者；b>c 为真取 b，即 3。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int x = 1, y = 0;
    switch (x)
    {
        case 0: y++;
        case 1: y += 2; break;
        case 2: y += 3;
    }
    printf("%d", y);
    return 0;
}""",
  options=["0", "2", "3", "5"], answer=1, expect="2",
  explain="x=1 从 case 1 进入，执行 y+=2 后遇 break 跳出，y=2。case 0 的分支不会被执行，因为它只是一个入口标签。"),
]

# ---------------- 第5章 循环结构（重点：嵌套） ----------------
QUIZ["ch05"] = [
 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i, j, s = 0;
    for (i = 1; i <= 3; i++)
        for (j = 1; j <= i; j++)
            s += j;
    printf("%d", s);
    return 0;
}""",
  options=["6", "10", "12", "9"], answer=1, expect="10",
  explain="外层 i 取 1、2、3，内层分别累加 1、(1+2)、(1+2+3)，总和 1+3+6=10。嵌套循环要先看外层每一轮内层执行多少次。"),

 dict(level="hard", tag=["常考", "易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i, j, c = 0;
    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 3; j++)
        {
            if (j == 2) break;
            c++;
        }
    }
    printf("%d", c);
    return 0;
}""",
  options=["1", "3", "6", "9"], answer=1, expect="3",
  explain="break 只能跳出它所在的那一层循环。内层每轮在 j==2 时跳出，每轮只累加 1 次；外层执行 3 轮，故 c=3。"),

 dict(level="hard", tag=["易错", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i, j, c = 0;
    for (i = 1; i <= 3; i++)
    {
        for (j = 1; j <= 3; j++)
        {
            if (j == 2) continue;
            c++;
        }
    }
    printf("%d", c);
    return 0;
}""",
  options=["3", "6", "9", "12"], answer=1, expect="6",
  explain="continue 只结束内层本次循环，不影响外层。内层每轮跳过 j==2 一次，累加 2 次；外层 3 轮，共 6 次。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i = 5, s = 0;
    do
    {
        s += i;
        i++;
    } while (i < 3);
    printf("%d,%d", s, i);
    return 0;
}""",
  options=["0,5", "5,6", "5,5", "15,6"], answer=1, expect="5,6",
  explain="do-while 先执行循环体再判断条件，至少执行一次。s 加 5 得 5，i 变 6，条件 6<3 为假，循环结束。"),

 dict(level="hard", tag=["常考", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i, j;
    for (i = 0, j = 10; i < j; i++, j--)
        ;
    printf("%d,%d", i, j);
    return 0;
}""",
  options=["4,6", "5,5", "6,4", "0,10"], answer=1, expect="5,5",
  explain="for 的表达式中可用逗号同时更新两个变量。i 从 0 增、j 从 10 减，各走 5 次后 i=j=5，条件不成立结束。注意循环体是空语句 ;。"),

 dict(level="hard", tag=["常考", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int n, k, cnt = 0;
    for (n = 2; n <= 100; n++)
    {
        int flag = 1;
        for (k = 2; k * k <= n; k++)
        {
            if (n % k == 0) { flag = 0; break; }
        }
        if (flag) cnt++;
    }
    printf("%d", cnt);
    return 0;
}""",
  options=["24", "25", "26", "50"], answer=1, expect="25",
  explain="100 以内（含 2 和 100）素数共 25 个。内层用 k*k<=n 判断到平方根即可，找到因子就 break 并置 flag=0。"),

 dict(level="hard", tag=["难题", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int n, cnt = 0;
    for (n = 100; n <= 999; n++)
    {
        int a = n / 100, b = n / 10 % 10, c = n % 10;
        if (a * a * a + b * b * b + c * c * c == n) cnt++;
    }
    printf("%d", cnt);
    return 0;
}""",
  options=["3", "4", "5", "6"], answer=1, expect="4",
  explain="水仙花数只有 153、370、371、407 四个。注意各位数字的取法：百位 n/100、十位 n/10%10、个位 n%10。"),

 dict(level="hard", tag=["常考", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int i, j, c = 0;
    for (i = 0; i < 5; i++)
        for (j = i; j < 5; j++)
            c++;
    printf("%d", c);
    return 0;
}""",
  options=["10", "15", "20", "25"], answer=1, expect="15",
  explain="内层起点随外层变化：i=0 时 5 次、i=1 时 4 次……共 5+4+3+2+1=15 次。这是内层初值依赖外层变量的典型嵌套。"),

 dict(level="hard", tag=["易错", "常考"],
  q="下面这段循环存在的问题是：",
  code="""#include <stdio.h>
int main()
{
    int i = 1;
    while (i <= 10)
    {
        printf("%d ", i);
    }
    return 0;
}""",
  options=[
   "输出 1 到 10，结果正确",
   "循环变量 i 从未改变，条件恒成立，形成死循环",
   "while 条件写成 i<=10 应为 i<10，否则出错",
   "printf 在循环体内，编译会报错"], answer=1,
  explain="while 循环必须在循环体内修改循环变量，本题漏写 i++，i 恒为 1，条件永远为真，程序陷入死循环。for 循环把初值、条件、更新写在一起，就是为了避免这种遗漏。"),
]


def norm(s):
    lines = [x.rstrip() for x in (s or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def verify(item, key):
    code = item.get("code")
    if not code:
        return True, ""
    src = os.path.join(TMP, key + ".c")
    exe = os.path.join(TMP, key + ".exe")
    open(src, "w", encoding="utf-8").write(code)
    r = subprocess.run([GCC, "-std=c11", "-O0", "-o", exe, src], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return False, "compile: " + (r.stderr or "")[:400]
    try:
        run = subprocess.run([exe], capture_output=True, text=True, encoding="utf-8", errors="replace",
                             input=item.get("stdin", ""), timeout=10)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    got = norm(run.stdout)
    if got != norm(item["expect"]):
        return False, "stdout=%r expect=%r" % (got, item["expect"])
    return True, ""


total = 0
for chap, items in QUIZ.items():
    path = os.path.join(DATA, chap + ".json")
    d = json.load(open(path, encoding="utf-8"))
    used = [q["id"] for q in d["choice"]]
    nums = [int(m.group(1)) for x in used for m in [re.search(r"-c(\d+)$", x)] if m]
    nxt = max(nums) + 1 if nums else 1
    added = 0
    for k, it in enumerate(items):
        key = "%s_h%d" % (chap, k)
        ok, msg = verify(it, key)
        if not ok:
            print("FAIL", chap, it["q"][:24], msg)
            continue
        if norm(it["options"][it["answer"]]) != norm(it.get("expect") or it["options"][it["answer"]]):
            print("ANSWER-MISMATCH", chap, it["q"][:24])
            continue
        item = dict(it)
        item.pop("stdin", None)
        item["id"] = "%s-c%d" % (chap.replace("ch", ""), nxt)
        item.setdefault("code", None)
        d["choice"].append(item)
        nxt += 1
        added += 1
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(chap, "added", added, "total choice", len(d["choice"]))
    total += added
print("ALL ADDED", total)

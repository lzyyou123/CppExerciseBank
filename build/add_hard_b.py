# -*- coding: utf-8 -*-
"""第6-10章追加 易错/难题/常考 型选择题（带 code 的逐题用 gcc 实跑校验输出）"""
import json, os, re, subprocess

BASE = r"C:\Users\26051\AppData\Roaming\Tencent\Marvis\User\oAN1i2ZjKve3rkORzl0fXM-Pu35M\workspace\conv_93ef20205c5f43f0a45dd0245bb0cb63"
DATA = os.path.join(BASE, "temp", "data3")
TMP = os.path.join(BASE, "temp", "verify")
os.makedirs(TMP, exist_ok=True)
GCC = r"C:\msys2\ucrt64\bin\gcc.exe"

QUIZ = {}

# ---------------- 第6章 函数 ----------------
QUIZ["ch06"] = [
 dict(level="hard", tag=["常考", "易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
void swap(int a, int b)
{
    int t = a;
    a = b;
    b = t;
}
int main()
{
    int x = 1, y = 2;
    swap(x, y);
    printf("%d,%d", x, y);
    return 0;
}""",
  options=["1,2", "2,1", "2,2", "编译错误"], answer=0, expect="1,2",
  explain="C 函数参数是单向值传递，形参 a、b 只是实参的副本，函数内交换副本不影响 main 里的 x、y。要交换实参必须传地址（指针）。"),

 dict(level="hard", tag=["难题", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int f(void)
{
    static int x = 0;
    return ++x;
}
int main()
{
    int i, s = 0;
    for (i = 0; i < 3; i++)
        s += f();
    printf("%d,%d", s, f());
    return 0;
}""",
  options=["3,1", "6,4", "6,1", "3,4"], answer=1, expect="6,4",
  explain="static 局部变量只初始化一次，且函数调用结束后值仍保留。前三次调用返回 1、2、3，s=6；第四次返回 4，因此输出 6,4。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int fact(int n)
{
    if (n <= 1) return 1;
    return n * fact(n - 1);
}
int main()
{
    printf("%d", fact(5));
    return 0;
}""",
  options=["5", "24", "120", "死循环"], answer=2, expect="120",
  explain="递归求阶乘：5*4*3*2*1=120。递归必须有使递归终止的条件（n<=1 时返回 1），否则会无限递归导致栈溢出。"),

 dict(level="mid", tag=["易错", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int x = 10;
void show(void)
{
    printf("%d", x);
}
int main()
{
    int x = 20;
    printf("%d,", x);
    show();
    return 0;
}""",
  options=["20,20", "10,10", "20,10", "10,20"], answer=2, expect="20,10",
  explain="局部变量在其作用域内屏蔽同名的全局变量，所以 main 里输出 20；show 函数内没有局部 x，访问的是全局 x，输出 10。"),

 dict(level="hard", tag=["难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int fib(int n)
{
    if (n <= 1) return 1;
    return fib(n - 1) + fib(n - 2);
}
int main()
{
    printf("%d", fib(5));
    return 0;
}""",
  options=["5", "8", "13", "16"], answer=1, expect="8",
  explain="注意终止条件是 n<=1 返回 1（不是 0）。数列为 1,1,2,3,5,8，fib(5)=8。递归题要顺着终止条件一层层算，不能凭斐波那契的通常初值套用。"),
]

# ---------------- 第7章 数组 ----------------
QUIZ["ch07"] = [
 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[2][3] = {{1, 2}, {3}};
    printf("%d,%d", a[1][2], a[0][1]);
    return 0;
}""",
  options=["0,2", "3,2", "0,0", "随机值,2"], answer=0, expect="0,2",
  explain="二维数组部分初始化时，未显式赋值的元素自动为 0。a[1][2] 未赋值得 0，a[0][1] 赋值 2。"),

 dict(level="hard", tag=["易错", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
#include <string.h>
int main()
{
    char s[] = "a\\0b";
    printf("%d,%d", (int)strlen(s), (int)sizeof(s));
    return 0;
}""",
  options=["1,4", "3,4", "1,3", "3,3"], answer=0, expect="1,4",
  explain="strlen 从首地址数到第一个 '\\0' 为止，故为 1；sizeof 求数组占用的字节数，含字符串结束符 '\\0'，共 4 字节。string.h 中的字符串处理函数遇到 '\\0' 就认为字符串结束。"),

 dict(level="hard", tag=["难题", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[5] = {5, 4, 3, 2, 1};
    int i, j, t, cnt = 0;
    for (i = 0; i < 4; i++)
        for (j = 0; j < 4 - i; j++)
            if (a[j] > a[j + 1])
            {
                t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
                cnt++;
            }
    printf("%d,%d", a[0], cnt);
    return 0;
}""",
  options=["1,10", "1,4", "5,10", "1,15"], answer=0, expect="1,10",
  explain="冒泡排序把逆序数组排成升序，首元素为 1；逆序对共 4+3+2+1=10 个，故交换 10 次。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[5] = {1, 2, 3, 4, 5};
    int n = sizeof(a) / sizeof(a[0]);
    printf("%d", n);
    return 0;
}""",
  options=["4", "5", "20", "1"], answer=1, expect="5",
  explain="sizeof(a) 是整个数组的字节数 20，sizeof(a[0]) 是单个元素 4 字节，相除得元素个数 5。这是求数组长度最常用的写法。"),

 dict(level="hard", tag=["难题", "易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
#include <string.h>
int main()
{
    char s1[10] = "abc", s2[10] = "abd";
    printf("%d", strcmp(s1, s2) < 0);
    return 0;
}""",
  options=["1", "0", "-1", "3"], answer=0, expect="1",
  explain="strcmp 逐字符比较 ASCII 码，第三位 'c'(99) < 'd'(100)，返回负值，表达式成立输出 1。注意 strcmp 不能直接用 == 判断字符串相等。"),
]

# ---------------- 第8章 指针 ----------------
QUIZ["ch08"] = [
 dict(level="hard", tag=["常考", "易错"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[3] = {1, 2, 3};
    int *p = a;
    int x = *p++;
    printf("%d %d", x, *p);
    return 0;
}""",
  options=["1 2", "2 2", "1 1", "编译错误"], answer=0, expect="1 2",
  explain="++ 与 * 同级？不是：后缀 ++ 优先级高于 *，故 *p++ 等价于 *(p++)——先把 p 当前指向的值 1 取出赋给 x，然后 p 自增指向 a[1]，所以再输出 *p 得 2。若写成 (*p)++ 则是把 1 自增为 2，含义完全不同。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a, *q = a + 3;
    printf("%d,%d", (int)(q - p), *(p + 2));
    return 0;
}""",
  options=["3,30", "12,30", "3,20", "4,40"], answer=0, expect="3,30",
  explain="指向同一数组的两个指针相减，结果是它们之间相隔的元素个数，不是字节数，所以 q-p=3；*(p+2) 等价于 a[2]，值为 30。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
void swap(int *p, int *q)
{
    int t = *p;
    *p = *q;
    *q = t;
}
int main()
{
    int x = 1, y = 2;
    swap(&x, &y);
    printf("%d,%d", x, y);
    return 0;
}""",
  options=["1,2", "2,1", "1,1", "编译错误"], answer=1, expect="2,1",
  explain="形参是指针，&x 把实参地址传给函数，*p 就是 x 本身，函数内交换的是实参的值，所以 main 中 x、y 变成 2,1。这是指针最典型的用途。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[5] = {1, 2, 3, 4, 5};
    int *p, s = 0;
    for (p = a; p < a + 5; p++)
        s += *p;
    printf("%d", s);
    return 0;
}""",
  options=["5", "15", "20", "随机值"], answer=1, expect="15",
  explain="数组名 a 等价于首元素地址 &a[0]，p 从 a 递增到 a+4（p<a+5 为界），每次取 *p 累加，结果 15。指针遍历数组与下标访问等价。"),

 dict(level="hard", tag=["难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    int (*p)[3] = a;
    printf("%d", *(*(p + 1) + 2));
    return 0;
}""",
  options=["3", "5", "6", "地址值"], answer=2, expect="6",
  explain="int (*p)[3] 是指向一维数组（含 3 个 int）的指针，p+1 指向第二行，*(p+1) 得到第二行首地址，再 +2 指向该行第 3 个元素，得 6，等价于 a[1][2]。"),
]

# ---------------- 第9章 结构体/共用体/枚举 ----------------
QUIZ["ch09"] = [
 dict(level="hard", tag=["易错", "难题"],
  q="下列程序的运行结果是（按常见 8 字节对齐）：",
  code="""#include <stdio.h>
struct S
{
    int a;
    char b;
    double c;
};
int main()
{
    printf("%d", (int)sizeof(struct S));
    return 0;
}""",
  options=["13", "16", "24", "8"], answer=1, expect="16",
  explain="结构体存在内存对齐：int 占 4 字节，char 占 1 字节后需填充 3 字节对齐到 8 字节边界，double 占 8 字节，共 4+1+3+8=16 字节。所以 sizeof 结构体不等于各成员大小简单相加。"),

 dict(level="hard", tag=["难题"],
  q="下列程序的运行结果是（按常见 8 字节对齐）：",
  code="""#include <stdio.h>
union U
{
    int a;
    char b[5];
    double c;
};
int main()
{
    printf("%d", (int)sizeof(union U));
    return 0;
}""",
  options=["5", "8", "13", "17"], answer=1, expect="8",
  explain="共用体的所有成员共用同一块存储空间，其大小等于最长成员并满足对齐要求：最长成员为 double 的 8 字节，故 sizeof 为 8，不是各成员之和。"),

 dict(level="hard", tag=["易错", "常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
struct P
{
    int x;
};
int main()
{
    struct P p = {5}, *q = &p;
    int a = q->x++;
    printf("%d,%d", a, p.x);
    return 0;
}""",
  options=["5,5", "5,6", "6,6", "6,5"], answer=1, expect="5,6",
  explain="q->x++ 是后缀自增：先把 x 的原值 5 赋给 a，再让 x 增 1 变成 6，所以输出 5,6。-> 运算符与 . 优先级相同，均高于 ++。"),

 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
struct P
{
    int a;
    int b;
};
int main()
{
    struct P p1 = {1, 2}, p2;
    p2 = p1;
    p2.a = 9;
    printf("%d,%d", p1.a, p2.a);
    return 0;
}""",
  options=["9,9", "1,9", "1,1", "编译错误"], answer=1, expect="1,9",
  explain="同类型的结构体变量可以整体赋值，赋值是把各成员的值逐个复制一份（值拷贝），之后修改 p2.a 不影响 p1.a，输出 1,9。"),
]

# ---------------- 第10章 文件 ----------------
QUIZ["ch10"] = [
 dict(level="mid", tag=["常考"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    FILE *fp = fopen("qt10_a.txt", "w");
    fputs("abc", fp);
    fclose(fp);

    fp = fopen("qt10_a.txt", "r");
    fseek(fp, 0, SEEK_END);
    printf("%ld", ftell(fp));
    fclose(fp);
    return 0;
}""",
  options=["0", "3", "4", "随机值"], answer=1, expect="3",
  explain="写入 3 个字符后文件长度为 3 字节。fseek(fp,0,SEEK_END) 把位置指针移到文件末尾，ftell 返回当前位置相对文件开头的字节偏移，即 3。"),

 dict(level="hard", tag=["常考", "难题"],
  q="下列程序的运行结果是：",
  code="""#include <stdio.h>
int main()
{
    FILE *fp = fopen("qt10_b.txt", "w");
    fprintf(fp, "12 34");
    fclose(fp);

    fp = fopen("qt10_b.txt", "r");
    int a, b, n;
    n = fscanf(fp, "%d%d", &a, &b);
    printf("%d,%d,%d", n, a, b);
    fclose(fp);
    return 0;
}""",
  options=["2,12,34", "1,12,34", "0,0,0", "12,34,0"], answer=0, expect="2,12,34",
  explain="fscanf 的返回值是成功读入的数据项个数，两个 %d 都读成功故返回 2，a=12、b=34。可用返回值判断读取是否成功。"),

 dict(level="hard", tag=["易错", "常考"],
  q="关于文件打开方式，下列说法正确的是：",
  code=None, options=[
   "用 \"w\" 打开已存在的文件时，原内容会被清空（截断）",
   "用 \"w\" 打开不存在的文件会失败，返回 NULL",
   "用 \"r\" 打开不存在的文件会自动新建一个空文件",
   "用 \"a\" 打开文件后，写入的数据会覆盖文件开头的内容"], answer=0,
  explain="\"w\" 会创建文件或把已有文件截断为 0 长度；\"r\" 打开不存在的文件直接失败返回 NULL；\"a\" 是追加，写入的数据总在文件末尾。打开文件后必须判断返回值是否为 NULL。"),

 dict(level="hard", tag=["易错"],
  q="关于 fgetc 与 feof，下列说法正确的是：",
  code=None, options=[
   "fgetc 返回 char，读到文件尾返回 -1 的 char 形式",
   "fgetc 返回 int，读到文件尾返回 EOF（值为 -1），必须用 int 接收才能正确判断结束",
   "feof 在刚打开文件时就返回真，可用于判断文件是否为空",
   "读取二进制文件时不能用 fgetc，因为会丢失数据"], answer=1,
  explain="fgetc 的返回值类型是 int，这样既能返回 0~255 的字节值，也能返回 -1（EOF）。若用 char 接收，值 0xFF 的字节会与 EOF 混淆，导致判断错误。feof 只在读操作失败后才置位，不能用来预判文件是否为空。"),
]


def norm(s):
    lines = [x.rstrip() for x in (s or "").replace("\r\n", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def verify(item, key):
    code = item.get("code")
    if not code or item.get("norun"):
        return True, ""
    src = os.path.join(TMP, key + ".c")
    exe = os.path.join(TMP, key + ".exe")
    open(src, "w", encoding="utf-8").write(code)
    r = subprocess.run([GCC, "-std=c11", "-O0", "-o", exe, src], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return False, "compile: " + (r.stderr or "")[:400]
    run = subprocess.run([exe], cwd=TMP, capture_output=True, text=True, encoding="utf-8", errors="replace",
                         input=item.get("stdin", ""), timeout=15)
    got = norm(run.stdout)
    if got != norm(item["expect"]):
        return False, "stdout=%r expect=%r" % (got, item["expect"])
    return True, ""


total = 0
for chap, items in QUIZ.items():
    path = os.path.join(DATA, chap + ".json")
    d = json.load(open(path, encoding="utf-8"))
    nums = [int(m.group(1)) for x in d["choice"] for m in [re.search(r"-c(\d+)$", x["id"])] if m]
    nxt = max(nums) + 1 if nums else 1
    added = 0
    for k, it in enumerate(items):
        key = "%s_h%d" % (chap, k)
        ok, msg = verify(it, key)
        if not ok:
            print("FAIL", chap, it["q"][:24], msg)
            continue
        if it.get("expect") and norm(it["options"][it["answer"]]) != norm(it["expect"]):
            print("ANSWER-MISMATCH", chap, it["q"][:24])
            continue
        item = dict(it)
        item.pop("stdin", None)
        item.pop("norun", None)
        item["id"] = "%s-c%d" % (chap.replace("ch", ""), nxt)
        item.setdefault("code", None)
        d["choice"].append(item)
        nxt += 1
        added += 1
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(chap, "added", added, "total choice", len(d["choice"]))
    total += added
print("ALL ADDED", total)

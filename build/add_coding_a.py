# -*- coding: utf-8 -*-
"""按选择题同样的方式，为第 1-5 章编程题补充 常考/易错/难题 标注题，并逐题实跑校验。"""
import json, os, subprocess, tempfile, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data3")
WORK = os.path.join(BASE, "_runc")
os.makedirs(WORK, exist_ok=True)


def norm(text):
    if text is None:
        return ""
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run(code, stdin_text):
    cpath = os.path.join(WORK, "m.c")
    epath = os.path.join(WORK, "m.exe")
    with open(cpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
    if os.path.exists(epath):
        os.remove(epath)
    cp = subprocess.run(["gcc", "-std=c11", "-O2", cpath, "-o", epath, "-lm"],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if cp.returncode != 0:
        raise RuntimeError("编译失败: " + cp.stderr[:800])
    rp = subprocess.run([epath], input=stdin_text, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=10)
    return norm(rp.stdout)


Q = []


def add(ch, key, title, level, tag, tags, desc, inp, outp, hint, code, inputs):
    Q.append(dict(ch=ch, id=key, title=title, level=level, tag=tag, tags=tags,
                  desc=desc, input=inp, output=outp, hint=hint, code=code, inputs=inputs))


# ============ 第 1 章 ============
add(1, "1-p13", "整数的平方、立方与平方根", "mid", ["常考"], ["顺序结构", "printf", "sqrt"],
    "输入一个正整数 n，分行输出它的平方、立方和平方根（平方根保留 2 位小数）。",
    "一行，一个正整数 n（1 ≤ n ≤ 1000）。",
    "共三行：第一行为 n 的平方，第二行为 n 的立方，第三行为 n 的平方根（保留 2 位小数）。",
    "平方用的是同一个变量自乘两次；求平方根要先 #include <math.h>，并把 n 强制转换成 double：sqrt((double)n)。",
    """#include <stdio.h>
#include <math.h>

int main()
{
    int n;
    scanf("%d", &n);
    printf("%d\\n", n * n);
    printf("%d\\n", n * n * n);
    printf("%.2f\\n", sqrt((double)n));
    return 0;
}""",
    ["9", "1", "2", "16", "25"])

add(1, "1-p14", "把总钱数换成元角分", "mid", ["易错"], ["顺序结构", "整除", "取余"],
    "输入一个用“分”表示的总钱数 m，把它换算成“元、角、分”的形式输出。",
    "一行，一个非负整数 m（0 ≤ m ≤ 99999），单位为分。",
    "输出一行，格式为：x元y角z分（x、y、z 均为整数，不加前导零）。",
    "元 = m / 100，角 = m % 100 / 10，分 = m % 10。注意先把“元”取走，再在剩下的两位里取角，不能直接用 m / 10 % 10。",
    """#include <stdio.h>

int main()
{
    int m;
    scanf("%d", &m);
    printf("%d元%d角%d分\\n", m / 100, m % 100 / 10, m % 10);
    return 0;
}""",
    ["1234", "100", "99", "8", "99999"])

# ============ 第 2 章 ============
add(2, "2-p14", "数字字符转成数值", "easy", ["常考"], ["字符", "ASCII", "类型转换"],
    "输入一个数字字符（'0'~'9'），输出它所代表的整数以及该整数的平方。",
    "一行，一个数字字符。",
    "共两行：第一行为该字符对应的整数，第二行为该整数的平方。",
    "数字字符的 ASCII 码是连续的，'0' 的码值是 48，所以字符 c 对应的数值是 c - '0'。",
    """#include <stdio.h>

int main()
{
    char c;
    int v;
    scanf("%c", &c);
    v = c - '0';
    printf("%d\\n", v);
    printf("%d\\n", v * v);
    return 0;
}""",
    ["7", "0", "9", "5", "3"])

add(2, "2-p15", "两个大整数相乘（小心溢出）", "hard", ["易错", "难题"], ["数据类型", "long long", "溢出"],
    "输入两个整数 a 和 b，输出它们的乘积。注意乘积可能超出 int 的表示范围。",
    "一行，两个整数 a、b（-100000 ≤ a, b ≤ 100000）。",
    "输出一行，为 a 与 b 的乘积。",
    "int 只能存到约 21 亿，100000×100000=10^10 早就溢出了。要先把其中一个数转成 long long 再乘：printf(\"%lld\\n\", (long long)a * b)；直接用 %d 输出会得到错误结果。",
    """#include <stdio.h>

int main()
{
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%lld\\n", (long long)a * b);
    return 0;
}""",
    ["100000 100000", "65536 65536", "46341 46341", "1000 1000", "-50000 50000"])

add(2, "2-p16", "字母大小写互换", "hard", ["难题"], ["位运算", "字符", "ASCII"],
    "输入一个英文字母，输出它大小写互换后的字母（大写变小写，小写变大写）。",
    "一行，一个英文字母。",
    "输出一行，为互换大小写后的字母。",
    "大写字母与对应小写字母的 ASCII 码只差第 5 位（32），用异或即可互换：c ^ 32。也可以用条件表达式 c >= 'a' ? c - 32 : c + 32。",
    """#include <stdio.h>

int main()
{
    char c;
    scanf("%c", &c);
    printf("%c\\n", c ^ 32);
    return 0;
}""",
    ["a", "Z", "m", "B", "x"])

add(2, "2-p17", "整数的八进制与十六进制形式", "mid", ["常考", "易错"], ["格式输出", "进制"],
    "输入一个非负整数 n，分行输出它的八进制形式和十六进制形式（小写字母）。",
    "一行，一个非负整数 n（0 ≤ n ≤ 100000）。",
    "共两行：第一行为八进制形式，第二行为十六进制形式。",
    "%o 输出八进制，%x 输出小写十六进制，%X 输出大写十六进制。注意输出的是形式，不是数值。",
    """#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);
    printf("%o\\n", n);
    printf("%x\\n", n);
    return 0;
}""",
    ["255", "8", "100", "4095", "16"])

# ============ 第 3 章 ============
add(3, "3-p14", "按权重计算综合成绩", "mid", ["常考"], ["顺序结构", "浮点运算", "格式输出"],
    "某课程成绩由三部分组成：平时成绩占 30%，期中成绩占 30%，期末成绩占 40%。输入这三项成绩（整数），输出综合成绩（保留 1 位小数）。",
    "一行，三个整数，依次为平时、期中、期末成绩（0 ≤ 成绩 ≤ 100）。",
    "输出一行，为综合成绩，保留 1 位小数。",
    "权重是小数，直接写 a * 0.3 + b * 0.3 + c * 0.4 即可；如果写成 a * 3 / 10 容易因整除丢精度。",
    """#include <stdio.h>

int main()
{
    int a, b, c;
    double s;
    scanf("%d%d%d", &a, &b, &c);
    s = a * 0.3 + b * 0.3 + c * 0.4;
    printf("%.1f\\n", s);
    return 0;
}""",
    ["90 80 70", "100 100 100", "60 60 60", "85 92 78", "0 50 100"])

add(3, "3-p15", "平均值四舍五入取整", "mid", ["易错"], ["整除", "强制类型转换", "四舍五入"],
    "输入三个整数，输出它们的平均值按四舍五入规则取整后的结果。",
    "一行，三个整数（0 ≤ 整数 ≤ 1000）。",
    "输出一行，一个整数，为三个数平均值四舍五入后的结果。",
    "先算浮点平均值（除以 3.0，不能写 / 3，否则整数除法直接截断），再加上 0.5 后强制转换成 int：(int)(sum / 3.0 + 0.5)。",
    """#include <stdio.h>

int main()
{
    int a, b, c;
    double avg;
    scanf("%d%d%d", &a, &b, &c);
    avg = (a + b + c) / 3.0;
    printf("%d\\n", (int)(avg + 0.5));
    return 0;
}""",
    ["1 2 4", "2 3 3", "5 5 5", "1 1 1", "9 10 11"])

add(3, "3-p16", "求平面两点间的距离", "hard", ["难题", "常考"], ["顺序结构", "math.h", "sqrt"],
    "输入平面直角坐标系中两个点的坐标，输出这两点之间的距离（保留 2 位小数）。",
    "一行，四个实数 x1 y1 x2 y2，两两构成一个点。",
    "输出一行，为两点间的距离，保留 2 位小数。",
    "距离公式 d = sqrt((x1-x2)^2 + (y1-y2)^2)。读实数用 %lf，开方要 #include <math.h>；注意平方要用 (x1-x2)*(x1-x2)，不能写 x1^2。",
    """#include <stdio.h>
#include <math.h>

int main()
{
    double x1, y1, x2, y2, dx, dy;
    scanf("%lf%lf%lf%lf", &x1, &y1, &x2, &y2);
    dx = x1 - x2;
    dy = y1 - y2;
    printf("%.2f\\n", sqrt(dx * dx + dy * dy));
    return 0;
}""",
    ["0 0 3 4", "1 1 4 5", "0 0 1 1", "2 3 5 7", "0 0 2.5 0"])

add(3, "3-p17", "三位数逆序并按三位宽度输出", "mid", ["易错"], ["顺序结构", "拆位", "格式输出"],
    "输入一个三位正整数，把它逆序后按 3 位宽度输出（不足 3 位前面补 0）。",
    "一行，一个三位正整数 n（100 ≤ n ≤ 999）。",
    "输出一行，为 n 逆序后的数，按 3 位宽度输出，不足补前导 0。",
    "拆位：百位 n/100，十位 n/10%10，个位 n%10；逆序数 = 个位*100 + 十位*10 + 百位。输出用 %03d 补零。",
    """#include <stdio.h>

int main()
{
    int n, r;
    scanf("%d", &n);
    r = n % 10 * 100 + n / 10 % 10 * 10 + n / 100;
    printf("%03d\\n", r);
    return 0;
}""",
    ["123", "120", "100", "999", "507"])

# ============ 第 4 章 ============
add(4, "4-p14", "三个整数从小到大排序", "hard", ["难题", "常考"], ["选择结构", "if", "交换"],
    "输入三个整数，把它们按从小到大的顺序输出。",
    "一行，三个整数（-10000 ≤ 整数 ≤ 10000）。",
    "输出一行，三个整数从小到大排列，数与数之间用一个空格分隔。",
    "用三次比较交换：先让 a≤b，再让 a≤c，最后让 b≤c。每次比较若不满足顺序就借助临时变量交换，不用写复杂的分支嵌套。",
    """#include <stdio.h>

int main()
{
    int a, b, c, t;
    scanf("%d%d%d", &a, &b, &c);
    if (a > b)
    {
        t = a;
        a = b;
        b = t;
    }
    if (a > c)
    {
        t = a;
        a = c;
        c = t;
    }
    if (b > c)
    {
        t = b;
        b = c;
        c = t;
    }
    printf("%d %d %d\\n", a, b, c);
    return 0;
}""",
    ["3 1 2", "1 2 3", "5 5 1", "9 8 7", "-1 0 -5"])

add(4, "4-p15", "判断三角形的类型", "hard", ["难题", "易错"], ["选择结构", "多分支", "勾股定理"],
    "输入三条边的长度（整数），判断它们能否构成三角形；若能，再判断是等边、等腰、直角还是一般三角形。",
    "一行，三个正整数（1 ≤ 边长 ≤ 1000）。",
    "输出一行：不能构成三角形输出 none；等边三角形输出 equilateral；等腰三角形输出 isosceles；直角三角形输出 right；其他输出 scalene。",
    "先用任意两边之和大于第三边排除不成立的情况（注意要写三组判断并注意 <= ）；再依次判断三边相等、勾股定理（a*a+b*b==c*c，三组要都试）、两边相等。判断顺序决定优先级。",
    """#include <stdio.h>

int main()
{
    int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    if (a + b <= c || a + c <= b || b + c <= a)
        printf("none\\n");
    else if (a == b && b == c)
        printf("equilateral\\n");
    else if (a * a + b * b == c * c || a * a + c * c == b * b || b * b + c * c == a * a)
        printf("right\\n");
    else if (a == b || b == c || a == c)
        printf("isosceles\\n");
    else
        printf("scalene\\n");
    return 0;
}""",
    ["3 4 5", "3 3 3", "3 3 4", "1 2 3", "2 3 4"])

add(4, "4-p16", "BMI 指数与健康等级", "mid", ["常考"], ["选择结构", "浮点比较", "多分支"],
    "输入身高（米）和体重（千克），先输出 BMI 指数（保留 2 位小数），再输出健康等级。",
    "一行，两个实数：身高 h（米）和体重 w（千克）。",
    "共两行：第一行为 BMI 指数，保留 2 位小数；第二行为等级，BMI<18.5 输出 thin，18.5≤BMI<24 输出 normal，24≤BMI<28 输出 overweight，BMI≥28 输出 obese。",
    "BMI = w / (h*h)。多分支用 if ... else if ... else 从上往下判断，条件只写上限即可，因为前面的分支已经排除了更小的情况。",
    """#include <stdio.h>

int main()
{
    double h, w, bmi;
    scanf("%lf%lf", &h, &w);
    bmi = w / (h * h);
    printf("%.2f\\n", bmi);
    if (bmi < 18.5)
        printf("thin\\n");
    else if (bmi < 24)
        printf("normal\\n");
    else if (bmi < 28)
        printf("overweight\\n");
    else
        printf("obese\\n");
    return 0;
}""",
    ["1.75 70", "1.70 50", "1.60 65", "1.75 90", "1.80 80"])

add(4, "4-p17", "判断元音字母还是辅音字母", "mid", ["易错"], ["switch", "break", "字符判断"],
    "输入一个英文字母，判断它是元音字母（a、e、i、o、u，大小写都算）还是辅音字母。",
    "一行，一个英文字母。",
    "输出一行：元音字母输出 vowel，辅音字母输出 consonant。",
    "用 switch 时可以把多个 case 写在一起共用一段代码，例如 case 'a': case 'A': ...，但这段代码末尾必须有 break，否则会“穿透”到 default 输出错误结果。",
    """#include <stdio.h>

int main()
{
    char c;
    scanf("%c", &c);
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
    case 'A':
    case 'E':
    case 'I':
    case 'O':
    case 'U':
        printf("vowel\\n");
        break;
    default:
        printf("consonant\\n");
    }
    return 0;
}""",
    ["a", "Z", "E", "m", "U"])

# ============ 第 5 章 ============
add(5, "5-p14", "输出 n 行菱形", "hard", ["难题"], ["循环嵌套", "图形输出"],
    "输入一个奇数 n，输出一个由星号组成、共 n 行的菱形（星号之间不留空格）。",
    "一行，一个奇数 n（1 ≤ n ≤ 19）。",
    "输出 n 行菱形图案。每行的星号前有若干空格，用来把星号顶到中间位置，行末不要输出多余空格。",
    "把菱形拆成上半部分（含中间最长一行）和下半部分。第 i 行（i 从 0 数）前面有 mid-i 个空格、2*i+1 个星号，其中 mid=n/2；下半部分把 i 从 mid-1 递减到 0 再做一遍。",
    """#include <stdio.h>

int main()
{
    int n, i, j, mid;
    scanf("%d", &n);
    mid = n / 2;
    for (i = 0; i <= mid; i++)
    {
        for (j = 0; j < mid - i; j++)
            printf(" ");
        for (j = 0; j < 2 * i + 1; j++)
            printf("*");
        printf("\\n");
    }
    for (i = mid - 1; i >= 0; i--)
    {
        for (j = 0; j < mid - i; j++)
            printf(" ");
        for (j = 0; j < 2 * i + 1; j++)
            printf("*");
        printf("\\n");
    }
    return 0;
}""",
    ["5", "1", "3", "7", "9"])

add(5, "5-p15", "找出 1 到 n 之间的完数", "hard", ["常考", "易错"], ["循环", "因子", "枚举"],
    "如果一个数恰好等于它所有真因子（除自身以外的因子）之和，这样的数称为完数。输入 n，输出 1 到 n 之间所有的完数。",
    "一行，一个正整数 n（2 ≤ n ≤ 10000）。",
    "输出一行，为 1 到 n 之间所有的完数，数与数之间用一个空格分隔，行末换行。",
    "对每个 i，用 j 从 1 试到 i/2 累加因子和，再和 i 比较。注意每个 i 的因子和必须先清零，1 不是完数所以从 2 开始试；输出时用 first 标记控制空格的个数。",
    """#include <stdio.h>

int main()
{
    int n, i, j, s, first = 1;
    scanf("%d", &n);
    for (i = 2; i <= n; i++)
    {
        s = 0;
        for (j = 1; j <= i / 2; j++)
            if (i % j == 0)
                s = s + j;
        if (s == i)
        {
            if (!first)
                printf(" ");
            printf("%d", i);
            first = 0;
        }
    }
    printf("\\n");
    return 0;
}""",
    ["10", "100", "1000", "10000", "6"])

add(5, "5-p16", "阶乘的累加和", "hard", ["常考"], ["循环", "累乘", "累加"],
    "输入 n，计算并输出 1! + 2! + 3! + ... + n! 的值。",
    "一行，一个正整数 n（1 ≤ n ≤ 12）。",
    "输出一行，为阶乘和的值。",
    "不要为每一项重新算阶乘（那样是双重循环）。用一个变量 f 边乘边用：每次 f = f * i 就是 i!，再累加到 s 里，单层循环即可。n 到 12 时结果超出 int，s 要用 long long，输出用 %lld。",
    """#include <stdio.h>

int main()
{
    int n, i;
    long long f = 1, s = 0;
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
    {
        f = f * i;
        s = s + f;
    }
    printf("%lld\\n", s);
    return 0;
}""",
    ["1", "3", "5", "10", "12"])

add(5, "5-p17", "能被 3 整除但不能被 5 整除", "mid", ["易错"], ["循环", "逻辑运算", "条件累加"],
    "输入 n，统计 1 到 n 之间能被 3 整除但不能被 5 整除的数的个数，并求这些数的和。",
    "一行，一个正整数 n（1 ≤ n ≤ 1000）。",
    "共两行：第一行为满足条件的数的个数，第二行为这些数的和。",
    "条件是“能被 3 整除 且 不能被 5 整除”，写成 i % 3 == 0 && i % 5 != 0；不要漏掉 != 0 的取反，也不要写成 || 把 5 的倍数的 3 的倍数算进去（如 15）。",
    """#include <stdio.h>

int main()
{
    int n, i, c = 0, s = 0;
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
        if (i % 3 == 0 && i % 5 != 0)
        {
            c++;
            s = s + i;
        }
    printf("%d\\n", c);
    printf("%d\\n", s);
    return 0;
}""",
    ["10", "30", "15", "100", "7"])

add(5, "5-p18", "求 1+(1+2)+...+(1+2+...+n)", "hard", ["难题"], ["循环嵌套", "累加"],
    "输入 n，计算并输出 1 + (1+2) + (1+2+3) + ... + (1+2+...+n) 的值。",
    "一行，一个正整数 n（1 ≤ n ≤ 100）。",
    "输出一行，为一个整数，即上述和。",
    "外层循环控制项数 i 从 1 到 n，内层循环把 1 加到 i 累加这一项，再加到总和 s。也可以只用一个循环，用 s = s + i*(i+1)/2 直接算每一项。",
    """#include <stdio.h>

int main()
{
    int n, i, j, s = 0;
    scanf("%d", &n);
    for (i = 1; i <= n; i++)
        for (j = 1; j <= i; j++)
            s = s + j;
    printf("%d\\n", s);
    return 0;
}""",
    ["1", "3", "5", "10", "20"])


def main():
    by_ch = {}
    for q in Q:
        tests = []
        for t in q["inputs"]:
            out = run(q["code"], t)
            tests.append({"in": t, "out": out})
        item = {
            "id": q["id"], "title": q["title"], "level": q["level"],
            "tags": q["tags"], "tag": q["tag"],
            "desc": q["desc"], "input": q["input"], "output": q["output"],
            "samples": [{"in": tests[0]["in"], "out": tests[0]["out"]}],
            "tests": tests, "hint": q["hint"], "code": q["code"],
        }
        by_ch.setdefault(q["ch"], []).append(item)
        print("[OK] %-6s %s  %s" % (q["id"], q["title"], "/".join(q["tag"])))
        print("     样例输出: %r" % tests[0]["out"][:70])
    for ch, items in by_ch.items():
        path = os.path.join(DATA, "ch%02d.json" % ch)
        d = json.load(open(path, encoding="utf-8"))
        ids = {c["id"] for c in d["coding"]}
        keep = [c for c in d["coding"] if c["id"] not in {i["id"] for i in items}]
        d["coding"] = keep + items
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        total_tag = sum(1 for c in d["coding"] if c.get("tag"))
        print("ch%02d: 编程题 %d 道，其中带标注 %d 道" % (ch, len(d["coding"]), total_tag))


if __name__ == "__main__":
    main()

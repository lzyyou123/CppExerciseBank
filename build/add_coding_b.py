# -*- coding: utf-8 -*-
"""为第 6-10 章编程题补充 常考/易错/难题 标注题，并逐题实跑校验。"""
import json, os, subprocess

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
    cpath = os.path.join(WORK, "n.c")
    epath = os.path.join(WORK, "n.exe")
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


# ============ 第 6 章 ============
add(6, "6-p11", "用函数输出 1 到 n 内的所有素数", "hard", ["常考"], ["函数", "循环", "素数"],
    "编写函数判断一个整数是否为素数，并在 main 函数中输出 1 到 n 之间的所有素数。",
    "一行，一个正整数 n（2 ≤ n ≤ 1000）。",
    "输出一行，为 1 到 n 之间的所有素数，数与数之间用一个空格分隔。",
    "判断素数只需用 j 从 2 试到 sqrt(i)（写 j*j<=i 也行）。1 不是素数，循环从 2 开始；找到因子就 break，用一个标志变量记录是否为素数。",
    """#include <stdio.h>

int isPrime(int n)
{
    int j;
    if (n < 2)
        return 0;
    for (j = 2; j * j <= n; j++)
        if (n % j == 0)
            return 0;
    return 1;
}

int main()
{
    int n, i, first = 1;
    scanf("%d", &n);
    for (i = 2; i <= n; i++)
        if (isPrime(i))
        {
            if (!first)
                printf(" ");
            printf("%d", i);
            first = 0;
        }
    printf("\\n");
    return 0;
}""",
    ["10", "30", "2", "100", "7"])

add(6, "6-p12", "值传递与地址传递的差别", "hard", ["易错", "难题"], ["函数", "参数传递", "指针"],
    "分别写两个交换函数：swap1 用普通参数（值传递），swap2 用指针参数（地址传递）。输入两个整数，先调用 swap1 输出两个数，再调用 swap2 输出两个数。",
    "一行，两个整数 a、b（-1000 ≤ a, b ≤ 1000）。",
    "共两行：第一行为调用 swap1 之后 a、b 的值，第二行为调用 swap2 之后 a、b 的值，数与数之间用一个空格分隔。",
    "值传递时函数里交换的只是形参副本，实参根本不受影响，所以第一行仍按原顺序输出；地址传递时函数用 *x、*y 直接改主函数里的变量，交换才真正生效。",
    """#include <stdio.h>

void swap1(int x, int y)
{
    int t;
    t = x;
    x = y;
    y = t;
}

void swap2(int *x, int *y)
{
    int t;
    t = *x;
    *x = *y;
    *y = t;
}

int main()
{
    int a, b;
    scanf("%d%d", &a, &b);
    swap1(a, b);
    printf("%d %d\\n", a, b);
    swap2(&a, &b);
    printf("%d %d\\n", a, b);
    return 0;
}""",
    ["1 2", "5 9", "100 200", "-3 7", "8 8"])

add(6, "6-p13", "用函数分解质因数", "hard", ["难题"], ["函数", "循环", "分解"],
    "编写函数，把输入的正整数分解成质因数连乘的形式并输出。",
    "一行，一个正整数 n（2 ≤ n ≤ 100000）。",
    "输出一行，格式为 n=质因数*质因数*...，质因数按从小到大排列，乘号用 *。",
    "从 i=2 开始试，只要能整除就一直除下去（用 while），除完再让 i 加一。注意别用原来的 n 直接参与判题，最好先把它存到局部变量里。乘号用 first 标记只在第一个因数前不加。",
    """#include <stdio.h>

void factor(int n)
{
    int i, first = 1, m = n;
    printf("%d=", n);
    for (i = 2; i <= m; i++)
        while (m % i == 0)
        {
            if (!first)
                printf("*");
            printf("%d", i);
            first = 0;
            m = m / i;
        }
    printf("\\n");
}

int main()
{
    int n;
    scanf("%d", &n);
    factor(n);
    return 0;
}""",
    ["12", "7", "100", "360", "97"])

add(6, "6-p14", "判断回文数", "mid", ["常考"], ["函数", "循环", "回文"],
    "编写函数把整数逆序，再在主函数中判断输入的整数是否为回文数（正着读和倒着读相同的数）。",
    "一行，一个正整数 m（1 ≤ m ≤ 100000000）。",
    "输出一行：是回文数输出 yes，否则输出 no。",
    "逆序用循环：r = r * 10 + n % 10; n = n / 10;。注意用局部变量保存原数，比较的是逆序结果与原数是否相等。",
    """#include <stdio.h>

int reverse(int n)
{
    int r = 0;
    while (n > 0)
    {
        r = r * 10 + n % 10;
        n = n / 10;
    }
    return r;
}

int main()
{
    int m;
    scanf("%d", &m);
    if (reverse(m) == m)
        printf("yes\\n");
    else
        printf("no\\n");
    return 0;
}""",
    ["121", "123", "1001", "12321", "10"])

# ============ 第 7 章 ============
add(7, "7-p11", "数组去重（保持原顺序）", "hard", ["难题"], ["数组", "去重", "查找"],
    "输入 n 个整数，把其中重复出现的元素去掉，只保留每个数第一次出现的那一个，按原来的先后顺序输出。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数，用空格分隔。",
    "共两行：第一行为去重后剩下的元素个数；第二行为去重后的元素，按原顺序排列，数与数之间用一个空格分隔。",
    "借助第二个数组 b 存放结果：对每个 a[i]，先用循环在 b 里查一遍有没有出现过，没出现过才追加到 b 末尾并让长度 k 加一。",
    """#include <stdio.h>

int main()
{
    int n, i, j, k = 0, dup, a[100], b[100];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (i = 0; i < n; i++)
    {
        dup = 0;
        for (j = 0; j < k; j++)
            if (b[j] == a[i])
            {
                dup = 1;
                break;
            }
        if (!dup)
        {
            b[k] = a[i];
            k++;
        }
    }
    printf("%d\\n", k);
    for (i = 0; i < k; i++)
    {
        if (i)
            printf(" ");
        printf("%d", b[i]);
    }
    printf("\\n");
    return 0;
}""",
    ["6\n1 2 2 3 1 4", "5\n5 5 5 5 5", "3\n1 2 3", "8\n3 1 3 1 4 4 1 2", "1\n7"])

add(7, "7-p12", "矩阵转置", "hard", ["难题", "常考"], ["二维数组", "嵌套循环"],
    "输入一个 m 行 n 列的整数矩阵，输出它的转置矩阵（把行变成列）。",
    "第一行两个正整数 m、n（1 ≤ m, n ≤ 10）；接下来 m 行，每行 n 个整数。",
    "输出 n 行，每行 m 个整数，为转置后的矩阵，同一行的数用一个空格分隔。",
    "转置后行数是原来的列数 n，列数是原来的行数 m。输出时把两层循环的下标互换：外层 j 从 0 到 n-1，内层 i 从 0 到 m-1，输出 a[i][j]。",
    """#include <stdio.h>

int main()
{
    int m, n, i, j, a[10][10];
    scanf("%d%d", &m, &n);
    for (i = 0; i < m; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    for (j = 0; j < n; j++)
    {
        for (i = 0; i < m; i++)
        {
            if (i)
                printf(" ");
            printf("%d", a[i][j]);
        }
        printf("\\n");
    }
    return 0;
}""",
    ["2 3\n1 2 3\n4 5 6", "3 3\n1 2 3\n4 5 6\n7 8 9", "1 1\n5", "2 2\n1 2\n3 4", "3 1\n1\n2\n3"])

add(7, "7-p13", "把一个数插入到有序数组中", "mid", ["易错"], ["数组", "插入", "移位"],
    "有一个已按从小到大排好序的数组，再输入一个整数，把它插入到数组中，使数组仍然有序。",
    "第一行一个正整数 n（1 ≤ n ≤ 20）；第二行 n 个从小到大排列的整数；第三行一个待插入的整数 x。",
    "输出一行，为插入 x 之后的 n+1 个整数，从小到大排列，数与数之间用一个空格分隔。",
    "从数组末尾往前找：只要 a[i] 比 x 大，就把它往后挪一位（a[i+1]=a[i]），直到找到不比 x 大的位置，把 x 放进 a[i+1]。这样不用额外开数组，也不会覆盖数据。",
    """#include <stdio.h>

int main()
{
    int n, i, x, a[30];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    scanf("%d", &x);
    i = n - 1;
    while (i >= 0 && a[i] > x)
    {
        a[i + 1] = a[i];
        i--;
    }
    a[i + 1] = x;
    for (i = 0; i <= n; i++)
    {
        if (i)
            printf(" ");
        printf("%d", a[i]);
    }
    printf("\\n");
    return 0;
}""",
    ["5\n1 3 5 7 9\n4", "5\n1 3 5 7 9\n0", "5\n1 3 5 7 9\n10", "3\n2 4 6\n2", "1\n5\n5"])

add(7, "7-p14", "删除数组中指定的元素", "mid", ["常考", "易错"], ["数组", "原地删除", "双下标"],
    "输入 n 个整数和一个整数 x，把数组中所有等于 x 的元素删除，输出剩下的元素。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数；第三行一个整数 x。",
    "共两行：第一行为删除后剩下的元素个数；第二行为剩下的元素，按原顺序排列，数与数之间用一个空格分隔。",
    "用两个下标：i 遍历原数组，k 记录保留下来的元素个数。a[i] 不等于 x 就执行 a[k]=a[i] 并让 k 加一。不要一边遍历一边往前挪，很容易越界丢数据。",
    """#include <stdio.h>

int main()
{
    int n, i, k = 0, x, a[100];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    scanf("%d", &x);
    for (i = 0; i < n; i++)
        if (a[i] != x)
        {
            a[k] = a[i];
            k++;
        }
    printf("%d\\n", k);
    for (i = 0; i < k; i++)
    {
        if (i)
            printf(" ");
        printf("%d", a[i]);
    }
    printf("\\n");
    return 0;
}""",
    ["6\n1 2 3 2 4 2\n2", "5\n7 7 7 7 7\n9", "4\n1 2 3 4\n1", "5\n5 1 5 2 5\n5", "2\n1 2\n1"])

# ============ 第 8 章 ============
add(8, "8-p11", "用指针原地逆序字符串", "hard", ["易错", "难题"], ["指针", "字符串", "双指针"],
    "输入一个不含空格的字符串，用指针把它在原数组中逆序存放，然后输出。",
    "一行，一个长度不超过 50 的字符串（不含空格）。",
    "输出一行，为逆序后的字符串。",
    "用两个指针：p 指向首字符，q 先走到最后一个字符（q 走到 '\\0' 后要回退一格）。两头交换后 p 后移、q 前移，直到 p >= q 停止。注意不要改动末尾的 '\\0'。",
    """#include <stdio.h>

void reverse(char *s)
{
    char *p = s, *q = s, t;
    while (*q != '\\0')
        q++;
    q--;
    while (p < q)
    {
        t = *p;
        *p = *q;
        *q = t;
        p++;
        q--;
    }
}

int main()
{
    char s[60];
    scanf("%s", s);
    reverse(s);
    printf("%s\\n", s);
    return 0;
}""",
    ["abc", "hello", "a", "abcd", "12345"])

add(8, "8-p12", "用指针实现选择排序", "hard", ["难题"], ["指针", "排序", "数组"],
    "输入 n 个整数，用指针访问数组元素，用选择排序把它们从小到大排序后输出。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数。",
    "输出一行，为从小到大排列的 n 个整数，数与数之间用一个空格分隔。",
    "用指针 p 指向当前待定位位置，内层指针 q 从 p+1 走到末尾找最小元素的位置 minp，找到后若 minp 不等于 p 就交换 *p 和 *minp。全部通过指针运算完成，不用下标。",
    """#include <stdio.h>

int main()
{
    int n, i, t, a[100];
    int *p, *q, *minp;
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    for (p = a; p < a + n - 1; p++)
    {
        minp = p;
        for (q = p + 1; q < a + n; q++)
            if (*q < *minp)
                minp = q;
        if (minp != p)
        {
            t = *p;
            *p = *minp;
            *minp = t;
        }
    }
    for (p = a; p < a + n; p++)
    {
        if (p != a)
            printf(" ");
        printf("%d", *p);
    }
    printf("\\n");
    return 0;
}""",
    ["5\n5 4 3 2 1", "3\n1 2 3", "6\n3 1 4 1 5 9", "4\n-1 0 -5 2", "1\n7"])

add(8, "8-p13", "用指针求二维数组每行的最大值", "mid", ["常考"], ["指针", "二维数组"],
    "输入一个 m 行 n 列的整数矩阵，用指针求出每一行的最大值并逐行输出。",
    "第一行两个正整数 m、n（1 ≤ m, n ≤ 10）；接下来 m 行，每行 n 个整数。",
    "输出 m 行，每行一个整数，依次为矩阵第 1 行到第 m 行的最大值。",
    "二维数组的行可以看成一维数组：p = a[i] 就是第 i 行的首地址，之后用 *(p+j) 访问第 j 个元素，先令 mx=*p 再逐个比较。",
    """#include <stdio.h>

int main()
{
    int m, n, i, j, a[10][10], *p, mx;
    scanf("%d%d", &m, &n);
    for (i = 0; i < m; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    for (i = 0; i < m; i++)
    {
        p = a[i];
        mx = *p;
        for (j = 1; j < n; j++)
            if (*(p + j) > mx)
                mx = *(p + j);
        printf("%d\\n", mx);
    }
    return 0;
}""",
    ["2 3\n1 5 3\n9 2 4", "3 2\n-1 -8\n7 0\n6 6", "1 4\n3 8 2 9", "2 2\n1 1\n1 1", "3 3\n5 5 5\n1 2 3\n9 0 4"])

add(8, "8-p14", "用指针参数同时求出最大值和最小值", "mid", ["常考", "易错"], ["指针", "函数参数", "出参"],
    "编写函数，通过指针参数把数组中的最大值和最小值一起带回主函数，并在主函数中输出。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数。",
    "输出一行，依次为最大值和最小值，中间用一个空格分隔。",
    "函数的指针参数可以用来“带回”多个结果：void mm(int *a, int n, int *pmax, int *pmin)，函数里用 *pmax、*pmin 赋值。调用时传 &mx、&mn 的地址，不要传值。",
    """#include <stdio.h>

void mm(int *a, int n, int *pmax, int *pmin)
{
    int i;
    *pmax = a[0];
    *pmin = a[0];
    for (i = 1; i < n; i++)
    {
        if (a[i] > *pmax)
            *pmax = a[i];
        if (a[i] < *pmin)
            *pmin = a[i];
    }
}

int main()
{
    int n, i, a[100], mx, mn;
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    mm(a, n, &mx, &mn);
    printf("%d %d\\n", mx, mn);
    return 0;
}""",
    ["5\n3 1 9 2 7", "1\n42", "4\n-5 -2 -9 -1", "6\n0 0 0 0 0 0", "5\n100 -100 50 0 25"])

# ============ 第 9 章 ============
add(9, "9-p11", "成绩表按总分降序、总分相同按学号升序", "hard", ["难题"], ["结构体", "排序", "多关键字"],
    "输入 n 个学生的学号和总分，按总分从高到低排序；总分相同的，学号小的排在前面。",
    "第一行一个正整数 n（1 ≤ n ≤ 50）；接下来 n 行，每行一个学号（整数）和总分（整数）。",
    "输出 n 行，每行为排序后的学号和总分，中间用一个空格分隔。",
    "交换条件写成：总分小的往后放；总分相等且学号大的往后放。也就是 if (a[i].total < a[i+1].total || (a[i].total == a[i+1].total && a[i].id > a[i+1].id)) 时交换这两个结构体，整体用冒泡即可。",
    """#include <stdio.h>

struct Stu
{
    int id;
    int total;
};

int main()
{
    int n, i, j;
    struct Stu a[50], t;
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d%d", &a[i].id, &a[i].total);
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (a[j].total < a[j + 1].total ||
                (a[j].total == a[j + 1].total && a[j].id > a[j + 1].id))
            {
                t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
            }
    for (i = 0; i < n; i++)
        printf("%d %d\\n", a[i].id, a[i].total);
    return 0;
}""",
    ["4\n1001 260\n1002 280\n1003 260\n1004 250", "3\n5 90\n1 90\n3 90", "1\n7 100", "5\n101 50\n102 60\n103 70\n104 80\n105 90"])

add(9, "9-p12", "统计高于平均分的人数", "mid", ["常考"], ["结构体数组", "平均值", "统计"],
    "输入 n 个学生的姓名和成绩，先输出平均分（保留 1 位小数），再输出高于平均分的人数。",
    "第一行一个正整数 n（1 ≤ n ≤ 50）；接下来 n 行，每行一个姓名（不含空格）和一个成绩（整数）。",
    "共两行：第一行为平均分，保留 1 位小数；第二行为成绩高于平均分的人数。",
    "先把成绩累加求平均值（除以 1.0*n 避免整除截断），再遍历一遍统计 a[i].score > avg 的人数。注意两次遍历用的是同一份数据，不要边累加边统计。",
    """#include <stdio.h>

struct Stu
{
    char name[20];
    int score;
};

int main()
{
    int n, i, s = 0, c = 0;
    double avg;
    struct Stu a[50];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%s%d", a[i].name, &a[i].score);
    for (i = 0; i < n; i++)
        s = s + a[i].score;
    avg = s / (1.0 * n);
    for (i = 0; i < n; i++)
        if (a[i].score > avg)
            c++;
    printf("%.1f\\n", avg);
    printf("%d\\n", c);
    return 0;
}""",
    ["4\nzhang 80\nli 90\nwang 70\nzhao 60", "3\nA 100\nB 100\nC 100", "1\nTom 55", "5\na 60\nb 61\nc 62\nd 63\ne 64"])

add(9, "9-p13", "结构体作为参数：值传递与指针传递", "hard", ["易错"], ["结构体", "参数传递", "指针"],
    "定义学生结构体（姓名、成绩）。写两个函数：addByValue 用结构体值参数给成绩加 10 分，addByPointer 用结构体指针参数给成绩加 10 分。主函数先输出加分前的成绩，再依次调用两个函数并各输出一次成绩。",
    "一行，一个姓名（不含空格）和一个成绩（整数，0 ≤ 成绩 ≤ 100）。",
    "共三行：第一行为原始成绩，第二行为调用 addByValue 后的成绩，第三行为调用 addByPointer 后的成绩。",
    "结构体作为值参数时，函数里改的是副本，主函数的成绩不变；用指针参数（struct Stu *p）配合 p->score 才能改到主函数的变量。先加一次再取地址传给指针函数即可。",
    """#include <stdio.h>

struct Stu
{
    char name[20];
    int score;
};

void addByValue(struct Stu s)
{
    s.score = s.score + 10;
}

void addByPointer(struct Stu *p)
{
    p->score = p->score + 10;
}

int main()
{
    struct Stu a;
    scanf("%s%d", a.name, &a.score);
    printf("%d\\n", a.score);
    addByValue(a);
    printf("%d\\n", a.score);
    addByPointer(&a);
    printf("%d\\n", a.score);
    return 0;
}""",
    ["zhang 80", "li 0", "wang 90", "A 55", "tom 100"])

add(9, "9-p14", "用结构体求某日期是这一年的第几天", "hard", ["难题", "常考"], ["结构体", "数组", "闰年"],
    "用结构体表示日期（年、月、日），输入一个日期，输出它是这一年的第几天。",
    "一行，三个整数：年、月、日（1900 ≤ 年 ≤ 2100，日期保证合法）。",
    "输出一行，为这一天是该年的第几天。",
    "用一个 12 个月的数组存每月天数，先算出前 m-1 个月的天数总和再加上日；如果是闰年且月份大于 2，还要把 2 月从 28 天改成 29 天（多加 1 天）。闰年条件是 (y%4==0 && y%100!=0) || y%400==0。",
    """#include <stdio.h>

struct Date
{
    int y;
    int m;
    int d;
};

int dayOfYear(struct Date t)
{
    int a[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int i, s = t.d;
    if ((t.y % 4 == 0 && t.y % 100 != 0) || t.y % 400 == 0)
        a[2] = 29;
    for (i = 1; i < t.m; i++)
        s = s + a[i];
    return s;
}

int main()
{
    struct Date t;
    scanf("%d%d%d", &t.y, &t.m, &t.d);
    printf("%d\\n", dayOfYear(t));
    return 0;
}""",
    ["2024 3 1", "2023 3 1", "2024 12 31", "2023 1 1", "2000 2 29"])

# ============ 第 10 章 ============
add(10, "10-p11", "统计文件中字母、数字和其他字符的个数", "mid", ["常考", "易错"], ["文件", "fgetc", "EOF"],
    "输入一个不含空格的字符串，先把它写入文件 f111.txt，再用 fgetc 逐个字符读回，统计其中字母、数字和其他字符各有多少个。",
    "一行，一个长度不超过 200 的字符串（不含空格）。",
    "输出一行，三个整数，依次为字母个数、数字个数和其他字符个数，中间用空格分隔。",
    "fgetc 的返回值必须用 int 型变量接收，才能正确判断 EOF：while ((ch = fgetc(fp)) != EOF)。判断字母用 (ch>='a'&&ch<='z') || (ch>='A'&&ch<='Z')，数字用 ch>='0' && ch<='9'。",
    """#include <stdio.h>

int main()
{
    FILE *fp;
    int ch;
    int letters = 0, digits = 0, others = 0;
    char s[300];
    scanf("%s", s);
    fp = fopen("f111.txt", "w");
    fprintf(fp, "%s", s);
    fclose(fp);
    fp = fopen("f111.txt", "r");
    while ((ch = fgetc(fp)) != EOF)
    {
        if ((ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'))
            letters++;
        else if (ch >= '0' && ch <= '9')
            digits++;
        else
            others++;
    }
    fclose(fp);
    remove("f111.txt");
    printf("%d %d %d\\n", letters, digits, others);
    return 0;
}""",
    ["abc123", "a1B2c3!", "hello", "2024", "Ab!2"])

add(10, "10-p12", "读到文件末尾求平均值", "hard", ["易错"], ["文件", "fscanf", "EOF"],
    "输入 n 个整数，把它们写入文件 f112.txt；再打开文件，用 fscanf 反复读数直到文件结束，求出这些数的平均值（保留 2 位小数）。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数。",
    "输出一行，为文件中所有整数的平均值，保留 2 位小数。",
    "判断读到末尾要写 while (fscanf(fp, \"%d\", &x) == 1)，表示成功读到一个整数；写成 != EOF 时，读失败会重复处理，容易多算或死循环。平均值要用 (double)s / c 计算。",
    """#include <stdio.h>

int main()
{
    FILE *fp;
    int n, i, x, s = 0, c = 0;
    scanf("%d", &n);
    fp = fopen("f112.txt", "w");
    for (i = 0; i < n; i++)
    {
        scanf("%d", &x);
        fprintf(fp, "%d ", x);
    }
    fclose(fp);
    fp = fopen("f112.txt", "r");
    while (fscanf(fp, "%d", &x) == 1)
    {
        s = s + x;
        c++;
    }
    fclose(fp);
    remove("f112.txt");
    printf("%.2f\\n", (double)s / c);
    return 0;
}""",
    ["5\n1 2 3 4 5", "3\n2 4 6", "4\n-1 0 1 2", "1\n10", "6\n1 2 3 4 5 6"])

add(10, "10-p13", "读出文件数据排序后写回并输出", "hard", ["难题"], ["文件", "排序", "读写"],
    "输入 n 个整数写入文件 f113.txt，再从文件中读出这 n 个数，用冒泡排序按从小到大排好，把排序结果重新写回同一个文件，最后读出文件内容逐行输出。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数。",
    "输出 n 行，每行一个整数，为排序后文件中的内容。",
    "写文件后必须 fclose 才能保证数据真正落盘；重写同一个文件时要用 \"w\" 模式重新打开（会自动清空）。排序在数组里做，排好后再统一写回，不要边读边写。",
    """#include <stdio.h>

int main()
{
    FILE *fp;
    int n, i, j, t, x, a[100];
    scanf("%d", &n);
    fp = fopen("f113.txt", "w");
    for (i = 0; i < n; i++)
    {
        scanf("%d", &a[i]);
        fprintf(fp, "%d\\n", a[i]);
    }
    fclose(fp);
    fp = fopen("f113.txt", "r");
    for (i = 0; i < n; i++)
        fscanf(fp, "%d", &a[i]);
    fclose(fp);
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1])
            {
                t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
            }
    fp = fopen("f113.txt", "w");
    for (i = 0; i < n; i++)
        fprintf(fp, "%d\\n", a[i]);
    fclose(fp);
    fp = fopen("f113.txt", "r");
    while (fscanf(fp, "%d", &x) == 1)
        printf("%d\\n", x);
    fclose(fp);
    remove("f113.txt");
    return 0;
}""",
    ["5\n5 3 1 4 2", "3\n9 8 7", "1\n5", "6\n2 2 1 3 3 0", "4\n-1 -5 0 3"])

add(10, "10-p14", "把文件中的负数全部改成 0", "hard", ["难题", "常考"], ["文件", "读入修改", "重写"],
    "输入 n 个整数写入文件 f114.txt，然后把文件中所有的负数都改成 0，再读出文件内容逐行输出。",
    "第一行一个正整数 n（1 ≤ n ≤ 100）；第二行 n 个整数。",
    "输出 n 行，每行一个整数，为修改后文件中的内容。",
    "思路是“读出来—改—写回去”：先用 \"w\" 写原始数据并关闭，再用 \"r\" 读进数组，把小于 0 的元素置 0，然后用 \"w\" 模式重新打开同一个文件整体重写（\"w\" 会清空原内容），最后读回输出。",
    """#include <stdio.h>

int main()
{
    FILE *fp;
    int n, i, x, a[100];
    scanf("%d", &n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);
    fp = fopen("f114.txt", "w");
    for (i = 0; i < n; i++)
        fprintf(fp, "%d ", a[i]);
    fclose(fp);
    fp = fopen("f114.txt", "r");
    for (i = 0; i < n; i++)
        fscanf(fp, "%d", &a[i]);
    fclose(fp);
    for (i = 0; i < n; i++)
        if (a[i] < 0)
            a[i] = 0;
    fp = fopen("f114.txt", "w");
    for (i = 0; i < n; i++)
        fprintf(fp, "%d ", a[i]);
    fclose(fp);
    fp = fopen("f114.txt", "r");
    while (fscanf(fp, "%d", &x) == 1)
        printf("%d\\n", x);
    fclose(fp);
    remove("f114.txt");
    return 0;
}""",
    ["5\n-1 2 -3 4 -5", "3\n1 2 3", "4\n-5 -6 -7 -8", "1\n-100", "6\n0 -1 0 -2 3 -4"])


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
        print("[OK] %-7s %s  %s" % (q["id"], q["title"], "/".join(q["tag"])))
        print("     样例输出: %r" % tests[0]["out"][:70])
    for ch, items in by_ch.items():
        path = os.path.join(DATA, "ch%02d.json" % ch)
        d = json.load(open(path, encoding="utf-8"))
        keep = [c for c in d["coding"] if c["id"] not in {i["id"] for i in items}]
        d["coding"] = keep + items
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        total_tag = sum(1 for c in d["coding"] if c.get("tag"))
        print("ch%02d: 编程题 %d 道，其中带标注 %d 道" % (ch, len(d["coding"]), total_tag))


if __name__ == "__main__":
    main()

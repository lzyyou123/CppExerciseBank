# -*- coding: utf-8 -*-
"""给 10 章统一追加"读代码写结果"型经典选择题，每题用 g++ 实跑验证。
第 3 章（顺序结构）严格不使用分支与循环。
"""
import io, os, json, re, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data3")
WORK = os.path.join(BASE, ".verify")
os.makedirs(WORK, exist_ok=True)

NEW = {
"1": [
 dict(level="easy", q="以下程序的输出结果是？",
      code='printf("Hello");\nprintf(" World");\nprintf("\\n");',
      options=["Hello World", "HelloWorld", "Hello\\nWorld", "WorldHello"], answer=0,
      explain="三个 printf 是三条独立输出语句，前面没有换行符，内容会接在同一行拼成 Hello World；最后一个 printf 只输出换行，不显示 \\n 两个字符本身。"),
 dict(level="easy", q="以下程序的输出结果是？",
      code='printf("A");\n/* printf("B"); */\nprintf("C");',
      options=["AC", "ABC", "A", "C"], answer=0,
      explain="/* ... */ 内的内容整段是注释，编译时被忽略，其中的 printf 不会执行，因此只输出 A 和 C。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='printf("%d%%", 90);',
      options=["90%", "90%%", "90", "%90"], answer=0,
      explain="格式串中 %% 是输出一个百分号字符的转义写法，%d 输出 90，所以屏幕上显示 90%。若写成 %d% 则会输出不确定字符。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='printf("%d", 5 + 3 * 2 - 4 / 2);',
      options=["9", "11", "7", "12"], answer=0,
      explain="先乘除后加减：3*2=6、4/2=2（整数除法），再 5+6-2=9。C 语言中 / 两侧都是整数时做整除，结果舍去小数。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='int n;\nn = printf("12345");\nprintf("%d", n);',
      options=["123455", "512345", "12345", "6"], answer=0,
      explain="printf 是有返回值的函数，返回值是实际输出的字符个数。先输出 12345（5 个字符），n 得 5，再输出 5，屏幕上是 123455。"),
],
"2": [
 dict(level="easy", q="以下程序的输出结果是？",
      code='int a = 5;\nprintf("%d", a / 2 * 2);',
      options=["4", "5", "5.0", "2"], answer=0,
      explain="a/2 是两个 int 相除，结果取整为 2，再乘 2 得 4，小数部分已经丢掉，不会恢复成 5。若要得到 5 需写 (double)a/2*2。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='printf("%d %d", -7 % 3, 7 % -3);',
      options=["-1 1", "1 -1", "-1 -1", "1 1"], answer=0,
      explain="C 语言求余的结果符号与被除数相同：-7%3 中 -7 是被除数，结果为 -1；7%-3 中被除数是 7，结果为 1。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='char c = \'a\';\nprintf("%c,%d", c, c);',
      options=["a,97", "97,97", "a,a", "97,a"], answer=0,
      explain="char 变量存放的是字符的 ASCII 码。%c 按字符形式输出 a，%d 按整数形式输出它对应的 ASCII 码 97。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int i = 5;\nint a = i++;\nint b = i;\nprintf("%d,%d", a, b);',
      options=["5,6", "6,6", "6,5", "5,5"], answer=0,
      explain="i++ 是后置自增：先把 i 的当前值 5 赋给 a，i 再变 6，所以 a=5、b=6。若写 ++i 则 a、b 都是 6。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='printf("%d %d", (int)sizeof(int), (int)sizeof(char));',
      options=["4 1", "2 1", "4 2", "8 1"], answer=0,
      explain="sizeof 求类型所占字节数，常见 32/64 位编译器下 int 占 4 字节、char 占 1 字节。sizeof 的结果是无符号整型，输出时加上 (int) 强制转换更规范。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='double d = 3.99;\nint n = d;\nprintf("%d %d", n, (int)(d + 0.5));',
      options=["3 4", "4 4", "3 3", "4 3"], answer=0,
      explain="浮点数赋给整型变量只取整数部分，不四舍五入，故 n=3；d+0.5=4.49，再强制转换为 int 得 4。这就是用「加 0.5 再取整」实现四舍五入的经典写法。"),
],
"3": [
 dict(level="mid", q="以下程序的输出结果是？",
      code='int a = 7, b = 2;\nprintf("%d %d %.1f", a / b, a % b, (double)a / b);',
      options=["3 1 3.5", "3.5 1 3.5", "3 1 3.0", "3.5 0.5 3.5"], answer=0,
      explain="a/b 是整数除法得 3；a%b 求余得 1；(double)a/b 先把 a 转成浮点数再除，得 3.5。对比可见整除与浮点除的区别。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int n = 1234;\nprintf("%d%d", n / 100 % 10, n % 100 / 10);',
      options=["23", "32", "12", "34"], answer=0,
      explain="拆位经典方法：n/100%10 先得 12 再对 10 取余得百位 2；n%100/10 先得 34 再整除 10 得十位 3。依次输出 2 和 3。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int x = 3, y = 3;\nint a = x++;\nint b = ++y;\nprintf("%d,%d,%d,%d", a, b, x, y);',
      options=["3,4,4,4", "4,4,4,4", "3,3,4,4", "4,3,3,3"], answer=0,
      explain="x++ 先用后加：a 得 3，x 变 4；++y 先加后用：y 变 4，b 得 4。因此输出 3,4,4,4。"),
 dict(level="hard", q="程序运行时从键盘输入 1234567 后，输出结果是？（scanf 中的宽度修饰符表示最多读入几位）",
      code='int x = 0, y = 0;\nscanf("%2d%3d", &x, &y);\nprintf("%d,%d", x, y);',
      options=["12,345", "12,34", "123,456", "1234567,0"], answer=0,
      explain="%2d 表示最多读 2 位数字，取 12；接着 %3d 从剩下的 34567 中最多读 3 位，取 345；后面的 67 留在输入缓冲区。故输出 12,345。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int x = 65;\nprintf("%c%c", x, x + 1);',
      options=["AB", "65 66", "BA", "A65"], answer=0,
      explain="%c 按字符输出整数对应的 ASCII 码：65 是 'A'，x+1=66 是 'B'。所以输出 AB。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='int n = 0;\nn = printf("ab");\nprintf(",%d", n);',
      options=["ab,2", "ab,0", ",2ab", "2,ab"], answer=0,
      explain="先执行 printf(\"ab\")，屏幕输出 ab，函数返回输出字符数 2 赋给 n；再输出 \",2\"。整体为 ab,2。"),
],
"4": [
 dict(level="easy", q="以下程序的输出结果是？",
      code='int a = 5, b = 3;\nif (a > b)\n    if (a > 0) printf("A");\n    else printf("B");',
      options=["A", "B", "AB", "无输出"], answer=0,
      explain="else 与最近的 if 配对，即与 if (a > 0) 配对。a>b 成立进入内层，a>0 也成立，输出 A，else 分支不执行。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int x = 2, s = 0;\nswitch (x)\n{\ncase 1: s = s + 1;\ncase 2: s = s + 2;\ncase 3: s = s + 3; break;\ndefault: s = 100;\n}\nprintf("%d", s);',
      options=["5", "2", "3", "100"], answer=0,
      explain="switch 从匹配的 case 2 处开始，但没有 break，会继续向下贯穿执行 case 3：s 先得 2，再得 5，遇到 break 结束。这就是「case 贯穿」。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int i = 0;\nif (i++ && i++)\n    printf("T%d", i);\nelse\n    printf("F%d", i);',
      options=["F1", "T1", "F2", "T2"], answer=0,
      explain="i++ 是后置自增，表达式值为 0（假），&& 发生短路，右边第二个 i++ 不再执行；只有第一个 i++ 让 i 变成 1，走 else 输出 F1。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int a = 3, b = 4, c = 5;\nprintf("%d", a > b ? a : b > c ? b : c);',
      options=["5", "4", "3", "1"], answer=0,
      explain="条件运算符从右向左结合：先算 b>c?b:c，4>5 不成立取 c=5；再算 a>b?3:5，3>4 不成立取 5。故输出 5。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='int x = 3;\nprintf("%d %d", 1 < x < 5, 5 < x < 1);',
      options=["1 1", "1 0", "0 1", "0 0"], answer=0,
      explain="关系运算符从左向右结合：1<x 得 1，再算 1<5 得 1；5<x 得 0，再算 0<1 得 1。两个结果都是 1。判断区间不能写成 1<x<5 这种连续形式。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='char ch = \'B\';\nswitch (ch)\n{\ncase \'A\': printf("90+"); break;\ncase \'B\':\ncase \'C\': printf("60-89"); break;\ndefault: printf("fail");\n}',
      options=["60-89", "90+", "60-8990+", "fail"], answer=0,
      explain="ch='B' 匹配 case 'B'，该 case 后没有语句，直接贯穿到 case 'C' 执行 printf(\"60-89\")，然后 break 结束。多个 case 共用一段代码是常见写法。"),
],
"5": [
 dict(level="mid", q="以下程序的输出结果是？",
      code='int i = 0, s = 0;\nwhile (i++ < 3)\n    s = s + i;\nprintf("%d,%d", s, i);',
      options=["6,4", "6,3", "3,4", "3,3"], answer=0,
      explain="判断表达式为 i++：先用 i 的旧值比较再自增。i=0<3 成立、i 变 1，s=1；i=1<3 成立、i=2，s=3；i=2<3 成立、i=3，s=6；i=3<3 不成立但 i 已自增为 4，退出。输出 6,4。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int n = 12345, c = 0;\nwhile (n > 0)\n{\n    c++;\n    n = n / 10;\n}\nprintf("%d", c);',
      options=["5", "4", "6", "12345"], answer=0,
      explain="每循环一次 n 去掉最低位：12345→1234→123→12→1→0，共循环 5 次，c 得 5。这是「逐位剥离」求整数位数的经典写法。"),
],
"6": [
 dict(level="mid", q="以下程序的输出结果是？",
      pre='void swap(int a, int b)\n{\n    int t = a;\n    a = b;\n    b = t;\n}',
      code='int x = 3, y = 8;\nswap(x, y);\nprintf("%d,%d", x, y);',
      options=["3,8", "8,3", "8,8", "3,3"], answer=0,
      explain="函数参数是值传递：形参 a、b 只是实参的副本，函数内交换的只是副本，x、y 不受影响，输出 3,8。要交换实参必须传地址（指针）。"),
 dict(level="mid", q="以下程序的输出结果是？",
      pre='int f(int n)\n{\n    if (n <= 1) return 1;\n    return n * f(n - 1);\n}',
      code='printf("%d", f(4));',
      options=["24", "12", "6", "4"], answer=0,
      explain="f(4)=4*f(3)=4*3*f(2)=4*3*2*f(1)=4*3*2*1=24，即 4 的阶乘。"),
 dict(level="hard", q="以下程序的输出结果是？",
      pre='int f()\n{\n    static int s = 0;\n    s = s + 1;\n    return s;\n}',
      code='int a, b, c;\na = f();\nb = f();\nc = f();\nprintf("%d%d%d", a, b, c);',
      options=["123", "111", "321", "333"], answer=0,
      explain="static 局部变量只在第一次调用时初始化为 0，之后保持上次的值，调用三次依次返回 1、2、3。若去掉 static 则每次都输出 1。"),
 dict(level="hard", q="以下程序的输出结果是？",
      pre='void add(int a[], int n)\n{\n    a[0] = a[0] + 100;\n}',
      code='int x[3] = {1, 2, 3};\nadd(x, 3);\nprintf("%d", x[0]);',
      options=["101", "1", "100", "3"], answer=0,
      explain="数组名作实参传的是首地址，形参 a 与实参 x 指向同一段内存，函数内修改 a[0] 就是修改 x[0]，故输出 101。数组传参不复制整个数组。"),
 dict(level="hard", q="以下程序的输出结果是？",
      pre='int x = 10;\nvoid f()\n{\n    int x = 20;\n    printf("%d,", x);\n}',
      code='f();\nprintf("%d", x);',
      options=["20,10", "10,10", "10,20", "20,20"], answer=0,
      explain="局部变量优先：函数 f 内定义的局部 x 屏蔽同名的全局 x，函数内输出 20；函数返回后 main 中的 x 仍是全局变量的 10，输出 20,10。"),
],
"7": [
 dict(level="mid", q="以下程序执行的是冒泡排序的一趟扫描，输出结果是？",
      code='int a[5] = {5, 3, 8, 1, 9};\nint i, t;\nfor (i = 0; i < 4; i++)\n    if (a[i] > a[i + 1])\n    {\n        t = a[i];\n        a[i] = a[i + 1];\n        a[i + 1] = t;\n    }\nfor (i = 0; i < 5; i++)\n    printf("%d", a[i]);',
      options=["35189", "35819", "13589", "53819"], answer=0,
      explain="一趟冒泡只把最大数送到末尾：5>3 交换得 3,5,8,1,9；5>8 不换；8>1 交换得 3,5,1,8,9；8>9 不换。最终 35189。要完全有序需多趟。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int a[2][3] = {{1, 2, 3}, {4, 5, 6}};\nint i, j, s = 0;\nfor (i = 0; i < 2; i++)\n    for (j = 0; j < 3; j++)\n        s = s + a[i][j];\nprintf("%d", s);',
      options=["21", "15", "6", "12"], answer=0,
      explain="二维数组按行优先遍历全部 6 个元素：1+2+3+4+5+6=21。若内层 j<=3 越界则结果错误，注意下标范围 0~2。"),
 dict(level="hard", q="以下程序的输出结果是？",
      pre='#include <string.h>',
      code='char s[] = "abc";\nprintf("%d %d", (int)strlen(s), (int)sizeof(s));',
      options=["3 4", "4 3", "3 3", "4 4"], answer=0,
      explain="strlen 数到 '\\0' 为止，不计结束标志，得 3；sizeof 求数组占用字节数，包含结尾的 '\\0'，得 4。这是最常考的 strlen 与 sizeof 区别。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int a[4] = {1, 2, 3, 4};\nint i, t;\nfor (i = 0; i < 2; i++)\n{\n    t = a[i];\n    a[i] = a[3 - i];\n    a[3 - i] = t;\n}\nfor (i = 0; i < 4; i++)\n    printf("%d", a[i]);',
      options=["4321", "1234", "4231", "1243"], answer=0,
      explain="只交换前一半与后一半的元素：i=0 交换 a[0]、a[3]，i=1 交换 a[1]、a[2]，结果为 4,3,2,1。循环到一半即停，避免又换回来。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='char s[] = "hello world";\nint i, c = 0;\nfor (i = 0; s[i] != \'\\0\'; i++)\n    if (s[i] == \'l\') c++;\nprintf("%d", c);',
      options=["3", "2", "11", "1"], answer=0,
      explain="逐个字符扫描到字符串结束标志 '\\0'，统计字母 l 的个数：hello 中有 2 个 l，world 中有 1 个，共 3 个。"),
],
"8": [
 dict(level="easy", q="以下程序的输出结果是？",
      code='int a[4] = {10, 20, 30, 40};\nint *p = a;\nprintf("%d,%d", *p, *(p + 2));',
      options=["10,30", "20,30", "10,20", "30,40"], answer=0,
      explain="数组名 a 是首元素地址，p 指向 a[0]。*p 取第 1 个元素 10；p+2 指向 a[2]，解引用得 30。指针加 2 是移动 2 个元素而非 2 个字节。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='int a[3] = {1, 2, 3};\nint *p = a, s = 0, i;\nfor (i = 0; i < 3; i++)\n    s = s + *p++;\nprintf("%d", s);',
      options=["6", "3", "1", "9"], answer=0,
      explain="*p++ 先取 *p 的值参与运算，再让 p 后移一个元素。循环依次累加 1、2、3，s=6。这是用指针遍历数组的标准写法。"),
 dict(level="mid", q="以下程序通过指针交换两个变量的值，输出结果是？",
      pre='void swap(int *a, int *b)\n{\n    int t = *a;\n    *a = *b;\n    *b = t;\n}',
      code='int x = 3, y = 8;\nswap(&x, &y);\nprintf("%d,%d", x, y);',
      options=["8,3", "3,8", "8,8", "3,3"], answer=0,
      explain="实参传的是 x、y 的地址，形参指针指向原变量，*a、*b 的交换就是直接改 x、y 所在内存，所以成功交换，输出 8,3。"),
 dict(level="hard", q="以下程序的输出结果是？",
      code='int a[2][3] = {{1, 2, 3}, {4, 5, 6}};\nint (*p)[3] = a;\nprintf("%d,%d", *(*(p + 1) + 2), *(*(p) + 1));',
      options=["6,2", "2,6", "6,5", "3,2"], answer=0,
      explain="p 是行指针，p+1 指向第 2 行，*(p+1) 化为该行首地址，再 +2 指向第 2 行第 3 个元素，解引用得 6；*(*p+1) 即 a[0][1]=2。注意行指针 p+1 跳过整行 3 个元素。"),
 dict(level="mid", q="以下程序的输出结果是？",
      code='char *s[3] = {"ab", "cd", "ef"};\nprintf("%s%s", s[2], s[0]);',
      options=["efab", "abef", "ef", "abcd"], answer=0,
      explain="s 是指针数组，3 个元素各指向一个字符串常量。s[2] 指向 \"ef\"、s[0] 指向 \"ab\"，用 %s 依次输出即为 efab。"),
],
"9": [
 dict(level="easy", q="以下程序的输出结果是？",
      pre='struct stu\n{\n    int num;\n    char name[10];\n};',
      code='struct stu s = {1001, "Li"};\nprintf("%d,%s", s.num, s.name);',
      options=["1001,Li", "1001,1001", "Li,1001", "编译错误"], answer=0,
      explain="结构体变量用成员运算符 . 访问各成员，s.num 为 1001，s.name 为字符数组 \"Li\"，按 %d、%s 顺序输出 1001,Li。"),
 dict(level="mid", q="以下程序的输出结果是？",
      pre='struct stu\n{\n    int num;\n    char name[10];\n};',
      code='struct stu s = {1002, "Wang"};\nstruct stu *p = &s;\nprintf("%d,%s", p->num, p->name);',
      options=["1002,Wang", "1002,1002", "Wang,1002", "编译错误"], answer=0,
      explain="指针访问成员用 ->，p->num 等价于 (*p).num。p 指向 s，故输出 1002,Wang。注意 -> 只能用于指针，. 只能用于变量。"),
 dict(level="mid", q="以下程序的输出结果是？",
      pre='struct point\n{\n    int x;\n    int y;\n};',
      code='struct point p[3] = {{1, 2}, {3, 4}, {5, 6}};\nint i, s = 0;\nfor (i = 0; i < 3; i++)\n    s = s + p[i].x;\nprintf("%d", s);',
      options=["9", "21", "15", "6"], answer=0,
      explain="结构体数组元素用 p[i].成员 访问。累加各元素 x 成员：1+3+5=9。若累加 y 成员则为 12。"),
 dict(level="hard", q="以下程序的输出结果是？",
      pre='union data\n{\n    int i;\n    char c;\n};',
      code='union data d;\nd.i = 0;\nd.c = \'A\';\nprintf("%d", d.i);',
      options=["65", "0", "1", "16706"], answer=0,
      explain="共用体所有成员共用同一段存储空间，后写 c 会覆盖 i 的第一个字节。'A' 的 ASCII 码是 65，且 i 此前已清 0，故 d.i 读出来是 65。"),
 dict(level="mid", q="以下程序的输出结果是？",
      pre='enum color { red, green = 3, blue };',
      code='printf("%d %d %d", red, green, blue);',
      options=["0 3 4", "0 1 2", "1 2 3", "0 3 3"], answer=0,
      explain="枚举值从 0 开始递增；red 未指定故为 0，green 显式指定为 3，后面的 blue 在 green 基础上加 1 得 4。"),
],
"10": [
 dict(level="mid", q="以下程序执行后输出结果是？",
      code='FILE *fp;\nint n = 0;\nfp = fopen("t10a.txt", "w");\nfprintf(fp, "%d", 123);\nfclose(fp);\nfp = fopen("t10a.txt", "r");\nfscanf(fp, "%d", &n);\nfclose(fp);\nprintf("%d", n + 1);',
      options=["124", "123", "1", "0"], answer=0,
      explain="先用 \"w\" 方式把 123 以文本形式写入文件，关闭后再用 \"r\" 方式读出到 n=123，输出 n+1 即 124。文件使用完必须 fclose，否则缓冲区内容可能未真正写入。"),
 dict(level="mid", q="以下程序执行后输出结果是？",
      code='FILE *fp;\nint c, n = 0;\nfp = fopen("t10b.txt", "w");\nfputs("abcd", fp);\nfclose(fp);\nfp = fopen("t10b.txt", "r");\nwhile ((c = fgetc(fp)) != EOF)\n    n++;\nfclose(fp);\nprintf("%d", n);',
      options=["4", "5", "0", "1"], answer=0,
      explain="fputs 写入 4 个字符 abcd（不含额外内容），逐字符读到文件末尾 EOF 为止，计数 4。EOF 是文件结束标志，不是文件中的字符，故不计入。"),
 dict(level="hard", q="以下程序先后两次以 \"w\" 方式打开同一文件，输出结果是？",
      code='FILE *fp;\nchar s[10] = {0};\nfp = fopen("t10c.txt", "w");\nfputs("AAAA", fp);\nfclose(fp);\nfp = fopen("t10c.txt", "w");\nfputs("B", fp);\nfclose(fp);\nfp = fopen("t10c.txt", "r");\nfscanf(fp, "%s", s);\nfclose(fp);\nprintf("%s", s);',
      options=["B", "AAAAB", "AAAA", "AB"], answer=0,
      explain="\"w\" 方式打开会清空原文件内容再从头写。第二次打开时把 AAAA 抹掉，只写入 B，所以读出 B。若要追加应使用 \"a\" 方式。"),
 dict(level="hard", q="若把上题第二次打开的方式由 \"w\" 改成 \"a\"，同样的代码输出结果是？",
      code='FILE *fp;\nchar s[10] = {0};\nfp = fopen("t10d.txt", "w");\nfputs("AAAA", fp);\nfclose(fp);\nfp = fopen("t10d.txt", "a");\nfputs("B", fp);\nfclose(fp);\nfp = fopen("t10d.txt", "r");\nfscanf(fp, "%s", s);\nfclose(fp);\nprintf("%s", s);',
      options=["AAAAB", "B", "AAAA", "BAAAA"], answer=0,
      explain="\"a\" 为追加方式，保留原内容并把新内容写到文件末尾，故文件内容为 AAAAB。r 只读、w 清空重写、a 末尾追加，是文件打开方式最常考的三种。"),
 dict(level="mid", q="以下程序执行后输出结果是？",
      code='FILE *fp;\nint n = 0;\nchar ch;\nfp = fopen("t10e.txt", "w");\nfprintf(fp, "%s", "12");\nfprintf(fp, "%s", "345");\nfclose(fp);\nfp = fopen("t10e.txt", "r");\nwhile (fscanf(fp, "%c", &ch) != EOF)\n    n++;\nfclose(fp);\nprintf("%d", n);',
      options=["5", "6", "2", "3"], answer=0,
      explain="两次 fprintf 连续向同一文件写入 \"12\" 和 \"345\"，中间没有换行或空格，文件内容就是 12345，共 5 个字符，逐个读入计数得 5。"),
],
}


def run(snippet, pre="", stdin_data=""):
    src = "#include <stdio.h>\n" + (pre + "\n" if pre else "") + "int main(){\n" + snippet + "\nreturn 0;\n}\n"
    c = os.path.join(WORK, "t.c")
    exe = os.path.join(WORK, "t.exe")
    with io.open(c, "w", encoding="utf-8") as f:
        f.write(src)
    cr = subprocess.run(["g++", "-std=c++11", "-x", "c++", c, "-o", exe],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if cr.returncode != 0:
        return None, "编译失败: " + (cr.stderr or "")[:300]
    rr = subprocess.run([exe], input=stdin_data, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=10, cwd=WORK)
    return rr.stdout.strip(), ""


def norm(s):
    return re.sub(r"\s+", "", s or "")


allok = True
for ch, items in NEW.items():
    path = os.path.join(DATA, "ch%02d.json" % int(ch))
    data = json.load(io.open(path, encoding="utf-8"))
    start = len(data["choice"]) + 1
    added = []
    bad = 0
    for k, item in enumerate(items):
        stdin_d = "1234567\n" if "%2d%3d" in item["code"] else ""
        out, err = run(item["code"], item.get("pre", ""), stdin_d)
        if out is None:
            print("[编译失败] 第%s章 %s -> %s" % (ch, item["q"][:18], err))
            bad += 1
            continue
        pick = item["options"][item["answer"]]
        if norm(out) != norm(pick):
            print("[答案不符] 第%s章 实测=%r 选项=%r 代码首行=%r" % (ch, out, pick, item["code"].splitlines()[0]))
            bad += 1
            continue
        it = dict(id="%s-c%d" % (ch, start + len(added)))
        it.update({kk: item[kk] for kk in ("level", "q", "code", "options", "answer", "explain")})
        if item.get("pre"):
            it["pre"] = item["pre"]
        added.append(it)
        print("[OK] %s 实测=%r" % (it["id"], out))
    if bad == 0:
        data["choice"].extend(added)
        with io.open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print("== 第%s章写入完成：%d -> %d 道\n" % (ch, start - 1, len(data["choice"])))
    else:
        allok = False
        print("== 第%s章有 %d 题未通过，本章未写入\n" % (ch, bad))

print("全部通过" if allok else "存在未通过题目，请检查")

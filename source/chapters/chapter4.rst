==========================
第3章 QRunes表达式与运算符
==========================

    

**本章节及后续的第四章来详细叙述下QRunes中的表达式和语句，因为当前的量子编程涉及三个部分：经典计算机模块，测控系统模块和量子芯片模块，故这种混合（量子、经典、经典辅助）程序各自分别运行在其对应的硬件模块上，他们的编译和运行方式也将会不同。**

3.1 表达式
-------------

**在QRunes中，表达式由运算符和操作数组成，主要的作用是：** 

- 计算经典辅助类型操作数的值。
- 指定函数。


**操作数可以是常量或者一个数据对象。比如：** 

- 常量：3.14,1  
- 数据对象：变量？？

3.2 表达式的类型介绍：
--------------------------

3.2.1 主表达式 
*******************************

**它是构造其他表达式的基本块。** 

语法构成：

::

 主表达式：标识符 | 常量 | 括号表达式  
 primary_expression: idetifier | constant |parenthesis_expression  
 例如：qubit_s1,3.1415,(c1 + c2)     
 注：支持量子类型，经典类型，经典辅助类型

3.2.2 括号表达式  
*******************************

语法构成：

::

 parenthesis_expression：（ expression ）  
 它表示在不更改括号封闭的里面的表达式类型或值的情况下来构造表达式的分组方式。  
 例如:  （ 2 + 3 ）/5 与 2 + 3 / 5   
 注：支持量子类型，经典类型，经典辅助类型

3.2.3 后缀表达式与其运算符  
*******************************

**它是后面跟运算符的主表达式。**  

==================       =======      ===========
后缀运算符                  示例         支持类型  
==================       =======      ===========
下标运算符                  [ ]          Q A C
函数调用运算符              （）          Q A C
对象成员访问运算符           .            Q A C
后缀递增运算符               ++           A
后缀递减法运算符             --           A
==================       =======      ===========

3.2.4 一元表达式与其运算符  
*******************************

==========    ================   =======    ===========
一元运算符     含义                 示例       支持类型 
==========    ================   =======    ===========
~              取反运算符                      A
!              逻辑非运算符                    A C
++             一元递增运算符                  A
--             一元递减运算符                  A
==========    ================   =======    ===========


3.2.5 二元表达式与其运算符
*******************************

==============          =============================================================    =======================   =====================    ======================
二元运算符                   含义                                                              示例                         类别                  支持类型 
==============          =============================================================    =======================   =====================    ======================
=                         赋值运算符，将右操作数的值赋给左操作数                                 x = y                     赋值运算符                 A C
+=                                                                                                                      赋值运算符                A C
-=                                                                                                                      赋值运算符                A C
*=                                                                                                                      赋值运算符                A C
/=                                                                                                                      赋值运算符                A C
\+                         两个操作数相加                                                       x + y                     算术运算符                 A C
\-                         第一个操作数减去第二个操作数                                          x - y                     算术运算符                 A C
\*                         两个操作数相乘                                                       x * y                     算术运算符                 A C
\/                         第一个操作数除                                                       x / y|                    算术运算符                 A C
%                         第一个操作数整除第二个操作数之后的余数                                 x % y                     算术运算符                 A
==                        判断两个操作数是否相等,相等则返回真值                                  x == y                    关系运算符                 A C
!=                        判断两个数是否相等，不相等则返回真值                                   x != y                    关系运算符                 A C
>                         判断左操作数是否大于右操作数，大于则返回真值                            x > y                     关系运算                  A C
<                         判断左操作数是否小于右操作数，小于则返回真值                            x < y                     关系运算                  A C
>=                        判断左操作数是否大于等于右操作数，大于等于则返回真值                     x > y                     关系运算符                A C
<=                        判断左操作数是否小于等于右操作数，小于等于则返回真值                     x <= y                    关系运算符                 A C
&&                        如果两个操作数都非零，则返回真值                                       x && y                    逻辑运算符                 A C
\|\|                      如果两个操作数任意一个非零，则返回真值                                  x \|\| y                  逻辑运算                  A C
&                         按位与                                                               x & y                     位运算符                  A
/                         按位或                                                               x \| y                    位运算符                  A
^                         异或运算符                                                           x ^ y                     位运算符                   A
<<                        二进制左移运算符                                                                                移位运算符                A
>>                        二进制右移运算符                                                                                移位运算符                 A
==============          =============================================================    =======================   =====================    ======================
       
3.2.6 三元表达式与运算符 
*******************************


===========   ===================================        ====================       ===============         ===============
三元运算符          含义                                      示例                    类别                      支持类型   
===========   ===================================        ====================       ===============         ===============
？：           根据计算的值结果选择true还是false             a > b ? a : b             三元运算符                A
===========   ===================================        ====================       ===============         ===============

3.2.7 逗号运算符
*******************************

::

 逗号运算符的作用是将几个表达式放在一起，起到分割表达式的作用。  
 注：支持 A Q C

3.2.8 常量表达式  
*******************************

::

 常量表达式是在编译时计算而不是在运行时计算。
 注：支持 A
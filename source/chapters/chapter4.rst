第4章 语句
=====================

- QRunes中语句近似与人类的自然语言，既有完成单一任务的简单语句也有作为一个集合的一组语句组成的复合语句。同时QRunes既能支持辅助类型的条件分支和循环控制结构，也支持经典类型的QIF和QWHILE的量子分支和量子循环控制结构。  
- QRunes中的语句大部分都是以分号；结尾。

4.1 简单语句
------------------
4.1.1 表达式语句
*********************
表达式语句的类型取决于表达式类型，表达式类型参见Chapter 3.2。  

举例如下：

::

 c2 = c1 + 1; //Assign statement

4.1.2 声明语句
*********************
- QRunes中声明语句主要分为两种：函数的声明和变量的定义与。
- 具体可以参见Chapter 2.3 和Chapter 5.2，其中变量的定义支持A Q C类型的变量定义。

举例如下：

::

 qubit q;// declaration a variable with qubit type named q  
 let i = 3.14;// declaration a variable with assist-classical type which named i and intialized 3.14

4.2 复合语句
------------------
- QRunes中复合语句通常按块的概念，表现形式为使用一对花括号{}括起来的语句序列。
- 在复合语句中的一组语句不仅仅是一堆简单语句的组合，同时根据程序的逻辑要求，一个程序逻辑也被称为一条语句块，比如if,for,qif,qwhile。

例如：

::

   if (oracle_function[0] == False && oracle_function[1] == True) {  
        // f(x) = x;  
        CNOT(q1, q2);  
    } else if (oracle_function[0] == True && oracle_function[1] == False) {  
        // f(x) = x + 1;  
        X(q2);  
        CNOT(q1, q2);  
        X(q2);  
    }        

**注意：**
::

 1. 与其他语句不同的是，复合语句不是以分号；结尾。
 2. 只能用在某个函数体中书写。

4.3 函数调用语句
------------------

4.3.1 量子逻辑门操作函数调用语句
******************************************

- 在QRunes中所有对于量子比特的操作，我们称为逻辑门函数或者XX门，比如我们常说的X门，Y门，CNOT门，他们都是类似于QRunes的库文件中实现过其函数实现，预先定义好的，用户可以直接通过调用的形式实现逻辑门的操作。
- 当前QRunes支持18中量子逻辑门函数的操作，其函数声明分别如下：

::

 H(qubit);  
 NOT(qubit);    
 T(qubit);      
 S(qubit);      
 Y(qubit);      
 Z(qubit);      
 X1(qubit);      
 Y1(qubit);      
 Z1(qubit);      
 U4(qubit,alpha,beta,gamma,delta);      
 RX(qubit,alpha);      
 RY(qubit,alpha);      
 RZ(qubit,alpha);      
 CNOT(qubit,qubit);     
 CZ(qubit,qubit);      
 CU(qubit,qubit,alpha,beta,gamma,delta);      
 ISwap(qubit,qubit,alpha);       
 CR(qubit,qubit,alpha);   

4.3.2 可变量子逻辑门函数调用语句
******************************************

可变量子逻辑门是构成可变量子线路VQC的基本单位,可变量子逻辑门函数内部维护着一组变量参数以及一组常量参数。
当前QRunes支持6种可变量子逻辑门函数调用： 

::

 VQG_H(qubit);    
 VQG_RX(qubit,alpha);  
 VQG_RY(qubit,alpha);  
 VQG_RZ(qubit,alpha);  
 VQG_CNOT(qubit,qubit);    
 VQG_CZ(qubit,qubit);

4.3.3 经典返回值类型函数调用语句
******************************************

定义一个函数，但是该函数并不会自动的执行。定义了函数仅仅是赋予函数以名称并明确函数被调用时该做些什么。
调用函数才会以给定的参数真正执行这些动作，比如如下函数：

::

    Reset_Qubit_Circuit(qubit q, cbit c, bool setVal) {  
    Measure(q, c);  
    if (setVal == False) {  
        qif (c) {  
            X(q);  
        }  
    } else {  
        qif (c) {  
        } qelse {  
            X(q);  
        }  
    }   
    }  
    Reset_Qubit(qubit q, cbit c, bool setVal) {     
    // quantum logic gate function call,and can reference to its function definition  
        Reset_Qubit_Circuit(q, c, setVal);  
    }

其中的Reset_Qubit_Circuit函数在Reset_Qubit中的调用，该表示方法就是函数调用。 

**注意：**  

1.函数调用语句必须严格按照函数调用的格式进行书写：  

::

    function_name(args....);  

2.回调函数中的参数必须严格匹配原函数定义中的参数的类型、个数。  

3.函数调用语句只能在调用函数体内书写。

4.4 辅助类型控制语句
---------------------

4.4.1选择语句
*********************

QRunes中的选择语句主要是if-else格式的语句，其计算流程为根据if中表达式的是否有条件地执行分支语句，其中else分支可以是可选项。

语法结构如下：

::

    if(condition)
        statement;
    else
        statement;

举例如下：

::

    if (fx) {  
        X(q[0]);  
    }else{
        H(q[0]);
        X(q[1]);
    }  
    
其中if中的condition必须是一个返回值为bool类型的表达式或者可以转换为bool类型的表达式，此外statement部分可以是用花括号括起来的复合语句。

4.4.2 循环语句
*********************

QRunes中的循环语语句主要是for循环语句，其语法格式如下：

::

    for(initializer:condition:expression)  
        statement

其中initializer、condition和expression都是以冒号结束，initializer用于循环结构的变量初始化;condition(循环条件)则是用来控制循坏的，当判断条件为true的时候则执行statement;expression用来修改initializer的值。特殊情况如下，当循环结构第一次在求解condition的时候就返回false，则该循环体将始终不会执行。通常，循环体中的statement可以是单个语句也可以是复合语句。

举例如下：

::

    for(let i=0: 1: qlist.size()){
        VQG_RX(qlist[i],2.0*beta);
    }

展示的程序用将以qubit为类型的集合qlist中的每个qubit进行可变量子线路构造的操作。

4.5 量子类型控制语句
-------------------------

4.5.1 QIF语句
*********************
QIF的结构如下：

::

    qif(condition)
        statement
    qelse
        statment

与4.4.1中的if相比较，二者的差别在condition和statement中，QIF语句中的condition必须是是经典类型且返回值为bool类型的表达式,statement只能为返回值为经典类型的语句、量子逻辑门操作函数调用语句、返回值为量子类型（QProg,QCircuit）的函数调用、量子比特测量语句和QIF/QWHILE语句。

举例如下：

::

    qif(!c1){  
        Measure(q[2],c[2]);  
    }  
    qelse{  
        Measure(q[1],c[1]);  
    }  

4.5.2 QWHILE语句
*********************

QWHIE的结构如下： 

::

    qwhile(condition)  
        statement

与4.4.2中的for相比较，二者的差别在condition和statement中，QWHILE语句中的condition必须是是经典类型且返回值为bool类型的表达式,statement只能为返回值为经典类型的语句、量子逻辑门操作函数调用语句、返回值为量子类型（QProg,QCircuit）的函数调用、量子比特测量语句和QIF/QWHILE语句。  

举例如下：

::

 qwhile(c[0] < 3){ //c is declarated by type cbit  
    H(qvec[c[0]]);  
    let i = 1; //the value of declaration statement is assist-classical.EEROR!  
    c[0] = c[i] + 1; //ERROR?  
    c[0] = c[0] + 1;  
 } 

4.6 量子比特测量语句
---------------------------

量子测量是指通过量子计算机的测控系统对量子系统进行干扰来获取需要的信息，测量比特使用的是蒙特卡洛方法的测量。
QRunes中的量子比特测量语句的结构如下：

::

 Measure(qubitType,cbitType);

举例如下：

::

 H(q);  
 Measure(q,c);

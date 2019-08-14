第5章 函数
==============

在QRunes中，函数可以被看作是由开发人员自己定义的为了完成某个功能任务的一组语句的集合，每个QRunes程序都会至多有一个入口函数，在QRunes中入口函数即main函数都是在第三方经典语言中来进行实现。

5.1 函数的声明
-------------------
函数声明和变量的定义和声明一样，必须是声明之后才可以使用。函数的声明很函数的定义可以分离开来，同时一个函数只能定义一次，但是可以声明多次。

函数声明的结构如下：

::

 return_type? function_name(args);

举例如下：

::

 circuit createCircuit(qubit qu);

返回值，函数名和函数形参列表称为函数原型。函数的声明为定义函数的使用者和调用函数的使用者之间提供了一种天然的接口。

5.2 函数的定义
-------------------
QRunes中，函数是由返回值，函数名，函数参数和一组语句组成。其中函数名在同一个.qrunes文件中必须唯一；函数参数即函数的形式参数，它们由一对圆括号包围并在其中进行声明，形参之间的以逗号进行分割；一组语句即函数的函数体是函数的执行部分。每一个函数都有一个相关联的返回类型。

函数定义的格式如下：

::

    return_type? function_name(args){  
        // function_body  
    }

举例如下：

::

    Two_Qubit_DJ_Algorithm_Circuit(qubit q1, qubit q2, cbit c, vector<bool> oracle_function) {  
        H(q1);  
        measure(q1, c);  
    }
    
5.3 函数的参数
-------------------

- QRunes中函数不能省略或者为空，函数的形参表由一系列的由逗号分隔符分离的参数类型和参数名组成，如果两个形参的类型相同，则其类型必须重复声明。
- 在QRunes中所有的函数参数都必须命名之后才可以使用。
- 形参和实参：类似于局部变量，函数的形参为函数提供了已命名的局部存储空间。他们之间的差别在于形参是在函数的形参表中定义的，并由调用函数时传递给函数的实参初始化。

5.4 函数的返回值
-------------------

QRunes中函数的返回类型可以是内置类型、复合类型也可以是void类型。其中，

- **内置类型**

::

 qprog  
 circuit  
 variationalCircuit 
 int 
 double
 bool  
 cbit 

下面给出一个返回值为qprog 的函数供读者参考：
::

    BV_QProg(vector<qubit> qVec, vector<cbit> cVec, vector<bool> a, circuit<vector<qubit>,qubit> oracle){

    if(qVec.length() != (a.length()+1)){

    }

    let cd = qVec.length();

    X(qVec[cd-1]);
    apply_QGate(qVec, H);
    oracle(qVec, qVec[cd - 1]);

    qVec.pop();

    apply_QGate(qVec, H);
    measure_all(qVec, cVec);
}



- **复合类型**

复合类型即由vector关键字构造的类型集合，其中的vector集合中的类型为经典类型。
  
比如：

::

    vector<cbit>

下面给出一个例子工读者参考：
::
  
  circuit<vector<qubit>,qubit> generate_3_qubit_oracle(int target){
    return lambda (vector<qubit> qvec,qubit qu):{
        if(target == 0){
            X(qvec[0]);
            X(qvec[1]);
            Toffoli(qvec[0], qvec[1], qu);
            X(qvec[0]);
            X(qvec[1]);
        }
        if(target == 1){
            X(qvec[0]);
            Toffoli(qvec[0], qvec[1], qu);
            X(qvec[0]);
        }
        if(target == 2){
            X(qvec[1]);
            Toffoli(qvec[0], qvec[1], qu);
            X(qvec[1]);
        }
        if(target == 3){
            Toffoli(qvec[0], qvec[1], qu);
        }
    };
}


- **void 类型**

不带返回值的return语句只能用于返回类型为void的函数。在返回类型为void的函数中，return返回语句不是必需的。下面给出一个C++的例子：

::


void swap(int& a, int&b)

{

    if(a == b)

    {
        return;
    }
    int temp;
    temp = a;
    a = b;
    b = temp;
}

- **函数回调类型**

callback_type是回调函数类型，由 返回类型<参数> 组成。

比如：

::

    circuit<vector<qubit> >

注：最右边的两个尖括号（> >）在中间应该要加一个空格。如果空格不存在，则在编译时会存在错误。

根据函数的返回值可以将QRunes中的函数分为两个部分：量子函数和经典函数。
其中的返回值为经典类型、经典类型构造的集合类型和void类型为经典函数，其余为量子函数。

函数的定义举例如下：

::

    //quantum function  
    qu_function(vector<qubit> qvec, vector<cbit> cvec){
        for(let i = 0: 1: len(qvec)){
            H(qvec[i]);
            Measure(qvec[i], cvec[i]);
        }
        vector<cbit> cc = getCbitNotEqualZero(cvec);
        for(let c in cc){
            c = c + 1;
        }
    }

::

    //classical function  
    vector<cbit> getCbitNotEqualZero(vector<cbit> cvec){  
        vector<cbit> c2;
        for(let c in cevc){
            if(c == 1){
                c = c + 1;
                c2.insert(c);
            }
        }  
        return c2;
    }

::

    //return value is null
    void rotateOperation(vector<qubit> qlist){
        for(let qu in qlist){
            H(qlist[i]);
        }
    }

5.5 函数调用
-------------------
函数调用的结构：

::

    function_name(args...);

其中的实参可以是常量，变量，多个实参之间用逗号进行分割。

函数调用的方式：

- 函数调用作为表达式中的一项，常用于赋值表达式，也可称为函数调用表达式

举例：

::

 c = getCbit(cbit c);

- 函数作为单独的语句，及函数调用语句

举例：

::

 ker(qlist,clist);

- 函数也可以作为另一个函数的实参


6.6 Simon算法
================

6.6.1 Simon算法介绍
----------------------

西蒙算法便是适用于量子计算机算法中的一种,它由丹尼尔·西蒙20年前提出,认为这种算法能够挖掘量子计算机的加速潜力。西蒙算法的目的,是为了解决量子黑箱问题,即将执行计算任务的一段程序或者一个公式看作黑箱,看黑箱是否对每一个可能的输入给出一个唯一的输出。

6.6.2 Simon算法的实现
----------------------

下面给出 QRunes 实现 Simon 算法的代码示例：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    QCircuit controlfunc(qvec q, int index, int value) {
        let length = q.size() / 2;
        qvec qvtemp;
        qvtemp.insert(q, 0, length);
        if (index == 1) {
            X(q[0]);
        } else if (index == 2) {
            X(q[1]);
        } else if (index == 0) {
            X(q[0]);
            X(q[1]);
        }
        
        if (value == 1) {
            X(q[3]).control(qvtemp);
        } else if (value == 2) {
            X(q[2]).control(qvtemp);
        } else if (value == 3) {
            X(q[2]).control(qvtemp);
            X(q[3]).control(qvtemp);
        }
    
        if (index == 1) {
            X(q[0]);
        } else if (index == 2) {
            X(q[1]);
        } else if (index == 0) {
            X(q[0]);
            X(q[1]);
        }
    }
    
    //f(x),x is 2bits variable
    QCircuit oraclefunc(qvec q, ivec funvalue) {
        let length = q.size()/2;
        for (let i=0: 1: 4){
            let value = funvalue[i];
            controlfunc(q, i, value);
        }
    }
    
    Simon_QProg(qvec q, cvec c, ivec funvalue) {
        let length = c.size();
        for (let i=0: 1: length) {
            H(q[i]);
        }
        oraclefunc(q, funvalue);
        for (let i=0: 1: length) {
            H(q[i]);
        }
        for (let i=0: 1: length) {
            Measure(q[i], c[i]);
        }
    }
    
    @script:
    if __name__ == '__main__':
        print('4-qubit Simon Algorithm')
        print('f(x)=f(y)\t x+y=s')
        print('input f(x),f(x):[0,3]')
        func_value = []
        func_value.append(int(input('input f(0):\n')))
        func_value.append(int(input('input f(1):\n')))
        func_value.append(int(input('input f(2):\n')))
        func_value.append(int(input('input f(3):\n')))
        print('f(0)=%d' %(func_value[0]))
        print('f(1)=%d' %(func_value[1]))
        print('f(2)=%d' %(func_value[2]))
        print('f(3)=%d' %(func_value[3]))
        print('Programming the circuit...')
    
        init(QMachineType.CPU_SINGLE_THREAD)
        qubit_num = 4
        cbit_num = 2
        qv = qAlloc_many(qubit_num)
        cv = cAlloc_many(cbit_num)
        simonAlgorithm = Simon_QProg(qv, cv, func_value)
    
        result = []
        for i in range(0, 20, 1):
            re = directly_run(simonAlgorithm)
            result.append(cv[0].eval()*2 + cv[1].eval())
        if 3 in result:
            if 2 in result:
                print('s=00')
            else:
                print('s=11')
        elif 2 in result:
            print('s=01')
        elif 1 in result:
            print('s=10')
        
        finalize()

6.6.3 Simon算法小结
----------------------
    
在一台量子计算机上运行了该算法的最简单版本,仅仅用了六个量子比特,量子计算机完成 这一任务仅用了两次迭代,而普通计算机得用三次。这种区别似乎不算什么,但人们相信,如果增加更多量子比特,量子计算机和普通计算机运算能力的差别就会拉 大,这也意味着,量子计算机能更快、更高效地解决此类算法问题。不过,还是要泼一盆冷水,到目前为止,能够运行西蒙算法并没有什么实际价值,该实验的唯一 目的是证明量子计算机在一种算法上能够做得更好。
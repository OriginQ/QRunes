7.2 D_J算法 
===============

7.2.1 D_J算法介绍  
-------------------

D-J算法是一种经过设计的情况，它证明了量子算法相对于经典算法有指数级别的加速能力。D-J算法的问题描述是这样的：
    
如果你具有一个黑盒子，黑盒子里面是一些逻辑门，这个黑盒子可以接受n位的输入，并且产生一个1位的输出。并且我们已知黑盒子有两种可能性：
    
1、对于所有的输入，它只输出0或者1——我们称之为“常数”；

2、恰好对于一半的输入，输出为0，另一半输入，输出为1——我们称之为“平衡”。问题是：对于一个随机的盒子，要区分盒子到底是“平衡”的还是“常数”的。注意，我们不考虑这两种情况之外的输出分布情况，例如对于一个2位输入的黑盒子，输入00输出0，而输入01,10,11都输出1，此时它既不属于“平衡”也不属于“常数”，故被排除到了讨论之外。
    
如果在经典计算的角度上去看，我们要一个一个地检查输出的情况。因为输入是n位的，所以一共具有 2n 种情况（每位上都是0/1两种可能）。不需要检查所有的情况来验证它到底是哪一种盒子，但是最坏的情况下，你检查了一半的情况（ 2n−1 ），得到了一样的结果，例如全为0。这时，你需要再检查一种情况，如果它是0，那么一定是“常数”的；如果它是1，那么一定是“平衡”的。   

其中Target_Function就是这个黑盒子，而bitNum代表输入比特个数。    
然而，量子计算机只需要通过一步运算就可以得到结果。

7.2.2 D_J算法的实现 
-----------------------

下面贴出使用 qurator 插件编写的 QRunes 代码：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    Two_Qubit_DJ_Algorithm_Circuit(qubit q1, qubit q2, cbit c, bvec oracle_function) {
        H(q1);
        H(q2);
        // Perform Hadamard gate on all qubits
        if (oracle_function[0] == False && oracle_function[1] == True) {
            // f(x) = x;
            CNOT(q1, q2);
        } else if (oracle_function[0] == True && oracle_function[1] == False) {
            // f(x) = x + 1;
            X(q2);
            CNOT(q1, q2);
            X(q2);
        } else if (oracle_function[0] == True && oracle_function[1] == True) {
            // f(x) = 1
            X(q2);
        } else {
            // f(x) = 0, do nothing  
        }
        // Finally, Hadamard the first qubit and measure it
        H(q1);
        Measure(q1, c);
    }
    
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
        Reset_Qubit_Circuit(q, c, setVal);
    }
        
    @script:
    import sys
    def DJ_Algorithm(qv, c):
        if len(qv) != 2:
            print('error: qvec size error，the size of qvec must be 2')
            sys.exit(1)
        print('input the input function')
        print('The function has a boolean input')
        print('and has a boolean output')
        fx0 = int(input('f(0)= (0/1)?\n'))
        fx1 = int(input('f(1)= (0/1)?\n'))
        oracle_function = [fx0, fx1]
        print('Programming the circuit... ')
        cbit = cAlloc()
        Reset_Qubit(qv[0], cbit, False)
        Reset_Qubit(qv[1], cbit, True)
        prog = Two_Qubit_DJ_Algorithm_Circuit(qv[0], qv[1], c, oracle_function)
        return prog
    
    if __name__ == '__main__':
        init(QMachineType.CPU_SINGLE_THREAD)
        
        qubit_num = 2
        qv = qAlloc_many(qubit_num)
        c = cAlloc()
        prog = DJ_Algorithm(qv, c)
        result = directly_run(prog)
        if result["c0"] == False:
            print('Constant function!')
        elif result["c0"] == True:
            print('Balanced function!')
    
        finalize()

7.2.3 D_J算法小结
---------------------

经典算法的验证次数是 O(2^n) 的，量子算法算上叠加态的准备和测量的时间，需要的操作步骤为 O(n)。所以我们说明量子算法相对于经典算法具有指数级别加速的特性。
D-J算法的问题在于它解决的问题既不实用，又具有很大的限制（要求平衡函数中必须恰好为一半0一半1）。另外，我们还对黑盒子本身的形态有要求。所以说D-J算法的理论意义是远大于其实用意义的。

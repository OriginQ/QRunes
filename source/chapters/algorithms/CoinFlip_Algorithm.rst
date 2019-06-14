6.7 CoinFlip算法
====================

6.7.1 CoinFlip算法介绍
-------------------------

你扔出一枚硬币，硬币要么正面朝上，要么背面朝上。但是在微观情况下，事情并非完全那么确定。如果你扔出的是一枚“原子”硬币，那么你得到的可能是一种正面和反面的叠加态，但是，这样的情况只是发生在你不在观察硬币的时候。如果你去观察，呈现在你眼前的可以是正面也可以是反面，随你喜欢而定。如果你像抛硬币一样扔出一个量子粒子，你就会看到不同寻常的效应。德国波恩大学的物理学家首次在铯原子实验中展示了这种效应。

6.7.2 CoinFlip算法的实现
--------------------------

下面给出 QRunes 实现 CoinFlip 算法的代码示例：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    CoinFlip_Algorithm(vector<qubit> q, vector<cbit> c, bool fx) {
        X(q[0]);
        H(q[0]);
        X(q[1]);
        CNOT(q[0], q[1]);
        H(q[1]);
        if (fx) {
            X(q[0]);
        }
        H(q[0]);
        CNOT(q[0], q[1]);
        H(q[0]);
        Measure(q[0], c[0]);
        Measure(q[1], c[1]);
    }
        
    @script:
    import sys
    def CoinFlip_Prog(prog, q, c, fx):
        temp = CoinFlip_Algorithm(q, c, fx)
        prog.insert(temp)
        res = directly_run(prog)
        return ( c[1].eval() << 1) + int(c[0].eval())
    
    if __name__ == '__main__':
        print('Entanglement Flip Game')
        fx = int(input('Input choice of Q:(0/1)\n'))
        print('Programming the circuit...')
    
        init(QMachineType.CPU_SINGLE_THREAD)
    
        qubit_num = 2
        cbit_num = 2
        qv = qAlloc_many(qubit_num)
        cv = cAlloc_many(cbit_num)
        out_come = 0
        prog = QProg()
        temp = CoinFlip_Prog(prog, qv, cv, fx)
        for i in range(0, 10, 1):
            out_come = CoinFlip_Prog(prog, qv, cv, fx)
            if out_come != temp:
                print('Q wins!')
                sys.exit(0)
        print('max entanglement!')
        print('P wins!')
    
        finalize()

6.7.3 CoinFlip算法小结
------------------------

我们传统的电脑构建模块，只能存储两个状态中的其中一个，就如硬币，50个同时抛掷你只能记录一种正反面的状态，50个硬币同时记录的话，就需要量子计算机就数千兆字节的数据存储才能达到。量子计算机就是这样的，它们是基于量子位的，它可以同时处于两个状态。这可以使每个硬币的单个量子位一次存储所有配置的概率分布
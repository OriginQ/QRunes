6.10 Shor算法
================

6.10.1 Shor算法介绍
----------------------

舒尔算法，即秀尔算法（Shor算法），以数学家彼得·秀尔命名，是一个在1994年发现的，针对整数分解这题目的的量子算法（在量子计算机上面运作的算法）。它解决如下题目：给定一个整数N，找出他的质因数。

在一个量子计算机上面，要分解整数N，秀尔算法的运作需要多项式时间（时间是logN的某个多项式这么长，logN在这里的意义是输入的档案长度）。更精确的说，这个算法花费O((logN))的时间，展示出质因数分解问题可以使用量子计算机以多项式时间解出，因此在复杂度类BQP里面。这比起传统已知最快的因数分解算法，普通数域筛选法还要快了一个指数的差异。

秀尔算法非常重要，因为它代表使用量子计算机的话，我们可以用来破解已被广泛使用的公开密钥加密方法，也就是RSA加密算法。RSA算法的基础在于假设了我们不能很有效率的分解一个已知的整数。就目前所知，这假设对传统的（也就是非量子）电脑为真；没有已知传统的算法可以在多项式时间内解决这个问题。然而，秀尔算法展示了因数分解这问题在量子计算机上可以很有效率的解决，所以一个足够大的量子计算机可以破解RSA。这对于建立量子计算机和研究新的量子计算机算法，是一个非常大的动力。

6.10.2 Shor算法的实现
----------------------

下面给出 QRunes 实现 Shor 算法的代码示例：

::

    @settings:
    language = Python;
    autoimport = True;
    compile_only = False;
    
    @qcodes:
    //Quantum adder MAJ module
    QCircuit MAJ(qubit a, qubit b, qubit c) {
        CNOT(c, b);
        CNOT(c, a);
        Toffoli(a, b, c);
    }

    //Quantum adder UMA module
    QCircuit UMA(qubit a, qubit b, qubit c) {
        Toffoli(a, b, c);
        CNOT(c, a);
        CNOT(c, b);
    }

    //Quantum adder MAJ2 module
    QCircuit MAJ2(vector<qubit> a, vector<qubit> b, qubit c) {
        let nbit = a.size();
        MAJ(c, a[0], b[0]);
        for(let i=1: 1: nbit) {
            MAJ(b[i-1], a[i], b[i]);
        }
    }

    //Quantum adder, consists of MAJ and UMA modules, regardless of the carry term
    QCircuit Adder(vector<qubit> a, vector<qubit> b, qubit c) {
        let nbit = a.size();
        MAJ(c, a[0], b[0]);
        for(let i=1: 1: nbit) {
            MAJ(b[i-1], a[i], b[i]);
        }
        for(let i=nbit-1: -1: 0) {
            MAJ(b[i-1], a[i], b[i]);
        }
        UMA(c, a[0], b[0]);
    }

    //Determine if there is a carry
    QCircuit isCarry(vector<qubit> a, vector<qubit> b, qubit c, qubit carry) {
        MAJ2(a, b, c);
        CNOT(b[-1], carry);
        MAJ2(a, b, c).dagger();
    }

    //Binding classic data with qubits
    QCircuit bindData(vector<qubit> qlist, int data) {
        let checkValue = 1 << qlist.size();

        let i = 0;
        let tmp = data >> 1;
        for(data: -tmp: 1) {
            if ((data % 2) == 1) {
                X(qlist[i]);
            }
            tmp = tmp >> 1;
            data = data >> 1;
            i = i + 1;
        }
    }

    //Constant modular addition
    QCircuit constModAdd(vector<qubit> qa, int C, int M, vector<qubit> qb, vector<qubit> qs1) {
        let qNum = qa.size();
        let tmpValue = (1 << q_num) - M + C;
        
        bindData(qb, tmpValue);
        isCarry(qa, qb, qs1[1], qs1[0]);
        bindData(qb, tmpValue);

        QCircuit qCircuitTmp1;
        qCircuitTmp1.insert(bindData(qb, tmpValue));
        qCircuitTmp1.insert(Adder(qa, qb, qs1[1]));
        qCircuitTmp1.insert(bindData(qb, tmpValue));
        qCircuitTmp1.control([qs1[0]]);
        qCircuitTmp1.push();

        X(qs1[0]);

        QCircuit qCircuitTmp2;
        qCircuitTmp2.insert(bindData(qb, C));
        qCircuitTmp2.insert(Adder(qa, qb, qs1[1]));
        qCircuitTmp2.insert(bindData(qb, C));
        qCircuitTmp2.control([qs1[0]]);
        qCircuitTmp2.push();

        X(qs1[0]);

        tmpValue = (1 << qNum) - C
        bindData(qb, tmpValue);
        isCarry(qa, qb, qs1[1], qs1[0]);
        bindData(qb, tmpValue);
        X(qs1[0]);
    }

    //Constant modular multiple
    QCircuit constModMul(vector<qubit> qa, int constNum, int M, vector<qubit> qs1, vector<qubit> qs2, vector<qubit> qs3) {
        let qNum = qa.size();

        for(let i=0: 1: qNum) {
            let tmp = constNum * pow(2, i) % M;
            QCircuit qCircuitTmp;
            qCircuitTmp.insert(constModAdd(qs1, tmp, M, qs2, qs3));
            qCircuitTmp.control(qa[i]);
            qCircuitTmp.push();
        }

        for(let i=0: 1: qNum) {
            CNOT(qa[i], qs1[i]);
            CNOT(qs1[i], qa[i]);
            CNOT(qa[i], qs1[i]);
        }

        let crev = modReverse(constNum, M);
        QCircuit qCircuitTmp1;
        for(let i=0: 1: qNum) {
            let tmp = crev * pow(2, i);
            tmp = tmp % M;
            QCircuit qCircuitTmp2;
            qCircuitTmp2.insert(constModAdd(qs1, tmp, M, qs2, qs3));
            qCircuitTmp2.control(qa[i]);
            qCircuitTmp1.insert(qCircuitTmp2);
            qCircuitTmp1.dagger();
            qCircuitTmp1.push();
        }
    }

    //Constant modular power operation
    QCircuit constModExp(vector<qubit> qa, vector<qubit> qb, int base, int M, vector<qubit> qs1, vector<qubit> qs2, vector<qubit> qs3) {
        let cqNum = qa.size();
        let temp = base;

        for(let i=0: 1: cqNum) {
            constModMul(qb, temp, M, qs1, qs2, qs3).control(qa[i]);
            temp = temp * temp;
            temp = temp % M;
        }
    }

    //Quantum Fourier transform
    QCircuit qft(vector<qubit> qlist) {
        let qNum = qlist.size();
        for (let i=0: 1: qNum) {
            H(qlist[qNum-1-i]);
            for (let j=i+1: 1: qNum) {
                CR(qlist[qNum-1-j], qlist[qNum-1-i], Pi/(1 << (j-i)));
            }
        }

        for(let i=0: 1: qNum) {
            CNOT(qlist[i], qlist[qNum - 1 - i]);
            CNOT(qlist[qNum - 1 - i], qlist[i]);
            CNOT(qlist[i], qlist[qNum - 1 - i]);
        }
    }

    @script:
    def gcd(m,n):
        if not n:
            return m
        else:
            return gcd(n, m%n)

    def modReverse(c, m):
        if (c == 0):
            raise RecursionError('c is zero!')
        
        if (c == 1):
            return 1
        
        m1 = m 
        quotient = []
        quo = m // c
        remainder = m % c

        quotient.append(quo) 

        while (remainder != 1):
            m = c
            c = remainder
            quo = m // c
            remainder = m % c
            quotient.append(quo)

        if (len(quotient) == 1):
            return m - quo

        if (len(quotient) == 2):
            return 1 + quotient[0] * quotient[1]

        rev1 = 1
        rev2 = quotient[-1]
        reverse_list = quotient[0:-1]
        reverse_list.reverse()
        for i in reverse_list:
            rev1 = rev1 + rev2 * i
            temp = rev1
            rev1 = rev2
            rev2 = temp

        if ((len(quotient) % 2) == 0):
            return rev2

        return m1 - rev2

    def shorAlg(base, M):
        if ((base < 2) or (base > M - 1)):
            raise('Invalid base!')

        if (gcd(base, M) != 1):
            raise('Invalid base! base and M must be mutually prime')
        
        binary_len = 0
        while M >> binary_len != 0 :
            binary_len = binary_len + 1
        
        machine = init_quantum_machine(QMachineType.CPU_SINGLE_THREAD)

        qa = machine.qAlloc_many(binary_len*2)
        qb = machine.qAlloc_many(binary_len)

        qs1 = machine.qAlloc_many(binary_len)
        qs2 = machine.qAlloc_many(binary_len) 
        qs3 = machine.qAlloc_many(2) 

        prog = QProg()

        prog.insert(X(qb[0]))
        prog.insert(single_gate_apply_to_all(H, qa))
        prog.insert(constModExp(qa, qb, base, M, qs1, qs2, qs3))
        prog.insert(qft(qa).dagger())

        directly_run(prog)
        result = quick_measure(qa, 100)
        print(result)
        return result

    if __name__=="__main__":
        base = 7
        N = 15
        shorAlg(base, N) 

6.10.3 Shor算法小结
----------------------
    
Shor算法并不能保证每次运行都能得到正确的结果，当计算成功给一个数，可以除N,既能验证得到的结果是不是N的因子。假设成功的概率是1-j,我们通过重复k次试验，则至少成功一次的概率是1-j^k。我们可以看出，可以通过增加实验的次数来增加成功的概率。所以Shor算法是一种随机算法。
6.8 Bernstein-Vazirani算法
=============================

6.8.1 Bernstein-Vazirani算法介绍
----------------------------------

量子计算机是相对经典计算机而言的，量子计算机并不是在通常的计算问题上取代传统的电子计算机，而是针对特定问题完成经典计算机难以胜任的高难度计算工作。它是以量子力学为基础，实现量子计算的机器。比如：若运Deutsch-Jozsa 问题的量子算法（DJ算法），只需运行一次，就可以分辨函数是常数函数还是对称函数，而运用相应的经典算法则需要运行O(N)次才能达到该目的。 后来，Bernstein和Vazirani运用DJ算法有效地解决了询问量子数据库的
问题（即BV算法）。

6.8.2 Bernstein-Vazirani算法的实现
-------------------------------------

下面给出 QRunes 实现 Bernstein-Vazirani 算法的代码示例：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    BV_QProg(vector<qubit> q, vector<cbit> c, vector<bool> a, bool b) {
        let length = q.size();
        X(q[length - 1]);
        for (let i=0: 1: length) {
            H(q[i]);
        }
        for (let i=0: 1: length-1) {
            if (a[i]) {
                CNOT(q[i], q[length - 1]);
            }
        }
        for (let i=0: 1: length-1) {
            H(q[i]);
        }
        for (let i=0: 1: length-1) {
            Measure(q[i], c[i]);
        }  
    }
        
    @script:
    import sys
    if __name__ == '__main__':
        print('Bernstein Vazirani Algorithm')
        print('f(x)=a*x+b')
        input_a = input('input a\n')
        a = []
        for i in input_a:
            if i == '0':
                a.append(0)
            else:
                a.append(1)
        b = int(input('input b\n'))
        print('a=\t%s' %(int(input_a)))
        print('b=\t%s' %(int(bool(b))))
        print('Programming the circuit...')

        init(QMachineType.CPU_SINGLE_THREAD)
        qubit_num = len(a)
        cbit_num = qubit_num
        qv = qAlloc_many(qubit_num+1)
        cv = cAlloc_many(cbit_num)
        
        if len(qv) != (len(a)+1):
            print("error: param error")
            sys.exit(1)
        bvAlgorithm = BV_QProg(qv, cv, a, b)
        directly_run(bvAlgorithm)

        print('a=\t', end='')
        for c in cv:
            print(c.eval())
        print('b=\t%s' %(int(bool(b))))

        finalize()


6.8.3 Bernstein-Vazirani算法小结
-----------------------------------
	
Bernstein-Vazirani的工作建立在Deutsch和Jozsa早期工作理论上来探索量子查询复杂度。他们对该领域的 贡献是一个用于隐藏字符串问题的量子算法, 该算法的非递归量子查询复杂度仅为1，同比经典情况O(n)。这一量子算法的真正突破在于加快查询复杂度, 而不是执行时间本身。

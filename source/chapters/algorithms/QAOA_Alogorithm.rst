6.1 QAOA算法
================

6.1.1 QAOA算法介绍
----------------------

量子近似优化算法(QAOA)，是由Farhi, Goldstone和Gutmann开发的一个多项式时间算法，用于寻找“最优化问题的一种‘好’的解决方案”。对于给定的NP-Hard问题，近似算法是一种多项式时间算法，QAOA算法以期望的一些质量保证来解决每个问题实例。品质因数是多项式时间解的质量与真实解的质量之间的比率。QAOA算法涉及到的原理有：绝热量子计算和最大切割问题。

绝热量子计算

绝热量子计算（Adiabatic quantum computation）是量子计算的一种形式，它依赖于绝热定理进行计算。首先，对于一个特定的问题，找到一个（可能复杂的）哈密顿量，其基态描述了该问题的解决方案。接下来，准备一个具有简单哈密顿量的系统并初始化为基态。最后，简单的哈密顿量绝热地演化为期望的复杂哈密顿量。根据绝热定理，系统保持在基态，因此最后系统的状态描述了问题的解决方案。绝热量子计算已经被证明在线路模型中与传统的量子计算是多项式等价的。

最大切割问题

最大切割问题（MAXCUT）是原始量子近似优化算法论文中描述的第一个应用。此问题类似于图形着色，对于给定节点和边的图形，并给每个边分配一个分值，接着将每个节点着色为黑色或白色，然后计算不同颜色节点边的分值之和，目的是找到一组得分最高的着色方式。更正式地表述是将图的节点划分为两组，使得连接相对组中的节点的边的数量最大化。

6.1.2 QAOA算法的实现
-----------------------

下面给出 QRunes 实现 QAOA 算法的代码示例：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    //Solving the problem of Maximum Cutting
    variationalCircuit oneCircuit(vector<qubit> qlist, hamiltonian hp, var beta, var gamma){
        for(int i = 0: 1: hp.size()){ 
            vector<qubit> tmp_vec;
            let item = hp[i];
            map dict_p = item.getFirst();
            for(map m in dict_p) {
                tmp_vec.add(qlist[m.first()]);
            }

            let coef = item.getSecond();
            VQG_CNOT(tmp_vec[0],tmp_vec[1]);
            VQG_RZ(tmp_vec[1], 2*gamma*coef);
            VQG_CNOT(tmp_vec[0],tmp_vec[1]);
        }

        for(int i=0: 1: qlist.size()){
            VQG_RX(qlist[i],2.0*beta);
        }
    }

    @script:
    import numpy as np

    #Convert the data format to be processed
    def trans(friendShip):
        pro = {}
        for i in range(len(friendShip)):
            for j in range (len(friendShip[i])):
                if i != j:
                    s = "Z" + str(i) + " " + "Z" + str(j)
                    pro[s] = friendShip[i][j]
        return pro

    if __name__=="__main__":
        firendShip =[[0, 0.8, 0.2, -0.2],[0.8, 0, 0, 0.7],[0.2, 0, 0, -0.3],[-0.2, 0.7, -0.3, 0]]
        print("what we r need to handle:")
        print(firendShip)
        problem = trans(firendShip)

        #Bulid pauli operator base on the data of problem
        Hp = PauliOperator(problem)
        qubit_num = Hp.getMaxIndex()

        machine = init_quantum_machine(QMachineType.CPU_SINGLE_THREAD)
        qlist = machine.qAlloc_many(qubit_num)
        step = 4
        beta = var(np.ones((step,1), dtype = 'float64'), True)
        gamma = var(np.ones((step,1), dtype = 'float64'), True)
       
        #Create a variable quantum circuit
        vqc = VariationalQuantumCircuit()

        #Insert Hadamard gates to each qubit as initial condition
        for i in qlist:
            vqc.insert(VariationalQuantumGate_H(i))

        #Insert quantum circuits corresponding to each step according to the step size
        for i in range(step):    
            vqc.insert(oneCircuit(qlist, Hp.toHamiltonian(1), beta[i], gamma[i]))

        #Calculate loss variables
        loss = qop(vqc, Hp, machine, qlist)  
        #Use momentum-based optimizer and get result variables
        optimizer = MomentumOptimizer.minimize(loss, 0.02, 0.9)
        leaves = optimizer.get_variables()

        for i in range(100):
            loss_value = optimizer.get_loss()
            print("i: ", i, " loss:", loss_value )
            optimizer.run(leaves, 0)

        prog = QProg()
        qcir = vqc.feed()
        prog.insert(qcir)
        #Run quantum programs
        directly_run(prog)

        result = quick_measure(qlist, 100)
        print(result)

6.1.3 QAOA算法小结
--------------------

我们用于求解这些问题的经典方法已经历了数十年的打磨发展，效果已经相当好了。即使早期 NISQ 时代的量子设备还无法与最好的经典计算机媲美，实验结果也可能会激励我们期待看到 QAOA 或 VQE 在未来超越经典方法，从而近一步推动技术发展。QAOA很有意思的一个原因是它具有展示量子霸权潜力。


7.5 quantumWalk算法
=====================

7.5.1 quantumWalk算法介绍
-----------------------------

quantumWalk作为一种新的量子计算模型具有巨大的前景，为经典算法寻求量子版本的解决方案提供了新思路。将量子漫步理论与聚类算法相结合，在分析图上离散量子漫步特点及其在解决聚类问题时存在不足的前提下，采取将漫步空间网格化的方式将模型简化，提出一种网格化量子漫步聚类模型，使之能够很好的完成聚类任务，该模型将数据点考虑为在量子网格世界中的根据特定规则执行漫步过程的量子，由于量子叠加等特性的存在，量子漫步聚类居右更好的时间效率和侦探能力，仿真实验也表明算法在聚类正确性上具有不错的表现。

近十年来，量子漫步作为一种新的量子计算模型崭露头角，并由于量子漫步构造的量子算法在许多问题的求解上相比于经典算法具有明显的优势，因此其在搜索、组合优化、元素区分等领域均取得了重大的进展。另外，Childs和Lovett等分别提出了离散和连续两种具有通用意义上的量子漫步架构，阐述了一切量子算法均可在建立于量子漫步模型的一般算法框架，这促成了量子漫步模型成为构建通用算法的新思路。

7.5.2 quantumWalk算法的实现
-----------------------------

下面贴出使用 qurator 插件编写的 QRunes 代码：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    QCircuit addOne(qvec q) {
        qvec vControlQubit;
        vControlQubit.insert(q, 1, q.size()-1);
        for (let i=0: 1: q.size()) {
            X(q[i]).control(vControlQubit);
            if (vControlQubit.size() >= 1) {
                vControlQubit.remove(0);
            }
        }
    }
    
    QCircuit walkOneStep(qvec q) {
        let iLength = q.size();
        X(q[iLength-1]);
        qvec vCQubit;
        vCQubit.insert(q, 1, q.size());
        addOne(q);
        X(q[iLength-1]);
        addOne(q).dagger();
    }
    
    quantumWalk(qvec q, cvec c) {  
        let length = q.size();
        X(q[length-2]);
        X(q[length-2]);
        for (let i=0: ((1 << length)-1): 1) {
            H(q[length - 1]);
            walkOneStep(q);
        }
    }
    
    @script:
    import sys
    if __name__ == '__main__':
        print('welcome to Quantum walk')
        qubit_num = int(input('please input qubit num\n'))
        if qubit_num < 0 or qubit_num > 24:
            print('error: qubitnum need > 0 and < 24')
            sys.exit(1)
        init(QMachineType.CPU_SINGLE_THREAD)
    
        cbit_num = qubit_num
        qv = qAlloc_many(qubit_num)
        cv = cAlloc_many(cbit_num)
        qv.append(qAlloc())
        qwAlgorithm = quantumWalk(qv, cv)
        result = prob_run_dict(qwAlgorithm, qv)
        for key,value in result.items():
            print(str(key) + " : " + str(value))
    
        finalize()

7.5.3 quantumWalk算法小结
----------------------------

量子漫步是一种典型的量子计算模型, 近年来开始受到量子计算理论研究者们的广泛关注。该算法的时间复杂度与Grover算法相同, 但是当搜索的目标数目多于总数的1/3时搜索成功概率大于Grover算法。
量子漫步的实现对研发量子计算机具有开创性的重大意思，通过它新的算法就可以得到应用。比如，在现在技术中，要从一串0中找到某一个0，人们必须检查每个数位，所需的时间随0的总体数量的增加而线性增加。如果使用量子漫步算法，漫步者可以同时在多处搜索，“大海捞针”的速度就被极大的提高了
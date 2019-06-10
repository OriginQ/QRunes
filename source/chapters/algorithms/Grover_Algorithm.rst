7.3 Grover算法
=================

7.3.1 Grover算法介绍
------------------------

什么是搜索算法呢？举一个简单的例子，在下班的高峰期，我们要从公司回到家里。开车走怎样的路线才能够耗时最短呢？我们最简单的想法，当然是把所有可能的路线一次一次的计算，根据路况计算每条路线所消耗的时间，最终可以得到用时最短的路线，即为我们要找的最快路线。这样依次的将每一种路线计算出来，最终对比得到最短路线。搜索的速度与总路线数N相关，记为 O(N) 。而采用量子搜索算法，则可以以 O(sqrt(N)) 的速度进行搜索，要远快于传统的搜索算法

7.3.2 Grover算法的实现
------------------------

下面贴出使用 qurator 插件编写的 QRunes 代码：

::

    @settings:
        language = Python;
        autoimport = True;
        compile_only = False;
        
    @qcodes:
    Grover(qvec q, cvec c, int target) {
        qvec controlVector;
        controlVector.add(q[0]);
        controlVector.add(q[1]);
        H(q[0]);
        H(q[1]);
        X(q[2]);
        H(q[2]);
        
        if (target == 0) {
            X(q[0]);
            X(q[1]);
            X(q[2]).control(controlVector);
            X(q[0]);
            X(q[1]);
        } else if (target == 1) {
            X(q[0]);
            X(q[2]).control(controlVector);
            X(q[0]);
        } else if (target == 2) {
            X(q[1]);
            X(q[2]).control(controlVector);
            X(q[1]);
        } else if (target == 3) {
            X(q[2]).control(controlVector);
        }
    
        H(q[0]);
        H(q[1]);
        X(q[0]);
        X(q[1]);
        H(q[1]);
        CNOT(q[0], q[1]);
        H(q[1]);
        X(q[0]);
        X(q[1]);
        H(q[0]);
        H(q[1]);
        X(q[2]);
        Measure(q[0], c[0]);
        Measure(q[1], c[1]);
    }
    
    @script:
    if __name__ == '__main__':
        print('input the input function')
        print('The function has a boolean input')
        print('and has a boolean output')
        target = int(input('target=(0/1/2/3)?\n'))
        print('Programming the circuit...')
    
        init(QMachineType.CPU_SINGLE_THREAD)
    
        qubit_num = 3
        cbit_num = 2
        qv = qAlloc_many(qubit_num)
        cv = cAlloc_many(cbit_num)
        groverprog = Grover(qv, cv, target)
        resultMap = directly_run(groverprog)
        if resultMap['c0']:
            if resultMap['c1']:
                print('target number is 3 !')
            else:
                print('target number is 2 !')
        else:
            if resultMap["c1"]:
                print("target number is 1 !")
            else:
                print("target number is 0 !")
        
        finalize()

7.3.3 Grover算法小结
-----------------------

利用量子态的纠缠特性和量子并行计算原理,可以用最多n步的搜索寻找到所需项。Grover算法的思想极为简单,可用一句话“振幅平均后翻转”来概括。具体说来是以下几个基本步骤:

①初态的制备。运用Hadamard门将处于态|0>和|1>的各量子比特转化为等幅迭加态。

②设数据库为T[1,2,,N]共,n项。设其中满足我们要求的那一项标记为A。于是在T中搜索A类似于求解一个单调函数的根。运用量子并行计算可以将A所在态的相位旋转180°,其余各态保持不变。即当T[i]=A时,增加一个相位eiπ。

③相对各态的振幅的平均值作翻转。这一操作由幺正矩阵k1,k2…knD完成,其表达式为Dij=2/N,Dij=-1+2/N。

④以上②③两步可以反复进行,每进行一次,称为一次搜索。可以证明,最多只需搜索N次,便能以大于0.5的几率找到我们要找的数据项。Grover算法提出之后,引起了众人极大的兴趣。Grover算法中的翻转方法不仅被证明是最优化的搜索方式,而且也是抗干扰能力极强的方法
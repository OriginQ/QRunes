6.10 Shor算法
================

6.10.1 Shor算法介绍
----------------------

舒尔算法，即秀尔算法（Shor算法），以数学家彼得·秀尔命名，是一个在1994年发现的，针对整数分解这题目的的量子算法（在量子计算机上面运作的算法）。它解决如下题目：给定一个整数N，找出他的质因数。

在一个量子计算机上面，要分解整数N，秀尔算法的运作需要多项式时间（时间是logN的某个多项式这么长，logN在这里的意义是输入的档案长度）。更精确的说，这个算法花费O((logN))的时间，展示出质因数分解问题可以使用量子计算机以多项式时间解出，因此在复杂度类BQP里面。这比起传统已知最快的因数分解算法，普通数域筛选法还要快了一个指数的差异。

秀尔算法非常重要，因为它代表使用量子计算机的话，我们可以用来破解已被广泛使用的公开密钥加密方法，也就是RSA加密算法。RSA算法的基础在于假设了我们不能很有效率的分解一个已知的整数。就目前所知，这假设对传统的（也就是非量子）电脑为真；没有已知传统的算法可以在多项式时间内解决这个问题。然而，秀尔算法展示了因数分解这问题在量子计算机上可以很有效率的解决，所以一个足够大的量子计算机可以破解RSA。这对于建立量子计算机和研究新的量子计算机算法，是一个非常大的动力。

| 将两个质数乘起来，例如907*641=581387，是一件小学生都能做到的事情，用计算机去处理，看起来也没有什么难度。但是如果我给你581387，让你去找它的质因数，问题就变得很复杂了。也许你可以用计算机一个一个的去尝试，但是当数字变得更大，达到成百上千位的时候，就连计算机也无能为力。世界上面有很多问题都是这样，难以找到答案，但是一旦找到答案就很容易去验证。类似的问题我们称之为NP问题。NP问题之所以难于处理，是因为它的时间复杂度往往具有指数级别。这意味着随着问题规模的线性扩大，需要的时间却是指数增长的。利用这个原理，人们创造了RSA算法，它利用大数难以分解，但是易于验证的原理，对数据进行有效的加密。
| 量子计算机有将问题指数加速的能力，那是否意味着能攻克所有的NP问题呢？很遗憾，不能。但是幸运的是，我们有能力把“质因数分解”的时间复杂度降低到多项式级别，使大数分解问题的解决变为可能。这就是Shor算法。Shor算法的提出意味着RSA密钥的安全性受到了挑战。下面我们就来介绍Shor算法的内容。

问题的转化
*************
| Shor算法首先将质因数分解问题转换成了一个子问题，下面我们来看问题的转换过程。假设我们待分解的数为 N；

| STEP 1：随机取一个正整数 :math:`1<a<N` ，定义一个函数: :math:`f(x)= 2^{x}  mod N`；

| STEP 2：这个函数一定是一个周期函数，寻找到它的周期为  :math:`r` 。（这一步将使用量子计算机完成）；

| STEP 3：如果  :math:`r` 为奇数，那么回到STEP 1。如果  :math:`r` 为偶数，那么计算  :math:`f(r/2)` ；

| STEP 4：如果  :math:`f(r/2)=−1` ，那么回到STEP 1。否则，计算  :math:`f(r/2)+1` 和  :math:`f(r/2)−1` 分别对于N的最大公约数；

| STEP 5：这两个最大公约数就是  :math:`N` 的两个质因数；

| 举个例子，对于21而言，假设我们选择  :math:`a=2` ，那么

| STEP 1：定义函数  :math:`f(x)=2^{x} mod N`

| STEP 2：发现它的周期为6。

| STEP 3：计算出 :math:`f(3)=8`

| STEP 4：计算7和9分别对于21的最大公因数 :math:`gcd(7,21)=7， gcd(9,21)=3`

| 检验知7和3都是21的质因数，于是我们得到了问题的答案。

函数的引入
***********

| 我们要为STEP 1中描述的函数找到它引入量子计算机的方式。这种函数被称为模指数（Modular Exponential）函数，在经典逻辑电路中，它已经被以各种形式设计了出来。所以现在，我们要为它准备一个量子线路的版本。
| 根据在“Oracle是什么”这一节里面提到的量子函数概念，我们需要构建出一个酉变换U使得：

.. math:: U|x⟩|y⟩=|x⟩|y⋅a^{x}(modN)⟩

| 这种情况是一种比较普适的情况，我们令 :math:`y=1`，那么后面的这一组量子比特就作为辅助比特存储了 :math:`f(x)` 的计算结果。我们先来找一种比较简单的情况来分析具体问题，可以便于对其中的变量分解转换的理解。选取要分解的质因数15，和一个比15小的任意正整数7，所以我们要构建这样的酉变换：

.. math:: U|x⟩|1⟩=|x⟩|7^{x}(mod15)⟩

| 首先要提到的一点是要表示  :math:`7^{x}(mod15)⟩`，就意味着我们的辅助比特的取值是从0~14的，为了表示这个数，需要用到4个比特，即从0000~1110。对于前面的工作比特来说，它的位数选择比较自由，而且选取的位数越多，我们得到正确结果的概率越大，这一点在后面会解释。
| 乍一看这个函数让我们有些无从下手，所以我们要对它进行一定的转换，比如先把x转化为二进制：

.. math:: 7^x=7^{x_0+2x_1+2^2x_2+...}=7^{x_0}\cdot(7^2)^{x_1}\cdot(7^4)^{x_2}...\cdot(7^{2^n})^{x_n}

|  :math:`x_i` 是x转换为二进制后每一位上对应的数码，所以它的取值无非是0或者1。这样我们就可以简单的用一个控制酉操作得到每一项，即

.. math:: \begin{align*}
                            |x_i\rangle&=|1\rangle \ :\ U_a|y\rangle\rightarrow|y\cdot 7^{2^i} (mod15)\rangle\\
                            |x_i\rangle&=|0\rangle \ :\ U_a=I
                            \end{align*}

| 其中 :math:`I` 是单位操作。所以问题就转化为了构建“控制模乘”操作 :math:`Ua`。
| 顺带一提，因为我们关注的点不是如何纯粹的用量子线路来描述里面的每一步操作，某些操作也不引入额外的计算时间复杂度，那么这些操作是可以用经典计算机代为完成的。就比如说这里的 :math:`7^{2^i`。注意到

.. math:: y\cdot 7^{2^i}(mod15)=(y\cdot (7^{2^i}mod15))mod15

| 我们只需要事先用经典计算机将 :math:`7^{2^i}mod15(i=0\sim N-1)` （N是选取的工作位数）全部计算出来，就可以在接下来的设计时只考虑对应的几种情况。
| 我们可以看出， :math:`a^{2^i}=a^{2^{i-1}+2^{i-1}}=(a^{2^{i-1}})^2` ，根据这个公式，可以列举出来对于不同的 i 的取值情况，上述表达式的取值（这个过程用经典计算机就可以完成）。在例子中的这种情况中，有

.. math:: \begin{align*}
                            i&=0 \quad 7^{2^i}mod15=7\\
                            i&=1 \quad 7^{2^i}mod15=4\\
                            i&=2 \quad 7^{2^i}mod15=1\\
                            i&\geq3 \quad 7^{2^i}mod15=1
                            \end{align*}

| 也就是说我们只需要对应设计  :math:`U_a|y\rangle\rightarrow|7y\ mod15\rangle`， :math:`U_a|y\rangle\rightarrow|4y\ mod15\rangle` 两种就可以达到设计目的了。
| 最后我们来看一下引入了函数，量子态变成了什么。
| 首先是一组Hadamard变换，它们只作用在一组N个工作比特上，所以这个总状态就会变成

.. math:: |\text{Working}\rangle|\text{Ancilla}\rangle=\left(\sum_{x=0}^{2^{N}-1} |x\rangle\right) |00...001\rangle

| 在量子函数作用在这一组量子态时，相当于这个函数的自变量从0到 :math:`2^{N}-1` 的所有取值都被保存到了辅助比特上。也就是说，工作比特的每个状态分量都和辅助比特的一个状态分量纠缠在了一起。

.. math:: \sum |x\rangle|f(x)\rangle

| 在之前的计算中，我们知道了 :math:`f(x)=a^x (mod N)` 是一个周期函数，假设它的周期是T。明显地，

.. math:: f(x)=f(x+T)=f(x+2T)....

| 那么

.. math:: |x\rangle|f(x)\rangle+|x+T\rangle|f(x+T)\rangle+|x+2T\rangle|f(x+2T)\rangle+...=\left(|x\rangle+|x+T\rangle+|x+2T\rangle+...\right)|f(x)\rangle

| 回到 :math:`a=7`， :math:`N=15` 的例子中，我们有

.. math:: \begin{align*}
                            |\text{Working}\rangle|\text{Ancilla}\rangle&=(|0\rangle+|4\rangle+|8\rangle+...)|1\rangle\\
                            &+(|1\rangle+|5\rangle+|9\rangle+...)|7\rangle\\
                            &+(|2\rangle+|6\rangle+|10\rangle+...)|4\rangle\\
                            &+(|3\rangle+|7\rangle+|11\rangle+...)|13\rangle
                            \end{align*}

| 因为这个态是一个纠缠态，所以当我们测量辅助比特时，工作比特就会坍缩成对应的那种情况。但是不论你得到辅助比特的测量值是什么，工作比特总是会只保留为每个分量都恰好为一组周期数的叠加态。那么这一组叠加态表示的数的周期将会通过量子傅里叶变换来快速完成。

| 量子傅里叶变换

| 寻找态的周期可以通过量子傅里叶变换来快速完成。我们先以 :math:`|0\rangle+|4\rangle+|8\rangle+...` 为例子来看看量子傅里叶变换是怎么做的，之后你就会发现它对于1,5,9,13...或是2,6,10,14...都能得到类似的结果。

| 如图所示，量子傅里叶变换有两个重要的部分，第一是递归的依次控制旋转（CROT）操作，第二部分是改变比特的顺序。

| 数学表达上，每一项都是用离散傅里叶变换的形式去处理的。

.. math:: y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \omega^{jk}

| 其中 :math:`x_j` 表示输入量子态的第 :math:`j` 个分量，而 :math:`k` 表示输出量子态的分量，如果用 :math:`n` 个量子比特表示，则 :math:`\omega=e^{\frac{2\pi i}{2^n}}=e^{\frac{2\pi i}{N}}`。而从矩阵上来看，则为

.. math:: F_N = \frac{1}{\sqrt{N}} \begin{bmatrix}
                            1&1&1&1&\cdots &1 \\
                            1&\omega&\omega^2&\omega^3&\cdots&\omega^{N-1} \\
                            1&\omega^2&\omega^4&\omega^6&\cdots&\omega^{2(N-1)}\\ 1&\omega^3&\omega^6&\omega^9&\cdots&\omega^{3(N-1)}\\
                            \vdots&\vdots&\vdots&\vdots&&\vdots\\
                            1&\omega^{N-1}&\omega^{2(N-1)}&\omega^{3(N-1)}&\cdots&\omega^{(N-1)(N-1)}
                            \end{bmatrix}

| 不妨假设工作比特只有4个。那么输入的量子态则为

.. math:: |\text{Input}\rangle=|0\rangle+|4\rangle+|8\rangle+|12\rangle

| 这样就代表 :math:`x_0=x_4=x_8=x_{12}=1`，并且 :math:`\omega=e^{2\pi i/16}`，其它分量上都为0。根据傅里叶变换的公式我们可以计算出

.. math:: \begin{align*}
                            y_k &= \frac{1}{\sqrt{4}} (\omega^{0k}+\omega^{4k}+\omega^{8k}+\omega^{12k})\\
                            &=\frac{1}{2}(1+i^k+(-1)^k+(-i)^k)
                            \end{align*}

| 这里就是工作比特执行完量子傅里叶变换之后的输出态上的每个分量（第k个分量）的值。从而我们可以得到 :math:`y_0=y_4=y_8=y_{12}=\frac{1}{2}`，其它情况下 :math:`y_k=0\ (k\neq 0,4,8,12)`， 那么最后输出的量子态则为

.. math:: |\text{Output}\rangle=|0\rangle+|4\rangle+|8\rangle+|12\rangle

| 利用连分数分解得到周期
| 在最后的测量时，我们会随机得到0，4，8，12四个结果中的一个，但是这个结果并不是周期。但是量子傅里叶变换的结果揭示了一点：

.. math:: \omega^{irx}=e^{2\pi i rx/2^N}\sim 1

| 其中我们假设测量结果是 :math:`x`，总工作比特数为 :math:`N`，函数的周期为 :math:`r`。那么我们有

.. math:: \frac{x}{2^N}=\frac{c}{r}

| 其中 :math:`c` 为一个未知的整数。所以我们可以通过这个式子近似地找出函数周期。例如 :math:`x=4`，:math:`N=4`，我们有

.. math:: \frac{c}{r}=\frac{1}{4}

| 这样我们就找到了周期r=4。Shor算法的量子计算机部分至此解出。你可以检验一下 :math:`f(x)=7^x (mod15)` 这个函数的周期是否确实为4。你也可以检验一下 :math:`f(r/2)+1` 和 :math:`f(r/2)−1` 和15的最大公因数是否就是15的质因数。
| 有时候 :math:`x/2^N` 并不一定能顺利约出合理的 :math:`r`，这样我们就可以通过连分数分解法，得到一个逼近的分数，从而获得 :math:`r`。这里就不再细讲了。

6.10.2 Shor算法的实现
----------------------

下面给出 QRunes 实现 Shor 算法的代码示例：

.. tabs::

   .. code-tab:: python

        @settings:
            language = Python;
            autoimport = True;
            compile_only = False;

        @qcodes:
        //Quantum adder MAJ module
        circuit MAJ(qubit a, qubit b, qubit c) {
            CNOT(c, b);
            CNOT(c, a);
            Toffoli(a, b, c);
        }

        //Quantum adder UMA module
        circuit UMA(qubit a, qubit b, qubit c) {
            Toffoli(a, b, c);
            CNOT(c, a);
            CNOT(a, b);
        }

        //Quantum adder MAJ2 module
        circuit MAJ2(vector<qubit> a, vector<qubit> b, qubit c) {
            let nbit = a.length();
            MAJ(c, a[0], b[0]);
            for(let i=1: 1: nbit) {
                MAJ(b[i-1], a[i], b[i]);
            }
        }

        //Quantum adder, consists of MAJ and UMA modules, regardless of the carry term
        circuit Adder(vector<qubit> a, vector<qubit> b, qubit c) {
            let nbit = a.length();
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
        circuit isCarry(vector<qubit> a, vector<qubit> b, qubit c, qubit carry) {
            MAJ2(a, b, c);
            CNOT(b[-1], carry);
            MAJ2(a, b, c).dagger();
        }

        //Binding classic data with qubits
        circuit bindData(vector<qubit> qlist, int data) {
            let i = 0;
            while(data >= 1){
                if(data % 2 == 1){
                    X(qlist[i]);
                }
                data = data >> 1;
                i = i + 1;
            };

        }

        //Constant modular addition
        circuit constModAdd(vector<qubit> qa, int C, int M, vector<qubit> qb, vector<qubit> qs1) {
            let qNum = qa.length();
            let tmpValue = (1 << qNum) - M + C;

            bindData(qb, tmpValue);
            isCarry(qa, qb, qs1[1], qs1[0]);
            bindData(qb, tmpValue);

            circuit qCircuitTmp1;
            qCircuitTmp1.insert(bindData(qb, tmpValue));
            qCircuitTmp1.insert(Adder(qa, qb, qs1[1]));
            qCircuitTmp1.insert(bindData(qb, tmpValue));
            qCircuitTmp1.control([qs1[0]]);

            X(qs1[0]);

            circuit qCircuitTmp2;
            qCircuitTmp2.insert(bindData(qb, C));
            qCircuitTmp2.insert(Adder(qa, qb, qs1[1]));
            qCircuitTmp2.insert(bindData(qb, C));
            qCircuitTmp2.control([qs1[0]]);

            X(qs1[0]);

            tmpValue = (1 << qNum) - C;
            bindData(qb, tmpValue);
            isCarry(qa, qb, qs1[1], qs1[0]);
            bindData(qb, tmpValue);
            X(qs1[0]);
        }

        //Constant modular multiple
        circuit constModMul(vector<qubit> qa, int constNum, int M, vector<qubit> qs1, vector<qubit> qs2, vector<qubit> qs3) {
            let qNum = qa.length();

            for(let i=0: 1: qNum) {
                let tmp = constNum * pow(2, i) % M;
                circuit qCircuitTmp;
                qCircuitTmp.insert(constModAdd(qs1, tmp, M, qs2, qs3));
                qCircuitTmp.control([qa[i]]);
            }

            for(let i=0: 1: qNum) {
                CNOT(qa[i], qs1[i]);
                CNOT(qs1[i], qa[i]);
                CNOT(qa[i], qs1[i]);
            }

            let crev = modReverse(constNum, M);
            circuit qCircuitTmp1;
            for(let i=0: 1: qNum) {
                let tmp = crev * pow(2, i);
                tmp = tmp % M;
                circuit qCircuitTmp2;
                qCircuitTmp2.insert(constModAdd(qs1, tmp, M, qs2, qs3));
                qCircuitTmp2.control([qa[i]]);
                qCircuitTmp1.insert(qCircuitTmp2);
                qCircuitTmp1.dagger();
            }
        }

        //Constant modular power operation
        circuit constModExp(vector<qubit> qa, vector<qubit> qb, int base, int M, vector<qubit> qs1, vector<qubit> qs2, vector<qubit> qs3) {
            let cqNum = qa.length();
            let temp = base;

            for(let i=0: 1: cqNum) {
                constModMul(qb, temp, M, qs1, qs2, qs3).control([qa[i]]);
                temp = temp * temp;
                temp = temp % M;
            }
        }

        //Quantum Fourier transform
        circuit qft(vector<qubit> qlist) {
            let qNum = qlist.length();
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

        def plotBar(xdata, ydata):
            fig, ax = plt.subplots()
            fig.set_size_inches(6,6)
            fig.set_dpi(100)

            rects =  ax.bar(xdata, ydata, color='b')

            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha="center", va="bottom")

            plt.rcParams['font.sans-serif']=['Arial']
            plt.title("Origin Q", loc='right', alpha = 0.5)
            plt.ylabel('Times')
            plt.xlabel('States')

            plt.show()


        def reorganizeData(measure_qubits, quick_meausre_result):
            xdata = []
            ydata = []

            for i in quick_meausre_result:
                xdata.append(i)
                ydata.append(quick_meausre_result[i])

            return xdata, ydata


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

            xdata, ydata = reorganizeData(qa, result)
            plotBar(xdata, ydata)

            return result

        if __name__=="__main__":
            base = 7
            N = 15
            shorAlg(base, N)

   .. code-tab:: c++

        To Be Continue!


6.10.3 Shor算法小结
----------------------
    
| Shor算法首先把问题分解为了“经典计算机部分”和“量子计算机部分”。然后利用了量子态的叠加原理，快速取得了函数在一个很大范围内的取值（对于 :math:`n` 个工作比特而言，取值范围为 :math:`0\sim2^n-1` 。由于函数本身是周期的，所以自变量和函数值自动地纠缠了起来，从而对于某一个函数值来说，工作比特上的态就是一组周期数态的叠加态。在取得“周期数叠加态”之后，我们自然可以通过傅里叶变换得到这组周期数的周期，从而快速解决了这个问题。

| 反过来看，之所以找函数周期问题能被量子计算机快速解决，是因为在工作比特上执行了一组Hadamard变换。它在“量子函数”的作用下，相当于同时对指数级别的自变量上求出了函数值。在数据量足够大，周期足够长的情况下，这样执行的操作总量一定会小于逐个取值寻找这个函数值在之前是否出现过——这样的经典计算机“暴力破解”法要快得多。

| Shor算法的难点在于如何通过给出的 :math:`a` ， :math:`n` 来得到对应的“量子函数”形式。进一步地讲，是否存在某种方法（准确地说是具有合理时间复杂度的方法）得到任意函数的“量子计算机版本”？限于笔者知识水平不足，我只能给出目前大概的研究结论是存在某些无法表示为量子计算机版本的函数，但是幸运地是Shor算法属于可以表示的那一类里面。

| 最后，我们可以发现，量子计算机之所以快，和量子计算机本身的叠加特性有关，它使得在处理特定问题时，比如数据库搜索，比如函数求周期……有着比经典计算机快得多的方法。但是如果经典计算机在解决某个问题时已经足够快了，我们就不需要用量子计算机来解决了。

| 就像Shor算法里面所描述的那样——我们将问题分解为了量子计算机去处理的“困难问题”和经典计算机去处理的“简单问题”两个部分一样。所以，量子计算机的出现，不代表经典计算机将会退出历史舞台，而是代表着人类将要向经典计算机力所不及的地方伸出探索之手。靠着量子计算机，或许我们能提出新的算法解决化学问题，从而研制出新型药物；或许我们可以建立包含所有信息的数据库，每次只需要一瞬间就能搜索到任何问题……量子云平台是我们帮助量子计算机走出的第一步，但接下来的路怎么走，我们就要和你一同见证了。
第1章 Quick Start
========================

1.1 QRunes简介
------------------

QRunes是一种面向过程、命令式的量子编程语言Imperative language（这也是当前主流的一种编程范式），它的出现是为了实现量子算法。QRunes根据量子计算的经典与量子混合（Quantum-Classical Hybrid）特性，在程序编译之后可以操纵经典计算机与量子芯片来实现量子计算。

QRunes通过提供高级语言的形式（类C的编程风格）来量子算法的实现和程序逻辑控制。其丰富的类型系统(Quantum Type，Auxiliary Type，Classical Type)可以实现量子计算中数据对象的绑定和行为控制，
可以满足各类量子算法开发人员的算法实现需求。

QRunes构成：Settings, QCodes和Script。其中Settings部分定义了关于QRunes编译的全局信息；QCodes部分是具体的对于量子比特操作和行为的控制；Script部分是宿主程序的实现，它的实现依赖于经典编程语言（C++，Python等）和相关联的量子程序开发工具包（比如：QPanda/pyQPanda）。


1.2 QRunes开发环境 
------------------
1.2.1 QRunes与QPanda/pyQPanda 
+++++++++++++++++++++++++++++++++

**#### QPanda**

QPanda SDK是由本源量子推出的，基于量子云服务的，开源的量子软件开发包。用户可基于此开发包开发在云端执行的量子程序。QPanda使用C++语言作为经典宿主语言，支持以QRunes书写的量子语言。
目前，QPanda支持本地仿真运行模式和云仿真运行模式，最高可支持到32位。Q-Panda提供了一个可执行的命令行程序，通过指令控制量子程序的加载、运行和读出。另外，QPanda提供了一组API，可供用户自行定制功能。

**#### QPanda 2**

QPanda 2(Quantum Programming Architecture for NISQ Device Applications)是一个高效的量子计算开发工具库，可用于实现各种量子算法，QPanda 2基于C++实现，并可扩展到Python。

**#### PyQPanda**

PyQPanda是我们通过pybind11工具，以一种直接和简明的方式，对QPanda2中的函数、类进行封装，并且提供了几乎完美的映射功能。 封装部分的代码在QPanda2编译时会生成为动态库，从而可以作为python的包引入。

1.2.2 开发环境配置与运行
++++++++++++++++++++++++++++
为了兼容高效与便捷，我们为您提供了C++ 和 Python（pyQPanda）两个版本，pyQPanda封装了C++对外提供的接口。

**#### C++的使用**

使用QPanda 2相对于pyQPanda会复杂一些，不过学会编译和使用QPanda 2，您会有更多的体验，更多详情可以阅读 使用文档_。话不多说，我们先从介绍Linux下的编译环境开始。

.. _使用文档: https://qpanda-2.readthedocs.io/zh_CN/latest/

**#### 编译环境**

在下载编译之前，我们需要：

==================== ==========
software              version        
==================== ==========
  GCC                 >= 5.4.0        
  CMake               >= 3.1          
  Python              >= 3.6.0        
==================== ==========
   
**#### 下载和编译**

我们需要在Linux终端下输入以下命令：

- $ git clone https://github.com/OriginQ/QPanda-2.git

- $ cd qpanda-2

- $ mkdir build

- $ cd build

- $ cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. 

- $ make
    
**#### 安装**

编译完成后，安装就简单的多，只需要输入以下命令：

- $ make install

**#### 开始量子编程**

现在我们来到最后一关，创建和编译自己的量子应用。
我相信对于关心如何使用QPanda 2的朋友来说，如何创建C++项目，不需要我多说。不过，我还是需要提供CMakelist的示例，方便大家参考。

::

        cmake_minimum_required(VERSION 3.1)
        project(testQPanda)
        SET(CMAKE_INSTALL_PREFIX "/usr/local")
        SET(CMAKE_MODULE_PATH  ${CMAKE_MODULE_PATH} "${CMAKE_INSTALL_PREFIX} lib/cmake")
    
        add_definitions("-std=c++14 -w -DGTEST_USE_OWN_TR1_TUPLE=1")
        set(CMAKE_BUILD_TYPE "Release")
        set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -g -ggdb")
        set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3")
        add_compile_options(-fPIC -fpermissive)
        find_package(QPANDA REQUIRED)
        if (QPANDA_FOUND)
    
            include_directories(${QPANDA_INCLUDE_DIR}
                            ${THIRD_INCLUDE_DIR})
            add_executable(${PROJECT_NAME} test.cpp)
            target_link_libraries(${PROJECT_NAME} ${QPANDA_LIBRARIES})
        endif (QPANDA_FOUND)


我们接下来通过一个示例介绍QPanda 2的使用，此例子构造了一个量子叠加态。在量子程序中依次添加H门和CNOT门，最后对所有的量子比特进行测量操作。此时，将有50%的概率得到00或者11的测量结果。

::  

        #include "QPanda.h"
        #include <stdio.h>
        using namespace QPanda;
        int main()
        {
            init(QMachineType::CPU);
            QProg prog;
            auto q = qAllocMany(2);
            auto c = cAllocMany(2);
            prog << H(q[0])
                << CNOT(q[0],q[1])
                << MeasureAll(q, c);
            auto results = runWithConfiguration(prog, c, 1000);
            for (auto result : results){
                printf("%s : %d\n", result.first.c_str(), result.second);
            }
            finalize();
        }
    
最后，编译，齐活。
::

        $ mkdir build
        $ cd build
        $ cmake .. 
        $ make
    
运行结果如下:
::

        00 : 512
        11 : 488 


**#### python的使用**

pyQPanda只需要通过pip就可安装使用。

- -pip install pyqpanda

我们接下来通过一个示例介绍pyQPanda的使用，此例子构造了一个量子叠加态。在量子程序中依次添加H门和CNOT门，最后对所有的量子比特进行测量操作。此时，将有50%的概率得到00或者11的测量结果。
::

        from pyqpanda import *
    
        init(QMachineType.CPU)
        prog = QProg()
        q = qAlloc_many(2)
        c = cAlloc_many(2)
        prog.insert(H(q[0]))
        prog.insert(CNOT(q[0],q[1]))
        prog.insert(measure_all(q,c))
        result = run_with_configuration(prog, cbit_list = c, shots = 1000)
        print(result)
        finalize()

运行结果如下:
::

        {'00': 493, '11': 507}

1.3 Qurator介绍  
--------------------

qurator-vscode 是本源量子推出的一款可以开发量子程序的 VS Code 插件。其支持 QRunes2 语言量子程序开发，并支持 Python 和 C++ 语言作为经典宿主语言。

在 qurator-vscode 中，量子程序的开发主要分为编写和运行两个部分。

- 编写程序：插件支持模块化编程，在不同的模块实现不同的功能，其中量子程序的编写主要在 qcodes 模块中；

- 程序运行：即是收集结果的过程，插件支持图表化数据展示，将运行结果更加清晰的展现在您的面前。

1.3.1 qurator-vscode 设计思想
++++++++++++++++++++++++++++++++

考虑到目前量子程序的开发离不开经典宿主语言的辅助，qurator-vscode 插件设计时考虑到一下几点：

1. 模块编程：
qurator-vscode 插件支持模块编程，将整体程序分为三个模块：settings、qcodes 和 script 模块。在不同的模块完成不同的功能。 在 settings 模块中，您可以进行宿主语言类型、编译还是运行等设置；在 qcodes 模块中， 您可以编写 QRunes2 语言程序； 在 script 模块中，您可以编写相应的宿主语言程序。

2. 切换简单：
qurator-vscode 插件目前支持两种宿主语言，分别为 Python 和 C++。您可以在两种宿主语言之间自由的切换，您只需要在 settings 模块中设置 language 的 类型，就可以在 script 模块中编写对应宿主语言的代码。插件会自动识别您所选择的宿主语言，并在 script 模块中提供相应的辅助功能。

3. 图形展示：
qurator-vscode 插件提供图形化的结果展示，程序运行后会展示 json 格式的运行结果，您可以点击运行结果，会生成相应的柱状图，方便您对运行结果的分析。

1.4 初窥QRunes 
--------------------

1.4.1 QRunes关键字 
+++++++++++++++++++++++++

=============== ======================
  int                Hamiltionian
  float            variationalCircuit
  double                  var
  bool                 circuitGen
  map
  qubit  
  cbit  
  vector 
=============== ======================

1.4.2 QRunes程序结构  
+++++++++++++++++++++++++

**### QRunes由三部分组成**

* #### settings 模块中可以设置宿主语言，编译还是运行；

::

        @settings:
            language = Python;
            autoimport = True;
            compile_only = False;

* #### qcodes 模块中可以编写 QRunes2 量子语言代码；

::

        D_J(qvec q,cvec c){
            RX(q[1],Pi);
            H(q[0]);
            H(q[1]);
            CNOT(q[0],q[1]);
            H(q[0]);
            Measure(q[0],c[0]);
        }
        
* #### script 模块中可以编写宿主语言代码，目前支持 Python 和 C++ 两种宿主语言。

::

        init(QuantumMachine_type.CPU_SINGLE_THREAD)
        q = qAlloc_many(2)
        c = cAlloc_many(2)
        qprog1 = D_J(q,c)
        result = directly_run(qprog1)
        print(result)
        finalize()

1.4.3 Oops!你的第一个量子程序
++++++++++++++++++++++++++++++

点击右上方 Run this QRunes 运行程序，或者使用命令提示符 qurator-vscode: Run this QRunes 来运行程序(快捷键 F5)，点击运行结果可以以柱状图的的形式展示。

.. image::
    ../images/run.gif

**##### 小结**

# Processes_Threads

* 多任务 operating-system can run multiple tasks simultaneously
  ▲ For operating-system,a tasks is a Process(进程) 
  ▲ Within Process ,to do more than one things at a time, you need multiple "sub-tasks",which called threads
  ▲ multiple tasks can be achieved in three ways:
        one. multiple process
        two. multiple threads
        thr. fix multiple-(process and threads)
* 同时执行多个任务通常各个任务之间并不是没有关联的，而是需要相互通信和协调，有时，任务1必须暂停等待任务2完成后才能继续执行，有时，任务3和任务4又不能同时执行，所以，多进程和多线程的程序的复杂度要远远高于我们前面写的单进程单线程的程序

>>> 线程是最小的执行单元，而进程由至少一个线程组成。如何调度进程和线程，完全由操作系统决定，程序自己不能决定什么时候执行，执行多长时间。
    多进程和多线程的程序涉及到同步、数据共享的问题，编写起来更复杂。

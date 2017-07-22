Motivating the Problem

1. Define the problem: 
* Currently, porting an existing operating system kernel to a new machine is an
intensively manual process taking man years or decades. [all: needs case study
references]

> 1a. Why do we think it's so hard to port a kernel?

> * obviously it's not impossible, and various design tradeoffs make it easier

> * it's obviously not because the actual bulk of code that needs to be changed is frightfully large

> * it could be an artifact of the two most popular kernels (linux, linux and android linux) being the worst spaghetti

> * it's hard to bring up winNT because without cooperation from MSR and tech transfer, MS doesn't want anyone to know how hard it was for them to bring up the arm port (and then let it die and then bring it up and so on...)

> * often virtualization layers, particularly binary rewriting, become the most attractive and no porting is actually done.

2. Why is this bad?

* Often, the port makes significant trade-offs in implementation complexity vs. functionality. [margo: eh, not sure if i buy that] [ming: i think this often happens to kernel extensions (which in linux are larger than the kernel.. i think?]

* Further, maintaining a forest of kernel ports makes kernel source trees overly complicated, yielding, in addition, a build system intractable to all but seasoned hackers intimately familiar with the tree. [dholland: eh, not sure if I buy *this*...]

3. What is our approach to fixing this problem?

* We claim that the volume of the code in a kernel tree that must be changed when porting (hereafter "machine-dependent code") is 'small', consisting largely of small but potentially complex snippets of code.

* We claim that techniques borrowed from programming languages: machine description languages, specification languages, and code synthesis techniques, can mitigate or eliminate the manual burden of porting an OS kernel.

* In particular, we present a handful of key language constructs that abstract the functionality of machine-dependent code declaratively. We then integrate these constructs into a family of kernel description DSLs designed for synthesis, and transpilable into C.


# How will we justify our claims?
1. Machine-dependent code volume in an OS kernel is typically 'small'
* We perform a thorough inventory of machine-dependent code over three practical OS kernels. First, we consider OS161, a BSD-like teaching operating system in use for more than a decade in CS education. 
* Second, we consider the NetBSD kernel architecture, which has been designed for portability by hand, including clean separations between machine-dependent code and machine-independent code, which need not be changed to port to a new machine.
* Finally, we consider the Barrelfish Multikernel operating system, a microkernel system that abstracts machine-dependent code into driver-like containers. eg, a bootable CPU core is directly interfaced with by a corresponding _CPU Driver_.
2. Machine-dependent kernel code can be automatically synthesized.
* We show experimentally that several tricky modules for novel machines and machine variants can be automatically synthesized using the combination of our DSLs, constraint-solving synthesis engines and transpilers into C. 
* We use these modules as synthesized to build an operating system kernel port of the Barrelfish Multikernel to a new machine variant of ARM that has not previously been supported and show that our kernel passes validation tests.

# guppypy

*When I kernel hack, I run tests and fiddle around. An automatic kernel hacker should do this, too.*


This library is a prototype of a program synthesis toolkit for operating system
kernels. It allows you to write Python that injects C code into a kernel's
source and then run experiments on the synthesized versions of your OS using
Docker. 

![arch diagram](arch.png?raw=true "guppypy Architecture Diagram")

Advantages of using this library for kernel synthesis:
- **0 Haskell required** - synthesize C with 100% Python meta-programming.
- **Test-driven, probabilistic synthesis**
    - **Prove your code is correct by writing unit tests, not proofs.**
        - Ignore the the nasty internals of your kernel subsystems
        - Security and verification programming talent is expensive. AWS is
        cheap - throw computing power at the problem because computing power scales
        linearly and programmers do not.
    - **Synthesize code by bayesian inference** - run local search algorithms to
    synthesize code en mass on a grid of virtual machines in the cloud.
        - Talk about system correctness in terms of probabilities instead of
        static models. Find the correctness probability by sampling many times.
        - e.g. the synthesizing multi-armed bandit
    - **Perturb your machine architecture and then synthesize a kernel to run on it**
        - e.g. inject or synthesize code for both sys161 and os161
- **Abstract away your OS** - synthesize on arbitrary C code (just stick the
source in `os/` and write a Dockerfile).
    - **Separate your synthesis code from your kernel** - these are conceptually
    different things, mixing them leads to poorly organized code.
    - **Take advantage of the fact that you already have a working kernel to
    synthesize on.** Don't re-write all the DSL tooling from scratch for each
    particular subsystem component you want to synthesize.

# Demo

```python
"""
Insert a kprintf into the OS/161 thread creation routine and then check that it
worked with an experiment.
"""

import unittest

from guppypy.os_config import *
from guppypy.test_case import OS161ThreadTests
from guppypy.parser import C99Function, C99

# load OS/161 source
os161 = OSConfig('os161')

# create two identical images 
default_os = OSSynthesizer(os161, tag='default')
synth_os = OSSynthesizer(os161, tag='synth')

# modify thread_create() in the second image
func = C99Function(synth_os, 'kern/thread/thread.c', 'thread_create')
with func.open():
    kprintf = C99('kprintf("Creating new thread");')
    func.inject_beginning(kprintf)

# build each image 3 times, then run TT1 against each one
suite = unittest.TestSuite()
for i in range(3):
    for kernel in (synth_os, default_os):
        suite.add(OS161ThreadTests(kernel))

unittest.TextTestRunner().run(suite)

```

# Usage

To run yourself:

```
$ pip install -r requirements.txt
$ python guppypy/example.py
```

# Paper Story
 
- There is a difference between synthesizing kernel code and automating kernel
porting, talking about them as if they are the same conflates what you are
trying to make with how you are going to make it.
    - When you mix the code implementing your semantics with the code
    implementing your system, everyone has a bad time (Haskell + C, cough cough
    barrelfish cough).
    - **I want to argue that synthesis is more tractable if you try to abstract
    away the process of developing a kernel (rather than abstracting away the
    functionality of a kernel subsystem).**
        - Then you can statistics and unit testing to check the correctness of
        your code.

- The kind of software engineering you do when you do formal verification is
**correctness-by-construction** (see [Correct by
Construction](http://wiki.c2.com/?CorrectByConstruction)). Let's consider the
benefits and drawbacks of this development method for OS kernels.
    - you do "pure" engineering by providing a formal model of how your
    software is going to work, and then use your model to reason about which code
    to write.
    - this is supposed to be good because this is how civil engineering works 
        - before you build a bridge, you build a computer model for your bridge
    - But building an OS kernel is not like building a bridge, **it is like
    building a city**. 
        - The subsystems of a kernel often behave randomly and dynamically, you
        can't model the semantics of the entire system (this is why "bottom-up"
        synthesis was chosen, because top-down is too hard).
        - But "bottom up" and "top down" synthesis will both run into the same
        implementation difficulties - the former is the same as the latter, just on a
        smaller scale.
        - If you try to map out your entire city before building it, you will
        have a bad time and will probably get fired by the Mayor before you finish.
    - Instead imagine building a bridge by Test-Driven Development.
        - You build a foundation or truss or abutment or something, then you
        test it by itself in a lot of controlled environments (in a wind chamber, under
        heavy rain) to make sure it is durable and safe, and then eventually you
        install it on your bridge.
        - With software, you test that your code works by looking at how it behaves.
            - this is in contrast to trying to build a static computer model for
            your software before you build it.

- Doing formal verification is also too expensive for big systems like OS
kernels (and particularly for verifying *existing* systems).
    - Formal systems verification = You build verified layers on top of
    eachother to preserve the soundness of your proofs
        - this is how LEAN and Coq ensure that proofs are correct - they have
        small verified kernels that bigger proofs reduce to
        - sel4 has a small verified microcontrol that is isolated from the
        application-level components above it. By precisely defining and formalizing
        the microkernel, you get to verify things higher up and know your proofs are
        sound
    - sel4 costs $362 per line of code for correctness (["Mathematically
    Verified Software Kernels: Raising the Bar for High Assurance
    Implementations"](https://sel4.systems/Info/Docs/GD-NICTA-whitepaper.pdf))
        - the Linux kernel has 15 million lines of code
            - **$543,000,000** to verify the correctness of the Linux kernel
            - Much more given that you probably have to also re-write the
            entire Linux kernel to get soundness

- ["The Affordable Application of Formal Methods to Software Engineering",
(Davis
2005)](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.167.2487&rep=rep1&type=pdf)
is about how you need to do the formalization and figure out which systems need
verification *at the beginning of the project lifecycle*.
    - to reduce cost of development and maintenance: "front-[load] a
    development effort to ensure system requirements are validated  prior to
    implementation and further by selecting critical components to undergo formal
    verification,"
    - With an existing system, **you cannot do this** - you have to build on an existing design.

- How do we take advantage of the fact tha we have an existing kernel to synthesize on?
    - writing a kernel from scratch is very different than working on an existing kernel
        - there is behavior already there that you have to preserve
            - a formal model is just one way to check this behavior - you could
            also just have unit tests for all your pre- and post-conditions.
    - if I modify the kernel, then the way I check whether I am correct is
    by looking at the behavior of my modification against the behavior of the
    original.
        - with formal verification, you end up checking that your modification
        checks against a model of the subsystem - you have are checking a dynamic
        system statically, but dynamic systems should be tested dynamically
        - when you build a car you test it by driving it through some
        mud, not by formalizing how it ought to behave when driving through some mud.
    - you can't just gut subsystems and built them back up in a
    formally-verified way - there is a existing design of the subsystem and how it works with the broader system
    that is already there and that you have to capture/preserve with your model (instead of
    getting to dictate the high-level design *with* your model). Just swapping the subsystem out with a new subsystem + semantics is how you get **the second-system effect**.
    - **The Mythical Man-Month** is about the variability in systems, the
    reason systems engineering is hard is because your system is not going to match
    your mental model of the way it should be developed on, you have to adapt to
    that
        - why throwing man-power at a system does not scale horizontally
        - the second system effect - why second-systems never end well
        - no conceptual integrity - by formalizing a subsystem, you miss the
        high-level design of the OS and how the subsystems are related to each other in
        concept

- Consider continuous integration (CI):
    - With CI, you write a button that when pressed will compile, test, trigger
    reviews, use some data, and then deploy. And then you write code that presses
    the button for you. 
    - continuous integration is automating the build process.
    - Automating the porting process is more like automating the build process
    than it is like synthesizing arbitrary programming language code.
    - So before you think about synthesis in the PL context you need to think
    about automation in the systems context, there is a dependency constraint.

- To do kernel synthesis, we need to be able to say something about whether a kernel is
correct.
    - We have been talking about synthesizing kernel code by trying to model
    the semantics of small components of that system. **This is not the only
    possible abstraction, let's move one level up and treat the OS as a black box
    that we can run commands against.**
    - **Showing that a kernel is correct is hard.**
        - This is why CS161 staff grades manually. A student kernel could be
        correct and yet behave weirdly, or it could just crash or hang and you have to
        be able to deal with corner-case behavior.
        - You often have to run a kernel a bunch of times to see whether it is
        correct or incorrect.
    - In the bottom-up synthesis approach, you synthesize a little subsystem of
    a kernel, which means you have to synthesize within the kernel.
        - You learn how it is designed and organized and then write DSL that can
        write code according to that semantics.
        - But your semantics comes from your mental model of how the system
        should behave - the hacker who wrote the kernel may have a different model than
        you.
        - Why shouldn't you want to synthesize from outside the kernel, like
        when a human writes kernel code?
            - Then you don't have to abide by the same design as the author. You
            can just check whether your new system behaves the same as hers.

- For example, I want to add a debug statement to tell me when my kernel spawns a thread. 
    - The way I test whether I have done this is by turning on my kernel,
    spawning a thread, and then looking at the console.
    - If I automate that process, then I can inject both debug statements and machine code generated from a DSL.
        - Both of these are just some C code, the tests tell you whether each
        of them works.

- When you develop test-driven code and when you write kernels, you are doing
bayesian reasoning.
    - Bayesian inference is when you update your beliefs after considering evidence.
    - If you run enough tests or enough perturbations of your code, then you
    formulate inferences about the software you are writing.
    - There is a lot of uncertainty in OS code, this is why abstraction is good.
        - I don't want to deal with intricacies of how my system component
        interacts with other components, so i abstract them away
        - If you are trying to reason about the kernel and whether it works as
        a whole, though, **abstract away the entire OS**. Treat it as a black
        box of code that runs on a virtual machine and can be sent commands.
        - Don't start with the systems components, start with the system itself
    - **My synthesized code should be evaluated *relative to the other synthesis
    candidates*, finding the right candidate should mean looking at which of several
    variants is the best, and then doing a local search of the synthesis candidate
    space.**

- The conclusion is that we should not be writing PL code to synthesize systems
code, we should be using probabilistic programming.
    - when you talk about proving the semantics of a system you ignore the fact
    you there is a lot of variablity in the way the system works as a whole that
    isn't capture when you write a static formalization whole, you should talk about
    the system as a probability distribution of behaviors, not as a turing machine
    that is running a tape

# Design

What are the components of this system?

- parser
    - `C99` - C abstract syntax tree
    - `C99Function` - C function ast mapped to os source file
- os
    - `OSConfig` - stores info about source and build process
    - `BaseOSMixin` - os pipeline foundation
    - `OSBuilder` - takes an OSConfig and makes a docker image
    - `OSSynthesizer` - takes an OSBuilder and adds a parser to do synthesis with
    - `OS161ThreadTests` - OS161 tt1 thread test + a OS/161 Docker image to run it against

- things to define:
    - program synthesis
    - automated porting
    - top down synthesis
    - bottom down synthesis
    - images
    - containers
    - kernel test harness


## 07/21/17 brainstorm

This is very open ended at this point, we'll see where it goes.

- machine instances?
- we need to define what all these mean - architecture, platform, ISA, 
what is label for the thing i am interacting with when i run an OS on my computer
maybe like an "OS isntance"
- imagine you have a grid of machine instances
- you could hypothetically hook a debugger into any of them
- or you could write code that applies a matrix of permutations across the grid
- just represent the machine as a docker image
- use the image file hash as the "logical string of x1=a \and x2=b" that is the
model structure ???? look at books in office the one that was actually
interesting to read
- this is the top down approach to synthesizing operating systems code
- if you want to prove something then go for it, but synthesizing code =/=
formal verification of code, it has just happened so that the research in that
field has been fruitful when doing those together

Although I am competent at reading the math and models of the stack of books on
my desk, I went through 2/4 of them, sat on it for a few days, and concluded:

    Do I really need to know all of that to work on automatically porting my
    kernel to a different platform?

Code is code, at the end of the day you are not actually doing something that
is more complicated than writing code. What is happening is code needs to get
written and then a bunch of math needs to happen "on top" of that code to do
the verification/synthesis part, but I 

## ASPLOS outline/comments brainstorm

- > Ming: We primarily want to compare our technique of using a number of small
synthesis-oriented DSLs as opposed to using a large constructive theorem
proving language such as Coq to build kernels. I want to refer to our technique
as "bottom-up synthesis" from many little code snippets as opposed to "top-down
synthesis" in which a few large proofs are used to construct one or few large
modules.
- This doesn't seem definition of "top down" in the context of actually writing
kernels. Why do I have to formally prove that my code is correct? Can't I just
write tests that show you that the behavior of my synthesized (alternative) code
is the same or better than the behavior of the default (hypothesis) source?
- > Margo: we want to work with legacy systems (and barrelfish is a legacy
system), and build generalizable techniques that can be applied to any
traditional or well-designed non-traditional kernel
- How do we do this if we end up writing a bunch of little DSLs? Barrelfish is too
complicated to have write a bunch of new code in various places for every
different project you do on it, there is already a really big huge surface of
things that happen (Hake, Hamlet, etc.) that are built into the build chain,
these are hard to work with.
- > In particular, we present a handful of key language constructs that abstract
the functionality of machine-dependent code declaratively. We then integrate
these constructs into a family of kernel description DSLs designed for
synthesis, and transpilable into C.
- The word "abstract" is used here but I am unsure what this means. In my head
(from philosophy), "Abstract" means platonic forms and random ontologies and
metaphysics that nobody in computer science would ever have reason to care for.
If this is a technical term, we should define it - otherwise 
- coming from philosophy the sense I have
in my mind of that word and how you mean it as a technical term in the context
of OS kernel synthesis are just incompatible things. 
- The actual argument I would make against this is: Okay, so i write some code
that abstracts over some tiny part of some random kernel that is Barrelfish.
Are the big $ research results really going to be in the fact that you did
synthesis for like one very obscure portion of this one toy kernel that clearly
cannot run the JVM?
- Then you have just made a commitment of hundreds of man-months of work and 

> Machine-dependent kernel code can be automatically synthesized.

> We show experimentally that several tricky modules for novel machines and
machine variants can be automatically synthesized using the combination of our
DSLs, constraint-solving synthesis engines and transpilers into C.
> We use these modules as synthesized to build an operating system kernel port
of the Barrelfish Multikernel to a new machine variant of ARM that has not
previously been supported and show that our kernel passes validation tests.

- Can we prototype this without having to write a bunch of new code? How
important actually is using a static typed language, gc, etc. when all the time
is going to be spent compiling, not synthesizing.

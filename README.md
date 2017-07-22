# guppypy

guppypy is a framework for experimenting with the automated porting of
operating-system kernels. It is written in Python.

It is mostly at this point a rant on trying to mix functional programming and
imperative to implement modern OS kernels.

[architecture diagram]

# Design

## Terminology

- program synthesis
- automated porting
- top down synthesis
- bottom down synthesis
- images
- containers
- kernel test harness

- we want to say something about whether a kernel is correct
    - in the bottom-up synthesis approach, you develop a kernel from within the
    kernel. You decide which its behavior, features to add, and the design of your
    subsystems based on how the code is evolving.
    - There is a difference between synthesizing code and automating kernel
    porting, talking about them as if they are the same conflates what you are
    trying to make with how you are going to make it.
	- When you mix the code implementing your semantics with the code
	implementing your system, everyone has a bad time (Haskell + C).
    - We have been talking about synthesizing kernel code by trying to model
    the semantics of small components of that system. This is not the right layer of 
    *abstraction* 

- let us start with continuous integration
    - you are writing a button that when pressed will compile, test, trigger
    reviews, use some data, and then deploy. And then you write code that presses
    the button for you. 
    - continuous integration is automating the build process
    - automating the porting process is more like automating the build process
    than it is like synthesizing arbitrary programming language code
    - so before you think about synthesis in the PL context you need to think
    about automation in the systems context, there is a dependency constraint

- when you write test-driven code, you are doing bayesian reasoning
    - bayesian inference is when you update your beliefs after considering evidence
    - if you run enough tests or enough perturbations of your code, then you
    formulate inferences about the software you are writing
    - there is a lot of uncertainty in OS code, this is why abstraction is good
        - I don't want to deal with intricacies of how my system component
        interacts with other components, so i abstract them away
        - If you are trying to reason about the kernel and whether it works as
        a whole, though, **abstract away for the os container
        - Don't start with the systems components, start with the system itself

- the conclusion is that we should not be writing PL code to synthesize systems
code, we should be using probabilistic programming
    - when you talk about proving the semantics of a system you ignore the fact
    you ignore that there is some variable in the way the system works as a
    whole, you should talk about the system as a probability distribution of
    behaviors, not as a turing machine that is running a tape

The thesis of the project is that if you treat images as logical formulas, you
can "move up a level" in the semantic hierarchy and reason about the
construction of kernel subsystems.

For example:
- Problem: I want to test all the CS161 student kernels against the staff kernel
    - Testing is usually manual because it is difficult to write code to check
    whether a system is behaving correctly.
- Solution:
    - Write bindings for OS161 into ./runtest.py into guppypy
    - user writes code in figaro saying what it means to pass a test
        - instead of being defined by the behavior of a kernel, it is defined
        by the behavior a kernel *relative to the behavior of the other kernels*.
    - put each submission's source code into os/
    - guppypy uses dockerpy to build images for each kernel
    - guppypy runs a grid on aws that is really a docker swarm
        that turn all the submissions into docker containers and run 


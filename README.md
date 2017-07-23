# guppypy

# Usage 

```
pip install -r requirements.txt
python guppypy/main.py
```

## 07/22/2017

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

## 07/21/17

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

# On automating things

I am going to defend the following claims:

* We can automatically synthesize 
    - justification: here is some code

# bottoms up vs top down approach to synthesis


# Comments from ASPLOS18-sub-open-discussion

https://github.com/Harvard-PRINCESS/documents/wiki/ASPLOS18-sub-open-discussion

> Ming: We primarily want to compare our technique of using a number of small
synthesis-oriented DSLs as opposed to using a large constructive theorem
proving language such as Coq to build kernels. I want to refer to our technique
as "bottom-up synthesis" from many little code snippets as opposed to "top-down
synthesis" in which a few large proofs are used to construct one or few large
modules.

this is not a good definition of "bottom up" in the context of actually writing
kernels

> Margo: we want to work with legacy systems (and barrelfish is a legacy
system), and build generalizable techniques that can be applied to any
traditional or well-designed non-traditional kernel

# Terminology

* "automated porting" - this is what I will use in place of what we have been
calling "synthesis". Automated porting 

* "synthesis" - I have not found documentation for what the definition of what
this is anywhere in the project; I will not use this term.

# From ASPLOS-2018 Submission Tree in Harvard-PRINCESS/documents.wiki

> In particular, we present a handful of key language constructs that abstract
the functionality of machine-dependent code declaratively. We then integrate
these constructs into a family of kernel description DSLs designed for
synthesis, and transpilable into C.

* The word "abstract" is used here but I am unsure what this means. In my head
(from philosophy), "Abstract" means platonic forms and random ontologies and
metaphysics that nobody in computer science would ever have reason to care for.
If this is a technical term, we should define it - otherwise 

coming from philosophy the sense I have
in my mind of that word and how you mean it as a technical term in the context
of OS kernel synthesis are just incompatible things. 

* The actual argument I would make against this is: Okay, so i write some code
that abstracts over some tiny part of some random kernel that is Barrelfish.
Are the big $ research results really going to be in the fact that you did
synthesis for like one very obscure portion of this one toy kernel that clearly
cannot run the JVM?

Then you have just made a commitment of hundreds of man-months of work and 

> Machine-dependent kernel code can be automatically synthesized.

> We show experimentally that several tricky modules for novel machines and
machine variants can be automatically synthesized using the combination of our
DSLs, constraint-solving synthesis engines and transpilers into C.
> We use these modules as synthesized to build an operating system kernel port
of the Barrelfish Multikernel to a new machine variant of ARM that has not
previously been supported and show that our kernel passes validation tests.

# scratch

I think this problem also isn't just with the fact that Barrelfish is
complicated and is hard to work with. There is also part of this which is the
"synthesis" which is ill-defined l

I am honestly a little frustrated because I thought the barrier to entry on this
project was just being knowledgeable about OS161. The Barrelfish kernel is such
that in order to write a Makefile when I want to do something to my kernel I
need to be able to understand and write Haskell code.

I want to do the research storyline that Margo and Ming wrote but I don't want
to use Ocaml or Haskell at all and I basically don't want to have to touch the
Barrelfish kernel except to add bindings to its source code so that my code can
automatically run it.


We are about to write a lot of very obtuse code using a kernel that has far too
much Haskell for an operating systems kernel.


From mythical man month: 
- The pilot system
- The manual

This project is going to contain code that makes it reasonable to do research on
things relating to the automated porting of operating systems kernels. I am
trying to make it easier to achieve some of the higher-level goals set forth in
[ASPLOS18-sub-storyline](github.com/Harvard-PRINCESS/documents/wiki/ASPLOS18-sub-storyline).


Docker + https://en.wikipedia.org/wiki/SystemC

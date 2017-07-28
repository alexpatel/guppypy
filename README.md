# guppypy

This is a Python toolkit for performing program synthesis on the BarrelfishOS
operating system. The goal of this software is to make it easy for you to test
strategies for automatically porting the Barrelfish to new platforms/architectures.

The library itself currently 75 lines of Python (with the demo, still <150).

The way it works is:

- You create a "synthesis template" from a source file in BarrelfishOS
demarcating which code blocks are targeted
- You write a Python module with a synthesize() function that returns a list
of synthesized snippets to try
- My library calls your synthesize() function and:
    - Renders each candidate code snippet into your template and then
    commits it to a new branch in Guppy version control
    - Runs the test suite against live BarrelfishOS instances running your
    synthesized code using Docker/CircleCI

# Getting guppypy

You should clone this recursively, to pull down a copy of Guppy:
```bash
git clone --recursive git@github.com:alexpatel/guppypy.git
```
To update this copy in the future, invoke:
```bash
git submodule update --recursive
```

Running it requires pysmt and jinja2. You should be able to get these using:
```bash
sudo apt install python-pip
pip install --upgrade pip
pip install jinja2 pysmt
```

You will also want to have an SMT solver installed: pySMT works with msat,
z3, cvc4, yices, btor, picosat, and bdd. PySMT provides a convenient function
for installing your SMT solver of choice, along with its python bindings:
```bash
pysmt-install --z3
```
Finally, `pysmt-install --check` will check whether PySMT can use the installed solvers.

# Running guppypy
```bash
./synthesize.py
```
Arguments:
- `-f [file]` - synthesis template to use, e.g. `entry.S.jinja2`
- `-s [module.method]` - synthesizer to run, e.g. `stack_order.synthesize`
- `-d [dir]` - BFish path for synthesized output, e.g. `kernel/arch/x86_64/entry.S`

# Demo

This example synthesizes BarrelfishOS x86_64 assembly for loading user-space
syscall arguments into the kernel during a system call handler.

It creates three synthesis candidates: one by SMT solver and two random ones. It
then commits each candidate to version control and tests each candidate using
CircleCI and Docker.

The relevant files are:
- [templates/entry.S.jinja2](https://github.com/alexpatel/guppypy/blob/master/guppypy/templates/entry.S.jinja2#L459) - syscall handler code synthesis template
- [stack_order.py](https://github.com/alexpatel/guppypy/blob/master/guppypy/stack_order.py) - uses a constraint solver to synthesize assembly to fill the snippet
- [synthesize.py](https://github.com/alexpatel/guppypy/blob/master/guppypy/synthesize.py) - guppypy library internals & entrypoint

```asm
{% block synthesize %}
    pushq   %rcx            /* Save user-space RIP */
    pushq   %r11            /* Save user-space RFLAGS */
    pushq   %rbx            /* arg11 */
    pushq   %rbp            /* arg10 */
    pushq   %rax            /* arg9 */
    pushq   %r15            /* arg8 */
    pushq   %r14            /* arg7 */
    pushq   %r13            /* arg6 */
    pushq   %r12            /* arg5 */
    pushq   %r9             /* arg4 */
    pushq   %r8             /* arg3 */
    pushq   %r10            /* arg2 in r10, NOT rcx from syscall */
{% endblock %}
```

| Candidate     | Guppy Diff    | CircleCI build  |
| :-------------: |:-------------:| :-----:|
| rand-1      | [rand-1](https://github.com/Harvard-PRINCESS/Guppy/compare/dev...stack_order.synthesize_1501045021_rand-1.diff) | [rand-1](https://circleci.com/gh/Harvard-PRINCESS/Guppy/93) |
| rand-2     | [rand-2](https://github.com/Harvard-PRINCESS/Guppy/compare/dev...stack_order.synthesize_1501045021_rand-2.diff) | [rand-2](https://circleci.com/gh/Harvard-PRINCESS/Guppy/94) |
| smt | [smt](https://github.com/Harvard-PRINCESS/Guppy/compare/dev...stack_order.synthesize_1501045021_smt.diff) | [smt](https://circleci.com/gh/Harvard-PRINCESS/Guppy/95) |


```bash
$ git clone --recursive -j4 git@github.com:alexpatel/guppypy.git
$ cd guppypy
$ pip install -r requirements.txt
$ pysmt-install --msat
$ pysmt-install --env  # <-- run what it prints
$ pysmt-install --check # MSAT should be available
$ cd guppypy
$ ./synthesize.py \
    --synth stack_order.synthesize \
    --file entry.S.jinja2 \
    --dest kernel/arch/x86_64/entry.S
```

```bash
>>> Starting synthesizer test version=stack_order.synthesize_1501045021

>>> Loading synthesizer stack_order.synthesize for template entry.S.jinja2

>>> Synthesizing program...
> SMT synthesizer
    /* SYNTHESIZED_START */
        pushq  %rcx
        pushq  %r11
        pushq  %rbx
        pushq  %rbp
        pushq  %rax
        pushq  %r15
        pushq  %r14
        pushq  %r13
        pushq  %r12
        pushq  %r9
        pushq  %r8
        pushq  %r10
    /* SYNTHESIZED_END */
    
> Random synthesizer
    /* SYNTHESIZED_START */
        pushq  %rbp
        pushq  %rax
        pushq  %rcx
        pushq  %r14
        pushq  %r11
        pushq  %r8
        pushq  %r15
        pushq  %rbx
        pushq  %r10
        pushq  %r13
        pushq  %r12
        pushq  %r9
    /* SYNTHESIZED_END */
    
> Random synthesizer
    /* SYNTHESIZED_START */
        pushq  %r8
        pushq  %r13
        pushq  %rbp
        pushq  %r15
        pushq  %rbx
        pushq  %rcx
        pushq  %r10
        pushq  %r12
        pushq  %rax
        pushq  %r14
        pushq  %r9
        pushq  %r11
    /* SYNTHESIZED_END */
    

>>> Patching BarrelfishOS with synthesis candidate stack_order.synthesize_1501045021_rand-1
Switched to a new branch 'stack_order.synthesize_1501045021_rand-1'
[stack_order.synthesize_1501045021_rand-1 ec055a2f9] [auto] add stack_order.synthesize_1501045021_rand-1
 1 file changed, 17 insertions(+), 13 deletions(-)
To github.com:Harvard-PRINCESS/Guppy.git
 * [new branch]          stack_order.synthesize_1501045021_rand-1 -> stack_order.synthesize_1501045021_rand-1
Switched to branch 'dev'
Your branch is up-to-date with 'origin/dev'.

>>> Done patching BarrelfishOS source

>>> Patching BarrelfishOS with synthesis candidate stack_order.synthesize_1501045021_rand-2
Switched to a new branch 'stack_order.synthesize_1501045021_rand-2'
[stack_order.synthesize_1501045021_rand-2 6ee48584b] [auto] add stack_order.synthesize_1501045021_rand-2
To github.com:Harvard-PRINCESS/Guppy.git
 * [new branch]          stack_order.synthesize_1501045021_rand-2 -> stack_order.synthesize_1501045021_rand-2
Switched to branch 'dev'
Your branch is up-to-date with 'origin/dev'.

>>> Done patching BarrelfishOS source

>>> Patching BarrelfishOS with synthesis candidate stack_order.synthesize_1501045021_smt
Switched to a new branch 'stack_order.synthesize_1501045021_smt'
[stack_order.synthesize_1501045021_smt 23c8cc4cc] [auto] add stack_order.synthesize_1501045021_smt
To github.com:Harvard-PRINCESS/Guppy.git
 * [new branch]          stack_order.synthesize_1501045021_smt -> stack_order.synthesize_1501045021_smt
Switched to branch 'dev'
Your branch is up-to-date with 'origin/dev'.

>>> Done patching BarrelfishOS source
```

# Citations

- ["A Lightweight Symbolic Virtual Machine for Solver-Aided Host Languages"](http://homes.cs.washington.edu/%7Eemina/pubs/rosette.pldi14.pdf)
- ["Bayesian Sketch Learning for Program Synthesis"](https://arxiv.org/abs/1703.05698)
- ["Calibrating Research in Program Synthesis Using 72,000 Hours of Programmer Time"
](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.473.1963&rep=rep1&type=pdf) (Barman et al. 2010)
- ["Generalized Sketching: Programming with Angelic Non-Determinism"](http://dl.acm.org/citation.cfm?id=1706339) (Akiba et al. 2013)
```

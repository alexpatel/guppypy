# guppypy

# Usage

```
$ pysmt-install -env  # copy and run in shell
$ python guppypy/synthesize.py
```

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

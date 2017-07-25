# guppypy

# Usage

```
$ pysmt-install -env  # copy and run in shell
$ python guppypy/synthesize.py
```

# Example Output

```
syscall_path:
    movq    %rsp, user_stack_save(%rip)
    lea (KERNEL_STACK + KERNEL_STACK_SIZE)(%rip), %rsp

    /* SYNTHESIZED CODE START */
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
    /* SYNTHESIZED CODE END */

    movq    %r11, %r8   /* 5th function argument is user's flags */
    movq    %rcx, %r9   /* 6th function argument is user's IP */
    movq    %rsp, %rcx  /* 4th function argument is pointer to arg buffer */
    callq   sys_syscall     /* Process system call in C */
    addq    $0x50, %rsp     /* Remove buffer from stack */
    popq    %r11            /* Restore RFLAGS */
    popq    %rcx            /* Restore RIP */
    movq    user_stack_save(%rip), %rsp /* Restore user stack */
    sysretq             /* Return to user-space */
    .bss
    .comm   user_stack_save, 8
```

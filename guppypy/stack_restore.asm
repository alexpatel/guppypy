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

/* syscall number is in rdi (1st function argument) */
/* arg0 is in rsi (2nd function argument) */
/* arg1 is in rdx (3rd function argument) */
movq    %r11, %r8   /* 5th function argument is user's flags */
movq    %rcx, %r9   /* 6th function argument is user's IP */
movq    %rsp, %rcx  /* 4th function argument is pointer to arg buffer */

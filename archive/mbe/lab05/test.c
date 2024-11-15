#include <stdio.h>
int main()
{
   int x;
   
   x = 0;
   printf("Index: ");
   scanf("%u", &x);
   
   printf("Number: %d\nHex: %08x", x, x);
   
   return 0;
}
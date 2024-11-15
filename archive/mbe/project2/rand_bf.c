#include <stdio.h>
#include <stdlib.h>

int main( int argc, char *argv[] ) {
    
    
    int seed, wopr_addr, i;
    
    if( argc < 3) {
        printf("fuck off\n");
        return 1;
    }
    
    seed = atoi(argv[1]); 
    wopr_addr = atoi(argv[2]);
    srand(seed + wopr_addr);
    
    for( i = 0; i < 16; i++) {
        printf("%d ", rand());
    }
    printf("\n");

    return 0;
}
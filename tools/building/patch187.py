# patch187: the battle bus remodelled: a proper city bus under a big striped hot-air balloon (bus.js)
i=s.index("function brBusModel(){ if(BRBUS.g) return BRBUS.g;"); j=s.index("function brBusPos(",i)
s=s[:i]+open('/home/claude/mg/bus.js').read().rstrip()+"\n"+s[j:]

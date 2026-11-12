# patch170: the other two points of interest: Crater Labs (where Copper Ridge was) and Timber Yard (Mossy Mill).
POI_JS=open('/home/claude/mg/poi.js').read()
# the module is already in from patch169; replace it with the current one (all four sites)
i=s.index("/* ---------- points of interest ----------"); j=s.index("function buildWorld(){",i)
s=s[:i]+POI_JS+"\n"+s[j:]
rep("""const POI_ON={castle:1,factory:1};""","""const POI_ON={castle:1,factory:1,labs:1,timber:1};""")

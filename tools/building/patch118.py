# ---------- 118. the armoury rebuilt: every gun is a new model cut to its own outline (carbine, pump gun, stamped SMG,
# belt-fed, minigun, tube launcher, bullpup, laminate-stocked rifles, pan-fed LMG, drum shotgun ...) in real surfaces ----------
a=s.index("  rig.gun=grp(rig.armR.hand,0,0,0);\n  const GA=rig.gun, gm=C.metal, gl=C.metalL, gd=0x1b1f26, green=0x4fc142;")
b=s.index("\n  ['smg','mg','gatling','rpg','nade','pistol','revolver','hcannon','sniper','hunting','dmr','burst','heavyar','infantry','tac','dbarrel','heavysg','csmg','ssmg','lmg','glauncher'].forEach(k=>rig[k].visible=false);",a)
s=s[:a]+open('/home/claude/mg/guns2.js').read().rstrip('\n')+s[b:]

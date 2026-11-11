# patch137: building in water starts from the bottom. Over water the grid goes down below level 0 to the level the
# bed is on (a wall in the sea stands on the seabed and rises out of the water) instead of every piece sitting on top.
rep("function grounded(p){","""// the lowest build level at a cell: 0 on land; in water, the level the bed under it is on (never more than 4 down)
// (a floor goes no lower than the bed itself: one under the seabed would be no use to anyone)
function buildFloor(i,j,ty){ let bed=1e9; for(const [a,b] of [[0.5,0.5],[0.1,0.1],[0.9,0.1],[0.1,0.9],[0.9,0.9]]){ const x=(i+a)*CELL, z=(j+b)*CELL; if(waterDepth(x,z)>0.3) bed=Math.min(bed,terrainH(x,z)); }
  if(bed>1e8) return 0; return Math.max(-4,Math.min(0,ty==='floor'?Math.ceil((bed-0.2)/LVL):Math.floor((bed+0.25)/LVL))); }
function grounded(p){""")
rep("const feetL=onRamp?onRamp.l:Math.max(0,Math.floor((fy+0.5)/LVL));","const feetL=onRamp?onRamp.l:Math.max(buildFloor(Math.floor(x/CELL),Math.floor(z/CELL)),Math.floor((fy+0.5)/LVL));",2)
rep("l=Math.max(0,l);","l=Math.max(buildFloor(i,j,type),l);",4)
rep("l=Math.max(Math.max(0,feetL-1),Math.min(feetL+1,l)); }","l=Math.max(Math.max(buildFloor(i,j,type),feetL-1),Math.min(feetL+1,l)); }")

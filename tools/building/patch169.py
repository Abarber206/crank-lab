# patch169: points of interest. Four sites become themed places instead of towns (see the notes at the top of
# poi.js): Gearworks (factory) and Fort Granite (castle) here; Crater Labs and Timber Yard next.
POI_JS=open('/home/claude/mg/poi.js').read()
rep("""var TOWNS=WORLD.towns.map((t,k)=>{ const r=seeded(9000+k); return {x:SPAWN[0]+t.u,z:SPAWN[2]+t.v,R:t.R,h:t.h,name:TOWN_NAMES[k]||('Town '+(k+1)),seed:1+Math.floor(r()*1e9),houses:[]}; });""",
    """var TOWNS=WORLD.towns.map((t,k)=>{ const r=seeded(9000+k); return {x:SPAWN[0]+t.u,z:SPAWN[2]+t.v,R:t.R,h:t.h,name:TOWN_NAMES[k]||('Town '+(k+1)),seed:1+Math.floor(r()*1e9),houses:[]}; });
// four sites are points of interest, not towns
const POI_SITE={3:'castle',4:'timber',6:'factory',8:'labs'}, POI_NAME={castle:'Fort Granite',timber:'Timber Yard',factory:'Gearworks',labs:'Crater Labs'};
const POI_ON={castle:1,factory:1};
TOWNS.forEach((t,k)=>{ const kd=POI_SITE[k]; if(kd&&POI_ON[kd]){ t.kind=kd; t.name=POI_NAME[kd]; } });""")
rep("""function buildWorld(){
  for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
    for(const h of t.houses) for(const q of housePieces(h)){ worldKeys.add(q.key); if(pieces.has(q.key)) continue;
      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } } batchTown(t); }""",
    POI_JS+"""
function buildWorld(){
  for(const t of TOWNS){ if(!t.houses.length) planHouses(t);
    const all=t.houses.map(h=>housePieces(h)); if(t.kind) for(const b of planPOI(t)) all.push(b.pieces);
    for(const list of all) for(const q of list){ worldKeys.add(q.key); if(pieces.has(q.key)) continue;
      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } } batchTown(t); }""")
rep("""function planHouses(t){""","""function planHouses(t){ if(t.kind){ t.poi=null; t.houses=[]; return t.houses; } // a point of interest has its own buildings""")
# the new wall styles, floors, treads and trim
rep("""function houseWallTex(style,kind){
  return houseTex(512,""","""function houseWallTex(style,kind){ if(POI_STYLE[style]) return poiWallTex(style,kind);
  return houseTex(512,""")
rep("""function houseSkin(p){
  const s=p.skin;""","""function houseSkin(p){ const M=houseSkin0(p), s=p.skin; if(!POI_STYLE[s.style]&&!s.floor) return M;
  if(s.floor) M.floor=poiFloorMat(s.floor); if(s.tread) M.tread=poiFloorMat(s.tread); if(s.beam!=null) M.beam=poiTrimMat(s.beam); return M; }
const wallKindS=(s,m)=>POI_STYLE[s.style]?poiWallKind(m):wallKind(m==null?511:m);
function houseSkin0(p){
  const s=p.skin;""")
import re as _re
i=s.index("function houseSkin0(p){"); j=s.index("\n",s.index("    wall:houseMat('w'+s.style",i))
seg=s[i:j]; n=seg.count("wallKind(p.mask==null?511:p.mask)"); assert n==3,n
s=s[:i]+seg.replace("wallKind(p.mask==null?511:p.mask)","wallKindS(s,p.mask)")+s[j:]
rep("""  if(p.type==='wall'&&p.skin&&!mat&&p.mask!=null&&!(p.mask&16)&&(p.mask&2)){""","""  if(p.type==='wall'&&p.skin&&!mat&&p.mask!=null&&!(p.mask&16)&&(p.mask&2)&&(!POI_STYLE[p.skin.style]||(p.mask===POI_WIN&&p.skin.style!=='stone'))){""")
# fixtures may carry their own material
rep("""  if(p.fix&&p.skin&&!mat) p.fix.parts.forEach(([geo,k])=>add(geo,0,0,0,0,0,k==='inner'?housePlainMat(p.skin):M[k]));""",
    """  if(p.fix&&p.skin&&!mat) p.fix.parts.forEach(([geo,k])=>add(geo,0,0,0,0,0,typeof k!=='string'?k:k==='inner'?housePlainMat(p.skin):M[k]));""")
# loot: chests and floor loot on the sites' floors (more of it than in a town: these are hot drops)
rep("""  // one strongbox at the foot of each town's landmark, on the side facing the town""","""  for(const t of TOWNS) if(t.kind){ const cr=seeded(t.seed+4242); for(const b of planPOI(t)) b.spots.chest.forEach(p=>{ if(cr()<0.8) addChest(p.x,p.y,p.z,Math.floor(cr()*4)*Math.PI/2); }); }
  // one strongbox at the foot of each town's landmark, on the side facing the town""")
rep("""function spawnFloorLoot(){
  if(net.role==='client') return;
  for(const t of TOWNS) for(const h of t.houses){ const s=houseSpots(h);""","""function spawnFloorLoot(){
  if(net.role==='client') return;
  const sites=[]; for(const t of TOWNS){ for(const h of t.houses) sites.push(houseSpots(h)); if(t.kind) for(const b of planPOI(t)) sites.push(b.spots); }
  for(const s of sites){""")
# castles and sawmills have no sidewalks, stop signs or street lamps
rep("""  for(const t of TOWNS){ const Ls=t.streetL, y=t.h+0.045;""","""  for(const t of TOWNS){ if(t.kind) continue; const Ls=t.streetL, y=t.h+0.045;""")
rep("""  for(const t of TOWNS){ townBulbs(t);""","""  for(const t of TOWNS){ townBulbs(t); if(t.kind) continue;""")
# shots stop on solid decoration
rep("""  const bx=boxShot(o,d,range,nearT); let pt=ph?ph.distance:Infinity, pp=ph?ph.object.userData.piece:null;
  if(bx&&bx.t<pt-0.02){ pt=bx.t; pp=bx.p; }""","""  const bx=boxShot(o,d,range,nearT); let pt=ph?ph.distance:Infinity, pp=ph?ph.object.userData.piece:null;
  if(bx&&bx.t<pt-0.02){ pt=bx.t; pp=bx.p; }
  { const dt=decoShot(o,d,Math.min(range,pt),nearT); if(dt!=null&&dt<pt-0.02){ pt=dt; pp=POI_SOLID; } }""")
rep("""function damagePiece(p,dmg,point){
  if(!pieces.has(p.key)) return;""","""function damagePiece(p,dmg,point){
  if(!pieces.has(p.key)){ if(p.deco&&point) burst(point,3,3,0.07,hotSparkMat); return; }""")

# no streets through a point of interest (its roads stop at its edge), and walls whose both faces are outside faces
rep("""    // the two streets
    for(const X of [true,false]){ const pts=[];""","""    // the two streets (none through a point of interest: its roads stop at its edge)
    if(!t.kind) for(const X of [true,false]){ const pts=[];""")
rep("""  for(const t of TOWNS) for(const X of [true,false]) for(let s=-t.streetL;s<=t.streetL;s+=1)""","""  for(const t of TOWNS) if(!t.kind) for(const X of [true,false]) for(let s=-t.streetL;s<=t.streetL;s+=1)""")
rep("""houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1)""","""houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out==null?1:p.out)""")

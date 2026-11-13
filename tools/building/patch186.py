# patch186: draw distances pushed out (~30%): full trees, tree cards and terrain detail; people and their shadows; loot,
# furniture, props, towns and gardens; BR bots
rep("const TLOD=[170,480];","const TLOD=[230,640];")
rep("const NEAR_TREE=115, MID_TREE=290, FAR_TREE=1500;","const NEAR_TREE=150, MID_TREE=390, FAR_TREE=1500;")
rep("function heroLod(H,d){ const L=H&&H.lod; if(!L) return; const near=d<20, shad=d<45;","function heroLod(H,d){ const L=H&&H.lod; if(!L) return; const near=d<30, shad=d<60;")
rep("d.g.visible=D(d.pos.x,d.pos.z)<90;","d.g.visible=D(d.pos.x,d.pos.z)<130;")
rep("far=p.kind==='furn'?d2>45*45:d2>400*400;","far=p.kind==='furn'?d2>60*60:d2>520*520;")
rep("const on=Math.hypot(t.x-cx,t.z-cz)<700;","const on=Math.hypot(t.x-cx,t.z-cz)<900;")
rep("m.visible=Math.hypot(m.userData.town.x-cx,m.userData.town.z-cz)<450;","m.visible=Math.hypot(m.userData.town.x-cx,m.userData.town.z-cz)<600;")
rep("b.h.group.visible=d<320||b.sky;","b.h.group.visible=d<420||b.sky;")

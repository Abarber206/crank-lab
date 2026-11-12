# patch165: skins refresh and back bling as its own Locker slot.
#  - Hoods, capes, beanies, the knight helm, plate armour and the wings were boxes: now a smooth hood shell with a
#    collar, a draped two-sided cape, a slouchy beanie with a folded cuff, a round great helm, a breastplate that
#    follows the chest with shoulder caps, and feathered wings that show above the shoulders.
#  - Clothing detail on every outfit: jacket lapels and shoulder patches, tee prints and sleeve bands, flannel chest
#    pockets, and trouser styles (cargo pockets, knee pads, shorts with socks).
#  - New headwear: face mask, bucket hat, tricorn. New outfits: Raven, Pixel, Corsair, Atlas (glowing plates).
#  - Back bling is its own slot: the Locker's Back bling row takes it off or puts any back bling you own (from any
#    outfit you own, or bought in the shop) on any outfit. Other players see it.
import re

# ---- geometry: hood, cape, feather ----
rep("""// a flat strap following points on the body""","""// a hood: a shell round the skull, open at the face, drawn on both sides so you can see inside the opening
let _hoodG=null;
function hoodGeo(){ if(_hoodG) return _hoodG;
  const o=new THREE.SphereGeometry(1,30,18,Math.PI*1.5+0.66,Math.PI*2-1.32,0,Math.PI*0.74), p=o.attributes.position;
  for(let i=0;i<p.count;i++){ const x=p.getX(i), y=p.getY(i), z=p.getZ(i), lo=Math.max(0,-y);
    p.setXYZ(i,x*.188*(1-.1*lo*lo),y*.2+.025+(z>0?.03*z:0),z*(z>0?.2+.05*(1-Math.abs(y)):.19)); } // longer at the back, drawn down at the nape
  o.computeVertexNormals();
  const i=o.clone(); i.scale(.965,.965,.965); const ix=i.index.array; for(let k=0;k<ix.length;k+=3){ const t=ix[k]; ix[k]=ix[k+1]; ix[k+1]=t; } i.computeVertexNormals();
  return _hoodG=mergeGeos([o,i]); }
// a cape: hangs from the shoulders round the back and sides, flares to the hem, two-sided
let _capeG=null;
function capeGeo(){ if(_capeG) return _capeG;
  const prof=[[.205,0],[.235,-.06],[.252,-.16],[.262,-.3],[.272,-.48],[.288,-.68],[.31,-.9]].map(([r,y])=>new THREE.Vector2(r,y));
  const o=new THREE.LatheGeometry(prof,26,-0.46*Math.PI,0.92*Math.PI); o.scale(1,1,.78); const p=o.attributes.position;
  for(let i=0;i<p.count;i++){ const x=p.getX(i), y=p.getY(i), z=p.getZ(i); if(y<-.6) p.setY(i,y+.025*Math.sin(x*23)*((-y-.6)/.3)); } // a little wave in the hem
  o.computeVertexNormals();
  const i=o.clone(); i.scale(.985,1,.985); const ix=i.index.array; for(let k=0;k<ix.length;k+=3){ const t=ix[k]; ix[k]=ix[k+1]; ix[k+1]=t; } i.computeVertexNormals();
  return _capeG=mergeGeos([o,i]); }
// a wing: a flat shape in the x-y plane from the root at the origin out to the tip, scalloped along the trailing edge, two-sided
let _wingG=null;
function wingGeo(){ if(_wingG) return _wingG; const S=new THREE.Shape(); S.moveTo(0,0); S.quadraticCurveTo(.16,.24,.4,.27); S.quadraticCurveTo(.56,.28,.68,.2);
  const tips=[[.68,.2],[.62,.02],[.52,-.1],[.4,-.19],[.27,-.23],[.14,-.21],[.03,-.13]];
  for(let i=1;i<tips.length;i++){ const [ax,ay]=tips[i-1], [bx,by]=tips[i]; S.quadraticCurveTo((ax+bx)/2*.8,(ay+by)/2*.8+.01,bx,by); }
  S.lineTo(0,0); const o=new THREE.ShapeGeometry(S,8); const i=o.clone(); const ix=i.index.array; for(let k=0;k<ix.length;k+=3){ const t=ix[k]; ix[k]=ix[k+1]; ix[k+1]=t; } i.computeVertexNormals();
  return _wingG=mergeGeos([o,i]); }
// a face mask: the lower face of the skull, a little proud of it, tented from the tip of the nose down to the chin
let _maskG=null;
function maskGeo(){ if(_maskG) return _maskG; const h=headGeo2(), P=h.attributes.position, I=h.index.array, keep=[], map=new Map(), pos=[];
  const inMask=(x,y,z)=>z<0.035&&y<0.0&&y>-0.16;
  for(let k=0;k<I.length;k+=3){ const a=I[k],b=I[k+1],c=I[k+2]; let ok=true;
    for(const v of [a,b,c]) if(!inMask(P.getX(v),P.getY(v),P.getZ(v))) { ok=false; break; }
    if(!ok) continue; const t=[a,b,c].map(v=>{ if(!map.has(v)){ let x=P.getX(v)*1.05, y=P.getY(v)*1.03, z=P.getZ(v)*1.05;
        const tent=-(0.142-0.62*Math.abs(x)-0.26*Math.max(0,-0.025-y)); if(z<0&&tent<z) z=tent; // over the nose, then straight down to the chin
        map.set(v,pos.length/3); pos.push(x,y,z); } return map.get(v); }); keep.push(...t); }
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setIndex(keep); g.computeVertexNormals(); return _maskG=g; }
// a flat strap following points on the body""")

# ---- outfits: trouser styles, new looks, Nightfall's wing colours ----
rep("""  {id:'volt',name:'Volt',rarity:'legendary',jacket:0x1d1f27,pants:0x1d1f27,boot:0x15161b,glove:0xffd400,skin:0xe0ac8a,hair:0xb04cff,pack:0xffd400,packD:0x15161b,accent:0xffd400,top:'racer',head:'shades',hairStyle:'mohawk',back:'guitar'},""",
    """  {id:'volt',name:'Volt',rarity:'legendary',jacket:0x1d1f27,pants:0x1d1f27,boot:0x15161b,glove:0xffd400,skin:0xe0ac8a,hair:0xb04cff,pack:0xffd400,packD:0x15161b,accent:0xffd400,top:'racer',head:'shades',hairStyle:'mohawk',back:'guitar',pantStyle:'knee'},""")
rep("""top:'armor',head:'knight',back:'shield'},""","""top:'armor',head:'knight',back:'shield',pantStyle:'knee'},""")
rep("""  {id:'scout',name:'Scout',rarity:'common',shop:1,jacket:0x4f6d8f,pants:0x3b3f46,boot:0x6b4a2a,glove:0xe2b48f,skin:0xe2b48f,hair:0x6b3e1f,accent:0xd9483b,top:'tee',head:'cap',hairStyle:'swept',back:'pack'},""",
    """  {id:'scout',name:'Scout',rarity:'common',shop:1,jacket:0x4f6d8f,pants:0x3b3f46,boot:0x6b4a2a,glove:0xe2b48f,skin:0xe2b48f,hair:0x6b3e1f,accent:0xd9483b,top:'tee',head:'cap',hairStyle:'swept',back:'pack',pantStyle:'shorts'},""")
rep("""top:'vest',head:'hardhat',hairStyle:'buzz',back:'tank'},""","""top:'vest',head:'hardhat',hairStyle:'buzz',back:'tank',pantStyle:'cargo'},""")
rep("""top:'tee',head:'capb',hairStyle:'bun',back:'none'},""","""top:'tee',head:'capb',hairStyle:'bun',back:'none',pantStyle:'shorts'},""")
rep("""top:'coat',head:'bandana',hairStyle:'swept',back:'quiver'},""","""top:'coat',head:'bandana',hairStyle:'swept',back:'quiver',pantStyle:'cargo'},""")
rep("""top:'vest',head:'headset',hairStyle:'buzz',back:'tank'},""","""top:'vest',head:'headset',hairStyle:'buzz',back:'tank',pantStyle:'cargo'},""")
rep("""top:'suit',head:'visor',hairStyle:'bun',back:'tank'},""","""top:'suit',head:'visor',hairStyle:'bun',back:'tank',pantStyle:'knee'},""")
rep("""  {id:'nightfall',name:'Nightfall',rarity:'legendary',shop:1,jacket:0x15161b,pants:0x15161b,boot:0x2a2f38,glove:0x8a5cff,skin:0xd9b3a0,hair:0xeeeeff,accent:0x8a5cff,pack:0x2a2f38,packD:0x15161b,top:'racer',head:'headset',hairStyle:'swept',back:'wings'},""",
    """  {id:'nightfall',name:'Nightfall',rarity:'legendary',shop:1,jacket:0x15161b,pants:0x15161b,boot:0x2a2f38,glove:0x8a5cff,skin:0xd9b3a0,hair:0xeeeeff,accent:0x8a5cff,pack:0x3b2a66,packD:0x1a1430,top:'racer',head:'headset',hairStyle:'swept',back:'wings',pantStyle:'knee'},""")
rep("""top:'armor',head:'crown',hairStyle:'long',back:'banner'}
];""","""top:'armor',head:'crown',hairStyle:'long',back:'banner'},
  {id:'raven',name:'Raven',rarity:'epic',shop:1,jacket:0x1c1d24,pants:0x1c1d24,boot:0x101014,glove:0x101014,skin:0xd9b3a0,hair:0x101014,accent:0xc8102e,pack:0x2a2b33,packD:0x101014,top:'hoodie',head:'mask',hairStyle:'buzz',back:'sword',pantStyle:'knee'},
  {id:'pixel',name:'Pixel',rarity:'rare',shop:1,jacket:0xfff1a8,pants:0x2f7f6b,boot:0xff6a3d,glove:0xf3cfb0,skin:0xf3cfb0,hair:0x1c1c1c,accent:0xff6a3d,pack:0x2fc7ff,packD:0x1d6fa8,top:'tee',head:'bucket',hairStyle:'bun',back:'none',pantStyle:'cargo'},
  {id:'corsair',name:'Corsair',rarity:'legendary',shop:1,jacket:0x8a1f2e,pants:0x2a2420,boot:0x1a1410,glove:0x2a2420,skin:0xc98f6a,hair:0x2a1e14,accent:0xd4af37,pack:0x3a2a1e,packD:0x1a1410,top:'coat',head:'tricorn',hairStyle:'long',back:'sword'},
  {id:'atlas',name:'Atlas',rarity:'epic',shop:1,jacket:0x2b3140,pants:0x1d222c,boot:0x15181f,glove:0x15181f,skin:0xe0c2b0,hair:0x3a3f4a,accent:0x2fe0ff,pack:0x2b3140,packD:0x15181f,top:'armor',head:'visor',hairStyle:'buzz',back:'jetpack',pantStyle:'knee',glow:1}
];
// back bling: its own slot in the Locker. Each is the look of one outfit's back, in that outfit's colours, and can go on
// any outfit; 'auto' keeps the outfit's own.
const BACKS=[
  {id:'none',name:'Nothing',rarity:'common',kind:'none'},
  {id:'pack',name:'Trail Pack',rarity:'uncommon',kind:'pack',pack:0xe8a62c,packD:0xb07a16},
  {id:'jetpack',name:'Thruster',rarity:'epic',kind:'jetpack',pack:0xdfe4ea,packD:0x9aa3ad,accent:0xf28c28},
  {id:'cape',name:'Ember Cape',rarity:'rare',kind:'cape',pack:0x24252e,packD:0x15161b,accent:0xffa424},
  {id:'shield',name:'Round Shield',rarity:'uncommon',kind:'shield',pack:0x9a6a3a,packD:0x6b4a2a,accent:0xe0782b},
  {id:'guitar',name:'Riff Axe',rarity:'legendary',kind:'guitar',pack:0xffd400,packD:0x15161b},
  {id:'quiver',name:'Ranger Quiver',rarity:'rare',kind:'quiver',pack:0x6b4423,packD:0x3a2416,accent:0x8a2a2a},
  {id:'wings',name:'Night Wings',rarity:'legendary',kind:'wings',pack:0x3b2a66,packD:0x1a1430},
  {id:'tank',name:'Air Tank',rarity:'uncommon',kind:'tank',pack:0x7a6a4a,packD:0x4a3f2a},
  {id:'sword',name:'Greatsword',rarity:'epic',kind:'sword',pack:0x3a1f2e,packD:0x1a1410},
  {id:'banner',name:'Royal Banner',rarity:'legendary',kind:'banner',pack:0x7a1f3a,packD:0x4a1022,accent:0xd4af37}];
const backIdx=id=>Math.max(0,BACKS.findIndex(b=>b.id===id));
const backFor=o=>BACKS.find(b=>b.kind===(o.back||'pack'))||BACKS[0];""")

# heroFor / reskin take the back bling
rep("""function heroFor(o,pk){ const H=createHero(o.jacket,Object.assign({},o,{pickaxe:pk||'steel'})); heroLodPrep(H); return H; }""",
    """function heroFor(o,pk,bk){ const b=bk&&bk!=='auto'?BACKS[backIdx(bk)]:null, ex={pickaxe:pk||'steel'};
  if(b){ ex.back=b.kind; ex.pack=b.pack||o.pack; ex.packD=b.packD||o.packD; }
  const H=createHero(o.jacket,Object.assign({},o,ex)); heroLodPrep(H); H.back=bk||'auto'; return H; }""")
rep("""function reskin(H,o,pk){ pk=pk||'steel'; if(!o||(H.outfit===o.id&&H.pickaxe===pk)) return; const nh=heroFor(o,pk), g=H.group; H.pickaxe=pk;""",
    """function reskin(H,o,pk,bk){ pk=pk||'steel'; bk=bk||'auto'; if(!o||(H.outfit===o.id&&H.pickaxe===pk&&(H.back||'auto')===bk)) return; const nh=heroFor(o,pk,bk), g=H.group; H.pickaxe=pk; H.back=bk;""")

# ---- tops ----
rep("""  } else if(top==='armor'){
    part(rbox(.4,.25,.24,.09),C.jacketL,rig.chest,0,.12,-.005,null,null,0.01); // breastplate
    part(rbox(.06,.2,.02,.01),C.accent,rig.chest,0,.13,-.128,null,null,0);
    part(rbox(.33,.05,.22,.02),0x6b4a2a,rig.spine,0,.0,0,null,null,0.006); part(rbox(.06,.05,.02,.01),0xd4af37,rig.spine,0,.0,-.112,null,null,0);""",
    """  } else if(top==='armor'){ // plate: a breastplate that follows the chest, a gorget at the neck, a belt plate; glowing seams on tech suits
    pz(organ(CHR.slice(0,7).map(([y,a,b,c])=>[y,a+.013,b+.015,c+.013]),22),C.jacketL,rig.chest);
    pz(organ([[.235,.14,.1,.112],[.2,.172,.118,.128],[.14,.202,.126,.136],[.09,.19,.124,.132]],22),C.jacketL,rig.chest); // the plate over the collarbones
    const gm=opts.glow?new THREE.MeshBasicMaterial({color:C.accent}):C.accent;
    part(rbox(.03,.2,.012,.005),gm,rig.chest,0,.1,-.137,null,null,0); [-1,1].forEach(sx=>part(rbox(.012,.16,.01,.004),gm,rig.chest,sx*.085,.1,-.128,[0,sx*.3,0],null,0));
    part(rbox(.028,.1,.01,.004),opts.glow?0x4a5566:C.jacketD,rig.spine,0,.07,-.113,null,null,0);
    pz(organ([[.028,.148,.102,.108],[-.012,.15,.103,.109]],22,1),opts.glow?0x4a5566:0x6b4a2a,rig.spine); part(rbox(.07,.045,.016,.008),opts.glow?C.jacketL:0xd4af37,rig.spine,0,.008,-.113,null,null,0);
    if(opts.glow){ part(rbox(.012,.1,.008,.003),gm,rig.spine,0,.065,-.112,null,null,0); }""")
rep("""  } else if(top==='tee'){
    part(new THREE.CylinderGeometry(.075,.09,.03,16,1,true),C.skin,rig.chest,0,.265,-.005,null,[1,1,.8]); // open neckline""",
    """  } else if(top==='tee'){
    part(new THREE.CylinderGeometry(.075,.09,.03,16,1,true),C.skin,rig.chest,0,.265,-.005,null,[1,1,.8]); // open neckline
    part(new THREE.CylinderGeometry(.084,.092,.018,16,1,true),C.accent,rig.chest,0,.258,-.004,null,[1,1,.8],0); // ribbed collar
    { const [z,ry]=onChest(0,.13,.003); part(rbox(.11,.075,.007,.004),C.accent,rig.chest,0,.13,z,[0,ry,0],null,0); part(rbox(.05,.03,.006,.003),C.jacket,rig.chest,0,.14,z-.005,[0,ry,0],null,0); } // chest print""")
# jacket: lapels and shoulder patches
rep("""    part(sph(.12),C.jacketD,rig.chest,0,.24,.1,null,[1.15,.6,.7]);
    if(top==='racer'){""","""    part(sph(.12),C.jacketD,rig.chest,0,.24,.1,null,[1.15,.6,.7]);
    [-1,1].forEach(sx=>{ part(rbox(.055,.075,.012,.005),C.jacketD,rig.chest,sx*.052,.245,-.085,[.5,sx*.25,sx*.55],null,0.004); part(rbox(.05,.05,.02,.006),C.jacketD,rig.chest,sx*.178,.235,0,[0,0,sx*-.45],null,0.004); }); // lapels, shoulder patches
    if(top==='racer'){""")
# flannel: chest pockets
rep("""    [.03,.11,.19].forEach(y=>part(bodyLathe([[.162+y*.1,y],[.164+y*.1,y+.025]],.67),C.jacketD,rig.chest,0,0,0,null,null,0));""",
    """    [.03,.11,.19].forEach(y=>part(bodyLathe([[.162+y*.1,y],[.164+y*.1,y+.025]],.67),C.jacketD,rig.chest,0,0,0,null,null,0));
    [-1,1].forEach(sx=>{ const [z,ry]=onChest(sx*.075,.13,.004); part(rbox(.062,.065,.01,.004),C.jacket,rig.chest,sx*.075,.13,z,[0,ry,0],null,0.004); part(rbox(.062,.016,.012,.004),C.jacketD,rig.chest,sx*.075,.158,z-.002,[0,ry,0],null,0); }); // chest pockets""")

# ---- back bling ----
rep("""  } else if(back==='cape'){
    part(rbox(.36,.66,.02,.01),C.pack,rig.pack,0,-.36,.0,[.1,0,0]);
    part(rbox(.37,.04,.025,.01),C.accent,rig.pack,0,-.68,.03,[.1,0,0],null,0.004);
    [-1,1].forEach(sx=>part(sph(.03),0xd4af37,rig.chest,sx*.14,.25,-.09,null,null,0.005));""",
    """  } else if(back==='cape'){ // drapes from the shoulders, sways with the pack spring; a clasp cord across the chest
    part(capeGeo(),C.pack,rig.pack,0,.085,-.1,null,null,0.006);
    part(new THREE.CylinderGeometry(.215,.235,.035,26,1,true,-0.46*Math.PI,0.92*Math.PI),C.packD,rig.pack,0,.085,-.1,null,[1,1,.78],0); // the yoke
    [-1,1].forEach(sx=>part(sph(.028),0xd4af37,rig.chest,sx*.12,.235,-.1,null,[1,1,.6],0.005)); part(rbox(.2,.012,.008,.004),C.accent,rig.chest,0,.235,-.112,null,null,0);""")
rep("""  } else if(back==='wings'){
    [-1,1].forEach(sx=>{ const w=grp(rig.pack,sx*.06,-.02,.03); w.rotation.set(.15,sx*.35,sx*.35);
      for(let k=0;k<4;k++) part(rbox(.03,.34-k*.06,.012,.006),k%2?C.pack:C.packD,w,sx*(.07+k*.055),.02-k*.045,k*.004,[0,0,sx*(.5+k*.18)]); });""",
    """  } else if(back==='wings'){ // feathered wings: a flat wing shape with scalloped feather tips, a darker layer behind it, swept back and up from the shoulder blades
    [-1,1].forEach(sx=>{ const w=grp(rig.pack,sx*.05,.08,.03); w.rotation.order='YXZ'; w.rotation.set(.32,sx*-.6,sx*.12);
      part(wingGeo(),C.packD,w,0,0,.008,null,[sx*1.06,1.06,1],0); part(wingGeo(),C.pack,w,0,0,0,null,[sx,1,1],0);
      [[.6,.02],[.5,-.1],[.38,-.18],[.25,-.22],[.12,-.2]].forEach(([tx,ty])=>{ const dx=tx-.28, dy=ty-.16, l=Math.hypot(dx,dy); part(rbox(.01,l,.005,.002),C.packD,w,sx*(tx+.28)/2,(ty+.16)/2,-.004,[0,0,sx*-Math.atan2(dx,-dy)],null,0); }); // the feather shafts
      part(limbGeo(.02,.013,.36),C.packD,w,sx*.17,.14,-.006,[0,0,sx*-1.05],null,0.004); }); // the leading edge""")

# ---- headwear ----
rep("""    part(rbox(.285,.14,.285,.08),C.accent,rig.head,0,.25,.005);
    part(new THREE.CylinderGeometry(.148,.148,.05,20),new THREE.Color(C.accent).multiplyScalar(.8).getHex(),rig.head,0,.2,.005,null,null,0.006);""",
    """    part(new THREE.SphereGeometry(.15,22,12,0,Math.PI*2,0,Math.PI*.56),C.accent,rig.head,0,.195,.0,null,[1.02,1.18,1.05]); // a slouchy dome
    part(new THREE.CylinderGeometry(.154,.146,.07,22,1,true),new THREE.Color(C.accent).multiplyScalar(.8).getHex(),rig.head,0,.2,.0,null,[1,1,1.03],0.006); // the folded cuff""")
rep("""    const hc=headwear==='hood'?C.jacket:C.jacket, hd=new THREE.Color(hc).multiplyScalar(.75).getHex();
    part(rbox(.32,.08,.32,.04),hc,rig.head,0,.285,.02); part(rbox(.32,.34,.07,.04),hc,rig.head,0,.13,.15);
    [-1,1].forEach(sx=>part(rbox(.06,.34,.32,.03),hc,rig.head,sx*.155,.13,.02));
    part(rbox(.3,.06,.07,.025),hd,rig.head,0,.265,-.14,[.3,0,0],null,0.006);
    [-1,1].forEach(sx=>part(rbox(.05,.3,.05,.02),hd,rig.head,sx*.135,.12,-.14,null,null,0.005));""",
    """    const hc=C.jacket, hd=new THREE.Color(hc).multiplyScalar(.75).getHex();
    part(hoodGeo(),hc,rig.head,0,.135,.012,null,null,0.006); // the hood, open at the face
    part(new THREE.CylinderGeometry(.115,.185,.1,22,1,true),hc,rig.chest,0,.245,.012,null,[1,1,.9],0.005); // it gathers at the collar
    part(new THREE.TorusGeometry(.172,.014,8,26,Math.PI*2-1.32),hd,rig.head,0,.16,.012,[Math.PI/2,0,Math.PI*1.5+0.66],null,0); // the seam round the opening""")
rep("""  } else if(headwear==='knight'){
    part(rbox(.29,.31,.29,.1),0xcfdbe6,rig.head,0,.14,0,null,null,0.012);
    part(rbox(.2,.03,.01,.008),0x0f1a2a,rig.head,0,.15,-.146,null,null,0); part(rbox(.03,.12,.01,.008),0x0f1a2a,rig.head,0,.09,-.146,null,null,0);
    part(rbox(.03,.16,.296,.012),C.accent,rig.head,0,.22,0,null,null,0);
    for(let q=0;q<6;q++) part(rbox(.04,.1-q*.008,.06,.018),C.accent,rig.tuft,0,.05+q*.006,-.12+q*.055,[-.3+q*.15,0,0]);""",
    """  } else if(headwear==='knight'){ // a great helm: a round barrel with a domed top, an eye slit and breaths
    part(new THREE.CylinderGeometry(.148,.154,.27,26),0xcfdbe6,rig.head,0,.125,0,null,[1,1,.96],0.012);
    part(new THREE.SphereGeometry(.148,26,12,0,Math.PI*2,0,Math.PI*.5),0xcfdbe6,rig.head,0,.26,0,null,[1,.7,.96]);
    part(new THREE.CylinderGeometry(.152,.156,.03,26,1,true),C.accent,rig.head,0,.2,0,null,[1,1,.96],0); // the band
    part(rbox(.2,.025,.012,.006),0x0f1a2a,rig.head,0,.15,-.144,null,null,0); part(rbox(.024,.1,.012,.006),0x0f1a2a,rig.head,0,.08,-.144,null,null,0);
    [-1,1].forEach(sx=>[0,1,2].forEach(q=>part(sph(.006),0x0f1a2a,rig.head,sx*(.04+q*.02),.07-q*.012,-.142,null,null,0)));
    part(bladeGeo([-1,-.5,0,.5,1].map(t=>new THREE.Vector3(0,.335+.03*(1-t*t),t*.15+.02)),.026,.075,.075),C.accent,rig.head,0,0,0,null,null,0.004);""")
rep("""  } else if(headwear==='hardhat'){""","""  } else if(headwear==='mask'){ // a mask over the nose and mouth, a headband with its tails
    part(new THREE.SphereGeometry(.13,24,12,Math.PI*1.5-1.3,2.6,Math.PI*.44,Math.PI*.42),C.jacket,rig.head,0,.135,0,null,[1.06,1,1.06],0.005);
    part(new THREE.CylinderGeometry(.126,.126,.04,22,1,true),C.accent,rig.head,0,.19,0,null,[1,1,1.05],0);
    [-1,1].forEach(sx=>part(rbox(.035,.22,.008,.004),C.accent,rig.head,sx*.03,.09,.13,[-.35,0,sx*.25],null,0.003));
    rig.mouth.visible=false;
  } else if(headwear==='bucket'){ // bucket hat
    part(new THREE.CylinderGeometry(.122,.136,.1,22),C.accent,rig.head,0,.225,0,null,[1,1,1.02]);
    part(new THREE.CylinderGeometry(.195,.17,.028,24),new THREE.Color(C.accent).multiplyScalar(.85).getHex(),rig.head,0,.178,-.005,[.14,0,0],[1,1,1.04],0.005);
    part(new THREE.CylinderGeometry(.126,.126,.012,22,1,true),new THREE.Color(C.accent).multiplyScalar(.7).getHex(),rig.head,0,.21,0,null,[1,1,1.02],0);
  } else if(headwear==='tricorn'){ // a tricorn: a crown with the brim folded up on three sides, gold trim and a plume
    part(new THREE.CylinderGeometry(.118,.13,.1,22),0x2a1e16,rig.head,0,.22,0);
    part(new THREE.CylinderGeometry(.19,.19,.012,24),0x2a1e16,rig.head,0,.172,0,null,[1,1,1.05],0.005);
    [0,Math.PI/2,Math.PI].forEach(a=>{ const f=part(rbox(.24,.075,.014,.006),0x2a1e16,rig.head,Math.cos(a)*.165,.205,Math.sin(a)*.165,null,null,0.005); f.rotation.order='YXZ'; f.rotation.set(-.5,Math.PI/2-a,0);
      const t=part(rbox(.24,.012,.016,.004),C.accent,rig.head,Math.cos(a)*.165,.205,Math.sin(a)*.165,null,null,0); t.rotation.order='YXZ'; t.rotation.set(-.5,Math.PI/2-a,0); t.position.y+=.032; });
    part(new THREE.ConeGeometry(.022,.22,8),0xf3efe4,rig.head,.12,.25,.08,[.4,0,-.9],[1,1,.4],0.004);
  } else if(headwear==='hardhat'){""")

# ---- arms: armour shoulder caps, tee sleeve bands ----
rep("""    if(top==='tee'){ pz(organ([[.045,.045,.05,.052],[.02,.06,.062,.064],[-.04,.059,.064,.064],[-.1,.054,.058,.056],[-.135,.052,.056,.054]],16),C.jacket,sh); pz(organ([[-.09,.047,.052,.05],[-.2,.043,.047,.045],[-.27,.04,.042,.042],[-.31,.038,.04,.04]],16),C.skin,sh); }""",
    """    if(top==='tee'){ pz(organ([[.045,.045,.05,.052],[.02,.06,.062,.064],[-.04,.059,.064,.064],[-.1,.054,.058,.056],[-.135,.052,.056,.054]],16),C.jacket,sh); pz(organ([[-.09,.047,.052,.05],[-.2,.043,.047,.045],[-.27,.04,.042,.042],[-.31,.038,.04,.04]],16),C.skin,sh);
      pz(organ([[-.105,.0555,.0595,.0575],[-.132,.0535,.0575,.0555]],16,1),C.accent,sh); } // a band at the sleeve hem""")
rep("""    if(top==='armor') part(sph(.095),C.jacketL,sh,0,.0,0,null,[1.1,.75,1.1]);""",
    """    if(top==='armor'){ part(new THREE.SphereGeometry(.088,20,12,0,Math.PI*2,0,Math.PI*.58),C.jacketL,sh,sx*.012,.035,0,[0,0,sx*-.18],[1.18,.95,1.15],0.008); // shoulder cap
      pz(organ([[-.12,.058,.062,.06],[-.19,.05,.052,.051],[-.235,.047,.049,.048]],16),C.jacketL,sh); // vambrace over the upper arm
      if(opts.glow) part(rbox(.01,.09,.008,.003),new THREE.MeshBasicMaterial({color:C.accent}),sh,sx*.058,-.17,0,null,null,0); }""")

# ---- legs: trouser styles ----
rep("""    pz(organ([[.05,.07,.08,.084,sx*.004],[-.03,.086,.094,.1,sx*.003],[-.12,.083,.09,.093,sx*.001],[-.24,.07,.076,.074,-sx*.006],[-.34,.058,.062,.06,-sx*.011],[-.4,.055,.061,.055,-sx*.013],[-.44,.052,.056,.052,-sx*.013]],18),C.pants,hp);
    const kn=grp(hp,0,-.4,0);
    pz(organ([[.05,.054,.058,.054,-sx*.013],[.0,.055,.063,.054,-sx*.013],[-.06,.054,.052,.062,-sx*.011],[-.13,.057,.047,.07,-sx*.009],[-.22,.047,.042,.055,-sx*.005],[-.3,.039,.037,.041,-sx*.002],[-.385,.041,.041,.043,0]],18),C.pants,kn);
    [[.012,.15],[-.012,-.1]].forEach(([y,a])=>pz(rbox(.05,.004,.008,.002),C.pantsD,kn,-sx*.013,y,.052,[a,0,0])); // creases behind the knee
    pz(organ([[-.285,.041,.039,.043,-sx*.002],[-.31,.047,.045,.049,-sx*.001],[-.335,.046,.045,.048,0]],18,1),C.pants,kn); // where the trousers bunch into the boot
    pz(organ([[-.335,.0435,.0425,.0455,-sx*.001],[-.388,.0435,.0435,.0455,0]],18,1),C.pantsD,kn);                           // cuff""",
    """    const ps=opts.pantStyle||'plain', shorts=ps==='shorts';
    pz(organ([[.05,.07,.08,.084,sx*.004],[-.03,.086,.094,.1,sx*.003],[-.12,.083,.09,.093,sx*.001],[-.24,.07,.076,.074,-sx*.006],[-.34,.058,.062,.06,-sx*.011],[-.4,.055,.061,.055,-sx*.013],[-.44,.052,.056,.052,-sx*.013]],18),C.pants,hp);
    if(shorts) pz(organ([[-.36,.0605,.0645,.0625,-sx*.012],[-.405,.0595,.0655,.0595,-sx*.013],[-.43,.0585,.0645,.0585,-sx*.013]],18,1),C.pantsD,hp); // the hem of the shorts
    if(ps==='cargo'){ part(rbox(.055,.095,.03,.01),C.pantsD,hp,sx*.082,-.2,-.005,[0,0,sx*.04],null,0.004); part(rbox(.057,.028,.032,.008),C.pantsD,hp,sx*.082,-.158,-.005,[0,0,sx*.04],null,0.003); } // thigh pocket and its flap
    const kn=grp(hp,0,-.4,0);
    pz(organ([[.05,.054,.058,.054,-sx*.013],[.0,.055,.063,.054,-sx*.013],[-.06,.054,.052,.062,-sx*.011],[-.13,.057,.047,.07,-sx*.009],[-.22,.047,.042,.055,-sx*.005],[-.3,.039,.037,.041,-sx*.002],[-.385,.041,.041,.043,0]],18),shorts?C.skin:C.pants,kn);
    if(ps==='knee') pz(organ([[.06,.059,.064,.059,-sx*.013],[.0,.06,.07,.059,-sx*.013],[-.07,.058,.06,.066,-sx*.011],[-.11,.055,.052,.066,-sx*.01]],18),C.accent,kn); // knee pad
    if(!shorts) [[.012,.15],[-.012,-.1]].forEach(([y,a])=>pz(rbox(.05,.004,.008,.002),C.pantsD,kn,-sx*.013,y,.052,[a,0,0])); // creases behind the knee
    if(!shorts) pz(organ([[-.285,.041,.039,.043,-sx*.002],[-.31,.047,.045,.049,-sx*.001],[-.335,.046,.045,.048,0]],18,1),C.pants,kn); // where the trousers bunch into the boot
    pz(organ([[-.335,.0435,.0425,.0455,-sx*.001],[-.388,.0435,.0435,.0455,0]],18,1),shorts?0xf3efe4:C.pantsD,kn);              // cuff, or a sock
    if(shorts) pz(organ([[-.3,.0415,.0395,.0435,-sx*.002],[-.335,.0445,.0435,.0465,-sx*.001]],18,1),0xf3efe4,kn);""")

# ---- the Locker: a Back bling row ----
rep("""      <h3 class="lk">Pickaxe</h3>
      <div id="picks" class="outfits picks" role="listbox" aria-label="Pickaxe"></div>""",
    """      <h3 class="lk">Back bling</h3>
      <p class="lkempty">Take it off, or wear any back bling you own on any outfit.</p>
      <div id="backs" class="outfits picks backs" role="listbox" aria-label="Back bling"></div>
      <h3 class="lk">Pickaxe</h3>
      <div id="picks" class="outfits picks" role="listbox" aria-label="Pickaxe"></div>""")
rep("""  const wear=()=>reskin(localHero,OUTFITS[outfitIdx(settings.outfit)],PICKAXES[pickIdx(settings.pickaxe)].id);""",
    """  const wear=()=>reskin(localHero,OUTFITS[outfitIdx(settings.outfit)],PICKAXES[pickIdx(settings.pickaxe)].id,settings.back||'auto');
  const bbox=$('backs');""")
rep("""  const PRICE={o:{common:800,uncommon:1200,rare:1500,epic:2000,legendary:2500},p:{common:200,uncommon:200,rare:400,epic:400,legendary:800},e:{common:200,uncommon:200,rare:400,epic:400,legendary:800}}; // in Crank Bux
  const FREE={o:'rook',p:'steel'}, owned=(k,it)=>(k==='e'?!it.shop:it.id===FREE[k])||wallet.owned.includes(k+':'+it.id), price=(k,it)=>PRICE[k][it.rarity]||800;""",
    """  const PRICE={o:{common:800,uncommon:1200,rare:1500,epic:2000,legendary:2500},p:{common:200,uncommon:200,rare:400,epic:400,legendary:800},e:{common:200,uncommon:200,rare:400,epic:400,legendary:800},b:{common:0,uncommon:300,rare:500,epic:600,legendary:900}}; // in Crank Bux
  const FREE={o:'rook',p:'steel',b:'none'}, owned=(k,it)=>(k==='e'?!it.shop:it.id===FREE[k])||wallet.owned.includes(k+':'+it.id)||(k==='b'&&OUTFITS.some(o=>(o.back||'pack')===it.kind&&owned('o',o))), price=(k,it)=>PRICE[k][it.rarity]||800;
  if(settings.back&&settings.back!=='auto'&&!owned('b',BACKS[backIdx(settings.back)])){ settings.back='auto'; saveSettings(); }""")
rep("""    buy.hidden=false; buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'}""",
    """    buy.hidden=false; buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':k==='b'?'back bling':'pickaxe'}""")
rep("""    if(k==='o') pick(it.id); else if(k==='e') pickEm(it.id); else pickPk(it.id); });""",
    """    if(k==='o') pick(it.id); else if(k==='e') pickEm(it.id); else if(k==='b') pickBk(it.id); else pickPk(it.id); });""")
rep("""  window.renderShop=()=>{ [['o',box,OUTFITS],['p',pbox,PICKAXES],['e',$('emotesBox'),EMOTE_LIST]].forEach(([k,el,list])=>list.forEach(it=>{ const b=el.querySelector(`[data-id="${it.id}"]`); if(!b) return;
      const own=owned(k,it); b.hidden=!own; b.classList.remove('locked','afford'); const pr=b.querySelector('.price'); if(pr) pr.remove(); }));""",
    """  window.renderShop=()=>{ [['o',box,OUTFITS],['p',pbox,PICKAXES],['e',$('emotesBox'),EMOTE_LIST],['b',bbox,BACKS]].forEach(([k,el,list])=>list.forEach(it=>{ const b=el.querySelector(`[data-id="${it.id}"]`); if(!b) return;
      const own=owned(k,it); b.hidden=!own; b.classList.remove('locked','afford'); const pr=b.querySelector('.price'); if(pr) pr.remove(); }));
    { const b=bbox.querySelector('[data-id="auto"]'); if(b) b.hidden=false; }""")
rep("""  PICKAXES.forEach(p=>{ const b=document.createElement('button'); b.type='button'; b.className='ofit '+p.rarity; b.dataset.id=p.id; b.setAttribute('role','option');""",
    """  const pickBk=id=>{ if(id!=='auto'){ const it=BACKS[backIdx(id)]; if(!owned('b',it)){ offerBuy('b',it); return; } } buy.hidden=true; settings.back=id; saveSettings(); wear(); mark(bbox,id); window._stagePrev=null; };
  [{id:'auto',name:"Outfit's own",rarity:'common'}].concat(BACKS).forEach(p=>{ const b=document.createElement('button'); b.type='button'; b.className='ofit '+p.rarity; b.dataset.id=p.id; b.setAttribute('role','option');
    b.innerHTML=`<span>${p.name}<small>${p.id==='auto'?'default':p.rarity}</small></span>`; b.addEventListener('click',()=>pickBk(p.id)); bbox.appendChild(b); });
  mark(bbox,settings.back||'auto');
  PICKAXES.forEach(p=>{ const b=document.createElement('button'); b.type='button'; b.className='ofit '+p.rarity; b.dataset.id=p.id; b.setAttribute('role','option');""")
rep("""  window._locker={owned,price,pick,pickPk,pickEm,offerBuy};""","""  window._locker={owned,price,pick,pickPk,pickEm,pickBk,offerBuy};""")
# portraits for the back bling cards: the back bling alone, seen from behind
rep("""    r.dispose(); if(r.forceContextLoss) r.forceContextLoss();
  }catch(e){} },60);""","""    { const bcam=new THREE.PerspectiveCamera(30,1,0.05,10); bcam.position.set(0,.02,2.1); bcam.lookAt(0,.0,0);
      [{id:'auto'}].concat(BACKS).forEach(bk=>{ const h=heroFor(OUTFITS[0],'steel',bk.id==='auto'?'auto':bk.id), pg=h.rig.pack; pg.parent.remove(pg); pg.position.set(0,0,0); pg.rotation.set(0,0,0); pg.updateMatrixWorld(true);
        const bb=new THREE.Box3().setFromObject(pg); if(bb.isEmpty()) return; const cc=bb.getCenter(new THREE.Vector3()), sz=bb.getSize(new THREE.Vector3()), k=Math.min(1,.62/Math.max(sz.x,sz.y,.3)); pg.position.sub(cc).multiplyScalar(k); pg.scale.setScalar(k); sc.add(pg);
        r.render(sc,bcam); const img=new Image(); img.alt=''; img.src=r.domElement.toDataURL('image/png'); sc.remove(pg);
        const b=bbox.querySelector(`[data-id="${bk.id}"]`); if(b) b.prepend(img); }); }
    r.dispose(); if(r.forceContextLoss) r.forceContextLoss();
  }catch(e){} },60);""")

# ---- other players see your back bling ----
rep("""o:outfitIdx(settings.outfit),p:pickIdx(settings.pickaxe),s:[""","""o:outfitIdx(settings.outfit),p:pickIdx(settings.pickaxe),b:settings.back&&settings.back!=='auto'?backIdx(settings.back):-1,s:[""")
rep("""  if(m.o!=null&&OUTFITS[m.o]){ if(pl.o!==m.o&&net.role==='host') party.syncT=0; pl.o=m.o; reskin(pl.h,OUTFITS[m.o],(PICKAXES[m.p]||PICKAXES[0]).id); }""",
    """  if(m.o!=null&&OUTFITS[m.o]){ if(pl.o!==m.o&&net.role==='host') party.syncT=0; pl.o=m.o; reskin(pl.h,OUTFITS[m.o],(PICKAXES[m.p]||PICKAXES[0]).id,m.b>=0&&BACKS[m.b]?BACKS[m.b].id:'auto'); }""")
# the lobby stage and the loading screen show yours
rep("""o:lk.o!=null?lk.o:outfitIdx(settings.outfit),pk:lk.pk||settings.pickaxe,ready:true};""","""o:lk.o!=null?lk.o:outfitIdx(settings.outfit),pk:lk.pk||settings.pickaxe,bk:lk.bk||settings.back||'auto',ready:true};""")
assert s.count("const h=heroFor(OUTFITS[x.o]||OUTFITS[0],x.pk);")==2
s=s.replace("const h=heroFor(OUTFITS[x.o]||OUTFITS[0],x.pk);","const h=heroFor(OUTFITS[x.o]||OUTFITS[0],x.pk,x.bk);")
# the local hero starts with it on
rep("""const localHero=heroFor(OUTFITS[outfitIdx(settings.outfit)],PICKAXES[pickIdx(settings.pickaxe)].id), hero=localHero.group;""",
    """const localHero=heroFor(OUTFITS[outfitIdx(settings.outfit)],PICKAXES[pickIdx(settings.pickaxe)].id,settings.back||'auto'), hero=localHero.group;""")

# ---- pickaxe heads: a symmetric head on the handle, both ends arching toward the handle from the handle (none curl back up
# toward the hand); the mask is a mask over the nose and mouth, not a band across the eyes ----
rep("""    part(rbox(.05,.08,.1,.02),C.metalL,ph,0,0,0);
    part(rbox(.035,.05,.3,.012),C.steel,ph,0,.015,-.17,[-.25,0,0]);
    part(rbox(.03,.045,.18,.01),C.steel,ph,0,.01,.12,[.35,0,0]);""",
    """    part(rbox(.05,.08,.1,.02),C.metalL,ph,0,0,0);
    part(bladeGeo([0,1,2,3,4].map(q=>new THREE.Vector3(0,.012+.0085*q*q,-.04-.075*q)),.034,.056,.014),C.steel,ph); // the point: one curve, arching toward the handle
    part(bladeGeo([0,1,2,3].map(q=>new THREE.Vector3(0,.012+.0085*q*q,.04+.06*q)),.03,.05,.03),C.steel,ph);     // the flat blade behind it, the same sweep""")
rep("""    part(rbox(.06,.09,.11,.025),0xffc94a,ph,0,0,0);
    part(rbox(.04,.055,.32,.014),0xffd970,ph,0,.015,-.18,[-.25,0,0]);
    part(rbox(.034,.05,.2,.012),0xffd970,ph,0,.01,.13,[.35,0,0]);""",
    """    part(rbox(.06,.09,.11,.025),0xffc94a,ph,0,0,0);
    part(bladeGeo([0,1,2,3,4].map(q=>new THREE.Vector3(0,.014+.009*q*q,-.045-.08*q)),.038,.06,.016),0xffd970,ph);
    part(bladeGeo([0,1,2,3].map(q=>new THREE.Vector3(0,.014+.009*q*q,.045+.065*q)),.034,.054,.034),0xffd970,ph);""")
# the ice scythe and the summit axe curled up toward the hand: now they sweep down
rep("""    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,.02+.012*q*q,-.07-.085*q)),.02,.075,.02),0x9fe3ff,ph); // the blade, one curved piece
    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,-.016-q*.006+.012*q*q,-.07-.085*q)),.022,.012,.006),glow(0xeaffff),ph,0,0,0,null,null,0); // its glowing edge""",
    """    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,.0+.012*q*q,-.07-.085*q)),.02,.075,.02),0x9fe3ff,ph); // the blade, one curved piece, arching toward the handle
    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,-.016-q*.006+.012*q*q,-.07-.085*q)),.022,.012,.006),glow(0xeaffff),ph,0,0,0,null,null,0); // its glowing edge, on the inside of the curve
    part(bladeGeo([0,1,2].map(q=>new THREE.Vector3(0,.0+.012*q*q,.05+.05*q)),.018,.05,.02),0x9fe3ff,ph); // a short counter-blade so the head balances""")
rep("""    part(bladeGeo([0,1,2,3,4,4.6].map(q=>new THREE.Vector3(0,.015*q*q-.005,-.03-.06*q)),.016,.04,.01),0xc9d2dc,ph); // the tooth, one curved piece
    part(rbox(.012,.06,.09,.004),0xc9d2dc,ph,0,.01,.07,[.3,0,0]);""",
    """    part(bladeGeo([0,1,2,3,4,4.6].map(q=>new THREE.Vector3(0,.005+.014*q*q,-.03-.06*q)),.016,.04,.01),0xc9d2dc,ph); // the tooth, one curved piece, arching toward the handle
    part(bladeGeo([0,1,2].map(q=>new THREE.Vector3(0,.005+.014*q*q,.03+.045*q)),.014,.05,.028),0xc9d2dc,ph); // the adze, the same sweep""")
# the Bone Breaker's horns curled toward the hand too
rep("""    [[-1,.32],[1,.2]].forEach(([d,len])=>{ const c=new THREE.ConeGeometry(.035,len,10); c.rotateX(d<0?-Math.PI/2:Math.PI/2); part(c,0xf2ead6,ph,0,.02,d*(len/2+.04),[d*-.25,0,0]); });""",
    """    [[-1,.32],[1,.2]].forEach(([d,len])=>{ const c=new THREE.ConeGeometry(.035,len,10); c.rotateX(d<0?-Math.PI/2:Math.PI/2); part(c,0xf2ead6,ph,0,.0,d*(len/2+.04),[d*-.22,0,0]); });""")
# the Breach Tool's adze tilted up: level, arching toward the handle
rep("""    part(rbox(.03,.08,.13,.01),0x6b7380,ph,0,-.005,.1,[.25,0,0]);""","""    part(bladeGeo([0,1,2].map(q=>new THREE.Vector3(0,.0+.012*q*q,.04+.05*q)),.028,.06,.03),0x6b7380,ph);""")
# the mask
rep("""    part(new THREE.SphereGeometry(.13,24,12,Math.PI*1.5-1.3,2.6,Math.PI*.44,Math.PI*.42),C.jacket,rig.head,0,.135,0,null,[1.06,1,1.06],0.005);
    part(new THREE.CylinderGeometry(.126,.126,.04,22,1,true),C.accent,rig.head,0,.19,0,null,[1,1,1.05],0);
    [-1,1].forEach(sx=>part(rbox(.035,.22,.008,.004),C.accent,rig.head,sx*.03,.09,.13,[-.35,0,sx*.25],null,0.003));
    rig.mouth.visible=false;""",
    """    const mD=new THREE.Color(C.accent).multiplyScalar(.7).getHex();
    part(maskGeo(),C.accent,rig.head,0,.135,0,null,null,0.005);
    { const a=new THREE.Vector3(0,.128,-.145), b=new THREE.Vector3(0,.016,-.113), m=a.clone().add(b).multiplyScalar(.5), d=b.clone().sub(a); // the seam down the middle
      part(rbox(.006,d.length(),.006,.002),mD,rig.head,m.x,m.y,m.z,[Math.atan2(d.z,-d.y),0,0],null,0); }
    [-1,1].forEach(sx=>[0,1,2].forEach(q=>part(rbox(.026,.0045,.004,.002),new THREE.Color(C.accent).multiplyScalar(.45).getHex(),rig.head,sx*(.047+q*.004),.088-q*.013,-.1135+q*.0025,[0,sx*.55,0],null,0))); // filter vents, flush with the mask
    part(new THREE.CylinderGeometry(.121,.121,.014,22,1,true,-Math.PI/2,Math.PI),mD,rig.head,0,.1,0,null,[1.02,1,1.06],0); // the strap round the back of the head
    rig.mouth.visible=false;""")

# ---- the Item Shop sells back bling too (one each rotation) ----
rep("""e:pick(EMOTE_LIST.filter(e=>e.shop),5,'e')}; }""","""e:pick(EMOTE_LIST.filter(e=>e.shop),5,'e'),b:pick(BACKS.filter(b=>b.id!=='none'),5,'b')}; }""")
rep("""SHOP_N={o:3,p:2,e:2}; // 3 outfits, 2 pickaxes, 2 dances""","""SHOP_N={o:3,p:2,e:2,b:1}; // 3 outfits, 2 pickaxes, 2 dances, a back bling""")
rep("""return [...ids.o.slice(0,3),...ids.p.slice(0,2),...ids.e.slice(0,2)]; }""","""return [...ids.o.slice(0,3),...ids.p.slice(0,2),...ids.e.slice(0,2),...ids.b.slice(0,1)]; }""")
rep("""for(const kk of ['o','p','e']) next.push(""","""for(const kk of ['o','p','e','b']) next.push(""")
rep("""return [k,k==='o'?OUTFITS.find(o=>o.id===id):k==='p'?PICKAXES.find(p=>p.id===id):EMOTE_LIST.find(e=>e.id===id)]; }).filter(x=>x[1]); }""",
    """return [k,k==='o'?OUTFITS.find(o=>o.id===id):k==='p'?PICKAXES.find(p=>p.id===id):k==='b'?BACKS.find(b=>b.id===id):EMOTE_LIST.find(e=>e.id===id)]; }).filter(x=>x[1]); }""")
rep("""document.querySelector(`#${k==='o'?'outfits':'picks'} [data-id="${it.id}"] img`);""","""document.querySelector(`#${k==='o'?'outfits':k==='b'?'backs':'picks'} [data-id="${it.id}"] img`);""")
rep("""`<small class="kind">${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'}</small>`""","""`<small class="kind">${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':k==='b'?'back bling':'pickaxe'}</small>`""")
rep("""window._stagePickT=performance.now()+12000; } else { window._stageLook=null;""","""window._stagePickT=performance.now()+12000; } else if(k==='b'){ window._stageLook={bk:it.id}; window._stagePrev=null; } else { window._stageLook=null;""")
rep("""      if(own){ if(k==='o') L.pick(it.id); else if(k==='e') L.pickEm(it.id); else L.pickPk(it.id);""","""      if(own){ if(k==='o') L.pick(it.id); else if(k==='e') L.pickEm(it.id); else if(k==='b') L.pickBk(it.id); else L.pickPk(it.id);""")
# the Locker stage rebuilds when the back bling changes; back bling card pictures fill the card
rep("""key=L.map(x=>x.o+'/'+x.pk+'/'+x.name+'/'+(x.ready?1:0)).join('|');""","""key=L.map(x=>x.o+'/'+x.pk+'/'+(x.bk||'auto')+'/'+x.name+'/'+(x.ready?1:0)).join('|');""")
rep("""k=Math.min(1,.62/Math.max(sz.x,sz.y,.3));""","""k=Math.min(2.4,.66/Math.max(sz.x,sz.y,.12));""")

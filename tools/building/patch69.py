# ---------- 69. dances: five new emotes to buy (Floss, Robot, Hype, Disco Fever, Shuffle), an Emotes section in the
# Locker (the one you pick plays on your Emote key, and your hero shows it off in the lobby), and a bigger Item Shop:
# 3 outfits, 2 pickaxes and 2 dances each rotation ----------
rep("const EMOTES={wave:{name:'Wave',dur:2.6},dance:{name:'Groove',dur:12,beat:1.9},cheer:{name:'Cheer',dur:2.4},salute:{name:'Salute',dur:2.2}};\nconst EMOTE_IDS=Object.keys(EMOTES);",
"""const EMOTES={wave:{name:'Wave',dur:2.6,rarity:'common'},dance:{name:'Groove',dur:12,beat:1.9,rarity:'uncommon'},cheer:{name:'Cheer',dur:2.4,rarity:'common'},salute:{name:'Salute',dur:2.2,rarity:'common'},
  floss:{name:'Floss',dur:10,beat:2.2,rarity:'rare',shop:1},robot:{name:'Robot',dur:10,beat:2.2,rarity:'uncommon',shop:1},hype:{name:'Hype',dur:8,beat:2.1,rarity:'uncommon',shop:1},
  disco:{name:'Disco Fever',dur:10,beat:2,rarity:'epic',shop:1},shuffle:{name:'Shuffle',dur:10,beat:2,rarity:'rare',shop:1}};
const EMOTE_IDS=Object.keys(EMOTES), EMOTE_LIST=EMOTE_IDS.map(id=>Object.assign({id},EMOTES[id]));""")
rep("    else if(id==='cheer'){",r"""    else if(id==='floss'){ const b=t*Math.PI*2*1.6, s=Math.sin(b), q=Math.sin(b*2);
      T.shL=0.75*s; T.shR=-0.75*s; T.shLz=-0.3+0.7*s; T.shRz=0.3+0.7*s; T.elL=T.elR=0.12;
      T.hipsZ+=-0.13*s; T.hipsY+=0.12*q; T.chZ+=0.06*s; T.hipY+=-0.02-0.015*Math.abs(q); T.knL+=-0.15*Math.max(0,s); T.knR+=-0.15*Math.max(0,-s); T.nkZ=-0.06*s; }
    else if(id==='robot'){ const n=Math.floor(t*2.2), f=Math.min(1,(t*2.2-n)*5), K=[[1.57,1.57,0,0,0.5],[1.57,0.2,1.57,1.57,-0.5],[0.3,1.57,1.57,0.2,0.5],[1.57,1.57,1.57,1.57,0]], a=K[n%4], p=K[(n+3)%4], L=i=>p[i]+(a[i]-p[i])*f;
      T.shL=L(0); T.shR=L(1); T.elL=L(2); T.elR=L(3); T.nkY=L(4)*0.6; T.chY+=L(4)*0.2; T.shLz=-0.12; T.shRz=0.12; T.knL+=-0.12*(n%2); T.knR+=-0.12*((n+1)%2); }
    else if(id==='hype'){ const b=t*Math.PI*2*2.1, s=Math.sin(b), d=1-Math.abs(s), p1=Math.max(0,s), p2=Math.max(0,-s);
      T.hipY+=-0.06*d; T.knL+=-0.45*d; T.knR+=-0.45*d; T.hpL+=0.2*d; T.hpR+=0.2*d;
      T.shR=1.0+1.9*p1; T.elR=1.5-1.3*p1; T.shL=1.0+1.9*p2; T.elL=1.5-1.3*p2; T.shLz=-0.3; T.shRz=0.3; T.nkX+=0.1*s; T.chX+=-0.06*Math.abs(s); }
    else if(id==='disco'){ const b=t*Math.PI*2, up=Math.sin(b)>0?1:0, sw=Math.sin(b*2);
      T.shR=lerp(0.4,2.75,up); T.shRz=lerp(-0.35,0.55,up); T.elR=0.08; T.shL=0.1; T.shLz=-0.3; T.elL=0.45; // one arm loose at the side, the other points up, then down across
      T.hipsZ+=0.12*sw; T.chZ+=-0.08*sw; T.knL+=-0.25*Math.max(0,sw); T.knR+=-0.25*Math.max(0,-sw); T.nkY=up?0.35:-0.2; T.nkX+=up?-0.2:0.15; }
    else if(id==='shuffle'){ const b=t*Math.PI*2*2, s=Math.sin(b), c=Math.cos(b);
      T.hpL+=0.5*Math.max(0,s); T.knL+=-0.9*Math.max(0,s); T.hpR+=0.5*Math.max(0,-s); T.knR+=-0.9*Math.max(0,-s); T.hpLz=-0.15*Math.max(0,-c); T.hpRz=0.15*Math.max(0,c);
      T.hipY+=-0.03+0.03*Math.abs(c); T.hipsY+=0.25*s; T.chY+=-0.3*s; T.shL=0.7*s; T.shR=-0.7*s; T.elL=T.elR=1.35; T.shLz=-0.2; T.shRz=0.2; }
    else if(id==='cheer'){""")
# prices and the buy flow know about dances
rep("const PRICE={o:{common:150,uncommon:300,rare:600,epic:1000,legendary:1600},p:{common:100,uncommon:200,rare:400,epic:700,legendary:1100}};",
    "const PRICE={o:{common:150,uncommon:300,rare:600,epic:1000,legendary:1600},p:{common:100,uncommon:200,rare:400,epic:700,legendary:1100},e:{common:100,uncommon:250,rare:450,epic:700,legendary:1000}};")
rep("buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':'pickaxe'} ·","buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'} ·")
rep("    if(k==='o') pick(it.id); else pickPk(it.id); });","    if(k==='o') pick(it.id); else if(k==='e') pickEm(it.id); else pickPk(it.id); });")
rep("window.renderShop=()=>{ [['o',box,OUTFITS],['p',pbox,PICKAXES]].forEach(","window.renderShop=()=>{ [['o',box,OUTFITS],['p',pbox,PICKAXES],['e',$('emotesBox'),EMOTE_LIST]].forEach(")
rep('      <div id="picks" class="outfits picks" role="listbox" aria-label="Pickaxe"></div>','''      <div id="picks" class="outfits picks" role="listbox" aria-label="Pickaxe"></div>
      <h3 class="lk">Emotes</h3>
      <p class="lkempty">The one you pick plays on your Emote key.</p>
      <div id="emotesBox" class="outfits picks emotes" role="listbox" aria-label="Emote"></div>''')
rep("  window._locker={owned,price,pick,pickPk,offerBuy};",r"""  const ebox=$('emotesBox');
  const pickEm=id=>{ const it=EMOTE_LIST.find(e=>e.id===id); if(!it) return; if(!owned('e',it)){ offerBuy('e',it); return; } buy.hidden=true; settings.emote=id; saveSettings(); mark(ebox,id); window._stagePrev={id,t0:performance.now()}; };
  EMOTE_LIST.forEach(e=>{ const b=document.createElement('button'); b.type='button'; b.className='ofit '+e.rarity; b.dataset.id=e.id; b.setAttribute('role','option');
    b.innerHTML=emoteIcon(e.id)+`<span>${e.name}<small>${e.rarity}</small></span>`; b.addEventListener('click',()=>pickEm(e.id)); ebox.appendChild(b); });
  if(!owned('e',EMOTE_LIST.find(e=>e.id===settings.emote)||{})){ settings.emote='dance'; saveSettings(); }
  mark(ebox,settings.emote); renderShop();
  window._locker={owned,price,pick,pickPk,pickEm,offerBuy};""")
rep("function renderItemShop(){",r"""// a dancing figure for an emote card, posed a little differently for each dance
function emoteIcon(id){ const P={wave:[-40,150,0],dance:[-130,-50,1],cheer:[-150,-30,0],salute:[-40,-150,0],floss:[-20,200,1],robot:[-90,-90,0],hype:[-160,-20,1],disco:[-40,-20,1],shuffle:[-110,-70,1]}[id]||[-120,-60,1];
  const arm=(sx,deg)=>{ const a=deg*Math.PI/180, x2=50+sx*8+Math.cos(a)*22*sx, y2=38+Math.sin(a)*22; return `<line x1="${50+sx*8}" y1="38" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>`; };
  return `<svg class="emo" viewBox="0 0 100 100" aria-hidden="true"><g stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none"><circle cx="50" cy="22" r="9" fill="#fff" stroke="none"/><line x1="50" y1="34" x2="50" y2="62"/>${arm(-1,P[0])}${arm(1,P[1])}<line x1="50" y1="62" x2="${P[2]?36:42}" y2="86"/><line x1="50" y1="62" x2="${P[2]?66:58}" y2="${P[2]?78:86}"/></g><g fill="#fff" opacity=".85"><circle cx="82" cy="30" r="5"/><rect x="85" y="10" width="3" height="21"/><circle cx="16" cy="44" r="4"/><rect x="18.5" y="28" width="2.5" height="17"/></g></svg>`; }
function renderItemShop(){""")
rep(".shopgrid .ofit img{object-fit:contain}",".shopgrid .ofit img{object-fit:contain} .ofit svg.emo{position:absolute;left:16%;top:8%;width:68%;height:62%;pointer-events:none;filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))} .picks.emotes .ofit svg.emo{top:4%;height:66%}")
# the shop: dance cards and the right wording
rep("    const src=document.querySelector(`#${k==='o'?'outfits':'picks'} [data-id=\"${it.id}\"] img`);\n    b.innerHTML=(src?`<img alt=\"\" src=\"${src.src}\">`:'')+",
    "    const src=k==='e'?null:document.querySelector(`#${k==='o'?'outfits':'picks'} [data-id=\"${it.id}\"] img`);\n    b.innerHTML=(k==='e'?emoteIcon(it.id):src?`<img alt=\"\" src=\"${src.src}\">`:'')+")
rep("sp.insertAdjacentHTML('beforeend',`<small class=\"kind\">${RNAME[it.rarity]} ${k==='o'?'outfit':'pickaxe'}</small>`);","sp.insertAdjacentHTML('beforeend',`<small class=\"kind\">${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'}</small>`);")
rep("b.addEventListener('click',()=>{ if(own){ if(k==='o') L.pick(it.id); else L.pickPk(it.id); toast('Equipped '+it.name);","b.addEventListener('click',()=>{ if(own){ if(k==='o') L.pick(it.id); else if(k==='e') L.pickEm(it.id); else L.pickPk(it.id); toast('Equipped '+it.name);")
# the lobby hero shows off a dance you just picked
rep("pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:null};",
    "pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:i===0&&window._stagePrev&&EMOTES[_stagePrev.id]&&performance.now()-_stagePrev.t0<EMOTES[_stagePrev.id].dur*1000?{id:_stagePrev.id,t:(performance.now()-_stagePrev.t0)/1000}:null};")
rep(".mtab{display:grid;gap:14px;min-width:0}",".mtab{display:grid;gap:14px;min-width:0;align-content:start}")
rep("Get more outfits and pickaxes in the <b>Item Shop</b>.","Get more outfits, pickaxes and dances in the <b>Item Shop</b>.")
# dancing: the "pickaxe at the ready" arm pose doesn't override the dance (it was bending the right arm of every emote)
rep("  } else if(S.gun===false&&!building){","  } else if(S.gun===false&&!building&&!emo){")

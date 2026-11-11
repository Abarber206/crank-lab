/* ---------- full map: the whole island, north up (M, bindable, or tap the minimap) ----------
   The hillshade is painted once, the first time the map opens; roads, towns and players go on top. */
var mapOpen=false, bigMapImg=null;
function renderBigMapImage(){
  const S=1024, c=document.createElement('canvas'); c.width=c.height=S; const g=c.getContext('2d'), img=g.createImageData(S,S), d=img.data, {ROCK,SNOW}=WORLD;
  const mpp=2*WHALF/S, LX=-0.5, LY=0.75, LZ=-0.43; // lit from the north-west
  for(let py=0;py<S;py++){ const v=-WHALF+(py+0.5)*mpp, j=Math.min(WN-1,Math.round((v+WHALF)/WHS)), j0=Math.max(0,j-1), j1=Math.min(WN-1,j+1);
    for(let px=0;px<S;px++){ const u=-WHALF+(px+0.5)*mpp, i=Math.min(WN-1,Math.round((u+WHALF)/WHS)), i0=Math.max(0,i-1), i1=Math.min(WN-1,i+1), q=j*WN+i, h=WH[q];
      const gx=(WH[j*WN+i1]-WH[j*WN+i0])/((i1-i0)*WHS), gz=(WH[j1*WN+i]-WH[j0*WN+i])/((j1-j0)*WHS), nl=Math.sqrt(1+gx*gx+gz*gz);
      const lit=(-gx*LX+LY-gz*LZ)/nl, k=Math.max(0.3,Math.min(1.3,0.35+0.87*lit));
      const hi=Math.max(0,Math.min(1,(h-18)/80)), rk=ROCK[q]/255, sn=SNOW[q]/255;
      let r=93+(146-93)*hi, gg=143+(156-143)*hi, b=62+(86-62)*hi;
      r+=(128-r)*rk; gg+=(126-gg)*rk; b+=(122-b)*rk; r+=(240-r)*sn; gg+=(244-gg)*sn; b+=(248-b)*sn;
      const out=u*u+v*v>MAP_R*MAP_R?0.72:1, o=(py*S+px)*4;
      d[o]=Math.min(255,r*k*out); d[o+1]=Math.min(255,gg*k*out); d[o+2]=Math.min(255,b*k*out*(out<1?1.08:1)); d[o+3]=255; } }
  g.putImageData(img,0,0);
  const X=u=>(u+WHALF)/mpp;
  g.lineCap='round'; g.lineJoin='round';
  for(const [w,col] of [[7,'#26282c'],[3.6,'#9a9ea4']]){ g.strokeStyle=col; g.lineWidth=w;
    for(const rd of WORLD.roads){ g.beginPath(); rd.pts.forEach((p,k)=>k?g.lineTo(X(p[0]),X(p[1])):g.moveTo(X(p[0]),X(p[1]))); g.stroke(); }
    g.fillStyle=col; WORLD.towns.forEach(t=>{ g.beginPath(); g.arc(X(t.u),X(t.v),(PLAZA_R/mpp)+w/2+1,0,7); g.fill(); }); }
  g.setLineDash([10,8]); g.strokeStyle='rgba(255,255,255,.55)'; g.lineWidth=2; g.beginPath(); g.arc(X(0),X(0),MAP_R/mpp,0,7); g.stroke(); // the edge of the island
  g.setLineDash([]); g.strokeStyle='rgba(255,236,190,.8)'; g.lineWidth=2; g.beginPath(); g.arc(X(0),X(0),FLAT_R/mpp,0,7); g.stroke(); // the build field
  return c;
}
function drawBigMap(){
  if(!bigMapImg) return;
  const cv=$('bigmapC'), dpr=Math.min(2,devicePixelRatio||1), S=Math.round((cv.clientWidth||600)*dpr); if(cv.width!==S){ cv.width=cv.height=S; }
  const g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true; g.drawImage(bigMapImg,0,0,S,S);
  const k=S/(2*WHALF), X=x=>(x-SPAWN[0]+WHALF)*k, Z=z=>(z-SPAWN[2]+WHALF)*k, u=dpr*Math.max(0.8,Math.min(1.4,S/dpr/700));
  g.textAlign='center'; g.textBaseline='bottom'; g.font=`800 ${Math.round(12.5*u)}px "Chakra Petch",sans-serif`;
  TOWNS.forEach(t=>{ const px=X(t.x), pz=Z(t.z), q=u;
    g.fillStyle='#f6e7c6'; g.strokeStyle='#3a2a14'; g.lineWidth=1.4*q; g.beginPath(); g.moveTo(px,pz-7*q); g.lineTo(px+6*q,pz-1.5*q); g.lineTo(px+4.5*q,pz-1.5*q); g.lineTo(px+4.5*q,pz+5*q); g.lineTo(px-4.5*q,pz+5*q); g.lineTo(px-4.5*q,pz-1.5*q); g.lineTo(px-6*q,pz-1.5*q); g.closePath(); g.fill(); g.stroke();
    g.lineWidth=3.5*q; g.strokeStyle='rgba(0,0,0,.75)'; g.fillStyle='#fff'; g.strokeText(t.name,px,pz-9*q); g.fillText(t.name,px,pz-9*q); });
  const dot=(x,z,col)=>{ g.fillStyle=col; g.strokeStyle='#fff'; g.lineWidth=1.6*u; g.beginPath(); g.arc(X(x),Z(z),5*u,0,7); g.fill(); g.stroke(); };
  net.players.forEach(pl=>dot(pl.pos.x,pl.pos.z,'#'+(sameTeam(pl)?(horde.on?0x3f8fff:TEAM_COL[pl.team]):pl.id==='bot'?0xff4b3a:colorFor(pl.id)).toString(16).padStart(6,'0')));
  if(B&&B.active&&B.h.group.visible) dot(B.pos.x,B.pos.z,'#ff4b3a');
  // you: an arrow pointing where you face, with a soft pulse so it's easy to find
  const px=X(P.pos.x), pz=Z(P.pos.z), pulse=(performance.now()/900)%1;
  g.strokeStyle=`rgba(255,255,255,${0.7*(1-pulse)})`; g.lineWidth=2*u; g.beginPath(); g.arc(px,pz,(8+16*pulse)*u,0,7); g.stroke();
  g.save(); g.translate(px,pz); g.rotate(-P.yaw); g.fillStyle='#fff'; g.strokeStyle='#0d1726'; g.lineWidth=1.8*u;
  g.beginPath(); g.moveTo(0,-10*u); g.lineTo(7.5*u,8.5*u); g.lineTo(0,4.5*u); g.lineTo(-7.5*u,8.5*u); g.closePath(); g.fill(); g.stroke(); g.restore();
  g.textAlign='left'; g.font=`800 ${Math.round(13*u)}px "Chakra Petch",sans-serif`; g.fillStyle='rgba(255,255,255,.9)'; g.fillText('N',S/2-4*u,20*u);
}
function toggleMap(on){
  const want=on==null?!mapOpen:!!on; if(want===mapOpen) return; mapOpen=want;
  if(mapOpen&&!bigMapImg) bigMapImg=renderBigMapImage();
  $('bigmap').hidden=!mapOpen;
  if(mapOpen){ $('bigmapHint').textContent=isTouch?'Tap the map to close':codeName(settings.binds.map||'KeyM')+' or click to close'; drawBigMap(); }
}
$('miniWrap').addEventListener('pointerdown',e=>{ e.preventDefault(); e.stopPropagation(); if(playing) toggleMap(true); });
$('bigmap').addEventListener('pointerdown',e=>{ e.preventDefault(); e.stopPropagation(); toggleMap(false); });

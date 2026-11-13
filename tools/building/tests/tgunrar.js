// guns by rarity: the inventory pictures of each gun at every rarity it comes in, as one sheet
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,WEAPONS,BASE_WEAPONS,renderIcon,RARITIES'),{vp:{width:900,height:600}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.WEAPONS,null,{timeout:180000});
 const u=await pg.evaluate(async()=>{ const bases=Object.keys(T.BASE_WEAPONS), rows=[]; for(const bs of bases){ const ids=Object.keys(T.WEAPONS).filter(k=>T.WEAPONS[k].base===bs||k===bs).sort((a,c)=>T.RARITIES.indexOf(T.WEAPONS[a].rarity)-T.RARITIES.indexOf(T.WEAPONS[c].rarity)); rows.push([bs,ids]); }
   const S=96, c=document.createElement('canvas'); c.width=110+S*5; c.height=rows.length*S; const g=c.getContext('2d'); g.fillStyle='#20242c'; g.fillRect(0,0,c.width,c.height); g.font='12px sans-serif';
   const bg={common:'#5a6068',uncommon:'#2f6e2a',rare:'#1f4f8a',epic:'#55307e',legendary:'#8a5e18'};
   for(let r=0;r<rows.length;r++){ const [bs,ids]=rows[r]; g.fillStyle='#ccc'; g.fillText(bs,6,r*S+S/2);
     for(const id of ids){ const k=T.RARITIES.indexOf(T.WEAPONS[id].rarity), x=110+k*S, y=r*S; g.fillStyle=bg[T.WEAPONS[id].rarity]; g.fillRect(x+2,y+2,S-4,S-4); const im=new Image(); im.src=T.renderIcon(id); await new Promise(res=>{ im.onload=res; im.onerror=res; }); g.drawImage(im,x+4,y+4,S-8,S-8); } }
   return c.toDataURL('image/png'); });
 require('fs').writeFileSync('/home/claude/work/gun_rarity.png',Buffer.from(u.split(',')[1],'base64'));
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

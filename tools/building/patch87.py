# ---------- 87. furniture with variety: every piece comes in several colourways (fabrics and wood tones), corner rooms get a
# second piece on their other wall, and a chest is never placed inside a piece of furniture ----------
import re
a=s.index("  } else if(p.kind==='furn'){ const F=["); b=s.index("  } else if(p.kind==='rock'){",a)
blk=s[a:b].replace("variant===","fv===")
blk=blk.replace("  } else if(p.kind==='furn'){ const F=[0x6b7f99,0x9a5f4a,0x7d8c5a,0x8a6fa0][q()*4|0], wood=0x8a5a36, dk=0x5e3d24;",
  "  } else if(p.kind==='furn'){ const fv=variant%10, sty=Math.floor(variant/10)%6, F=[0x6b7f99,0x9a5f4a,0x7d8c5a,0x8a6fa0,0x3f5d6b,0xb08a4a][sty], wood=[0x8a5a36,0xa87a4a,0x5e4630,0xc9a878,0x6e4a3a,0x8f6a48][sty], dk=[0x5e3d24,0x7a5632,0x3a2a1c,0x9a7c52,0x4a3026,0x5f4630][sty];")
s=s[:a]+blk+s[b:]
rep("        const p=add('furn',x,z,1,yaw); p.ft=ft; p.yard=true; p.g.children[0].geometry=propVariant('furn',ft).geo; p.base=l*LVL; p.g.position.y=p.base; p.boxes=propBoxes(p); } } } } }",
r"""        const sty=(h.id*3+l+(q()*3|0))%6; // a house keeps to a couple of colourways
        const put=(ft,x,z,yaw)=>{ const p=add('furn',x,z,1,yaw); p.ft=ft; p.yard=true; p.g.children[0].geometry=propVariant('furn',ft+10*sty).geo; p.base=l*LVL; p.g.position.y=p.base; p.boxes=propBoxes(p); return p; };
        put(ft,x,z,yaw);
        // a corner room: something else from the same room against its other wall, if the two don't crowd each other
        const sd2=ok.find(o=>o!==sd); if(sd2){ const ft2=pool.find(f=>f!==ft&&!(SZ[f][1]>1.2&&Dp>1.2)); if(ft2!=null){ const [W2,D2]=SZ[ft2], al2=sd2[2]?1:0, off2=TALL[ft2]?(q()<0.5?-1:1)*(2.5-0.2-W2/2):(q()-.5)*0.6;
            const x2=sd2[0]+sd2[2]*(D2/2+0.03)+(al2?0:off2), z2=sd2[1]+sd2[3]*(D2/2+0.03)+(al2?off2:0);
            const hx1=along?Dp/2:W/2, hz1=along?W/2:Dp/2, hx2=al2?D2/2:W2/2, hz2=al2?W2/2:D2/2;
            if(Math.abs(x-x2)>hx1+hx2+0.35||Math.abs(z-z2)>hz1+hz2+0.35) put(ft2,x2,z2,Math.atan2(-sd2[2],-sd2[3])); } } } } } } }""")
# chests step clear of furniture
rep("function addChest(x,y,z,yaw){","""function addChest(x,y,z,yaw){ { const hit=(cx,cz)=>propsNear(cx,cz,[],1).some(p=>p.kind==='furn'&&Math.abs(p.base-y)<1&&p.boxes&&p.boxes.some(b=>cx+0.6>b[0]&&cx-0.6<b[3]&&cz+0.6>b[2]&&cz-0.6<b[5]));
    if(hit(x,z)){ const bx=(Math.floor(x/CELL)+0.5)*CELL, bz=(Math.floor(z/CELL)+0.5)*CELL; let done=false; for(const r of [0.7,1.1,1.5,1.8]){ for(let k=0;k<8&&!done;k++){ const nx=bx+Math.cos(k*Math.PI/4)*r, nz=bz+Math.sin(k*Math.PI/4)*r; if(!hit(nx,nz)){ x=nx; z=nz; done=true; } } if(done) break; } } }""")

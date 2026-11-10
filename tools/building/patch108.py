# ---------- 108. the sea: beyond the coastal town the outer mountains open onto a bay and open water, with a sand beach,
# rippling reflective water, wading and swimming, and the lighthouse out on the shore ----------
rep("const TOWN_NAMES=['Rustwood','Pebble Point',","const TOWN_NAMES=['Pebble Point','Rustwood',")
rep("function planHouses(t){","[TOWN_THEME[0],TOWN_THEME[1]]=[TOWN_THEME[1],TOWN_THEME[0]];\nfunction planHouses(t){")
rep("    const de=d+70*fbm(u*0.002,v*0.002,2,20), oR=","    const hb=h; let rid=0.42;\n    const de=d+70*fbm(u*0.002,v*0.002,2,20), oR=")
rep("      h+=oR*(50+(170+230*oR)*ridged(wu*0.0016,wv*0.0016,6,21,0.44)); }","      rid=ridged(wu*0.0016,wv*0.0016,6,21,0.44); h+=oR*(50+(170+230*oR)*rid); }")
rep("    h*=s; return h<0?0:h; }\n  return {genH,MASSIFS};","""    h*=s;
    seaLast=0;
    if(SEA){ const al=u*SEA.nx+v*SEA.nz; if(al>SEA.C0-130){ const lat=v*SEA.nx-u*SEA.nz, ang=Math.atan2(Math.abs(lat),al);
      if(ang<0.85){ // the sides of the bay follow the mountains: crests run out to sea as headlands, valleys drown as coves, and neither side is straight
        const out=sstep(SEA.C0+20,SEA.C0+260,al), rng=Math.min(1,oR*4);
        const aE=ang+0.34*(rid-0.42)*out*rng+0.085*fbm(u*0.0042+9.1,v*0.0042,2,93)*(0.4+0.6*out)+0.03*fbm(u*0.013,v*0.013+4.4,2,94)*out, A=lat<0?0.21:0.27, w=1-sstep(A,A+0.15,aE);
        if(w>0){ seaLast=w; const c=seaC=al-SEA.C0-0.0005*lat*lat-18*fbm(lat*0.006+3.1,al*0.006,2,91), bed=c<0?SEA.Y+0.25-c*0.05:SEA.Y-0.15-Math.min(9,c*0.05), b=sstep(-75,-18,c), g0=Math.max(0,hb*s), h0=h<0?0:h; return h0+((g0+(bed-g0)*b)-h0)*w; } } } } // (inland stays at or above 0, as everywhere else: only the bay floods)
    return h<0?0:h; }
  // the sea: a sector of the rim (toward one town) where the outer range gives way to a beach and open water
  let SEA=null, seaLast=0, seaC=0;
  const seaW=(u,v)=>{ if(!SEA) return 0; const al=u*SEA.nx+v*SEA.nz; if(al<=SEA.C0-130||Math.atan2(Math.abs(v*SEA.nx-u*SEA.nz),al)>=0.85) return 0; genH(u,v); return seaLast; };
  return {genH,MASSIFS,setSea:s=>{ SEA=s; },sea:()=>SEA,seaW,seaTop:()=>SEA?SEA.Y+1.4:-1e9,sandAt:(u,v,h)=>{ if(!SEA||h>SEA.Y+2.6) return 0; const w=seaW(u,v); return w>0?sstep(SEA.Y+2.6,SEA.Y+1.3,h)*w*sstep(-125,-75,seaC):0; }}; // sand only along the shore""")
rep("  for(const t of towns){ if(o.snap){ const q=o.snap(t.u,t.v); t.u=q[0]; t.v=q[1]; } t.h=Math.max(o.LVL,Math.round(t.avg/o.LVL)*o.LVL); t.R=o.townR; }",
"""  for(const t of towns){ if(o.snap){ const q=o.snap(t.u,t.v); t.u=q[0]; t.v=q[1]; } t.h=Math.max(o.LVL,Math.round(t.avg/o.LVL)*o.LVL); t.R=o.townR; }
  if(o.gen.setSea&&towns.length){ const t=towns[0], d=Math.sqrt(t.u*t.u+t.v*t.v); o.gen.setSea({nx:t.u/d,nz:t.v/d,C0:d+115,Y:t.h-5.5}); // below any natural ground, so only the bay floods // the first town is the coastal one
    for(let j=0;j<N;j++){ const v=-HALF+j*HS; for(let i=0;i<N;i++){ const u=-HALF+i*HS; if(o.gen.seaW(u,v)>0) H0[j*N+i]=genH(u,v); } } }""")
rep("avoid[j*M+i]=d>MAP_R-40?-1:d<FLAT_R+2?300:0; }","avoid[j*M+i]=d>MAP_R-40||(gh[j*M+i]<o.gen.seaTop()&&o.gen.seaW(u,v)>0)?-1:d<FLAT_R+2?300:0; }")
rep("  return {N,H0,H,RD,ROCK,SNOW,GRASS,at,towns,roads,edges:edges.length};","""  // sand and water: SAND is how sandy a cell is, WS the height of the water surface over it (-1e4 where it is dry)
  const SAND=new Uint8Array(N*N), WS=new Float32Array(N*N).fill(-1e4), sea=o.gen.sea();
  if(sea) for(let j=0;j<N;j++){ const v=-HALF+j*HS; for(let i=0;i<N;i++){ const u=-HALF+i*HS, w=o.gen.seaW(u,v); if(w<=0) continue; const c=j*N+i, h=H[c], sd=o.gen.sandAt(u,v,h);
    SAND[c]=Math.round(255*sd); if(sd>0.25) GRASS[c]=0; if(sd>0.5) ROCK[c]=Math.round(ROCK[c]*0.3); if(h<sea.Y&&w>0.02) WS[c]=sea.Y; } }
  return {N,H0,H,RD,ROCK,SNOW,GRASS,SAND,WS,at,towns,roads,edges:edges.length};""")
rep("    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.9,0.93,0.97)*(0.9+0.12*rk.r),clamp(vCover.y,0.0,1.0)); }","    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.66,0.58,0.41)*(0.84+0.3*rk.g),clamp(-vCover.z,0.0,1.0)*smoothstep(0.5,0.78,normalize(vWN).y)); // sand (a negative third cover value; not on cliff faces)\n    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.9,0.93,0.97)*(0.9+0.12*rk.r),clamp(vCover.y,0.0,1.0)); }")
rep("cov[k*3+2]=st===1?WORLD.DIRT[q]/255:0; },4*st+2);","cov[k*3+2]=WORLD.SAND[q]?-WORLD.SAND[q]/255:st===1?WORLD.DIRT[q]/255:0; },4*st+2);")
rep("cov[k*3+1]=sstep(line,line+24,h)*sstep(0.58,0.78,ny); cov[k*3+2]=0; },30);","cov[k*3+1]=sstep(line,line+24,h)*sstep(0.58,0.78,ny); cov[k*3+2]=-WGEN.sandAt(u,v,h); },30);")
rep("function terrainUnder(x,z){ let m=terrainH(x,z); for(const s of SAMP){ const t=terrainH(x+s[0],z+s[1]); if(t>m) m=t; } return m; }",
    "function terrainUnder(x,z){ let m=terrainH(x,z); for(const s of SAMP){ const t=terrainH(x+s[0],z+s[1]); if(t>m) m=t; } const w=waterAt(x,z)-1.3; if(w>m) m=w; return m; } // deep water holds you up, chest deep")
rep("  let spd=E.crouch?CROUCH_SPD:RUN; if(fw<0&&Math.abs(fw)>=Math.abs(st)) spd*=0.9;","  let spd=E.crouch?CROUCH_SPD:RUN; if(fw<0&&Math.abs(fw)>=Math.abs(st)) spd*=0.9;\n  { const wd=waterAt(E.pos.x,E.pos.z)-terrainH(E.pos.x,E.pos.z); if(wd>0.35) spd*=wd>1.15?0.5:0.72; } // wading and swimming are slower")
rep("    if(slopeAt(x,z)[0]<0.3&&terrainH(x,z)<h0+70) return [x,z]; }","    if(slopeAt(x,z)[0]<0.3&&terrainH(x,z)<h0+70&&waterAt(x,z)<-999) return [x,z]; }")
rep("props.forEach(p=>{ if(!p.yard&&townAt(p.x,p.z,6)){","props.forEach(p=>{ if((!p.yard&&townAt(p.x,p.z,6))||shoreAt(p.x,p.z)){")
rep("vmax=paved?KMAX:KMAX_OFF;","vmax=(paved?KMAX:KMAX_OFF)*(waterAt(k.x,k.z)-terrainH(k.x,k.z)>0.55?0.15:1);")
rep("    TERR.outer.push(m); }\n})();","""    TERR.outer.push(m); }
})();
/* ---------- water ----------
   One material for all of it: ripples from three layers of a small tiling normal map, the sky mirrored by angle
   (Fresnel), the sun or moon glittering off it, the bed showing through in the shallows and foam at the edge. */
var WATER={mat:null,map:null,meshes:[]};
function waterAt(x,z){ const c=worldCell(x,z); return c<0?-1e4:WORLD.WS[c]; }
function shoreAt(x,z){ const c=worldCell(x,z); return c>=0&&(WORLD.WS[c]>-999||WORLD.SAND[c]>40); }
(function makeWater(){
  const NS=128, d=new Uint8Array(NS*NS*4), r=seeded(5150), waves=[]; while(waves.length<14){ const kx=Math.round((r()*2-1)*6), ky=Math.round((r()*2-1)*6); if(kx||ky) waves.push([kx,ky,r()*6.28,1/Math.hypot(kx,ky)]); }
  for(let y=0;y<NS;y++) for(let x=0;x<NS;x++){ let gx=0, gy=0; for(const [kx,ky,ph,a] of waves){ const c=Math.cos(2*Math.PI*(kx*x+ky*y)/NS+ph)*a; gx+=c*kx; gy+=c*ky; }
    const o=(y*NS+x)*4; d[o]=Math.max(0,Math.min(255,128+gx*26)); d[o+1]=Math.max(0,Math.min(255,128+gy*26)); d[o+2]=255; d[o+3]=255; }
  const nT=new THREE.DataTexture(d,NS,NS,THREE.RGBAFormat); nT.wrapS=nT.wrapT=THREE.RepeatWrapping; nT.magFilter=THREE.LinearFilter; nT.minFilter=THREE.LinearMipmapLinearFilter; nT.generateMipmaps=true; nT.needsUpdate=true;
  WATER.mat=new THREE.ShaderMaterial({ transparent:true, depthWrite:false, fog:false,
    uniforms:{ nT:{value:nT}, reflT:{value:(()=>{ const t=new THREE.DataTexture(new Uint8Array([0,0,0,255]),1,1,THREE.RGBAFormat); t.needsUpdate=true; return t; })()}, reflM:{value:new THREE.Matrix4()}, reflK:{value:0}, reflY:{value:0}, hT:{value:null}, seaA:{value:new THREE.Vector4(1,0,0,1)}, seaB:{value:new THREE.Vector4(1,0,0,0)}, seaO:{value:new THREE.Vector2(SPAWN[0],SPAWN[2])}, time:{value:0}, lum:{value:1}, sunDir:{value:SUN_DIR.clone()}, sunCol:{value:new THREE.Color(1,0.95,0.86)}, zen:{value:new THREE.Color(0x3f86d4)}, hor:{value:new THREE.Color(HAZE)}, fogCol:{value:new THREE.Color(HAZE)} },
    vertexShader:`attribute float depth; attribute vec2 flow; uniform float time; uniform vec4 seaA, seaB; uniform vec2 seaO; varying vec3 vW; varying float vDepth, vWash; varying vec2 vFlow; varying vec3 vSea;
      void main(){ vec4 w=modelMatrix*vec4(position,1.0); vDepth=depth; vFlow=flow;
        // along the beach the sea knows the ground under it exactly (a small map of heights), and it washes up and back: the whole sheet rises and falls a little there
        vec2 r=w.xz-seaO; float al=dot(r,seaA.xy), lat=r.y*seaA.x-r.x*seaA.y, inside=step(seaA.z,al)*step(al,seaA.z+seaA.w)*step(abs(lat),seaB.x)*(1.0-step(0.0001,dot(flow,flow)));
        vSea=vec3((vec2(al-seaA.z,lat+seaB.x)*0.5+0.5)/seaB.zw,inside);
        vWash=inside*0.15*(0.5+0.5*sin(time*0.9+lat*0.035+1.7*sin(lat*0.011))); w.y+=vWash;
        vW=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }`,
    fragmentShader:`uniform sampler2D nT, reflT, hT; uniform mat4 reflM; uniform float time, lum, reflK, reflY; uniform vec3 sunDir, sunCol, zen, hor, fogCol; varying vec3 vW; varying float vDepth, vWash; varying vec2 vFlow; varying vec3 vSea;
      #ifdef TONE_MAPPING
        #define TM(c) toneMapping(c)
      #else
        #define TM(c) (c)
      #endif
      void main(){ float dist=length(cameraPosition-vW); vec3 V=(cameraPosition-vW)/dist; float riv=step(0.0001,dot(vFlow,vFlow)), D=vDepth;
        if(vSea.z>0.5){ float hh=texture2D(hT,vSea.xy).r; D=hh<0.01?max(vDepth,3.0):3.0-5.0*hh+vWash; if(D<=0.0) discard; } // how deep it is here, to the centimetre
        // ripples: a slow swell and two finer layers. On a river the fine layers ride the current: two copies half a cycle apart, cross-faded, so they never smear
        float ph=fract(time*0.3), fw=abs(ph*2.0-1.0)*riv; vec2 pA=vW.xz-vFlow*(ph*3.3), pB=vW.xz-vFlow*(fract(ph+0.5)*3.3)+vec2(11.7,4.3), s2=vec2(-time*0.02,time*0.016), s3=vec2(time*0.03,-time*0.027);
        vec2 n1=(texture2D(nT,vW.xz*0.021+vec2(time*0.011,time*0.007)).xy-0.5)*(1.0-0.7*riv);
        vec2 n2=mix(texture2D(nT,pA*0.063+s2).xy,texture2D(nT,pB*0.063+s2).xy,fw)-0.5, n3=mix(texture2D(nT,pA*0.19+s3).xy,texture2D(nT,pB*0.19+s3).xy,fw)-0.5;
        float fade=1.0/(1.0+dist*0.012); vec2 a=(n1*1.1+n2*0.8+n3*0.5*fade)*(0.3+0.7*fade)*1.25;
        vec3 N=normalize(vec3(a.x,1.0,a.y));
        float F=0.03+0.97*pow(1.0-max(dot(N,V),0.0),5.0);
        vec3 R=reflect(-V,N); R.y=abs(R.y);
        float fg=min(1.0-exp(-dist*0.0011),0.92);
        vec3 mir=TM(mix(mix(hor,zen,pow(R.y,0.55)),fogCol,fg));                                              // with no mirror image: the sky, by angle
        if(reflK>0.0){ vec4 rc=reflM*vec4(vW,1.0); vec2 ruv=rc.xy/rc.w+a*vec2(0.022,0.05)/(1.0+dist*0.03);   // the mirror image, wobbled by the ripples
          mir=mix(mir,texture2D(reflT,clamp(ruv,0.003,0.997)).rgb,reflK*(1.0-smoothstep(0.35,1.4,abs(vW.y-reflY)))); } // (only water at the mirror's own level shows it)
        vec3 body=TM(mix(mix(vec3(0.20,0.62,0.66),vec3(0.03,0.22,0.36),smoothstep(0.0,4.5,D))*lum,fogCol,fg));
        vec3 col=mix(body,mir,F);
        float sr=max(dot(R,sunDir),0.0); col+=sunCol*(pow(sr,220.0)*2.2+pow(sr,28.0)*0.1)*(1.0-fg);          // glitter
        float fn=texture2D(nT,vW.xz*0.09+vec2(time*0.02,0.0)).x;
        float foam=(1.0-smoothstep(0.0,0.5,D))*smoothstep(0.35,0.6,fn+0.25*sin(time*1.3+vW.x*0.3+vW.z*0.2));
        foam=max(foam,(1.0-smoothstep(0.0,0.12,D))*0.9)*(1.0-0.75*riv);
        foam=max(foam,vSea.z*0.55*smoothstep(0.8,1.0,sin(D*6.5+time*1.5+fn*2.0))*smoothstep(0.06,0.3,D)*(1.0-smoothstep(0.55,1.2,D))); // lines of surf rolling in through the shallows
        foam*=smoothstep(0.0,0.05,D);
        col=mix(col,TM(mix(vec3(0.96,0.98,1.0)*(0.35+0.65*lum),fogCol,fg)),foam*0.85);
        float al=smoothstep(0.0,0.18,D)*mix(0.62,0.96,smoothstep(0.0,2.5,D)); al=max(al,F*smoothstep(0.0,0.1,D)); al=max(al,foam*0.8);
        gl_FragColor=vec4(col,al);
      }` });
  for(let c=0;c<WN*WN;c++) if(WORLD.SAND[c]>64||WORLD.WS[c]>-999) WORLD.GRASS[c]=0; // no grass on the beach or under water
  const S=WGEN.sea(); if(!S) return;
  // the sea: a fine sheet along the shore (it knows how deep it is at every point) and one big sheet out to the horizon
  const px=-S.nz, pz=S.nx, A0=S.C0-80, A1=S.C0+260, LW=470, ST=4, na=Math.round((A1-A0)/ST), nl=Math.round(2*LW/ST), pos=[], dep=[], fl=[], idx=[];
  for(let b=0;b<=nl;b++) for(let a=0;a<=na;a++){ const al=A0+a*ST, lat=-LW+b*ST, u=S.nx*al+px*lat, v=S.nz*al+pz*lat; pos.push(SPAWN[0]+u,S.Y,SPAWN[2]+v); dep.push(Math.max(0,Math.min(9,S.Y-terrainH(SPAWN[0]+u,SPAWN[2]+v)))); fl.push(0,0); }
  { const hw=Math.round((A1-A0)/2)+1, hh=Math.round(LW)+1, hd=new Uint8Array(hw*hh); // the ground along the shore, every 2 m, from 3 m under the sea to 2 m over it
    for(let j=0;j<hh;j++) for(let i=0;i<hw;i++){ const al=A0+i*2, lat=-LW+j*2; hd[j*hw+i]=Math.max(0,Math.min(255,Math.round((terrainH(SPAWN[0]+S.nx*al+px*lat,SPAWN[2]+S.nz*al+pz*lat)-S.Y+3)/5*255))); }
    const hT=new THREE.DataTexture(hd,hw,hh,THREE.LuminanceFormat); hT.magFilter=hT.minFilter=THREE.LinearFilter; hT.needsUpdate=true; const wu=WATER.mat.uniforms; wu.hT.value=hT; wu.seaA.value.set(S.nx,S.nz,A0,A1-A0); wu.seaB.value.set(LW,S.Y,hw,hh); }
  for(let b=0;b<nl;b++) for(let a=0;a<na;a++){ const k=b*(na+1)+a; idx.push(k,k+na+1,k+1, k+1,k+na+1,k+na+2); }
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('depth',new THREE.Float32BufferAttribute(dep,1)); g.setAttribute('flow',new THREE.Float32BufferAttribute(fl,2)); g.setIndex(idx); g.computeBoundingSphere();
  const P4=(al,lat)=>[SPAWN[0]+S.nx*al+px*lat,S.Y,SPAWN[2]+S.nz*al+pz*lat], far=[[A1,-LW,3600,LW],[A0,-2600,3600,-LW],[A0,LW,3600,2600]], fp=[], fd=[], ff=[], fi=[];
  far.forEach(([a0,l0,a1,l1],q)=>{ fp.push(...P4(a0,l0),...P4(a1,l0),...P4(a0,l1),...P4(a1,l1)); fd.push(9,9,9,9); ff.push(0,0,0,0,0,0,0,0); fi.push(q*4,q*4+2,q*4+1, q*4+1,q*4+2,q*4+3); });
  const g2=new THREE.BufferGeometry(); g2.setAttribute('position',new THREE.Float32BufferAttribute(fp,3)); g2.setAttribute('depth',new THREE.Float32BufferAttribute(fd,1)); g2.setAttribute('flow',new THREE.Float32BufferAttribute(ff,2)); g2.setIndex(fi); g2.computeBoundingSphere();
  for(const gg of [g,g2]){ const m=new THREE.Mesh(gg,WATER.mat); m.matrixAutoUpdate=false; m.renderOrder=2; scene.add(m); WATER.meshes.push(m); }
  // the rivers: a ribbon of water down each one, level across, carrying its current
  for(const rv of WORLD.rivers||[]){ const p=rv.pts, n=p.length, AC=[-1.2,-0.85,-0.45,0,0.45,0.85,1.2], NC=AC.length, rp=[], rd=[], rf=[], ri=[]; let endQ=n-1;
    if(rv.into>=0){ const J=p[n-1], iw=WORLD.rivers[rv.into].pts[rv.jq][3]; while(endQ>2&&Math.hypot(p[endQ-1][0]-J[0],p[endQ-1][1]-J[1])<iw*0.5) endQ--; } // it stops well inside the water it joins
    else for(let q=0;q<n;q++) if(p[q][2]<=S.Y+0.02){ endQ=Math.min(n-1,q+6); break; }                                                              // or where it reaches the sea
    for(let q=0;q<=endQ;q++){ const a=p[Math.max(0,q-1)], b=p[Math.min(n-1,q+1)]; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl; const hw=p[q][3], fade=Math.min(1,q/3,rv.into>=0?1:(endQ-q)/3), sp=rv.main?0.8:1.1;
      for(const c of AC){ rp.push(SPAWN[0]+p[q][0]-tz*hw*c,p[q][2],SPAWN[2]+p[q][1]+tx*hw*c); rd.push(Math.max(0,p[q][5]*(1-c*c))*fade); rf.push(tx*sp,tz*sp); } }
    for(let q=0;q<endQ;q++) for(let c=0;c<NC-1;c++){ const k=q*NC+c; ri.push(k,k+1,k+NC, k+1,k+NC+1,k+NC); }
    const rg=new THREE.BufferGeometry(); rg.setAttribute('position',new THREE.Float32BufferAttribute(rp,3)); rg.setAttribute('depth',new THREE.Float32BufferAttribute(rd,1)); rg.setAttribute('flow',new THREE.Float32BufferAttribute(rf,2)); rg.setIndex(ri); rg.computeBoundingSphere();
    const m=new THREE.Mesh(rg,WATER.mat); m.matrixAutoUpdate=false; m.renderOrder=2; scene.add(m); WATER.meshes.push(m); }
  // for the maps: water and sand at 4 m a pixel
  const MS=Math.floor(WN/2), mc=document.createElement('canvas'); mc.width=mc.height=MS; const mg=mc.getContext('2d'), im=mg.createImageData(MS,MS);
  for(let j=0;j<MS;j++) for(let i=0;i<MS;i++){ const q=(j*2)*WN+i*2, o=(j*MS+i)*4, sd=WORLD.SAND[q]; if(WORLD.WS[q]>-999){ const dp=Math.min(1,(WORLD.WS[q]-WH[q])/5); im.data[o]=70-34*dp; im.data[o+1]=150-50*dp; im.data[o+2]=204-40*dp; im.data[o+3]=255; } else if(sd>20){ im.data[o]=222; im.data[o+1]=204; im.data[o+2]=158; im.data[o+3]=sd; } }
  mg.putImageData(im,0,0); WATER.map=mc;
  // where the nearest water is, on a coarse grid (for the mirror image): its level, and how far off it is
  const LC=32, LN=Math.ceil(2*WHALF/LC), lv=new Float32Array(LN*LN).fill(-1e4), ld=new Float32Array(LN*LN).fill(1e4), src=[], per=LC/WHS;
  for(let j=0;j<LN;j++) for(let i=0;i<LN;i++){ let best=-1e4; for(let b=0;b<per&&best<-999;b+=2) for(let a=0;a<per;a+=2){ const q=Math.min(WN-1,j*per+b)*WN+Math.min(WN-1,i*per+a); if(WORLD.WS[q]>-999){ best=WORLD.WS[q]; break; } }
    if(best>-999){ lv[j*LN+i]=best; ld[j*LN+i]=0; src.push(j*LN+i); } }
  for(let j=0;j<LN;j++) for(let i=0;i<LN;i++){ const k=j*LN+i; if(ld[k]===0) continue; let bd=1e9, bl=-1e4; for(const q of src){ const di=(q%LN)-i, dj=Math.floor(q/LN)-j, d=di*di+dj*dj; if(d<bd){ bd=d; bl=lv[q]; } } if(bd<1e9){ ld[k]=Math.sqrt(bd)*LC; lv[k]=bl; } }
  WATER.lv=lv; WATER.ld=ld; WATER.LN=LN; WATER.LC=LC;
})();""")
rep("function stepDusk(dt){ return stepSky(dt); }","""function stepDusk(dt){ stepSky(dt);
  if(WATER.mat){ const wu=WATER.mat.uniforms, c=PAL.cur; wu.time.value=performance.now()*0.001; wu.sunDir.value.copy(SUN_DIR); wu.sunCol.value.copy(sun.color).multiplyScalar(Math.min(1,sun.intensity));
    wu.zen.value.copy(c.zen); wu.hor.value.copy(c.hor); wu.fogCol.value.copy(scene.fog.color); wu.lum.value=Math.max(0.3,Math.min(1,0.3+0.55*sun.intensity+0.25*(1-TOD.night))); } }""")
# maps
rep("  const ox=P.pos.x, oz=P.pos.z, tx=x=>c+(x-ox)*sc, tz=z=>c+(z-oz)*sc;\n","  const ox=P.pos.x, oz=P.pos.z, tx=x=>c+(x-ox)*sc, tz=z=>c+(z-oz)*sc;\n  if(WATER.map){ const x0=SPAWN[0]-WHALF, z0=SPAWN[2]-WHALF, k=WATER.map.width/(2*WHALF); g.imageSmoothingEnabled=true; g.drawImage(WATER.map,(ox-R-x0)*k,(oz-R-z0)*k,2*R*k,2*R*k,tx(ox-R),tz(oz-R),2*R*sc,2*R*sc); }\n")
rep("      r+=(128-r)*rk; gg+=(126-gg)*rk; b+=(122-b)*rk; r+=(240-r)*sn; gg+=(244-gg)*sn; b+=(248-b)*sn;","      r+=(128-r)*rk; gg+=(126-gg)*rk; b+=(122-b)*rk; r+=(240-r)*sn; gg+=(244-gg)*sn; b+=(248-b)*sn;\n      { const sd=WORLD.SAND[q]/255; r+=(226-r)*sd; gg+=(208-gg)*sd; b+=(160-b)*sd; if(WORLD.WS[q]>-999){ const dp=Math.min(1,(WORLD.WS[q]-h)/5); r=(74-36*dp)/k; gg=(152-52*dp)/k; b=(206-40*dp)/k; } }")

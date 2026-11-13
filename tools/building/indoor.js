/* ---------- light indoors and under the trees ----------
   A map over the whole island says, for every metre, whether it's inside a house (and up to what height) and how thick
   the tree cover over it is. Every lit material looks it up by world position: indoors the sky's light falls to about a
   third and the sun's (where shadows don't already catch it) to two thirds, so rooms read as rooms; under a canopy the
   ground, grass, people and loot get the shade of the leaves. Trees themselves are left alone. */
const INDOOR={tex:null,dummy:null,N:2048,u:{map:{value:null},box:{value:new THREE.Vector4(0,0,0,400)}},mats:new WeakSet(),skip:new WeakSet(),t:0};
const INDOOR_GLSL=`
uniform sampler2D indoorMap; uniform vec4 indoorBox;
float indoorK(vec3 w,out float can){ can=0.0; if(indoorBox.z<=0.0) return 0.0; vec2 uv=(w.xz-indoorBox.xy)*indoorBox.z; if(uv.x<0.0||uv.y<0.0||uv.x>1.0||uv.y>1.0) return 0.0;
  vec4 t=texture2D(indoorMap,uv); float top=t.b*indoorBox.w-100.0, under=1.0-smoothstep(top-0.3,top+0.3,w.y); can=t.g*under; return t.r*under; }
`;
function indoorBuild(){ const N=INDOOR.N, W=WHALF*2, x0=SPAWN[0]-WHALF, z0=SPAWN[2]-WHALF, s=N/W, d=new Uint8Array(N*N*4), topEnc=y=>Math.max(0,Math.min(255,Math.round((y+100)/400*255)));
  const put=(x,z,ch,v,top)=>{ const i=Math.floor((x-x0)*s), j=Math.floor((z-z0)*s); if(i<0||j<0||i>=N||j>=N) return; const o=(j*N+i)*4; if(v>d[o+ch]){ d[o+ch]=v; } d[o+2]=Math.max(d[o+2],top); };
  // houses: the footprint, darkest well inside, easing off over the last metre or so to the walls
  for(const t of TOWNS) for(const h of (t.houses||[])){ const ax=h.i0*CELL, bx=(h.i0+h.w)*CELL, az=h.j0*CELL, bz=(h.j0+h.d)*CELL, top=topEnc(t.h+(h.floors||1)*LVL+0.15);
    for(let x=ax;x<=bx;x+=1/s) for(let z=az;z<=bz;z+=1/s){ const e=Math.min(x-ax,bx-x,z-az,bz-z), k=Math.max(0,Math.min(1,(e-0.2)/0.6)); if(k>0) put(x,z,0,Math.round(255*k*k*(3-2*k)),top); } }
  // the buildings at the named places: any floor with something built over it is indoors, up to that ceiling
  const cov=new Map(); pieces.forEach(p=>{ if(p.owner!=='world'||!p.town||!p.town.kind||p.type==='wall') return; const k=p.i+','+p.j; let a=cov.get(k); if(!a) cov.set(k,a=[]); a.push(p.l); });
  cov.forEach((ls,k)=>{ const [i,j]=k.split(',').map(Number); ls.sort((a,b)=>a-b); const t0=pieces.get(`f${i}_${j}_${ls[0]}`)?.town; for(let q=0;q+1<ls.length;q++){ const l=ls[q], top=topEnc(ls[q+1]*LVL-0.1);
      const open=(di,dj)=>{ const a=cov.get((i+di)+','+(j+dj)); return !a||!a.includes(l)||!a.some(x=>x>l); }, ax=i*CELL, bx=ax+CELL, az=j*CELL, bz=az+CELL;
      for(let x=ax;x<=bx;x+=1/s) for(let z=az;z<=bz;z+=1/s){ let e=9; if(open(-1,0)) e=Math.min(e,x-ax); if(open(1,0)) e=Math.min(e,bx-x); if(open(0,-1)) e=Math.min(e,z-az); if(open(0,1)) e=Math.min(e,bz-z);
        const kk=Math.max(0,Math.min(1,(e-0.2)/0.6)); if(kk>0) put(x,z,0,Math.round(255*kk*kk*(3-2*kk)),top); } } });
  // trees: a soft disc under each crown, up to the treetop
  if(FOREST.trees) for(const p of FOREST.trees){ const sc=p.s||1, R=(p.kind==='pine'?1.7:2.6)*sc+0.6, base=p.base!=null?p.base:terrainH(p.x,p.z), top=topEnc(base+6.5*sc);
    for(let x=p.x-R;x<=p.x+R;x+=1/s) for(let z=p.z-R;z<=p.z+R;z+=1/s){ const r=Math.hypot(x-p.x,z-p.z)/R; if(r>=1) continue; const k=1-r*r; put(x,z,1,Math.round(200*k),top); } }
  if(!INDOOR.tex){ INDOOR.tex=new THREE.DataTexture(d,N,N,THREE.RGBAFormat); INDOOR.tex.magFilter=INDOOR.tex.minFilter=THREE.LinearFilter; INDOOR.tex.generateMipmaps=false;
    INDOOR.dummy=new THREE.DataTexture(new Uint8Array(4),1,1,THREE.RGBAFormat); INDOOR.dummy.needsUpdate=true; }
  else INDOOR.tex.image.data=d;
  INDOOR.tex.needsUpdate=true; INDOOR.u.map.value=INDOOR.tex; INDOOR.u.box.value.set(x0,z0,1/W,400);
  // the trees' own materials keep their light
  const skipM=m=>{ if(!m) return; (Array.isArray(m)?m:[m]).forEach(x=>INDOOR.skip.add(x)); };
  for(const set of [FOREST.near,FOREST.mid,FOREST.far]) if(set) for(const k in set) for(const m of set[k]) skipM(m.material);
  if(IMP.mat) skipM(IMP.mat); props.forEach(p=>{ if(p.lazy&&p.g) p.g.traverse(o=>{ if(o.isMesh) skipM(o.material); }); });
  indoorTouch(); }
// give a lit material the lookup (once): it recompiles a single time
function indoorWrap(m){ if(INDOOR.mats.has(m)||INDOOR.skip.has(m)) return; const ph=m.isMeshPhongMaterial, la=m.isMeshLambertMaterial; if(!ph&&!la) return;
  INDOOR.mats.add(m); const prev=m.onBeforeCompile, key0=m.customProgramCacheKey();
  m.onBeforeCompile=(sh,r)=>{ if(prev) prev.call(m,sh,r); sh.uniforms.indoorMap=INDOOR.u.map; sh.uniforms.indoorBox=INDOOR.u.box;
    const fx='float a_=mix(1.0,0.5,ik_)*mix(1.0,0.62,cn_), d_=mix(1.0,0.3,ik_)*mix(1.0,0.8,cn_);';
    if(la&&sh.vertexShader.includes('#include <lights_lambert_vertex>')){ sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\n'+INDOOR_GLSL).replace('#include <lights_lambert_vertex>',`#include <lights_lambert_vertex>
  { vec4 iw_=vec4(transformed,1.0);
  #ifdef USE_INSTANCING
  iw_=instanceMatrix*iw_;
  #endif
  iw_=modelMatrix*iw_; float cn_; float ik_=indoorK(iw_.xyz,cn_); ${fx} vIndirectFront*=a_; vLightFront*=d_;
  #ifdef DOUBLE_SIDED
  vIndirectBack*=a_; vLightBack*=d_;
  #endif
  }`); }
    else if(ph&&sh.fragmentShader.includes('#include <lights_fragment_end>')){ sh.fragmentShader=sh.fragmentShader.replace('#include <common>','#include <common>\n'+INDOOR_GLSL).replace('#include <lights_fragment_end>',`#include <lights_fragment_end>
  { mat3 rt_=transpose(mat3(viewMatrix)); vec3 cp_=-(rt_*viewMatrix[3].xyz), wp_=cp_+rt_*(-vViewPosition); float cn_; float ik_=indoorK(wp_,cn_); ${fx}
    reflectedLight.indirectDiffuse*=a_; reflectedLight.directDiffuse*=d_; reflectedLight.directSpecular*=d_; }`); } };
  m.customProgramCacheKey=()=>'indoor|'+key0; m.needsUpdate=true; }
function indoorTouch(){ if(!INDOOR.tex) return; scene.traverse(o=>{ if(!o.isMesh||!o.material) return; if(Array.isArray(o.material)) o.material.forEach(indoorWrap); else indoorWrap(o.material); }); }
function stepIndoor(dt){ INDOOR.t-=dt; if(INDOOR.t<=0){ INDOOR.t=2; indoorTouch(); } }

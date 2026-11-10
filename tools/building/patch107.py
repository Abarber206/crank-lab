# ---------- 107. a day that passes: the sun crosses the sky, sets in orange and pink, the moon and stars come up over a
# dim blue night (never black), then sunrise. Sky, haze, light, shadows and clouds all follow. No grid on the minimap. ----------
rep("  const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({vertexColors:true,side:THREE.BackSide,fog:false,depthWrite:false})); m.renderOrder=-10; scene.add(m); return m; })();",
"""  const m=new THREE.Mesh(g,new THREE.ShaderMaterial({side:THREE.BackSide,fog:false,depthWrite:false,
    uniforms:{zen:{value:new THREE.Color(0x3f86d4)},mid:{value:new THREE.Color(0x8ec4e8)},hor:{value:new THREE.Color(HAZE)},glow:{value:new THREE.Color(0xfff2d6)},setCol:{value:new THREE.Color(0xff9a5a)},
      sunDir:{value:SUN_DIR.clone()},moonDir:{value:SUN_DIR.clone().negate()},sunK:{value:1},moonK:{value:0},starK:{value:0},setK:{value:0}},
    vertexShader:`varying vec3 vD; void main(){ vD=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader:`uniform vec3 zen,mid,hor,glow,setCol,sunDir,moonDir; uniform float sunK,moonK,starK,setK; varying vec3 vD;
      float hash(vec3 p){ p=fract(p*0.3183099+0.1); p*=17.0; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
      void main(){ vec3 v=normalize(vD); float h=max(v.y,0.0);
        vec3 c=h<0.25?mix(hor,mid,h/0.25):mix(mid,zen,min(1.0,(h-0.25)/0.6));
        float sr=dot(v,sunDir), sd=max(sr,0.0), md=max(dot(v,moonDir),0.0);
        c=mix(c,setCol,pow(1.0-h,5.0)*(0.25+0.75*pow(sr*0.5+0.5,2.0))*setK);                    // the sunset band along the horizon, strongest toward the sun
        c=mix(c,glow,min(1.0,(pow(sd,24.0)*0.85+pow(sd,4.0)*0.12)*sunK));
        c+=glow*smoothstep(0.99962,0.99985,sd)*sunK*1.4;                                        // the sun's disc
        vec3 q=v*170.0, f=fract(q)-0.5; float st=hash(floor(q));
        c+=vec3(0.86,0.92,1.0)*step(0.9978,st)*smoothstep(0.32,0.05,length(f))*(0.5+0.5*fract(st*91.7))*starK*smoothstep(0.03,0.3,v.y); // stars
        c+=vec3(0.5,0.62,0.95)*pow(md,110.0)*0.3*moonK; c=mix(c,vec3(0.95,0.96,1.0),smoothstep(0.99972,0.99984,md)*moonK); // the moon and its halo
        gl_FragColor=vec4(c,1.0);
        #include <tonemapping_fragment>
      }` })); m.renderOrder=-10; scene.add(m); return m; })();""")
# clouds take the colour of the light
rep("sunDir:{value:SUN_DIR.clone()}, haze:{value:new THREE.Color(HAZE)}, tint:{value:new THREE.Color(1,1,1)}","sunDir:{value:SUN_DIR.clone()}, haze:{value:new THREE.Color(HAZE)}, tint:{value:new THREE.Color(1,1,1)}, sunCol:{value:new THREE.Color(1,0.95,0.86)}",2)
rep("    fragmentShader:`uniform vec3 sunDir; uniform vec3 haze; uniform vec3 tint; varying vec3 vN;","    fragmentShader:`uniform vec3 sunDir; uniform vec3 haze; uniform vec3 tint; uniform vec3 sunCol; varying vec3 vN;")
rep("        col+=vec3(1.0,0.93,0.82)*pow(sun,6.0)*0.12;                       // warm sunlit highlights","        col+=sunCol*pow(sun,6.0)*0.12;                       // warm sunlit highlights\n        col*=mix(vec3(1.0),sunCol*vec3(1.0,1.053,1.163),0.8*wrap);        // the lit side takes the colour of the light")
rep("uniform vec3 camPos, sunDir, haze, tint; uniform float time, steps;","uniform vec3 camPos, sunDir, haze, tint, sunCol; uniform float time, steps;")
rep("            vec3 col=amb+vec3(1.0,0.95,0.86)*Ts*0.95*sil;","            vec3 col=amb+sunCol*Ts*0.95*sil;")
rep("u.haze.value.copy(cloudMat.uniforms.haze.value); }","u.haze.value.copy(cloudMat.uniforms.haze.value); u.sunCol.value.copy(cloudMat.uniforms.sunCol.value); u.sunDir.value.copy(SUN_DIR); }")
rep("function stepDusk(dt){\n","""/* Time of day. One full day takes TOD.len seconds and runs off the wall clock, so everyone in a party sees the same
   sky. The sun rides a tilted circle; when it is down the light comes from the moon opposite it. The light never
   comes from lower than about 14 degrees, and it fades right out at the moment sun hands over to moon. */
var TOD={len:960,fix:null,t:0,night:0};
const SKY_SUN=new THREE.Vector3().copy(SUN_DIR), _skyT=new THREE.Vector3();
const PAL=(()=>{ const C=h=>new THREE.Color(h), mk=o=>{ const r={}; for(const k in o) r[k]=C(o[k]); return r; };
  return { day:mk({zen:0x3f86d4,mid:0x8ec4e8,hor:HAZE,light:0xffe9c6,hemi:0xbddaff,tint:0xffffff,csun:0xfff2db,glow:0xfff2d6}),
           set:mk({zen:0x4668b0,mid:0xd79aa0,hor:0xffc890,light:0xffa868,hemi:0xdcc4d2,tint:0xffdcd0,csun:0xff9c62,glow:0xffd9a0}),
           night:mk({zen:0x141d44,mid:0x303b72,hor:0x4d5786,light:0x9fb8ff,hemi:0x8490c8,tint:0x8490c8,csun:0xa8c0ff,glow:0xfff2d6}),
           horde:mk({zen:0x2a2548,mid:0x4d4466,hor:0x4d4466,light:0xffb27a,hemi:0xbddaff,tint:0xc89aa8,csun:0xffb27a,glow:0xffd9a0}), cur:mk({zen:0,mid:0,hor:0,light:0,hemi:0,tint:0,csun:0,glow:0}) }; })();
function stepSky(dt){
  const want=horde.on?1:0; if(Math.abs(duskK-want)>0.001) duskK+=Math.sign(want-duskK)*Math.min(Math.abs(want-duskK),dt*0.6);
  const t=TOD.fix!=null?TOD.fix:((Date.now()/1000)%TOD.len)/TOD.len, E=0.2, PI=Math.PI, lr=(a,b,k)=>a+(b-a)*k, sm=(a,b,x)=>{ const k=Math.max(0,Math.min(1,(x-a)/(b-a))); return k*k*(3-2*k); };
  const th=t<0.6?lr(E,PI-E,t/0.6):t<0.68?lr(PI-E,PI+E,(t-0.6)/0.08):t<0.92?lr(PI+E,2*PI-E,(t-0.68)/0.24):lr(2*PI-E,2*PI+E,(t-0.92)/0.08); TOD.t=t;
  SKY_SUN.set(Math.cos(th),Math.sin(th)*0.866,Math.sin(th)*0.5); const el=SKY_SUN.y, sunW=sm(0,0.2,el), moonW=sm(0,0.2,-el), setK=1-sm(0,0.4,Math.abs(el-0.02)), nightK=sm(0.06,-0.18,el); TOD.night=nightK;
  // the light: from the sun, or from the moon opposite it; never lower than about 14 degrees
  { const tq=Math.round(th/0.0015)*0.0015; _skyT.set(Math.cos(tq),Math.sin(tq)*0.866,Math.sin(tq)*0.5).multiplyScalar(el>=0?1:-1); } // the light moves in small steps, so shadows hold still between them
  _skyT.y=Math.max(_skyT.y,0.25); SUN_DIR.copy(_skyT.normalize());
  _lX.set(0,1,0).cross(SUN_DIR).normalize(); _lY.copy(SUN_DIR).cross(_lX).normalize(); bounce.position.set(-SUN_DIR.x*40,-22,-SUN_DIR.z*40);
  const c=PAL.cur, hk=duskK*0.85; for(const k in c){ c[k].copy(PAL.day[k]).lerp(PAL.set[k],setK).lerp(PAL.night[k],nightK).lerp(PAL.horde[k],k==='light'||k==='csun'||k==='glow'?0:hk); }
  if(el>=0){ sun.color.copy(PAL.day.light).lerp(PAL.set.light,setK); sun.intensity=1.3*sunW*(1-0.28*setK)*(1-0.45*duskK); } else { sun.color.copy(PAL.night.light); sun.intensity=0.55*moonW*(1-0.2*duskK); }
  hemi.color.copy(c.hemi); hemi.intensity=0.6+0.14*(1-Math.max(sunW,moonW))+0.05*nightK-0.14*duskK; bounce.intensity=0.16*sunW*(1-duskK);
  scene.background.copy(c.mid); scene.fog.color.copy(c.hor); scene.fog.near=HAZE_DENS+(0.0042-HAZE_DENS)*duskK; scene.fog.far=HAZE_H-90*duskK;
  const u=skyDome.material.uniforms; u.zen.value.copy(c.zen); u.mid.value.copy(c.mid); u.hor.value.copy(c.hor); u.glow.value.copy(c.glow); u.sunDir.value.copy(SKY_SUN); u.moonDir.value.copy(SKY_SUN).negate();
  u.sunK.value=sm(-0.14,0.04,el)*(1-0.5*duskK); u.moonK.value=sm(0.0,0.1,-el)*(1-0.4*duskK); u.starK.value=nightK*(1-0.6*duskK); u.setK.value=setK*(1-0.7*duskK);
  if(cloudMat){ const cu=cloudMat.uniforms; cu.tint.value.copy(c.tint); cu.haze.value.copy(c.hor); cu.sunCol.value.copy(el>=0?c.csun:PAL.night.csun).multiplyScalar(el>=0?0.35+0.65*sunW:0.3+0.5*moonW); cu.sunDir.value.copy(SUN_DIR); }
}
function stepDusk(dt){ return stepSky(dt); }
function stepDuskOld(dt){
""")
rep("""  g.strokeStyle='rgba(225,245,200,.16)'; g.lineWidth=Math.max(1,dpr*.6);
  for(let gx=Math.ceil((ox-R)/CELL)*CELL; gx<=ox+R; gx+=CELL){ g.beginPath(); g.moveTo(tx(gx),0); g.lineTo(tx(gx),S); g.stroke(); }
  for(let gz=Math.ceil((oz-R)/CELL)*CELL; gz<=oz+R; gz+=CELL){ g.beginPath(); g.moveTo(0,tz(gz)); g.lineTo(S,tz(gz)); g.stroke(); }
""","")

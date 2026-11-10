# ---------- 23. volumetric, swirling clouds ----------
rep("// clouds drift with the wind and wrap around the sky\nfunction stepClouds(dt){",
r"""/* Volumetric clouds: a deck of real 3D cloud between 620 and 900 m (above every peak), ray-marched through
   layered noise that is warped through itself, so the shapes curl and swirl as they drift. Each sample is lit toward
   the sun (soft self-shadowed bellies, bright silver linings looking sunward) and fades into the haze far off.
   They are drawn at about a third of the screen's resolution into a texture, then laid over the sky behind
   everything (the deck is above all the terrain, so anything in front of a cloud really is in front of it).
   Settings > Clouds: Volumetric, Simple (the old puffs) or Off. */
const VCLOUD={on:false,rt:null,scene:null,cam:null,mat:null,sky:null,scale:isTouch?0.26:0.36};
function makeVolClouds(){
  const N=256, d=new Uint8Array(N*N*4), rnd=seeded(9181);
  for(let i=0;i<N*N;i++) d[i*4]=Math.floor(rnd()*256);
  for(let y=0;y<N;y++) for(let x=0;x<N;x++){ const i=y*N+x; d[i*4+1]=d[(((y+17)&255)*N+((x+37)&255))*4]; d[i*4+3]=255; } // G = R one slice up
  const nt=new THREE.DataTexture(d,N,N,THREE.RGBAFormat); nt.wrapS=nt.wrapT=THREE.RepeatWrapping; nt.magFilter=nt.minFilter=THREE.LinearFilter; nt.generateMipmaps=false; nt.needsUpdate=true;
  const mat=new THREE.ShaderMaterial({ depthTest:false, depthWrite:false,
    uniforms:{ noiseT:{value:nt}, camMat:{value:new THREE.Matrix4()}, projInv:{value:new THREE.Matrix4()}, camPos:{value:new THREE.Vector3()}, time:{value:0},
      sunDir:{value:SUN_DIR.clone()}, haze:{value:new THREE.Color(HAZE)}, tint:{value:new THREE.Color(1,1,1)}, steps:{value:isTouch?16:24} },
    vertexShader:`varying vec2 vN; void main(){ vN=position.xy; gl_Position=vec4(position.xy,0.0,1.0); }`,
    fragmentShader:`precision highp float;
      uniform sampler2D noiseT; uniform mat4 camMat, projInv; uniform vec3 camPos, sunDir, haze, tint; uniform float time, steps; varying vec2 vN;
      const float B0=620.0, B1=900.0;
      float n3(vec3 x){ vec3 p=floor(x), f=fract(x); f=f*f*(3.0-2.0*f); vec2 uv=p.xy+vec2(37.0,17.0)*p.z+f.xy; vec4 t=texture2D(noiseT,(uv+0.5)/256.0); return mix(t.r,t.g,f.z); }
      float fb2(vec3 p){ return 0.66*n3(p)+0.34*n3(p*2.03); }
      // the cloud field: warped twice through itself for the whirls; 'lite' skips the fine detail (for light samples)
      float dens(vec3 w,bool lite){ float h=(w.y-B0)/(B1-B0); if(h<0.0||h>1.0) return 0.0;
        vec3 q=vec3(w.x,w.z,w.y*1.3)*0.0016+vec3(time*0.010,time*0.004,time*0.002);
        vec2 a=vec2(fb2(q*0.5+vec3(0.0,0.0,time*0.006)),fb2(q*0.5+vec3(5.2,1.3,-time*0.005)));
        vec2 b=vec2(fb2(q*0.9+vec3(a*3.0,0.0)+vec3(1.7,9.2,0.0)),fb2(q*0.9+vec3(a*3.0,0.0)+vec3(8.3,2.8,0.0)));
        vec3 r=q+vec3(b*1.1-0.55,0.0);
        float f=0.53*n3(r)+0.27*n3(r*2.02)+0.13*n3(r*4.03); if(!lite) f+=0.07*n3(r*8.1);
        float shape=smoothstep(0.0,0.18,h)*smoothstep(1.0,0.5,h);  // flat-ish bases, rounded tops
        return clamp((f-0.5)*5.0,0.0,1.0)*shape; }
      void main(){
        vec4 v=projInv*vec4(vN,1.0,1.0); vec3 rd=normalize((camMat*vec4(v.xyz/v.w,0.0)).xyz), ro=camPos;
        if(abs(rd.y)<1e-4){ gl_FragColor=vec4(0.0); return; }
        float t0=(B0-ro.y)/rd.y, t1=(B1-ro.y)/rd.y; if(t0>t1){ float s=t0; t0=t1; t1=s; }
        t0=max(t0,0.0); if(t1<=0.0||t0>9000.0){ gl_FragColor=vec4(0.0); return; }
        t1=min(t1,t0+2600.0);
        float n=steps, dt=(t1-t0)/n, cosT=dot(rd,sunDir);
        float sil=1.0+2.2*pow(max(cosT,0.0),10.0);                                  // silver lining toward the sun
        float jit=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233)))*43758.5453);
        vec3 C=vec3(0.0); float Tr=1.0;
        for(int i=0;i<32;i++){ if(float(i)>=n||Tr<0.03) break;
          float t=t0+dt*(float(i)+jit); vec3 p=ro+rd*t; float d=dens(p,false);
          if(d>0.003){
            float l=dens(p+sunDir*45.0,true)*45.0+dens(p+sunDir*130.0,true)*85.0;
            float Ts=exp(-l*0.032), h=(p.y-B0)/(B1-B0);
            vec3 amb=mix(vec3(0.44,0.5,0.64),vec3(0.78,0.84,0.96),h*h*(3.0-2.0*h));
            vec3 col=amb+vec3(1.0,0.95,0.86)*Ts*0.95*sil;
            float a=1.0-exp(-d*0.034*dt);
            C+=Tr*a*col; Tr*=1.0-a; } }
        float A=1.0-Tr; if(A<0.002){ gl_FragColor=vec4(0.0); return; }
        vec3 col=C/A*tint; float far=smoothstep(1400.0,6500.0,t0);
        col=mix(col,haze,far*0.75); A*=1.0-smoothstep(5000.0,9000.0,t0);
        gl_FragColor=vec4(col*A,A); }` });
  const sc=new THREE.Scene(), q=new THREE.Mesh(new THREE.BufferGeometry().setAttribute('position',new THREE.Float32BufferAttribute([-1,-1,0,3,-1,0,-1,3,0],3)),mat); q.frustumCulled=false; sc.add(q);
  VCLOUD.scene=sc; VCLOUD.cam=new THREE.Camera(); VCLOUD.mat=mat;
  VCLOUD.rt=new THREE.WebGLRenderTarget(4,4,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat,depthBuffer:false,stencilBuffer:false});
  // laid over the sky behind the world: premultiplied colour, drawn before other see-through things
  const sky=new THREE.Mesh(new THREE.SphereGeometry(3000,24,12),new THREE.ShaderMaterial({ transparent:true, depthWrite:false, fog:false, side:THREE.BackSide,
    blending:THREE.CustomBlending, blendSrc:THREE.OneFactor, blendDst:THREE.OneMinusSrcAlphaFactor,
    uniforms:{tex:{value:VCLOUD.rt.texture},res:{value:new THREE.Vector2(1,1)}},
    vertexShader:`void main(){ gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader:`uniform sampler2D tex; uniform vec2 res; void main(){ gl_FragColor=texture2D(tex,gl_FragCoord.xy/res); }` }));
  sky.frustumCulled=false; sky.renderOrder=-6; scene.add(sky); VCLOUD.sky=sky; }
function setCloudMode(m){ settings.clouds=m; const vol=m==='volumetric';
  if(vol&&!VCLOUD.mat){ try{ makeVolClouds(); }catch(e){ console.warn('volumetric clouds unavailable',e); settings.clouds='simple'; return setCloudMode('simple'); } }
  VCLOUD.on=vol; if(VCLOUD.sky) VCLOUD.sky.visible=vol; clouds.forEach(c=>c.m.visible=m==='simple'); }
const _cv=new THREE.Vector2();
function renderClouds(){ if(!VCLOUD.on) return;
  renderer.getDrawingBufferSize(_cv); const w=Math.max(16,Math.round(_cv.x*VCLOUD.scale)), h=Math.max(16,Math.round(_cv.y*VCLOUD.scale));
  if(VCLOUD.rt.width!==w||VCLOUD.rt.height!==h) VCLOUD.rt.setSize(w,h);
  camera.updateMatrixWorld(); const u=VCLOUD.mat.uniforms; u.camMat.value.copy(camera.matrixWorld); u.projInv.value.copy(camera.projectionMatrixInverse); u.camPos.value.copy(camera.position);
  u.time.value=performance.now()*0.001; if(cloudMat){ u.tint.value.copy(cloudMat.uniforms.tint.value); u.haze.value.copy(cloudMat.uniforms.haze.value); }
  VCLOUD.sky.position.copy(camera.position); VCLOUD.sky.material.uniforms.res.value.copy(_cv);
  const prev=renderer.getRenderTarget(); renderer.setRenderTarget(VCLOUD.rt); renderer.render(VCLOUD.scene,VCLOUD.cam); renderer.setRenderTarget(prev); }
// clouds drift with the wind and wrap around the sky
function stepClouds(dt){""")
rep("makeClouds();\n","makeClouds(); setCloudMode(settings.clouds||'volumetric');\n")
rep("  renderer.render(scene,camera);\n  requestAnimationFrame(frame);","  renderClouds(); renderer.render(scene,camera);\n  requestAnimationFrame(frame);")
rep('<label for="grassSel">Grass detail','<label for="cloudSel">Clouds <select id="cloudSel"><option value="volumetric">Volumetric</option><option value="simple">Simple</option><option value="off">Off</option></select></label>\n          <label for="grassSel">Grass detail')
rep("  const gsl=$('grassSel');","  const csl=$('cloudSel'); csl.value=settings.clouds||'volumetric'; csl.addEventListener('change',()=>{ setCloudMode(csl.value); saveSettings(); });\n  const gsl=$('grassSel');")

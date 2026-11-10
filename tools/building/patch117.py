# ---------- 117. surfaces: gun metal, polymer, wood, paint, rubber and bright steel are drawn as materials, not flat colours.
# A part is given a surface kind; the merged model carries it per vertex and one shader adds the grain, wear on the
# edges, the right kind of shine and (for metal) a little of the sky reflected in it ----------
rep("function toon(c){ if(c&&c.isMaterial) return c;","""// what the sky lends to reflections in metal (dims at night)
const SURF_ENV={value:1};
const SURF_SH={1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1};
function surfShade(m,attr,glow){ m.onBeforeCompile=(sh,rnd)=>{ const gl2=!rnd||!rnd.capabilities||rnd.capabilities.isWebGL2;
    sh.uniforms.surfK={value:m.userData.surf||0}; sh.uniforms.surfEnv=SURF_ENV;
    sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\\nvarying vec3 vOP; varying float vSurf;\\n'+(attr?'attribute float surf;':'uniform float surfK;')+(glow?'\\nattribute float glow; varying float vGlow;':''))
      .replace('#include <begin_vertex>','#include <begin_vertex>\\n  vOP=position; vSurf='+(attr?'surf':'surfK')+';'+(glow?' vGlow=glow;':''));
    sh.fragmentShader=sh.fragmentShader.replace('#include <common>',`#include <common>
varying vec3 vOP; varying float vSurf; uniform float surfEnv;`+(glow?'\\nvarying float vGlow;':'')+`
float sh1(vec3 p){ p=fract(p*0.3183099+0.1); p*=17.0; return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
float sn(vec3 x){ vec3 i=floor(x), f=fract(x); f=f*f*(3.0-2.0*f);
  return mix(mix(mix(sh1(i),sh1(i+vec3(1,0,0)),f.x),mix(sh1(i+vec3(0,1,0)),sh1(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(sh1(i+vec3(0,0,1)),sh1(i+vec3(1,0,1)),f.x),mix(sh1(i+vec3(0,1,1)),sh1(i+vec3(1,1,1)),f.x),f.y),f.z); }`)
      .replace('void main() {','void main() {\\n  float sSpec=1.0, sShin=1.0, sMetal=0.0;')
      .replace('#include <color_fragment>',`#include <color_fragment>
  { float sK=floor(vSurf+0.5);
    if(sK>0.5){ vec3 p=vOP; float fine=sn(p*900.0), mid=sn(p*140.0);
      float ed=0.0;
`+(gl2?'#ifndef FLAT_SHADED\\n      ed=smoothstep(150.0,340.0,length(fwidth(normalize(vNormal)))/max(length(fwidth(vOP)),1e-6));\\n#endif\\n':'')+`
      if(sK<1.5){ // gun steel: a fine grain, hairline scratches along the gun, bare metal showing on the edges
        float scr=smoothstep(0.80,0.92,sn(vec3(p.x*1600.0,p.y*46.0,p.z*1600.0)));
        diffuseColor.rgb*=0.86+0.2*fine+0.1*mid; diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.5,0.52,0.54),0.14*scr+ed*(0.2+0.4*mid));
        sSpec=2.2; sShin=3.0; sMetal=0.4; }
      else if(sK<2.5){ // polymer: matt, finely stippled
        diffuseColor.rgb*=0.88+0.2*fine+0.06*mid; diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*1.5+0.03,ed*0.45); sSpec=0.9; sShin=0.7; }
      else if(sK<3.5){ // wood: grain running along the gun, darker rings, a few pores, oiled
        float w=sn(vec3(p.x*30.0,p.y*4.0,p.z*30.0)), g=0.5+0.5*sin((p.x*120.0+p.z*190.0+w*9.0)*6.2832), pore=smoothstep(0.78,0.9,sn(vec3(p.x*900.0,p.y*70.0,p.z*900.0)));
        diffuseColor.rgb*=mix(0.8,1.1,g)*(0.9+0.1*w)*(0.95+0.1*fine)*(1.0-0.22*pore); diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*0.7,ed*0.3); sSpec=1.8; sShin=2.2; }
      else if(sK<4.5){ // painted metal: mottled, chipped back to steel on the edges
        float chip=smoothstep(0.45,0.6,sn(p*260.0))*ed;
        diffuseColor.rgb*=0.88+0.14*mid+0.08*fine; diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.2,0.21,0.22)+0.2*fine,chip); sSpec=1.0; sShin=1.2; sMetal=0.06; }
      else if(sK<5.5){ // rubber or chequered grip: a fine diamond pattern
        float dm=abs(sin((p.y+p.z)*1500.0))*abs(sin((p.y-p.z)*1500.0)); diffuseColor.rgb*=0.72+0.4*dm; sSpec=0.5; sShin=0.6; }
      else if(sK<6.5){ // bright steel: brushed
        float br=sn(vec3(p.x*2200.0,p.y*30.0,p.z*2200.0)); diffuseColor.rgb*=0.84+0.2*br; sSpec=2.6; sShin=4.5; sMetal=0.6; }
      else if(sK<7.5){ // brass
        diffuseColor.rgb*=0.88+0.18*fine; sSpec=2.6; sShin=4.0; sMetal=0.5; }
      else { // glass: a lens
        sSpec=8.0; sShin=8.0; sMetal=1.0; } } }`)
      .replace('#include <lights_phong_fragment>','#include <lights_phong_fragment>\\n  material.specularColor=specular*sSpec+vec3(0.26)*sMetal; material.specularShininess=shininess*sShin;')
      .replace('#include <envmap_fragment>',`#include <envmap_fragment>
  if(sMetal>0.0){ vec3 vd=normalize(vViewPosition); vec3 rw=inverseTransformDirection(reflect(-vd,normal),viewMatrix); float fr=pow(1.0-max(dot(normal,vd),0.0),3.0);
    vec3 env=mix(vec3(0.2,0.19,0.17),vec3(0.72,0.84,1.0),smoothstep(-0.15,0.5,rw.y))*(0.75+0.5*sn(rw*3.0));
    outgoingLight+=env*surfEnv*sMetal*(0.07+0.45*fr)*(0.3+diffuseColor.rgb); }`)
      .replace('#include <tonemapping_fragment>',(glow?'gl_FragColor.rgb=mix(gl_FragColor.rgb,vColor*1.6,vGlow);\\n':'')+'#include <tonemapping_fragment>'); }; }
const surfMats=new Map();
// a part's material by colour and surface: 1 gun steel, 2 polymer, 3 wood, 4 painted metal, 5 rubber/chequering, 6 bright steel, 7 brass, 8 glass
function gunSurf(c,s){ const k=c+':'+s; let m=surfMats.get(k); if(!m){ m=new THREE.MeshPhongMaterial({color:c,shininess:16,specular:0x1c1c1c}); m.userData.part=true; m.userData.surf=s; surfShade(m,false,false); surfMats.set(k,m); } return m; }
function toon(c){ if(c&&c.isMaterial) return c;""")

rep("function bakedMat(flat,glow){ const k=flat+(glow?'g':''); if(bakedMats[k]) return bakedMats[k];",
    """function bakedMat(flat,glow,surf){ const k=flat+(glow?'g':'')+(surf?'s':''); if(bakedMats[k]) return bakedMats[k];
  if(surf){ const m=new THREE.MeshPhongMaterial({vertexColors:true,shininess:glow?6:16,specular:glow?0x101010:0x1c1c1c}); surfShade(m,true,glow); return bakedMats[k]=m; }""")
rep("function bakeGeo(list,withColor,withGlow){","function bakeGeo(list,withColor,withGlow,withSurf){")
rep("C=withColor?new Float32Array(n*3):null, GL=withGlow?new Float32Array(n):null, v=new THREE.Vector3()","C=withColor?new Float32Array(n*3):null, GL=withGlow?new Float32Array(n):null, SF=withSurf?new Float32Array(n):null, v=new THREE.Vector3()")
rep("if(GL) GL[o+i]=e.glow||0; }","if(GL) GL[o+i]=e.glow||0; if(SF) SF[o+i]=e.surf||0; }")
rep("if(GL) out.setAttribute('glow',new THREE.BufferAttribute(GL,1));","if(GL) out.setAttribute('glow',new THREE.BufferAttribute(GL,1)); if(SF) out.setAttribute('surf',new THREE.BufferAttribute(SF,1));")
rep("body.push({geo:m.geometry,M:m.matrix,col:m.material.color,glow:m.material.userData.glow||0});","body.push({geo:m.geometry,M:m.matrix,col:m.material.color,glow:m.material.userData.glow||0,surf:m.material.userData.surf||0});")
rep("const hasGlow=body.some(b=>b.glow>0); e={body:bakeGeo(body,true,hasGlow),ink:ink.length&&OUTLINES?bakeGeo(ink,false):null,cast,recv,glow:hasGlow}; }",
    "const hasGlow=body.some(b=>b.glow>0), hasSurf=body.some(b=>b.surf>0); e={body:bakeGeo(body,true,hasGlow,hasSurf),ink:ink.length&&OUTLINES?bakeGeo(ink,false):null,cast,recv,glow:hasGlow,surf:hasSurf}; }")
rep("const bm=new THREE.Mesh(e.body,bakedMat(flat,e.glow));","const bm=new THREE.Mesh(e.body,bakedMat(flat,e.glow,e.surf));")
rep("  hemi.color.copy(c.hemi); hemi.intensity=0.6+0.14*(1-Math.max(sunW,moonW))+0.05*nightK-0.14*duskK;","  SURF_ENV.value=1-0.7*nightK-0.25*duskK*(1-nightK);\n  hemi.color.copy(c.hemi); hemi.intensity=0.6+0.14*(1-Math.max(sunW,moonW))+0.05*nightK-0.14*duskK;")

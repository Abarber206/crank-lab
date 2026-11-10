# ---------- 79. polish pass 1 ----------
# (a) the Settings tab had a stray closing tag that threw the Controls tab out of the menu panel (it rendered beside the title)
rep('(off: farm trees, rocks and cars for builds) <input type="checkbox" id="infMats"></label>\n        </div>\n      </div>\n    </section>',
    '(off: farm trees, rocks and cars for builds) <input type="checkbox" id="infMats"></label>\n        </div>\n    </section>')
# (b) settings and keybinds sit in proper panels: padded, a readable width, two columns of settings on a wide screen
rep(".set{display:grid;gap:10px;font-size:13px}",""".set{display:grid;gap:12px 28px;font-size:14px;padding:16px 18px;border-radius:10px;background:rgba(255,255,255,.04);max-width:980px}
@media (min-width:900px){ .set{grid-template-columns:1fr 1fr} }
#menu.lobby .mtab[data-tab=controls]{max-width:980px;background:rgba(4,18,64,.5);border:1px solid rgba(255,255,255,.16);border-radius:10px;padding:16px 18px;backdrop-filter:blur(8px)}
#menu.lobby .mtab[data-tab=controls] .bindlist{background:none;border:0;backdrop-filter:none;max-height:none}
@media (max-width:520px){ #menu.lobby .mtabs{flex-wrap:wrap;width:auto} #menu.lobby .mtabs button{flex:1 1 auto;font-size:14px;padding:9px 10px 8px} }""")
# (c) the lobby hero (and the Locker portraits) stand relaxed and empty-handed instead of gripping an invisible pickaxe
rep("r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q);","if(S.bare) return; r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q);")
rep("  } else if(S.gun===false&&!building&&!emo){","  } else if(S.gun===false&&!building&&!emo&&!S.bare){")
rep("st={pos:e.pos,vel:_stZ,yaw:e.yaw+(i===0?S.spin:0),pitch:-0.05,","st={bare:true,pos:e.pos,vel:_stZ,yaw:e.yaw+(i===0?S.spin:0),pitch:-0.05,")
rep("animateRig(h,{pos:zero,vel:zero,yaw:0.35,pitch:0,","animateRig(h,{bare:true,pos:zero,vel:zero,yaw:0.35,pitch:0,")
# (d) house floors and ceilings: no slope-scaled depth offset (it let the hidden sides of neighbouring floor tiles show through as dashed seams)
rep("houseMat('floor',()=>new THREE.MeshPhongMaterial({map:hardwood.map,normalMap:hardwood.normal,shininess:22,specular:0x2a2016,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1})",
    "houseMat('floor',()=>new THREE.MeshPhongMaterial({map:hardwood.map,normalMap:hardwood.normal,shininess:22,specular:0x2a2016,polygonOffset:true,polygonOffsetFactor:0,polygonOffsetUnits:2})")
# (e) aiming the pickaxe at a house only shows its health once it has been damaged (it used to label every wall and floor you looked at)
rep("  if(!p||!$('buildReason').hidden){ el.hidden=true; return; }","  if(!p||!$('buildReason').hidden||(p.owner==='world'&&p.skin&&p.hp>=p.maxHp)){ el.hidden=true; return; }")
# (f) phones: the Knocked / Eliminated panel is compact and stays clear of the buttons and the minimap
rep("#rbWait.down{","""body.touch #rbWait{padding:8px 12px 8px;gap:4px;width:min(300px,calc(100vw - 24px))} body.touch #rbWait .rbt{font-size:18px} body.touch #rbWait p{font-size:13px} body.touch #rbWait small{font-size:11px}
@media (orientation:landscape){ body.touch #rbWait{top:calc(env(safe-area-inset-top,0px) + 6px);left:calc(env(safe-area-inset-left,0px) + 110px);transform:none} }
@media (orientation:portrait){ body.touch #rbWait{top:calc(env(safe-area-inset-top,0px) + 150px)} }
#rbWait.down{""")

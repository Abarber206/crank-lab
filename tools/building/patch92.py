# ---------- 92. keybinds by mode: weapon-only actions (reload, aim), build-only actions (rotate, switch material) and
# edit-only actions (reset) can share a key, and each only fires in its own mode ----------
rep("function pressAction(a){\n  if(invOpen&&a!=='inventory') return;",
"""const BIND_CTX={reload:'gun',aim:'gun',rotate:'build',material:'build',reset:'edit'};
function bindCtxNow(){ return edit?'edit':mode==='build'?'build':mode==='gun'?'gun':'other'; }
function pressAction(a){
  if(invOpen&&a!=='inventory') return;
  if(BIND_CTX[a]&&BIND_CTX[a]!==bindCtxNow()) return;""")
rep("    Object.keys(settings.binds).forEach(o=>{ if(o!==a&&settings.binds[o]===code) settings.binds[o]=old; }); // swap on conflict",
    "    Object.keys(settings.binds).forEach(o=>{ if(o!==a&&settings.binds[o]===code&&(!BIND_CTX[a]||!BIND_CTX[o]||BIND_CTX[a]===BIND_CTX[o])) settings.binds[o]=old; }); // swap on conflict (actions from different modes may share a key)")
rep("Esc cancels. Taken binds swap.","Esc cancels. Taken binds swap, except that weapon, build and edit actions can share a key: each only works in its own mode.")

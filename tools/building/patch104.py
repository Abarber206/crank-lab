# ---------- 104. sharper shadows: a 4096 shadow map on desktop (about 2 cm a texel), a tighter box on phones, and less
# bias so shadows start right at the feet of things ----------
rep("sun.shadow.mapSize.set(isTouch?1024:2048, isTouch?1024:2048);","{ const big=!isTouch&&renderer.capabilities.maxTextureSize>=4096?4096:2048; sun.shadow.mapSize.set(big,big); }")
rep("sun.shadow.bias=-0.0006; sun.shadow.normalBias=0.02; sc.left=-45; sc.right=45; sc.top=45; sc.bottom=-45; sc.far=200;","{ const hb=isTouch?48:45; sun.shadow.bias=isTouch?-0.0006:-0.00028; sun.shadow.normalBias=isTouch?0.02:0.012; sc.left=-hb; sc.right=hb; sc.top=hb; sc.bottom=-hb; sc.far=200; }")

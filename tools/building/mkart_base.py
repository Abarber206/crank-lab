# index.html (GitHub Pages) -> crank-lab.html (claude.ai artifact: no doc skeleton, multiplayer note, no peer connections)
src=open('/home/claude/mg/index.orig.html').read()
def rep(a,b):
    global src
    assert src.count(a)==1,(src.count(a),a[:80]); src=src.replace(a,b)
head='<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
assert src.startswith(head); src=src[len(head):]
rep('</head>\n<body>\n','')
rep('      <div id="roomIdle" class="mprow">','      <p class="sub" style="font-size:13px;margin:0">Multiplayer rooms work on the GitHub Pages version of Crank Lab.</p>\n      <div id="roomIdle" class="mprow" hidden>')
rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script>window.CRANK_NO_MP=true</script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>')
assert src.rstrip().endswith('</body>\n</html>'); src=src.rstrip()[:-len('</body>\n</html>')]
open('/home/claude/mg/base_art.html','w').write(src)
print('ok',len(src))

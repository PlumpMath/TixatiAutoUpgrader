from subprocess import run, PIPE
from urllib.request import urlopen
from re import compile
c=compile(r'(https?://(.+\.tixati.com)/download/(tixati-(\d+\.\d+-\d+)\.win64-install.exe))')

w=urlopen('http://www.tixati.com/download/windows64.html')
r=[]
v=''
wp=''
for l in w:
  s = c.search(l.decode())
  if s:
    if not wp:
      wp = s.group(3)
    if not v:
      v = s.group(4)
    r.append(s.groups()[:2])

print('latest version :',v)

c=compile(r'\r\n    .+ = (\d+)ms,')
ps=[]
for u, v in r:
  p=run('ping '+v, stdout=PIPE)
  s=c.search(p.stdout.decode('cp949')) # change this to your Windows encoding setting
  p=int(s.group(1)) if s else float('inf')
  ps.append(p)
  print(v, p)

i=min(list(enumerate(ps)), key=lambda a:a[1])[0]

print('best server :', r[i][1])

print('downloading ', r[i][0], 'to', wp)
w=urlopen(r[i][0])
with open(wp, 'wb') as f:
  f.write(w.read())

print('download done, executing.')
run(wp, shell=True)
from os import remove
remove(wp)

import json, re
import subprocess, sys
_chk = subprocess.run(['node','-e',"try{new Function(require('fs').readFileSync('data/listings.js','utf8'))}catch(e){console.error(e.message);process.exit(1)}"],capture_output=True,text=True)
if _chk.returncode: sys.exit('STOP: data/listings.js 문법 오류(사이트가 빈 화면이 됨): '+_chk.stderr.strip())
L = open('data/listings.js', encoding='utf-8').read().strip()
# split combined excluded rows into separate rows with links
m1 = re.search(r' \{"?n"?:\s?"3 Essex St G2 / 356-358 Main St G2".*?\},\n', L, re.S)
old1 = m1.group(0) if m1 else None
if old1: L = L.replace(old1,
 ' {reno:1986,n:"3 Essex St G2",addr:"3 Essex St G2, Charlestown, MA 02129",area:"Charlestown",built:1900,unit:"2베드 730",sq:730,rent:2800,rentT:"Plus Fees",park:"-",est:"-",estLo:null,wd:"y",gym:"n",mgd:"n",dist:null,move:"-",sp:"-",s:5,url:"https://www.harvardhousingoffcampus.com/housing/property/3-essex-st-unit-g2/fmqw7dv",memo:"제외: 반지하(garden level)"},\n'
 ' {n:"356-358 Main St G2",addr:"356-358 Main St G2, Charlestown, MA 02129",area:"Charlestown",built:1900,unit:"2베드 730",sq:730,rent:2800,rentT:"Plus Fees",park:"-",est:"-",estLo:null,wd:"y",gym:"n",mgd:"n",dist:null,move:"-",sp:"-",s:5,url:"https://www.harvardhousingoffcampus.com/housing/property/356-358-main-st-unit-g2/kx3y50b",memo:"제외: 반지하(garden level)"},\n')
m2 = re.search(r' \{"?n"?:\s?"1410 Columbia Rd 6A / 4 Elko St".*?\},\n', L, re.S)
old2 = m2.group(0) if m2 else None
if old2: L = L.replace(old2,
 ' {n:"1410 Columbia Rd 6A",addr:"1410 Columbia Rd #6A, South Boston, MA 02127",area:"South Boston",built:1972,unit:"1베드 557",sq:557,rent:2950,rentT:"Plus Fees",park:"-",est:"-",estLo:null,wd:"y",gym:"y",mgd:"n",dist:null,move:"-",sp:"-",s:5,url:"https://www.harvardhousingoffcampus.com/housing/property/1410-columbia-rd-unit-6a/8nfvp53",memo:"제외: 신청비 1인 $500 (주의 신호)"},\n'
 ' {reno:2024,n:"4 Elko St B3",addr:"4 Elko St #B3, Brighton, MA 02135",area:"Brighton",built:1920,unit:"2베드 600",sq:600,rent:2350,rentT:"Plus Fees",park:"-",est:"-",estLo:null,wd:"y",gym:"n",mgd:"n",dist:null,move:"-",sp:"-",s:5,url:"https://www.harvardhousingoffcampus.com/housing/property/4-elko-st-unit-b3/xcqmrwq",memo:"제외: 신청비 1인 $500, 600 sq ft로 좁음"},\n')
T = json.load(open('data/transit.json', encoding='utf-8'))
# shuttle hub + transit commute estimate to 401 Park Drive (agent estimates)
EX = {
"Schoolhouse at Lower Mills":["Mattapan 트롤리 → Ashmont(Red) → JFK/UMass에서 LMA 셔틀","55~70분"],
"E3 Apartments":["Green B → Kenmore 환승·도보, 또는 버스 66","35~45분"],
"Linden Apartments":["통근열차 Needham선 → Ruggles에서 LMA 셔틀","45~60분"],
"Imprint":["Fields Corner(Red) → JFK/UMass에서 LMA 셔틀","50~60분"],
"The Proof":["Readville 통근열차 → Ruggles에서 LMA 셔틀","50~65분"],
"River Park Lofts":["버스 71 → Harvard Square에서 M2 셔틀","55~70분"],
"Tempo Cambridge":["Alewife(Red) → Harvard Square에서 M2 셔틀","45~55분"],
"Jade":["버스 → Wellington(Orange) → Ruggles에서 LMA 셔틀","60~75분"],
"Neponset Landing":["North Quincy(Red) → JFK/UMass에서 LMA 셔틀","45~55분"],
"MetroMark":["Forest Hills(Orange) → Ruggles에서 LMA 셔틀, 또는 버스 39","30~40분"],
"175 Cottage St #702":["버스 → Wood Island(Blue) → 환승","55~65분"],
"36 Gove St":["Maverick(Blue) → Government Center → Green D Fenway","40~50분"],
"110 Lucerne St":["Morton St 통근열차 또는 버스 28 → Ruggles에서 LMA 셔틀","45~55분"],
"Velo Forest Hills":["Forest Hills(Orange) → Ruggles에서 LMA 셔틀, 또는 버스 39","30~40분"],
"1550 on the Charles":["Boston Landing 통근열차 또는 Green B → Kenmore","40~50분"],
"Dot Block":["Savin Hill(Red) → JFK/UMass에서 LMA 셔틀 또는 버스 8","40~50분"],
"87 Murdock St":["Green B → Kenmore 환승·도보","35~45분"],
"CHR Coolidge Corner":["Green C 또는 도보 15분","15~20분"],
"Parmelee Court":["버스 47·8 직행","20~25분"],
"Gamma North Quincy":["North Quincy(Red) → JFK/UMass에서 LMA 셔틀","45~55분"],
"3 Essex St G2":["Community College(Orange) → Ruggles","45~55분"],
"356-358 Main St G2":["Community College(Orange) → Ruggles","45~55분"],
"1410 Columbia Rd 6A":["Andrew(Red) → JFK/UMass LMA 셔틀 또는 버스","40~50분"],
"4 Elko St B3":["버스 65·66 또는 Green B","35~45분"],
}
EX.update(json.load(open("data/extra_ex.json", encoding="utf-8")))
data = "const EV=%s;\nconst MURDERS=%s;\n" % (open("data/eval.json",encoding="utf-8").read(), open("data/murders.json",encoding="utf-8").read()) + "const GEO=%s;\nconst TR=%s;\nconst EX=%s;\nconst DRIVE=%s;\nconst GG=%s;\nconst UNIS=%s;\nconst SHAPES=%s;\n" % (
  json.dumps(T['GEO'],ensure_ascii=False), json.dumps(T['TR'],ensure_ascii=False),
  json.dumps(EX,ensure_ascii=False), json.dumps(T.get('DRIVE',{})), json.dumps(json.load(open('data/google.json',encoding='utf-8')),ensure_ascii=False), json.dumps(T.get('UNIS',{})), json.dumps(T['SHAPES']))
tpl = open('template.html', encoding='utf-8').read()
data += 'const PZL=%s;\n' % open('data/pzlist.json',encoding='utf-8').read()
data += 'const STORES=%s;\n' % json.dumps(json.load(open('data/stores.json',encoding='utf-8'))['stores'],ensure_ascii=False)
# 후보·경계 행이 화면에서 빠질 수 있는 누락 경고
try:
    _G=json.load(open('data/transit.json',encoding='utf-8'))['GEO']
    for _l in open('data/listings.js',encoding='utf-8'):
        if '"n": ' not in _l: continue
        _r=json.loads(_l.strip().rstrip(','))
        if _r.get('s') in (1,2,3):
            _m=[k for k,ok in (('좌표',_r['n'] in _G),('월세',isinstance(_r.get('rent'),(int,float))),('url',bool(_r.get('url')))) if not ok]
            if _m: print('WARN 후보 화면 필드 누락:',_r['n'],_m)
except Exception as _e: print('WARN 후보 점검 실패',_e)
out = tpl.replace('/*DATA*/', L + '\n' + data)
out = out.replace('__ARA__', open('data/ara.json',encoding='utf-8').read().strip() or '{}')
out = out.replace('__DONGIN__', open('data/dongin.json',encoding='utf-8').read().strip() or '{}')
import os, subprocess
# 문의 대화 기록(records/messages.json, 비공개)을 매물별로 붙인다
MS={}
if os.path.exists('records/messages.json'):
    for t in json.load(open('records/messages.json',encoding='utf-8'))['threads']:
        MS[t['listing']]={k:t.get(k) for k in ('status','contact','summary','next','msgs')}
out = out.replace('__MSGS__', json.dumps(MS,ensure_ascii=False))
# 사용자가 답해야 할 질문(records/asks.json, 비공개)
AS={}
if os.path.exists('records/asks.json'):
    AS=json.load(open('records/asks.json',encoding='utf-8')).get('asks',{})
out = out.replace('__ASKS__', json.dumps(AS,ensure_ascii=False))
# 사이트 전체를 비밀번호로 암호화해서 공개한다. 비밀번호 파일이 없으면 평문으로 내보내지 않고 멈춘다.
if not os.path.exists('records/.messages_password'):
    raise SystemExit('records/.messages_password 없음: 암호화할 수 없어서 index.html을 만들지 않음')
os.makedirs('records',exist_ok=True)
open('records/site_plain.html','w',encoding='utf-8').write(out)
node = '/Users/jo/.aside/runtime/bin/node' if os.path.exists('/Users/jo/.aside/runtime/bin/node') else 'node'
subprocess.run([node,'records/encrypt_site.mjs','records/site_plain.html','index.html'],check=True)
names = re.findall(r'[{,]\s*"?n"?:\s*"([^"]+)"', L)
missing = [n for n in names if n not in T['GEO'] or not T['GEO'][n]]
print('listings', len(names), 'missing geo', missing, 'missing EX', [n for n in names if n not in EX], 'missing drive', [n for n in names if n not in T.get('DRIVE',{})])

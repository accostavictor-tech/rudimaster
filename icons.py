from PIL import Image, ImageDraw, ImageFont
import math, os

INK=(25,21,16,255); CREAM=(248,244,233,255); BG=(231,223,204,255); RED=(190,58,40,255)

def rot_ellipse(d,cx,cy,rx,ry,ang,fill,steps=220):
    a=math.radians(ang);p=[]
    for i in range(steps):
        t=2*math.pi*i/steps;x=rx*math.cos(t);y=ry*math.sin(t)
        p.append((cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)))
    d.polygon(p,fill=fill)

def mark(size,disc=True,pad=0.0,ss=6):
    S=int(size*ss);img=Image.new('RGBA',(S,S),(0,0,0,0));d=ImageDraw.Draw(img)
    inset=S*pad; s=S-2*inset; u=s/64.0
    def X(v): return inset+v*u
    if disc: d.ellipse([X(0),X(0),X(64),X(64)],fill=INK)
    d.ellipse([X(7),X(7),X(57),X(57)],outline=(248,244,233,82),width=max(1,int(1.9*u)))
    d.line([(X(16.5),X(19.5)),(X(25.5),X(23))],fill=CREAM,width=max(1,int(3.1*u)))
    d.line([(X(25.5),X(23)),(X(16.5),X(26.5))],fill=CREAM,width=max(1,int(3.1*u)))
    d.rounded_rectangle([X(34),X(18.5),X(37.4),X(40)],radius=1.2*u,fill=CREAM)
    rot_ellipse(d,X(27.4),X(39),10*u,7.2*u,-20,CREAM)
    return img.resize((size,size),Image.LANCZOS)

os.makedirs('.',exist_ok=True)
mark(192).save('icon-192.png')
mark(512).save('icon-512.png')
mark(180).save('apple-touch-icon.png')
m=Image.new('RGBA',(512,512),INK); m.alpha_composite(mark(512,disc=False,pad=0.10)); m.save('icon-maskable.png')

FB="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
FM="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
STICK={'pt':'D E D D   |   E D E E','en':'R L R R   |   L R L L','es':'D I D D   |   I D I I'}
TAG={'pt':'prática de rudimentos no pad, com metrônomo',
     'en':'pad practice for drum rudiments, with metronome',
     'es':'práctica de rudimentos en el pad, con metrónomo'}
for code,tag in TAG.items():
    W,H=1200,630
    img=Image.new('RGB',(W,H),BG[:3]);d=ImageDraw.Draw(img)
    d.rectangle([0,H-14,W,H],fill=RED[:3])
    img.paste(mark(150),(88,150),mark(150))
    f1=ImageFont.truetype(FB,116); f2=ImageFont.truetype(FR,38); f3=ImageFont.truetype(FM,26)
    w1=d.textlength("Rudi",font=f1)
    d.text((270,150),"Rudi",font=f1,fill=INK[:3])
    d.text((270+w1,150),"Master",font=f1,fill=(94,87,73))
    d.text((274,290),tag,font=f2,fill=(94,87,73))
    d.text((274,372),STICK[code],font=f3,fill=(145,137,119))
    d.line([(88,470),(W-88,470)],fill=(145,137,119),width=2)
    d.text((88,500),"rudimaster.com",font=f3,fill=(94,87,73))
    img.save(f'og-{code}.png')
print('icones e og gerados')

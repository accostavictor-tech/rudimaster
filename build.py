#!/usr/bin/env python3
"""Gera as paginas localizadas do RudiMaster a partir de uma unica fonte."""
import json, os, re
import donate as DN

BASE = "https://rudimaster.com"   # troque aqui se o dominio mudar
OUT = os.path.dirname(os.path.abspath(__file__))

# Analytics. Vercel Web Analytics e sem cookie e nao exige banner de consentimento.
# Precisa estar habilitado em Settings > Analytics no painel do projeto.
VERCEL_ANALYTICS = True
VERCEL_SPEED_INSIGHTS = False

ANALYTICS_TAG = ""
if VERCEL_ANALYTICS:
    ANALYTICS_TAG += '<script defer src="/_vercel/insights/script.js"></script>\n'
if VERCEL_SPEED_INSIGHTS:
    ANALYTICS_TAG += '<script defer src="/_vercel/speed-insights/script.js"></script>\n'



UI = {
"pt": {
  "home":"Início","toRud":"Treinar rudimentos","toMet":"Só o metrônomo","back":"Início",
  "beatsLab":"Batidas por compasso","subLab":"Subdivisão","subs":["Semínima","Colcheias","Tercinas","Semicolcheias"],
  "lugHint":"Toque nos pontos para acentuar ou silenciar cada tempo","elapsed":"Tempo",
  "html":"pt-BR","label":"Português","tagline":"Prática de rudimentos no pad, com metrônomo e partitura.","rud":"Rudimento","settings":"Ajustes",
  "sig":"Compasso","hand":"Mão que conduz","right":"Direita","left":"Esquerda",
  "sound":"Som e leitura","met":"Metrônomo","rudSnd":"Rudimento","hands":"Mãos","countIn":"Entrada",
  "volMet":"Volume metrônomo","volRud":"Volume rudimento","prog":"Treino progressivo","auto":"Acelerar sozinho",
  "every":"bpm a cada","bars":"compassos","tap":"Tap tempo","search":"Buscar rudimento",
  "play":"Tocar","stop":"Parar","theme":"Alternar tema","start":"toque para começar","ready":"prepara…",
  "bar":"compasso","beats":"tempos","strokes":"toques","unit4":"bpm · semínima","unit8":"bpm · semínima pontuada",
  "keys":"<kbd>espaço</kbd> toca e para · <kbd>↑</kbd><kbd>↓</kbd> muda o bpm","empty":"Nada encontrado",
  "cats":{"roll":"Rufos","para":"Paradiddles","flam":"Flams","drag":"Drags"},
  "figs":{"q":"semínimas","e":"colcheias","t":"tercinas","s":"semicolcheias","x":"sextinas"},
  "letters":{"R":"D","L":"E"},
  "names":{"s1":"Rufo simples","s2":"Rufo duplo","s3":"Rufo triplo","r5":"Rufo de 5 toques","r6":"Rufo de 6 toques",
    "r7":"Rufo de 7 toques","r9":"Rufo de 9 toques","p1":"Paradiddle simples","p2":"Paradiddle duplo",
    "p3":"Paradiddle triplo","pd":"Paradiddle-diddle","f1":"Flam","f2":"Flam tap","f3":"Flam accent",
    "f4":"Flamacue","d1":"Drag","d2":"Drag tap simples","d3":"Ratamacue simples"}
},
"en": {
  "home":"Home","toRud":"Practise rudiments","toMet":"Metronome only","back":"Home",
  "beatsLab":"Beats per bar","subLab":"Subdivision","subs":["Quarter","Eighths","Triplets","Sixteenths"],
  "lugHint":"Tap the dots to accent or mute each beat","elapsed":"Elapsed",
  "html":"en","label":"English","tagline":"Pad practice for drum rudiments, with metronome and notation.","rud":"Rudiment","settings":"Settings",
  "sig":"Time signature","hand":"Leading hand","right":"Right","left":"Left",
  "sound":"Sound & reading","met":"Metronome","rudSnd":"Rudiment","hands":"Sticking","countIn":"Count-in",
  "volMet":"Metronome volume","volRud":"Rudiment volume","prog":"Progressive practice","auto":"Speed up automatically",
  "every":"bpm every","bars":"bars","tap":"Tap tempo","search":"Search rudiment",
  "play":"Play","stop":"Stop","theme":"Toggle theme","start":"tap to start","ready":"get ready…",
  "bar":"bar","beats":"beats","strokes":"strokes","unit4":"bpm · quarter note","unit8":"bpm · dotted quarter",
  "keys":"<kbd>space</kbd> play and stop · <kbd>↑</kbd><kbd>↓</kbd> change bpm","empty":"Nothing found",
  "cats":{"roll":"Rolls","para":"Paradiddles","flam":"Flams","drag":"Drags"},
  "figs":{"q":"quarter notes","e":"eighth notes","t":"triplets","s":"sixteenth notes","x":"sextuplets"},
  "letters":{"R":"R","L":"L"},
  "names":{"s1":"Single stroke roll","s2":"Double stroke roll","s3":"Triple stroke roll","r5":"Five stroke roll",
    "r6":"Six stroke roll","r7":"Seven stroke roll","r9":"Nine stroke roll","p1":"Single paradiddle",
    "p2":"Double paradiddle","p3":"Triple paradiddle","pd":"Paradiddle-diddle","f1":"Flam","f2":"Flam tap",
    "f3":"Flam accent","f4":"Flamacue","d1":"Drag (ruff)","d2":"Single drag tap","d3":"Single ratamacue"}
},
"es": {
  "home":"Inicio","toRud":"Practicar rudimentos","toMet":"Solo el metrónomo","back":"Inicio",
  "beatsLab":"Tiempos por compás","subLab":"Subdivisión","subs":["Negra","Corcheas","Tresillos","Semicorcheas"],
  "lugHint":"Toca los puntos para acentuar o silenciar cada tiempo","elapsed":"Tiempo",
  "html":"es","label":"Español","tagline":"Práctica de rudimentos en el pad, con metrónomo y partitura.","rud":"Rudimento","settings":"Ajustes",
  "sig":"Compás","hand":"Mano que conduce","right":"Derecha","left":"Izquierda",
  "sound":"Sonido y lectura","met":"Metrónomo","rudSnd":"Rudimento","hands":"Manos","countIn":"Entrada",
  "volMet":"Volumen metrónomo","volRud":"Volumen rudimento","prog":"Práctica progresiva","auto":"Acelerar solo",
  "every":"bpm cada","bars":"compases","tap":"Tap tempo","search":"Buscar rudimento",
  "play":"Tocar","stop":"Parar","theme":"Cambiar tema","start":"toca para empezar","ready":"prepárate…",
  "bar":"compás","beats":"tiempos","strokes":"golpes","unit4":"bpm · negra","unit8":"bpm · negra con puntillo",
  "keys":"<kbd>espacio</kbd> toca y para · <kbd>↑</kbd><kbd>↓</kbd> cambia el bpm","empty":"Sin resultados",
  "cats":{"roll":"Redobles","para":"Paradiddles","flam":"Flams","drag":"Drags"},
  "figs":{"q":"negras","e":"corcheas","t":"tresillos","s":"semicorcheas","x":"seisillos"},
  "letters":{"R":"D","L":"I"},
  "names":{"s1":"Redoble simple","s2":"Redoble doble","s3":"Redoble triple","r5":"Redoble de 5 golpes",
    "r6":"Redoble de 6 golpes","r7":"Redoble de 7 golpes","r9":"Redoble de 9 golpes","p1":"Paradiddle simple",
    "p2":"Paradiddle doble","p3":"Paradiddle triple","pd":"Paradiddle-diddle","f1":"Flam","f2":"Flam tap",
    "f3":"Flam accent","f4":"Flamacue","d1":"Drag","d2":"Drag tap simple","d3":"Ratamacue simple"}
}}

SEO = {
"pt": {
  "title":"RudiMaster — prática de rudimentos no pad com metrônomo e partitura",
  "desc":"Metrônomo grátis com partitura animada para treinar rudimentos de caixa: rufos, paradiddles, flams e drags. Escolha o rudimento, o compasso e o andamento e toque junto.",
  "h1sub":"Prática de rudimentos no pad, com metrônomo e partitura animada",
  "howTitle":"Como treinar com o RudiMaster",
  "howIntro":"O RudiMaster junta duas coisas que normalmente ficam separadas na estante: o metrônomo e a folha de rudimento. A partitura corre da direita para a esquerda, e o que estiver sobre a linha vermelha é o que você toca agora. Serve para caixa, pad de estudo, bateria ou a almofada do sofá.",
  "steps":["Escolha o rudimento na lista, agrupada por rufos, paradiddles, flams e drags.",
           "Defina o compasso e o andamento. Se não souber a velocidade, use o tap tempo batendo o pulso que tem na cabeça.",
           "Dê play. Um compasso de entrada toca antes do rudimento começar.",
           "Quando o padrão estiver na mão, ligue o treino progressivo e deixe o andamento subir sozinho a cada tantos compassos."],
  "listTitle":"Rudimentos disponíveis",
  "listIntro":"Dezoito rudimentos com sticking, acentos, flams e drags escritos em notação real. As letras D e E indicam a mão direita e a esquerda, e podem ser invertidas para canhotos.",
  "faqTitle":"Perguntas frequentes",
  "faq":[
    ("O que são rudimentos de bateria?","São os padrões básicos de baqueta que formam o vocabulário do baterista, como o rufo duplo, o paradiddle e o flam. Combinando esses blocos você constrói viradas, levadas e solos. Treinar rudimento é o equivalente a estudar escala em um instrumento harmônico."),
    ("Em que andamento devo começar?","Comece devagar o bastante para tocar o padrão sem nenhum erro, o que costuma ser entre 50 e 70 bpm. Suba de cinco em cinco apenas quando conseguir dois minutos limpos. O treino progressivo do RudiMaster faz isso automaticamente."),
    ("O que significam os acentos e as letras na partitura?","O sinal parecido com um sinal de maior indica o toque acentuado, que é tocado mais forte e com a baqueta mais alta. As letras abaixo da pauta indicam qual mão toca cada nota. As notinhas pequenas antes da nota principal são os flams, com uma nota de ornamento, e os drags, com duas."),
    ("Preciso de uma bateria para usar?","Não. A maior parte do treino de rudimento acontece em pad de estudo, que é mais silencioso e exige mais controle. Uma almofada firme ou uma revista dobrada também funcionam para começar."),
    ("Funciona no celular e offline?","Sim. A interface foi desenhada primeiro para celular e o site pode ser instalado na tela inicial. Depois do primeiro carregamento ele funciona sem internet.")],
  "footNote":"Feito para quem estuda caixa."
},
"en": {
  "title":"RudiMaster — drum rudiment practice with metronome and scrolling notation",
  "desc":"Free metronome with animated notation to practise snare drum rudiments: rolls, paradiddles, flams and drags. Pick a rudiment, set the tempo and play along.",
  "h1sub":"Pad practice for drum rudiments, with metronome and scrolling notation",
  "howTitle":"How to practise with RudiMaster",
  "howIntro":"RudiMaster puts together two things that usually sit apart on the shelf: the metronome and the rudiment sheet. Notation scrolls from right to left, and whatever sits on the red line is what you play right now. Works for snare, practice pad, drum kit or a couch cushion.",
  "steps":["Pick a rudiment from the list, grouped into rolls, paradiddles, flams and drags.",
           "Set the time signature and tempo. If you don't know the speed, tap the pulse you have in mind on the tap tempo button.",
           "Hit play. One count-in bar runs before the rudiment starts.",
           "Once the pattern feels comfortable, turn on progressive practice and let the tempo climb on its own every few bars."],
  "listTitle":"Rudiments included",
  "listIntro":"Eighteen rudiments with sticking, accents, flams and drags written in real notation. R and L mark the right and left hand, and can be swapped for left-handed players.",
  "faqTitle":"Frequently asked questions",
  "faq":[
    ("What are drum rudiments?","They are the basic sticking patterns that make up a drummer's vocabulary, such as the double stroke roll, the paradiddle and the flam. Combining these blocks is how fills, grooves and solos get built. Practising rudiments is the drummer's equivalent of practising scales."),
    ("What tempo should I start at?","Start slow enough to play the pattern with no mistakes at all, usually somewhere between 50 and 70 bpm. Move up in steps of five only after two clean minutes. RudiMaster's progressive practice does this for you."),
    ("What do the accents and letters in the notation mean?","The sign that looks like a greater-than symbol marks an accented stroke, played louder and from a higher stick height. The letters under the staff show which hand plays each note. The small notes before a main note are flams, with one grace note, and drags, with two."),
    ("Do I need a drum kit?","No. Most rudiment work happens on a practice pad, which is quieter and demands more control. A firm cushion or a folded magazine will do to get started."),
    ("Does it work on mobile and offline?","Yes. The interface was designed for phones first and the site can be installed to your home screen. After the first load it runs without a connection.")],
  "footNote":"Built for people who practise snare."
},
"es": {
  "title":"RudiMaster — práctica de rudimentos con metrónomo y partitura",
  "desc":"Metrónomo gratis con partitura animada para practicar rudimentos de caja: redobles, paradiddles, flams y drags. Elige el rudimento, el compás y el tempo y toca encima.",
  "h1sub":"Práctica de rudimentos en el pad, con metrónomo y partitura animada",
  "howTitle":"Cómo practicar con RudiMaster",
  "howIntro":"RudiMaster junta dos cosas que suelen estar separadas en el estante: el metrónomo y la hoja de rudimentos. La partitura corre de derecha a izquierda, y lo que esté sobre la línea roja es lo que tocas ahora. Sirve para caja, pad de estudio, batería o un cojín.",
  "steps":["Elige el rudimento en la lista, agrupada en redobles, paradiddles, flams y drags.",
           "Define el compás y el tempo. Si no sabes la velocidad, usa el tap tempo golpeando el pulso que tienes en la cabeza.",
           "Dale a tocar. Suena un compás de entrada antes de que empiece el rudimento.",
           "Cuando el patrón salga cómodo, activa la práctica progresiva y deja que el tempo suba solo cada cierto número de compases."],
  "listTitle":"Rudimentos incluidos",
  "listIntro":"Dieciocho rudimentos con sticking, acentos, flams y drags escritos en notación real. Las letras D e I indican la mano derecha y la izquierda, y se pueden invertir para zurdos.",
  "faqTitle":"Preguntas frecuentes",
  "faq":[
    ("¿Qué son los rudimentos de batería?","Son los patrones básicos de baqueta que forman el vocabulario del baterista, como el redoble doble, el paradiddle y el flam. Combinando estos bloques se construyen fills, grooves y solos. Practicar rudimentos equivale a estudiar escalas en un instrumento armónico."),
    ("¿A qué tempo debo empezar?","Empieza lo bastante lento como para tocar el patrón sin ningún error, normalmente entre 50 y 70 bpm. Sube de cinco en cinco solo cuando logres dos minutos limpios. La práctica progresiva de RudiMaster lo hace por ti."),
    ("¿Qué significan los acentos y las letras de la partitura?","El signo parecido a un mayor indica un golpe acentuado, tocado más fuerte y con la baqueta más alta. Las letras bajo el pentagrama indican qué mano toca cada nota. Las notas pequeñas antes de la principal son los flams, con una nota de adorno, y los drags, con dos."),
    ("¿Necesito una batería?","No. La mayor parte del trabajo de rudimentos se hace en un pad de estudio, más silencioso y más exigente en control. Un cojín firme o una revista doblada sirven para empezar."),
    ("¿Funciona en el móvil y sin conexión?","Sí. La interfaz se diseñó primero para móvil y el sitio se puede instalar en la pantalla de inicio. Tras la primera carga funciona sin internet.")],
  "footNote":"Hecho para quien estudia caja."
}}

HOME_SEO = {
"pt": {
  "title":"RudiMaster — metrônomo online e treino de rudimentos de bateria",
  "desc":"Escolha o metrônomo online, com acento por tempo e subdivisões, ou o treino de rudimentos com partitura animada. Grátis, sem anúncios e sem cadastro.",
  "h1":"O que você vai treinar hoje?",
  "lead":"Duas ferramentas para quem estuda no pad ou na caixa. Escolha uma e comece agora, sem cadastro.",
  "metTitle":"Metrônomo","metDesc":"Andamento, batidas por compasso e subdivisão. Acentue ou silencie cada tempo tocando nos pontos. Tap tempo e aceleração automática.",
  "rudTitle":"Rudimentos","rudDesc":"Dezoito rudimentos com partitura correndo na tela, sticking, acentos, flams e drags. O metrônomo toca junto.",
  "cta":"Abrir",
  "aboutTitle":"Sobre o RudiMaster",
  "about":"O RudiMaster nasceu de um problema simples: o metrônomo fica num app, a folha de rudimento fica noutro, e o estudo se perde entre os dois. Aqui as duas coisas moram no mesmo lugar, funcionam no celular e não pedem login. O relógio do áudio é o mesmo que move a partitura, então som e imagem nunca saem de sincronia."
},
"en": {
  "title":"RudiMaster — online metronome and drum rudiment trainer",
  "desc":"Pick the online metronome, with per-beat accents and subdivisions, or the rudiment trainer with scrolling notation. Free, ad-free, no sign-up.",
  "h1":"What are you practising today?",
  "lead":"Two tools for anyone working on a pad or a snare. Pick one and start now, no sign-up.",
  "metTitle":"Metronome","metDesc":"Tempo, beats per bar and subdivision. Accent or mute any beat by tapping the dots. Tap tempo and automatic speed-up.",
  "rudTitle":"Rudiments","rudDesc":"Eighteen rudiments with notation scrolling across the screen, sticking, accents, flams and drags. The metronome plays along.",
  "cta":"Open",
  "aboutTitle":"About RudiMaster",
  "about":"RudiMaster started from a simple problem: the metronome lives in one app, the rudiment sheet in another, and practice gets lost between the two. Here both sit in the same place, work on a phone and ask for no login. The audio clock that fires the click is the same one that moves the notation, so sound and image never drift apart."
},
"es": {
  "title":"RudiMaster — metrónomo online y entrenador de rudimentos de batería",
  "desc":"Elige el metrónomo online, con acentos por tiempo y subdivisiones, o el entrenador de rudimentos con partitura animada. Gratis, sin anuncios y sin registro.",
  "h1":"¿Qué vas a practicar hoy?",
  "lead":"Dos herramientas para quien estudia en el pad o en la caja. Elige una y empieza ahora, sin registro.",
  "metTitle":"Metrónomo","metDesc":"Tempo, tiempos por compás y subdivisión. Acentúa o silencia cada tiempo tocando los puntos. Tap tempo y aceleración automática.",
  "rudTitle":"Rudimentos","rudDesc":"Dieciocho rudimentos con partitura corriendo en la pantalla, sticking, acentos, flams y drags. El metrónomo suena a la vez.",
  "cta":"Abrir",
  "aboutTitle":"Sobre RudiMaster",
  "about":"RudiMaster nació de un problema simple: el metrónomo está en una app, la hoja de rudimentos en otra, y el estudio se pierde entre las dos. Aquí ambas cosas viven en el mismo sitio, funcionan en el móvil y no piden registro. El reloj de audio que dispara el clic es el mismo que mueve la partitura, así que sonido e imagen nunca se separan."
}}

MET_SEO = {
"pt": {
  "title":"Metrônomo online grátis — acentos, subdivisões e tap tempo | RudiMaster",
  "desc":"Metrônomo online preciso, com acento ou silêncio em cada tempo, subdivisão em colcheias, tercinas e semicolcheias, tap tempo e aceleração progressiva. Sem anúncios.",
  "h1sub":"Metrônomo online com acento por tempo, subdivisões e tap tempo",
  "aboutTitle":"Um metrônomo que faz o que o estudo pede",
  "about":"O clique é agendado pelo relógio do áudio do navegador, e não por temporizador de interface, que é o que causa aquela oscilação chata em metrônomo de site. O andamento se mantém estável mesmo com a aba ocupada.",
  "featTitle":"O que dá para configurar",
  "feats":["Andamento de 30 a 300 bpm, com botões de cinco em cinco, deslizador e tap tempo.",
           "De um a doze tempos por compasso.",
           "Subdivisão em semínimas, colcheias, tercinas ou semicolcheias, com clique mais baixo nas subdivisões.",
           "Acento, clique normal ou silêncio em cada tempo, tocando no ponto correspondente. Silenciar tempos é o jeito clássico de treinar tempo interno.",
           "Aceleração progressiva, subindo o andamento automaticamente a cada número de compassos.",
           "A tela não apaga durante o uso, e o contador mostra compasso e tempo decorrido."],
  "faqTitle":"Perguntas frequentes",
  "faq":[("O metrônomo funciona offline?","Sim. Depois do primeiro carregamento a página funciona sem internet, e dá para instalar na tela inicial do celular."),
         ("Por que silenciar alguns tempos?","Tocar com alguns tempos mudos obriga você a sustentar o pulso por conta própria. É um dos exercícios mais eficientes para melhorar tempo interno, e fica evidente quando você desacelera ou acelera sem perceber."),
         ("Qual a diferença para o modo rudimentos?","No modo rudimentos, além do clique, a partitura do rudimento escolhido corre na tela e o padrão toca junto, servindo de guia.")]
},
"en": {
  "title":"Free online metronome — accents, subdivisions and tap tempo | RudiMaster",
  "desc":"Accurate online metronome with per-beat accent or mute, subdivision in eighths, triplets and sixteenths, tap tempo and progressive speed-up. No ads.",
  "h1sub":"Online metronome with per-beat accents, subdivisions and tap tempo",
  "aboutTitle":"A metronome that does what practice needs",
  "about":"The click is scheduled by the browser's audio clock rather than by an interface timer, which is what causes the annoying wobble in most web metronomes. Tempo stays steady even when the tab is busy.",
  "featTitle":"What you can set",
  "feats":["Tempo from 30 to 300 bpm, with steps of five, a slider and tap tempo.",
           "One to twelve beats per bar.",
           "Subdivision in quarters, eighths, triplets or sixteenths, with a quieter click on subdivisions.",
           "Accent, normal click or silence on any beat by tapping its dot. Muting beats is the classic way to train internal time.",
           "Progressive speed-up, raising the tempo automatically every few bars.",
           "The screen stays awake while you practise, and the counter shows bar and elapsed time."],
  "faqTitle":"Frequently asked questions",
  "faq":[("Does the metronome work offline?","Yes. After the first load the page runs without a connection, and it can be installed to your phone's home screen."),
         ("Why mute some beats?","Playing with silent beats forces you to hold the pulse yourself. It is one of the most efficient exercises for internal time, and it makes any drifting obvious."),
         ("How is this different from the rudiments mode?","In rudiments mode, on top of the click, the notation for the chosen rudiment scrolls across the screen and the pattern plays along as a guide.")]
},
"es": {
  "title":"Metrónomo online gratis — acentos, subdivisiones y tap tempo | RudiMaster",
  "desc":"Metrónomo online preciso, con acento o silencio en cada tiempo, subdivisión en corcheas, tresillos y semicorcheas, tap tempo y aceleración progresiva. Sin anuncios.",
  "h1sub":"Metrónomo online con acentos por tiempo, subdivisiones y tap tempo",
  "aboutTitle":"Un metrónomo que hace lo que el estudio pide",
  "about":"El clic lo programa el reloj de audio del navegador y no un temporizador de interfaz, que es lo que provoca esa oscilación molesta en la mayoría de los metrónomos web. El tempo se mantiene estable aunque la pestaña esté ocupada.",
  "featTitle":"Qué puedes configurar",
  "feats":["Tempo de 30 a 300 bpm, con botones de cinco en cinco, deslizador y tap tempo.",
           "De uno a doce tiempos por compás.",
           "Subdivisión en negras, corcheas, tresillos o semicorcheas, con clic más bajo en las subdivisiones.",
           "Acento, clic normal o silencio en cada tiempo, tocando su punto. Silenciar tiempos es la forma clásica de entrenar el tiempo interno.",
           "Aceleración progresiva, subiendo el tempo automáticamente cada cierto número de compases.",
           "La pantalla no se apaga mientras practicas, y el contador muestra compás y tiempo transcurrido."],
  "faqTitle":"Preguntas frecuentes",
  "faq":[("¿El metrónomo funciona sin conexión?","Sí. Tras la primera carga la página funciona sin internet, y se puede instalar en la pantalla de inicio del móvil."),
         ("¿Por qué silenciar algunos tiempos?","Tocar con tiempos mudos te obliga a sostener el pulso por tu cuenta. Es uno de los ejercicios más eficientes para el tiempo interno, y deja en evidencia cualquier desvío."),
         ("¿En qué se diferencia del modo rudimentos?","En el modo rudimentos, además del clic, la partitura del rudimento elegido corre por la pantalla y el patrón suena a la vez, sirviendo de guía.")]
}}

PATTERNS = {
 "s1":"RLRLRLRL","s2":"RRLLRRLL","s3":"RRRLLLRRRLLL","r5":"RRLLR LLRRL","r6":"RLLRRL LRRLLR",
 "r7":"RRLLRRL LLRRLLR","r9":"RRLLRRLLR LLRRLLRRL","p1":"RLRR LRLL","p2":"RLRLRR LRLRLL",
 "p3":"RLRLRLRR LRLRLRLL","pd":"RLRRLL RLRRLL","f1":"RLRL","f2":"RRLL","f3":"RLRLRL",
 "f4":"RLRLR LRLRL","d1":"RLRL","d2":"RLLR","d3":"RLRL LRLR"}
CATS = {"roll":["s1","s2","s3","r5","r6","r7","r9"],"para":["p1","p2","p3","pd"],
        "flam":["f1","f2","f3","f4"],"drag":["d1","d2","d3"]}

HOME  = {"pt":"/","en":"/en/","es":"/es/"}
PATHS = {"pt":"/rudimentos/","en":"/en/rudiments/","es":"/es/rudimentos/"}
MET   = {"pt":"/metronomo/","en":"/en/metronome/","es":"/es/metronomo/"}

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def sticking(code, letters):
    return " ".join(letters[c] for c in PATTERNS[code].replace(" ",""))

def rud_lists(code):
    ui = UI[code]; out = []
    for cat, ids in CATS.items():
        items = "".join(
            '<li><b>%s</b><code>%s</code></li>' % (esc(ui["names"][i]), sticking(i, ui["letters"]))
            for i in ids)
        out.append('<div class="fam"><h3>%s</h3><ul class="rudlist">%s</ul></div>' % (esc(ui["cats"][cat]), items))
    return "".join(out)

def hreflang(code, group=None):
    g = group or PATHS
    tags = "".join('<link rel="alternate" hreflang="%s" href="%s%s" />' % (c, BASE, g[c]) for c in g)
    return tags + '<link rel="alternate" hreflang="x-default" href="%s%s" />' % (BASE, g["en"])

def langmenu(code, group=None):
    g = group or PATHS
    return "".join('<a href="%s" hreflang="%s" aria-current="%s">%s</a>' %
                   (g[c], UI[c]["html"], "true" if c == code else "false", UI[c]["label"]) for c in g)

def jsonld(code, seo=None, path=None, extra_type="WebApplication"):
    s = seo or SEO[code]
    app = {"@context":"https://schema.org","@type":"WebApplication","name":"RudiMaster",
           "url":BASE+(path or PATHS[code]),"description":s["desc"],"applicationCategory":"MultimediaApplication",
           "operatingSystem":"Any","inLanguage":UI[code]["html"],
           "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},
           "featureList":[UI[code]["names"][i] for i in PATTERNS]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
           {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faq"]]}
    return ('<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
            % (json.dumps(app, ensure_ascii=False), json.dumps(faq, ensure_ascii=False)))

FAB_LABEL = {"pt":"Apoiar o projeto","en":"Support the project","es":"Apoyar el proyecto"}
FAB_CLOSE = {"pt":"Esconder","en":"Hide","es":"Ocultar"}


def heart(code):
    return ('<a class="chip heart" href="%s" aria-label="%s" title="%s">'
            '<svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M12 20.3s-7.2-4.5-7.2-9.2a4 4 0 0 1 7.2-2.5 4 4 0 0 1 7.2 2.5c0 4.7-7.2 9.2-7.2 9.2z"/>'
            '</svg></a>' % (DN.PATHS[code], esc(FAB_LABEL[code]), esc(DN.NAV[code])))


def fab(code):
    """Bolha flutuante de apoio. Some enquanto o metronomo esta tocando."""
    return (
      '<a class="fab" id="fab" href="%s" aria-label="%s">'
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.7-7.5-9.6a4.2 4.2 0 0 1 7.5-2.6 4.2 4.2 0 0 1 7.5 2.6c0 4.9-7.5 9.6-7.5 9.6z"/></svg>'
      '<span>%s</span></a>'
      '<button class="fabx" id="fabx" aria-label="%s">&times;</button>'
      '<script>(function(){var f=document.getElementById("fab"),x=document.getElementById("fabx");'
      'try{var t=Number(localStorage.getItem("rudi-fab")||0);'
      'if(Date.now()-t<2592000000){f.remove();x.remove();return;}}catch(e){}'
      'setTimeout(function(){f.classList.add("show");x.classList.add("show");},60000);'
      'x.addEventListener("click",function(){f.remove();x.remove();'
      'try{localStorage.setItem("rudi-fab",String(Date.now()));}catch(e){}});})();</script>'
      % (DN.PATHS[code], esc(FAB_LABEL[code]), esc(DN.NAV[code]), esc(FAB_CLOSE[code])))

MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true">'
  '<circle cx="32" cy="32" r="32" fill="var(--btn)"/>'
  '<circle cx="32" cy="32" r="25" fill="none" stroke="var(--btn-ink)" stroke-opacity=".32" stroke-width="1.9"/>'
  '<path d="M16.5 19.5 L25.5 23 L16.5 26.5" fill="none" stroke="var(--btn-ink)" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"/>'
  '<rect x="34" y="18.5" width="3.4" height="21.5" rx="1.2" fill="var(--btn-ink)"/>'
  '<ellipse cx="27.4" cy="39" rx="10" ry="7.2" fill="var(--btn-ink)" transform="rotate(-20 27.4 39)"/>'
  '</svg>')

TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-theme="paper" data-lang="{code}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{base}{path}" />
{hreflang}
<meta name="theme-color" content="#E7DFCC" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="RudiMaster" />
<meta property="og:locale" content="{oglocale}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{base}{path}" />
<meta property="og:image" content="{base}/og-{code}.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{base}/og-{code}.png" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.webmanifest" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" />
<link rel="stylesheet" href="/styles.css" />
<script>try{{var t=localStorage.getItem('rudi-theme');if(t){{document.documentElement.dataset.theme=t;if(t==='night')document.querySelector('meta[name=theme-color]').content='#121110';}}}}catch(e){{}}</script>
{jsonld}
</head>
<body>

<div class="app rudpage">
  <div class="bar compact">
    <a class="chip back" href="{homepath}" aria-label="{homelab}">&#8592;</a>
    <a class="brand" href="{homepath}">
      {mark}
      <h1 class="wordmark"><b>Rudi</b><em>Master</em></h1>
    </a>
    <div class="tools">
      {heart}<button class="chip" id="langBtn" aria-haspopup="true" aria-label="{langlabel}">{langcode}</button>
      <nav class="langmenu" id="langMenu">{langmenu}</nav>
      <button class="chip" id="theme" aria-label="{theme}">&#9681;</button>
    </div>
    <p class="tagline">{tagline}</p>
  </div>

  <div class="now card">
    <button class="nav" id="prev" aria-label="&#8592;"><svg viewBox="0 0 12 12"><path d="M8 1L3 6l5 5"/></svg></button>
    <button class="body" id="openPicker">
      <span class="eyebrow">{rud}</span>
      <span class="name" id="rudName">{firstname}</span>
      <span class="stick" id="rudStick"></span>
      <span class="meta" id="rudMeta"></span>
    </button>
    <button class="nav" id="next" aria-label="&#8594;"><svg viewBox="0 0 12 12"><path d="M4 1l5 5-5 5"/></svg></button>
  </div>

  <div class="strip">
    <span class="tagsig" id="stripTag">4/4</span>
    <span class="lamp" id="lamp"></span>
    <canvas id="score" aria-label="{rud}"></canvas>
    <span class="fade l"></span><span class="fade r"></span>
  </div>

  <div class="console card">
    <div class="deck">
      <div class="pad" id="pad">
        <button id="play" aria-label="{play}"><svg viewBox="0 0 24 24" id="playIcon"><path d="M7 4l13 8-13 8z"/></svg></button>
      </div>
      <div class="tempo">
        <div class="stepper">
          <button class="step" id="minus" aria-label="-5 bpm">&minus;5</button>
          <div class="readout"><b id="bpmOut">100</b><span id="bpmUnit">{unit4}</span></div>
          <button class="step" id="plus" aria-label="+5 bpm">+5</button>
        </div>
        <input type="range" id="bpm" min="30" max="280" step="1" value="100" aria-label="bpm" />
        <div class="tempo-row">
          <button class="ghost" id="tap">{tap}</button>
          <span class="counter" id="counter">&mdash;</span>
        </div>
      </div>
    </div>
    <p class="hint" id="hint">{start}</p>
  </div>

  <details class="sheet card">
    <summary>{settings}</summary>
    <div class="body">
      <div><span class="lab">{sig}</span><div class="seg" id="segSig"></div></div>
      <div><span class="lab">{hand}</span><div class="seg" id="segHand">
        <button data-v="R" aria-pressed="true">{right}</button>
        <button data-v="L" aria-pressed="false">{left}</button>
      </div></div>
      <div><span class="lab">{sound}</span>
        <div class="checks">
          <label class="chk"><input type="checkbox" id="optMet" checked /> <span>{met}</span></label>
          <label class="chk"><input type="checkbox" id="optRud" checked /> <span>{rudSnd}</span></label>
          <label class="chk"><input type="checkbox" id="optStick" checked /> <span>{hands}</span></label>
          <label class="chk"><input type="checkbox" id="optCount" checked /> <span>{countIn}</span></label>
        </div>
      </div>
      <div class="pair">
        <div><label class="lab" for="volMet">{volMet}</label><input type="range" id="volMet" min="0" max="100" value="65" /></div>
        <div><label class="lab" for="volRud">{volRud}</label><input type="range" id="volRud" min="0" max="100" value="70" /></div>
      </div>
      <div><span class="lab">{prog}</span>
        <div class="checks"><label class="chk"><input type="checkbox" id="optProg" /> <span>{auto}</span></label></div>
        <div class="prog">
          <input type="number" id="progStep" value="4" min="1" max="20" inputmode="numeric" aria-label="bpm" /> <span>{every}</span>
          <input type="number" id="progEvery" value="8" min="1" max="64" inputmode="numeric" aria-label="{bars}" /> <span>{bars}</span>
        </div>
      </div>
    </div>
  </details>

  <p class="modeswitch"><a href="{metpath}">{tomet} &#8594;</a></p>
  <p class="keys">{keys}</p>
</div>

<div class="overlay" id="overlay">
  <div class="modal" role="dialog" aria-modal="true" aria-label="{rud}">
    <div class="head">
      <div class="grab"></div>
      <div class="search">
        <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="9" cy="9" r="6"/><path d="M13.5 13.5L17 17"/></svg>
        <input id="search" type="search" autocomplete="off" placeholder="{search}" aria-label="{search}" />
      </div>
    </div>
    <div class="list" id="rudList"></div>
  </div>
</div>

<main class="content">
  <section>
    <h2>{howTitle}</h2>
    <p>{howIntro}</p>
    <ol>{steps}</ol>
  </section>
  <section>
    <h2>{listTitle}</h2>
    <p>{listIntro}</p>
    {rudlists}
  </section>
  <section>
    <h2>{faqTitle}</h2>
    <div class="faq">{faq}</div>
  </section>
</main>

<footer class="sitefoot">
  <span>RudiMaster &middot; {footNote}</span>
  <span><a href="{donatepath}"><strong>{donatenav}</strong></a> &middot; {footlinks}</span>
</footer>

{fab}
<script src="/i18n.js"></script>
<script src="/app.js" defer></script>
</body>
</html>
"""

DONATE_TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-theme="paper" data-lang="{code}">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{base}{path}" />
{hreflang}
<meta name="theme-color" content="#E7DFCC" />
<meta name="robots" content="index,follow" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="RudiMaster" />
<meta property="og:locale" content="{oglocale}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{base}{path}" />
<meta property="og:image" content="{base}/og-{code}.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.webmanifest" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" />
<link rel="stylesheet" href="/styles.css" />
<script>try{{var t=localStorage.getItem('rudi-theme');if(t){{document.documentElement.dataset.theme=t;if(t==='night')document.querySelector('meta[name=theme-color]').content='#121110';}}}}catch(e){{}}</script>
</head>
<body>

<div class="app">
  <div class="bar">
    <a class="brand" href="{applink}" style="text-decoration:none">
      {mark}
      <span class="wordmark"><b>Rudi</b><em>Master</em></span>
    </a>
    <div class="tools">
      {heart}<button class="chip" id="langBtn" aria-haspopup="true" aria-label="{langlabel}">{langcode}</button>
      <nav class="langmenu" id="langMenu">{langmenu}</nav>
      <button class="chip" id="theme" aria-label="{theme}">&#9681;</button>
    </div>
  </div>
</div>

<main class="page">
  <h1 class="pagetitle">{h1}</h1>
  <p class="lead">{lead}</p>

  <section class="first">
    {options}
  </section>

  <section>
    <h2>{whatTitle}</h2>
    <ul class="ticks">{what}</ul>
  </section>

  <section>
    <h2>{freeTitle}</h2>
    <ul class="ticks">{free}</ul>
  </section>

  <p class="thanks">{thanks}</p>
  <p><a class="backlink" href="{applink}">&#8592; {back}</a></p>
</main>

<footer class="sitefoot">
  <span>RudiMaster</span>
  <span>{footlinks}</span>
</footer>

<script>
(function(){{
  var b=document.getElementById('langBtn'), m=document.getElementById('langMenu');
  b.addEventListener('click',function(e){{e.stopPropagation();m.classList.toggle('open');}});
  document.addEventListener('click',function(){{m.classList.remove('open');}});
  document.getElementById('theme').addEventListener('click',function(){{
    var n=document.documentElement.dataset.theme==='night'?'paper':'night';
    document.documentElement.dataset.theme=n;
    document.querySelector('meta[name=theme-color]').content=n==='night'?'#121110':'#E7DFCC';
    try{{localStorage.setItem('rudi-theme',n);}}catch(e){{}}
  }});
  var c=document.getElementById('pixCopy');
  if(c) c.addEventListener('click',function(){{
    var k=c.dataset.key, done=c.dataset.done, old=c.textContent;
    function ok(){{c.textContent=done;setTimeout(function(){{c.textContent=old;}},2200);}}
    if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(k).then(ok,ok);
    else {{var t=document.createElement('textarea');t.value=k;document.body.appendChild(t);t.select();
           try{{document.execCommand('copy');}}catch(e){{}}document.body.removeChild(t);ok();}}
  }});
}})();
</script>
</body>
</html>
"""


def donate_options(code):
    c, out = DN.COPY[code], []
    cfg = DN.DONATE
    if cfg["pix_key"]:
        out.append(
            '<div class="opt pix"><div class="opttxt"><h3>%s</h3><p>%s</p>'
            '<button class="btnmain" id="pixCopy" data-key="%s" data-done="%s">%s</button>'
            '<code class="pixkey">%s</code></div>'
            '<img class="qr" src="/pix-qr.png" width="220" height="220" alt="QR Code Pix" loading="lazy" /></div>'
            % (esc(c["pixTitle"]), esc(c["pixNote"]), esc(cfg["pix_key"]), esc(c["pixDone"]),
               esc(c["pixCopy"]), esc(cfg["pix_key"])))
    card = cfg["kofi"] or cfg["stripe"]
    if card:
        out.append('<div class="opt"><div class="opttxt"><h3>%s</h3><p>%s</p>'
                   '<a class="btnmain" href="%s" rel="noopener" target="_blank">%s</a></div></div>'
                   % (esc(c["kofiTitle"]), esc(c["kofiNote"]), esc(card), esc(c["kofiBtn"])))
    if cfg["paypal"]:
        out.append('<div class="opt"><div class="opttxt"><h3>%s</h3><p>%s</p>'
                   '<a class="btnmain" href="%s" rel="noopener" target="_blank">%s</a></div></div>'
                   % (esc(c["paypalTitle"]), esc(c["paypalNote"]), esc(cfg["paypal"]), esc(c["paypalBtn"])))
    if not out:
        out.append('<div class="opt"><div class="opttxt"><p>%s</p></div></div>' % esc(c["empty"]))
    return "".join(out)


def render_donate(code):
    ui, c = UI[code], DN.COPY[code]
    tags = "".join('<link rel="alternate" hreflang="%s" href="%s%s" />' % (k, BASE, v)
                   for k, v in DN.PATHS.items())
    tags += '<link rel="alternate" hreflang="x-default" href="%s%s" />' % (BASE, DN.PATHS["en"])
    menu = "".join('<a href="%s" hreflang="%s" aria-current="%s">%s</a>' %
                   (DN.PATHS[k], UI[k]["html"], "true" if k == code else "false", UI[k]["label"])
                   for k in DN.PATHS)
    footlinks = " &middot; ".join('<a href="%s" hreflang="%s">%s</a>' % (DN.PATHS[k], UI[k]["html"], UI[k]["label"])
                                  for k in DN.PATHS if k != code)
    oglocale = {"pt": "pt_BR", "en": "en_US", "es": "es_ES"}[code]
    return DONATE_TEMPLATE.format(
        htmllang=ui["html"], code=code, base=BASE, path=DN.PATHS[code], oglocale=oglocale,
        title=esc(c["title"]), desc=esc(c["desc"]), hreflang=tags, mark=MARK,
        langcode=code.upper(), langlabel=esc(ui["label"]), langmenu=menu, theme=esc(ui["theme"]),
        applink=PATHS[code], h1=esc(c["h1"]), lead=esc(c["lead"]),
        whatTitle=esc(c["whatTitle"]), what="".join("<li>%s</li>" % esc(x) for x in c["what"]),
        howTitle=esc(c["howTitle"]), options=donate_options(code),
        freeTitle=esc(c["freeTitle"]), free="".join("<li>%s</li>" % esc(x) for x in c["free"]),
        thanks=esc(c["thanks"]), back=esc(c["back"]), footlinks=footlinks, heart="")

HEAD_COMMON = """<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, maximum-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{base}{path}" />
{hreflang}
<meta name="theme-color" content="#E7DFCC" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="RudiMaster" />
<meta property="og:locale" content="{oglocale}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{base}{path}" />
<meta property="og:image" content="{base}/og-{code}.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{base}/og-{code}.png" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.webmanifest" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" />
<link rel="stylesheet" href="/styles.css" />
<script>try{{var t=localStorage.getItem('rudi-theme');if(t){{document.documentElement.dataset.theme=t;if(t==='night')document.querySelector('meta[name=theme-color]').content='#121110';}}}}catch(e){{}}</script>"""


HOME_TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-theme="paper" data-lang="{code}">
<head>
""" + HEAD_COMMON + """
{jsonld}
</head>
<body>

<div class="app">
  <div class="bar">
    <div class="brand">
      {mark}
      <span class="wordmark"><b>Rudi</b><em>Master</em></span>
    </div>
    <div class="tools">
      {heart}<button class="chip" id="langBtn" aria-haspopup="true" aria-label="{langlabel}">{langcode}</button>
      <nav class="langmenu" id="langMenu">{langmenu}</nav>
      <button class="chip" id="theme" aria-label="{theme}">&#9681;</button>
    </div>
    <p class="tagline">{tagline}</p>
  </div>
</div>

<main class="page home">
  <h1 class="pagetitle">{h1}</h1>
  <p class="lead">{lead}</p>

  <div class="choices">
    <a class="choice" href="{metpath}">
      <span class="glyph" aria-hidden="true">
        <svg viewBox="0 0 72 72"><circle cx="36" cy="36" r="27" fill="none" stroke="currentColor" stroke-width="2.4" opacity=".3"/><circle cx="36" cy="9.5" r="5" fill="var(--red)"/><circle cx="59" cy="49" r="4" fill="currentColor" opacity=".45"/><circle cx="13" cy="49" r="4" fill="currentColor" opacity=".45"/><rect x="34.4" y="20" width="3.2" height="18" rx="1.6" fill="currentColor"/></svg>
      </span>
      <span class="ctxt">
        <span class="ch2">{metTitle}</span>
        <span class="cdesc">{metDesc}</span>
        <span class="cgo">{cta} &#8594;</span>
      </span>
    </a>
    <a class="choice" href="{rudpath}">
      <span class="glyph" aria-hidden="true">
        <svg viewBox="0 0 72 72"><g stroke="currentColor" stroke-width="1.6" opacity=".3"><path d="M6 26h60M6 33h60M6 40h60M6 47h60"/></g><g fill="currentColor"><rect x="20" y="16" width="2.6" height="21" rx="1.3"/><rect x="38" y="16" width="2.6" height="21" rx="1.3"/><rect x="20" y="14" width="21" height="4.5" rx="1"/><ellipse cx="16.5" cy="37" rx="7" ry="5" transform="rotate(-20 16.5 37)"/><ellipse cx="34.5" cy="37" rx="7" ry="5" transform="rotate(-20 34.5 37)"/></g><path d="M50 46l8 3-8 3" fill="none" stroke="var(--red)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </span>
      <span class="ctxt">
        <span class="ch2">{rudTitle}</span>
        <span class="cdesc">{rudDesc}</span>
        <span class="cgo">{cta} &#8594;</span>
      </span>
    </a>
  </div>

  <section>
    <h2>{aboutTitle}</h2>
    <p>{about}</p>
  </section>
</main>

<footer class="sitefoot">
  <span><a href="{donatepath}"><strong>{donatenav}</strong></a></span>
  <span>{footlinks}</span>
</footer>

{fab}
<script src="/i18n.js"></script>
<script>
(function(){{
  var b=document.getElementById('langBtn'), m=document.getElementById('langMenu');
  b.addEventListener('click',function(e){{e.stopPropagation();m.classList.toggle('open');}});
  document.addEventListener('click',function(){{m.classList.remove('open');}});
  document.getElementById('theme').addEventListener('click',function(){{
    var n=document.documentElement.dataset.theme==='night'?'paper':'night';
    document.documentElement.dataset.theme=n;
    document.querySelector('meta[name=theme-color]').content=n==='night'?'#121110':'#E7DFCC';
    try{{localStorage.setItem('rudi-theme',n);}}catch(e){{}}
  }});
}})();
</script>
</body>
</html>
"""


MET_TEMPLATE = """<!DOCTYPE html>
<html lang="{htmllang}" data-theme="paper" data-lang="{code}">
<head>
""" + HEAD_COMMON + """
{jsonld}
</head>
<body>

<div class="app metpage">
  <div class="bar compact">
    <a class="chip back" href="{homepath}" aria-label="{homelab}">&#8592;</a>
    <a class="brand" href="{homepath}">
      {mark}
      <span class="wordmark"><b>Rudi</b><em>Master</em></span>
    </a>
    <div class="tools">
      {heart}<button class="chip" id="langBtn" aria-haspopup="true" aria-label="{langlabel}">{langcode}</button>
      <nav class="langmenu" id="langMenu">{langmenu}</nav>
      <button class="chip" id="theme" aria-label="{theme}">&#9681;</button>
    </div>
  </div>

  <h1 class="screentitle">{metTitle}<span class="sr"> — {h1sub}</span></h1>

  <div class="console card">
    <div class="deck">
      <div class="pad" id="pad">
        <button id="play" aria-label="{play}"><svg viewBox="0 0 24 24" id="playIcon"><path d="M7 4l13 8-13 8z"/></svg></button>
      </div>
      <div class="tempo">
        <div class="stepper">
          <button class="step" id="minus" aria-label="-5 bpm">&minus;5</button>
          <div class="readout"><b id="bpmOut">100</b><span>bpm</span></div>
          <button class="step" id="plus" aria-label="+5 bpm">+5</button>
        </div>
        <input type="range" id="bpm" min="30" max="300" step="1" value="100" aria-label="bpm" />
        <div class="tempo-row">
          <button class="ghost" id="tap">{tap}</button>
          <span class="counter"><span id="counter">&mdash;</span> &middot; <span id="elapsed">00:00</span></span>
        </div>
      </div>
    </div>
    <p class="hint" id="hint">{start}</p>
  </div>

  <div class="card metcfg">
    <div class="field">
      <span class="lab">{beatsLab}</span>
      <div class="numstep">
        <button class="step sm" id="beatsMinus" aria-label="-1">&minus;</button>
        <b id="beatsOut">4</b>
        <button class="step sm" id="beatsPlus" aria-label="+1">+</button>
      </div>
    </div>
    <div class="field wide">
      <span class="lab">{subLab}</span>
      <div class="seg" id="segSub">
        <button data-v="1" aria-pressed="true">{sub1}</button>
        <button data-v="2" aria-pressed="false">{sub2}</button>
        <button data-v="3" aria-pressed="false">{sub3}</button>
        <button data-v="4" aria-pressed="false">{sub4}</button>
      </div>
    </div>
    <p class="lughint">{lugHint}</p>
    <div class="field">
      <label class="lab" for="volMet">{volMet}</label>
      <input type="range" id="volMet" min="0" max="100" value="65" />
    </div>
    <div class="field">
      <span class="lab">{prog}</span>
      <div class="checks"><label class="chk"><input type="checkbox" id="optProg" /> <span>{auto}</span></label></div>
      <div class="prog">
        <input type="number" id="progStep" value="4" min="1" max="20" inputmode="numeric" aria-label="bpm" /> <span>{every}</span>
        <input type="number" id="progEvery" value="8" min="1" max="64" inputmode="numeric" aria-label="{bars}" /> <span>{bars}</span>
      </div>
    </div>
  </div>

  <p class="modeswitch"><a href="{rudpath}">{torud} &#8594;</a></p>
  <p class="keys">{keys}</p>
</div>

<main class="content">
  <section>
    <h2>{aboutTitle}</h2>
    <p>{about}</p>
  </section>
  <section>
    <h2>{featTitle}</h2>
    <ul class="ticks">{feats}</ul>
  </section>
  <section>
    <h2>{faqTitle}</h2>
    <div class="faq">{faq}</div>
  </section>
</main>

<footer class="sitefoot">
  <span><a href="{donatepath}"><strong>{donatenav}</strong></a> &middot; <a href="{homepath}">{homelab}</a></span>
  <span>{footlinks}</span>
</footer>

{fab}
<script src="/i18n.js"></script>
<script src="/metronome.js" defer></script>
</body>
</html>
"""


def render_home(code):
    ui, s = UI[code], HOME_SEO[code]
    footlinks = " &middot; ".join('<a href="%s" hreflang="%s">%s</a>' % (HOME[c], UI[c]["html"], UI[c]["label"])
                                  for c in HOME if c != code)
    ld = {"@context":"https://schema.org","@type":"WebSite","name":"RudiMaster",
          "url":BASE+HOME[code],"description":s["desc"],"inLanguage":UI[code]["html"]}
    return HOME_TEMPLATE.format(
        htmllang=ui["html"], code=code, base=BASE, path=HOME[code],
        oglocale={"pt":"pt_BR","en":"en_US","es":"es_ES"}[code],
        title=esc(s["title"]), desc=esc(s["desc"]), hreflang=hreflang(code, HOME),
        jsonld='<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False),
        mark=MARK, langcode=code.upper(), langlabel=esc(ui["label"]),
        langmenu=langmenu(code, HOME), theme=esc(ui["theme"]), tagline=esc(ui["tagline"]),
        h1=esc(s["h1"]), lead=esc(s["lead"]),
        metpath=MET[code], rudpath=PATHS[code],
        metTitle=esc(s["metTitle"]), metDesc=esc(s["metDesc"]),
        rudTitle=esc(s["rudTitle"]), rudDesc=esc(s["rudDesc"]), cta=esc(s["cta"]),
        aboutTitle=esc(s["aboutTitle"]), about=esc(s["about"]),
        donatepath=DN.PATHS[code], donatenav=esc(DN.NAV[code]), footlinks=footlinks, fab=fab(code), heart=heart(code))


def render_met(code):
    ui, s = UI[code], MET_SEO[code]
    footlinks = " &middot; ".join('<a href="%s" hreflang="%s">%s</a>' % (MET[c], UI[c]["html"], UI[c]["label"])
                                  for c in MET if c != code)
    return MET_TEMPLATE.format(
        htmllang=ui["html"], code=code, base=BASE, path=MET[code],
        oglocale={"pt":"pt_BR","en":"en_US","es":"es_ES"}[code],
        title=esc(s["title"]), desc=esc(s["desc"]), hreflang=hreflang(code, MET),
        jsonld=jsonld(code, s, MET[code]), mark=MARK,
        langcode=code.upper(), langlabel=esc(ui["label"]), langmenu=langmenu(code, MET),
        theme=esc(ui["theme"]), homepath=HOME[code], homelab=esc(ui["home"]),
        metTitle=esc(HOME_SEO[code]["metTitle"]), h1sub=esc(s["h1sub"]),
        play=esc(ui["play"]), tap=esc(ui["tap"]), start=esc(ui["start"]),
        beatsLab=esc(ui["beatsLab"]), subLab=esc(ui["subLab"]),
        sub1=esc(ui["subs"][0]), sub2=esc(ui["subs"][1]), sub3=esc(ui["subs"][2]), sub4=esc(ui["subs"][3]),
        lugHint=esc(ui["lugHint"]), volMet=esc(ui["volMet"]),
        prog=esc(ui["prog"]), auto=esc(ui["auto"]), every=esc(ui["every"]), bars=esc(ui["bars"]),
        rudpath=PATHS[code], torud=esc(ui["toRud"]), keys=ui["keys"],
        aboutTitle=esc(s["aboutTitle"]), about=esc(s["about"]),
        featTitle=esc(s["featTitle"]), feats="".join("<li>%s</li>" % esc(x) for x in s["feats"]),
        faqTitle=esc(s["faqTitle"]),
        faq="".join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in s["faq"]),
        donatepath=DN.PATHS[code], donatenav=esc(DN.NAV[code]), footlinks=footlinks, fab=fab(code), heart=heart(code))


def render(code):
    ui, s = UI[code], SEO[code]
    steps = "".join("<li>%s</li>" % esc(x) for x in s["steps"])
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in s["faq"])
    footlinks = " · ".join('<a href="%s" hreflang="%s">%s</a>' % (PATHS[c], UI[c]["html"], UI[c]["label"])
                           for c in PATHS if c != code)
    oglocale = {"pt":"pt_BR","en":"en_US","es":"es_ES"}[code]
    return TEMPLATE.format(
        htmllang=ui["html"], code=code, base=BASE, path=PATHS[code], oglocale=oglocale,
        title=esc(s["title"]), desc=esc(s["desc"]), hreflang=hreflang(code), jsonld=jsonld(code),
        mark=MARK, h1sub=esc(s["h1sub"]), tagline=ui["tagline"], langcode=code.upper(),
        langlabel=ui["label"], langmenu=langmenu(code), theme=esc(ui["theme"]),
        rud=esc(ui["rud"]), firstname=esc(ui["names"]["p1"]), play=esc(ui["play"]),
        unit4=esc(ui["unit4"]), tap=esc(ui["tap"]), start=esc(ui["start"]), settings=esc(ui["settings"]),
        sig=esc(ui["sig"]), hand=esc(ui["hand"]), right=esc(ui["right"]), left=esc(ui["left"]),
        sound=esc(ui["sound"]), met=esc(ui["met"]), rudSnd=esc(ui["rudSnd"]), hands=esc(ui["hands"]),
        countIn=esc(ui["countIn"]), volMet=esc(ui["volMet"]), volRud=esc(ui["volRud"]),
        prog=esc(ui["prog"]), auto=esc(ui["auto"]), every=esc(ui["every"]), bars=esc(ui["bars"]),
        keys=ui["keys"], search=esc(ui["search"]),
        howTitle=esc(s["howTitle"]), howIntro=esc(s["howIntro"]), steps=steps,
        listTitle=esc(s["listTitle"]), listIntro=esc(s["listIntro"]), rudlists=rud_lists(code),
        faqTitle=esc(s["faqTitle"]), faq=faq, footNote=esc(s["footNote"]), footlinks=footlinks,
        donatepath=DN.PATHS[code], donatenav=esc(DN.NAV[code]),
        homepath=HOME[code], homelab=esc(ui["home"]), metpath=MET[code], tomet=esc(ui["toMet"]),
        fab=fab(code), heart=heart(code))

def write(rel, text):
    if ANALYTICS_TAG and rel.endswith("index.html"):
        text = text.replace("</head>", ANALYTICS_TAG + "</head>", 1)
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)
    return rel

def main():
    made = []
    for code, path in HOME.items():
        rel = "index.html" if path == "/" else path.strip("/") + "/index.html"
        made.append(write(rel, render_home(code)))
    for code, path in PATHS.items():
        made.append(write(path.strip("/") + "/index.html", render(code)))
    for code, path in MET.items():
        made.append(write(path.strip("/") + "/index.html", render_met(code)))

    for code, dpath in DN.PATHS.items():
        made.append(write(dpath.strip("/") + "/index.html", render_donate(code)))

    if DN.DONATE["pix_key"]:
        payload = DN.pix_payload(DN.DONATE["pix_key"], DN.DONATE["pix_name"], DN.DONATE["pix_city"])
        DN.write_pix_qr(os.path.join(OUT, "pix-qr.png"), payload)
        made.append("pix-qr.png")
    else:
        print("aviso: chave Pix vazia em donate.py, o bloco de Pix nao aparece na pagina")
    if not (DN.DONATE["kofi"] or DN.DONATE["stripe"]):
        print("aviso: nenhum link de cartao configurado em donate.py")
    if not DN.DONATE["paypal"]:
        print("aviso: PayPal nao configurado em donate.py")

    made.append(write("i18n.js", "window.RUDI_I18N = %s;\n" % json.dumps(UI, ensure_ascii=False)))

    def block(group, prio):
        return "".join(
            "<url><loc>%s%s</loc><changefreq>monthly</changefreq><priority>%s</priority>%s</url>" % (
                BASE, p, prio,
                "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (c2, BASE, p2)
                        for c2, p2 in group.items()))
            for p in group.values())
    urls = block(HOME, "1.0") + block(MET, "0.9") + block(PATHS, "0.9") + block(DN.PATHS, "0.5")
    made.append(write("sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">%s</urlset>\n' % urls))

    made.append(write("robots.txt",
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE))

    made.append(write("manifest.webmanifest", json.dumps({
        "name":"RudiMaster","short_name":"RudiMaster","start_url":"/","display":"standalone",
        "background_color":"#E7DFCC","theme_color":"#E7DFCC","orientation":"any",
        "description":SEO["en"]["desc"],
        "icons":[{"src":"/icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
                 {"src":"/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
                 {"src":"/icon-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]
    }, ensure_ascii=False, indent=2)))

    made.append(write("vercel.json", json.dumps({
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": [
            {"source":"/(.*)","headers":[
                {"key":"X-Content-Type-Options","value":"nosniff"},
                {"key":"Referrer-Policy","value":"strict-origin-when-cross-origin"},
                {"key":"Permissions-Policy","value":"geolocation=(), camera=(), microphone=()"}]},
            {"source":"/(.*)\\.(png|svg|webmanifest|ico)","headers":[
                {"key":"Cache-Control","value":"public, max-age=31536000, immutable"}]},
            {"source":"/(app|i18n).js","headers":[
                {"key":"Cache-Control","value":"public, max-age=3600, must-revalidate"}]},
            {"source":"/styles.css","headers":[
                {"key":"Cache-Control","value":"public, max-age=3600, must-revalidate"}]}]
    }, indent=2)))

    print("gerado:", ", ".join(made))

if __name__ == "__main__":
    main()

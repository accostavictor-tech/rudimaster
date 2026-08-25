# RudiMaster

Prática de rudimentos no pad, com metrônomo e partitura animada. Site estático, sem framework, sem build step, sem dependências em runtime além das fontes do Google.

## Estrutura

```
index.html              home em português (escolha entre metrônomo e rudimentos)
en/index.html es/index.html          home em inglês e espanhol
metronomo/ en/metronome/ es/metronomo/    tela só do metrônomo
rudimentos/ en/rudiments/ es/rudimentos/  tela de treino de rudimentos
styles.css              estilos compartilhados
app.js                  motor da tela de rudimentos: áudio, notação e interface
metronome.js            motor da tela do metrônomo
i18n.js                 dicionário dos três idiomas (gerado pelo build)
build.py                gera todas as páginas, i18n.js, sitemap, robots, manifest e vercel.json
donate.py               configuração, textos e gerador do BR Code Pix da página de apoio
apoiar/ en/support/ es/apoyar/   página de doação nos três idiomas
icons.py                gera favicon PNG, ícones do PWA e as imagens de compartilhamento
favicon.svg             favicon vetorial
og-pt.png og-en.png og-es.png    imagens de compartilhamento (1200×630)
icon-192.png icon-512.png icon-maskable.png apple-touch-icon.png
manifest.webmanifest robots.txt sitemap.xml vercel.json
```

## Subir no Vercel

Não existe etapa de build. O Vercel serve a pasta como está.

**Pelo painel:** crie um repositório com esses arquivos, importe em vercel.com/new, deixe Framework Preset em `Other`, Build Command vazio e Output Directory vazio (raiz). Deploy.

**Pelo terminal:**

```bash
npm i -g vercel
cd rudimaster
vercel          # preview
vercel --prod   # produção
```

## Analytics

Usa Vercel Web Analytics, que é sem cookie e não exige banner de consentimento.
A tag é injetada nas doze páginas pelo `build.py`, a partir das constantes
`VERCEL_ANALYTICS` e `VERCEL_SPEED_INSIGHTS` no topo do arquivo.

Só funciona depois de habilitar em Settings, Analytics, no painel do projeto.
O caminho `/_vercel/insights/script.js` só existe quando o recurso está ligado.

O app chama `track('practice_start', ...)` quando alguém aperta o play, com o modo,
o rudimento, o bpm e a subdivisão. Eventos personalizados só são registrados em
plano Pro, então no plano gratuito a chamada não faz nada e não quebra nada.
Se você migrar de plano, os eventos passam a aparecer sem mexer no código.

## Configurar a página de apoio

Abra `donate.py` e preencha o dicionário `DONATE`. Cada bloco vazio simplesmente não aparece na página, e o build avisa no terminal o que ainda falta.

```python
DONATE = {
    "pix_key":  "sua@chave.pix",   # e-mail, telefone, CPF/CNPJ ou chave aleatória
    "pix_name": "SEU NOME",        # até 25 caracteres, sem acento
    "pix_city": "MACEIO",          # até 15 caracteres, sem acento
    "kofi":     "https://ko-fi.com/seuusuario",
    "paypal":   "https://paypal.me/seuusuario",
    "stripe":   "",                # alternativa ao Ko-fi, se preferir
}
```

Rode `python3 build.py`. Se a chave Pix estiver preenchida, ele gera `pix-qr.png` com o BR Code estático, sem valor fixo, então quem doa escolhe quanto. O algoritmo segue o padrão EMV do Banco Central, com CRC16-CCITT.

Sugestão de conta para receber cartão internacional: o Ko-fi não cobra taxa sobre doação, apenas a taxa do processador. O Stripe funciona igual via link de pagamento avulso, com taxa maior por transação.

## Antes de publicar

1. Abra `build.py` e troque a constante `BASE` pelo domínio real. Ela alimenta canonical, hreflang, Open Graph e sitemap.
2. Rode `python3 build.py` para regerar as páginas.
3. Se o domínio mudar, rode também `python3 icons.py` para atualizar o rodapé das imagens de compartilhamento (a URL está escrita nelas).
4. No painel do Vercel, adicione o domínio em Settings, Domains, e aponte o DNS.
5. Cadastre o site no Google Search Console e envie `https://SEUDOMINIO/sitemap.xml`.

## Para editar

Rudimentos ficam em `app.js`, no array `RUDIMENTS`. Cada nota é `{s, d, a, g}`: mão (`R` ou `L`), duração em tempos (0.25 é semicolcheia, 1/6 é sextina), acento e ornamento (1 é flam, 2 é drag). Ao adicionar um rudimento, inclua o nome nos três idiomas em `build.py`, dentro de `UI[lang]["names"]`, e o sticking em `PATTERNS`, depois rode `python3 build.py`.

Textos de interface e conteúdo de SEO também ficam em `build.py`, nos dicionários `UI` e `SEO`. O `build.py` é a única fonte de verdade: ele escreve o `i18n.js` consumido pelo navegador.

## Otimizações que valem depois

Auto-hospedar as fontes do Google elimina duas conexões externas e melhora o LCP. Baixe os arquivos woff2 do Big Shoulders Display e do IBM Plex, coloque em `/fonts` e substitua a tag `<link>` por um `@font-face` com `font-display: swap` em `styles.css`.

Um service worker simples com cache-first nos assets deixa o app funcional offline de forma confiável e completa o PWA.

O próximo passo de SEO é criar uma página por rudimento em cada idioma, no formato `/rufo-duplo/`, `/en/double-stroke-roll/`, `/es/redoble-doble/`, cada uma com explicação, aplicação musical e o app já carregado naquele rudimento via âncora (`/#s2`). São 54 páginas de intenção alta geradas pelo mesmo `build.py`.

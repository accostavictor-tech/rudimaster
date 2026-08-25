# Como colocar este repositório no seu GitHub

Este diretório já é um repositório Git com o primeiro commit feito.
Falta apenas apontar para o seu GitHub e enviar.

## 1. Ajuste a autoria do commit

O commit inicial foi criado com um autor genérico. Corrija para o seu:

```bash
git config user.name "Seu Nome"
git config user.email "seu@email.com"
git commit --amend --reset-author --no-edit
```

## 2. Crie o repositório vazio no GitHub

Pelo site: github.com/new, nome `rudimaster`, **sem** marcar README,
.gitignore ou licença. Um repositório vazio evita conflito no primeiro push.

Ou pela linha de comando, se você tiver o GitHub CLI instalado:

```bash
gh repo create rudimaster --private --source=. --remote=origin --push
```

Se usar o `gh`, pule o passo 3.

## 3. Aponte o remote e envie

```bash
git remote add origin git@github.com:SEU-USUARIO/rudimaster.git
git push -u origin main
```

Se preferir HTTPS no lugar de SSH:

```bash
git remote add origin https://github.com/SEU-USUARIO/rudimaster.git
git push -u origin main
```

## 4. Conecte ao Vercel

No painel do Vercel, vá em Add New, Project, e importe o repositório.
Framework Preset em `Other`, Build Command vazio, Output Directory vazio.

A partir daí, cada `git push` publica sozinho.

Se o projeto no Vercel já existe (criado via Drop, por exemplo), abra
Settings, Git, e conecte o repositório ao projeto existente em vez de
criar um novo. Assim você mantém o domínio já configurado.

## Fluxo do dia a dia

```bash
# editar textos, rotas ou rudimentos
python3 build.py          # regera as 12 páginas, sitemap e i18n.js
git add -A
git commit -m "descrição da mudança"
git push
```

O Vercel publica em seguida. Cada commit vira uma versão para a qual
você pode voltar com um clique em Deployments.

## Antes do primeiro deploy em produção

Abra `build.py`, troque a constante `BASE` pelo domínio real e rode
`python3 build.py`. É de lá que saem canonical, hreflang, Open Graph e
sitemap das doze páginas.

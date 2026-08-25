#!/usr/bin/env python3
"""Pagina de apoio do RudiMaster: configuracao, textos e geracao do BR Code Pix."""

# ---------------------------------------------------------------------------
# PREENCHA AQUI. Cada bloco vazio simplesmente nao aparece na pagina.
# ---------------------------------------------------------------------------
DONATE = {
    "pix_key":  "rudimasterapp@gmail.com",          # chave Pix: e-mail, telefone (+5582...), CPF/CNPJ ou chave aleatoria
    "pix_name": "VICTOR A C COSTA",          # nome do recebedor, ate 25 caracteres, sem acento
    "pix_city": "MACEIO",    # cidade, ate 15 caracteres, sem acento
    "kofi":     "https://ko-fi.com/rudimaster",          # ex.: https://ko-fi.com/rudimaster
    "paypal":   "",          # ex.: https://paypal.me/seuusuario
    "stripe":   "",          # link de pagamento avulso do Stripe
}

PATHS = {"pt": "/apoiar/", "en": "/en/support/", "es": "/es/apoyar/"}

COPY = {
"pt": {
  "title": "Apoie o RudiMaster — mantenha a ferramenta grátis e sem anúncios",
  "desc": "O RudiMaster é grátis, sem anúncios e sem cadastro. Se ele te ajuda a treinar, você pode apoiar o projeto com qualquer valor via Pix ou cartão.",
  "h1": "Apoie o projeto",
  "lead": "O RudiMaster é grátis e vai continuar assim. Sem anúncio, sem cadastro, sem versão paga escondida atrás de um paywall. Se ele faz parte do seu treino, uma contribuição ajuda a manter o projeto de pé.",
  "whatTitle": "Para onde vai o dinheiro",
  "what": ["Domínio e hospedagem, que são os custos fixos do site.",
           "Tempo de desenvolvimento: rudimentos novos, rotinas de treino salvas e histórico de andamento.",
           "Manter tudo sem anúncio, que é a parte que mais atrapalharia quem usa a tela durante o estudo."],
  "howTitle": "Como contribuir",
  "pixTitle": "Pix",
  "pixNote": "Aponte a câmera do seu banco para o código ou copie a chave. Você escolhe o valor.",
  "pixCopy": "Copiar chave Pix",
  "pixDone": "Chave copiada",
  "kofiTitle": "Cartão de crédito",
  "kofiNote": "Pagamento único, sem criar conta. Aceita cartão, Apple Pay e Google Pay.",
  "kofiBtn": "Contribuir com cartão",
  "paypalTitle": "PayPal",
  "paypalNote": "Para quem prefere PayPal ou está fora do Brasil.",
  "paypalBtn": "Contribuir pelo PayPal",
  "freeTitle": "Formas de ajudar sem gastar nada",
  "free": ["Mande o link para o seu professor, para a banda ou para o grupo de bateria.",
           "Conte o que está faltando. Feedback de quem treina de verdade é o que direciona o que vem depois.",
           "Se achou um erro em algum rudimento, avise. Notação errada atrapalha estudo."],
  "thanks": "Obrigado por manter isso vivo.",
  "back": "Voltar ao treino",
  "empty": "As formas de contribuição estão sendo configuradas. Volte em breve."
},
"en": {
  "title": "Support RudiMaster — keep the tool free and ad-free",
  "desc": "RudiMaster is free, ad-free and needs no account. If it helps your practice, you can support the project with any amount by Pix or card.",
  "h1": "Support the project",
  "lead": "RudiMaster is free and will stay that way. No ads, no sign-up, no paid tier hidden behind a paywall. If it is part of your practice routine, a contribution helps keep the project running.",
  "whatTitle": "Where the money goes",
  "what": ["Domain and hosting, the fixed costs of running the site.",
           "Development time: more rudiments, saved practice routines and tempo history.",
           "Keeping everything ad-free, which is the part that would hurt most for anyone staring at the screen while practising."],
  "howTitle": "How to contribute",
  "pixTitle": "Pix",
  "pixNote": "Brazilian instant payment. Scan the code with your bank app or copy the key. You choose the amount.",
  "pixCopy": "Copy Pix key",
  "pixDone": "Key copied",
  "kofiTitle": "Credit card",
  "kofiNote": "One-off payment, no account needed. Card, Apple Pay and Google Pay accepted.",
  "kofiBtn": "Contribute by card",
  "paypalTitle": "PayPal",
  "paypalNote": "For anyone who would rather use PayPal.",
  "paypalBtn": "Contribute via PayPal",
  "freeTitle": "Ways to help that cost nothing",
  "free": ["Send the link to your teacher, your band or your drum group.",
           "Tell me what is missing. Feedback from people who actually practise is what shapes what comes next.",
           "If you spot a mistake in a rudiment, say so. Wrong notation gets in the way of practice."],
  "thanks": "Thank you for keeping this alive.",
  "back": "Back to practice",
  "empty": "Contribution options are being set up. Please check back soon."
},
"es": {
  "title": "Apoya RudiMaster — mantén la herramienta gratis y sin anuncios",
  "desc": "RudiMaster es gratis, sin anuncios y sin registro. Si te ayuda a practicar, puedes apoyar el proyecto con cualquier cantidad por Pix o tarjeta.",
  "h1": "Apoya el proyecto",
  "lead": "RudiMaster es gratis y seguirá siéndolo. Sin anuncios, sin registro, sin versión de pago escondida tras un muro. Si forma parte de tu rutina, una contribución ayuda a mantener el proyecto en pie.",
  "whatTitle": "A dónde va el dinero",
  "what": ["Dominio y alojamiento, los costes fijos del sitio.",
           "Tiempo de desarrollo: más rudimentos, rutinas de práctica guardadas e historial de tempo.",
           "Mantenerlo todo sin anuncios, que es lo que más molestaría a quien mira la pantalla mientras practica."],
  "howTitle": "Cómo contribuir",
  "pixTitle": "Pix",
  "pixNote": "Pago instantáneo brasileño. Escanea el código con tu banco o copia la clave. Tú eliges la cantidad.",
  "pixCopy": "Copiar clave Pix",
  "pixDone": "Clave copiada",
  "kofiTitle": "Tarjeta de crédito",
  "kofiNote": "Pago único, sin crear cuenta. Acepta tarjeta, Apple Pay y Google Pay.",
  "kofiBtn": "Contribuir con tarjeta",
  "paypalTitle": "PayPal",
  "paypalNote": "Para quien prefiere PayPal.",
  "paypalBtn": "Contribuir por PayPal",
  "freeTitle": "Formas de ayudar sin gastar nada",
  "free": ["Manda el enlace a tu profesor, a tu banda o a tu grupo de batería.",
           "Cuéntame qué falta. El feedback de quien practica de verdad es lo que orienta lo que viene después.",
           "Si encuentras un error en algún rudimento, avísame. Una notación equivocada estorba el estudio."],
  "thanks": "Gracias por mantener esto vivo.",
  "back": "Volver a practicar",
  "empty": "Las formas de contribución se están configurando. Vuelve pronto."
}}

NAV = {"pt": "Apoiar", "en": "Support", "es": "Apoyar"}


# ---------------------------------------------------------------------------
# BR Code Pix estatico (EMV MPM), conforme manual do Banco Central
# ---------------------------------------------------------------------------
def _tlv(tag, value):
    return "%s%02d%s" % (tag, len(value), value)

def _crc16(payload):
    crc = 0xFFFF
    for ch in payload.encode("utf-8"):
        crc ^= ch << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return "%04X" % crc

def _ascii(s, limit):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s.upper()[:limit].strip()

def pix_payload(key, name, city, txid="***"):
    """Monta o BR Code estatico. Valor livre: quem paga escolhe."""
    gui = _tlv("00", "br.gov.bcb.pix") + _tlv("01", key)
    body = (_tlv("00", "01")
            + _tlv("26", gui)
            + _tlv("52", "0000")
            + _tlv("53", "986")
            + _tlv("58", "BR")
            + _tlv("59", _ascii(name, 25) or "RECEBEDOR")
            + _tlv("60", _ascii(city, 15) or "SAO PAULO")
            + _tlv("62", _tlv("05", txid)))
    return body + "6304" + _crc16(body + "6304")

def write_pix_qr(path, payload):
    import segno
    segno.make(payload, error="m").save(path, scale=10, border=2,
                                        dark="#191510", light="#F9F4E8")

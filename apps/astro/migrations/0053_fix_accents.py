"""Corrige las tildes/acentos del contenido sembrado (se escribio sin acentos).

Aplica un corrector ortografico a los campos de texto de Category, Lesson,
Card, Question y Option. Es idempotente: aplicar fix() sobre texto ya corregido
no lo cambia, asi que puede convivir con el reseed de las migraciones anteriores.
No toca los slugs (siguen en ASCII para mantener las URLs).
"""

import re

from django.db import migrations

CORR = {
    "mas": "más", "asi": "así", "segun": "según", "ademas": "además",
    "tambien": "también", "despues": "después", "aqui": "aquí", "ahi": "ahí",
    "alli": "allí", "alla": "allá", "jamas": "jamás", "estan": "están",
    "reves": "revés", "traves": "través", "cual": "cuál", "quien": "quién",
    "esta": "está", "cuan": "cuán", "menu": "menú",
    "leccion": "lección", "manten": "mantén",
    "via": "vía", "lactea": "láctea", "vialactea": "Vía Láctea", "orbitas": "órbitas",
    "ano": "año", "anos": "años", "dia": "día", "dias": "días",
    "energia": "energía", "atmosfera": "atmósfera", "atmosferas": "atmósferas",
    "nucleo": "núcleo", "nucleos": "núcleos", "rapido": "rápido",
    "hidrogeno": "hidrógeno", "numero": "número", "linea": "línea",
    "teoria": "teoría", "fisica": "física", "fisicas": "físicas",
    "astrofisica": "astrofísica", "optica": "óptica", "cosmologia": "cosmología",
    "astronomia": "astronomía", "astronomica": "astronómica",
    "astronomos": "astrónomos", "astronomo": "astrónomo", "astrologia": "astrología",
    "magnetico": "magnético", "magnetica": "magnética",
    "electromagnetico": "electromagnético", "cosmica": "cósmica", "cosmico": "cósmico",
    "galactico": "galáctico", "diametro": "diámetro", "metodo": "método",
    "limite": "límite", "satelite": "satélite", "satelites": "satélites",
    "cinturon": "cinturón", "oxigeno": "oxígeno", "oxido": "óxido",
    "brujula": "brújula", "boveda": "bóveda", "circulo": "círculo",
    "cubica": "cúbica", "cubicas": "cúbicas", "publico": "público",
    "unico": "único", "decadas": "décadas", "kilometro": "kilómetro",
    "kilometros": "kilómetros", "oceano": "océano", "oceanos": "océanos",
    "energetico": "energético", "caracteristica": "característica",
    "caracteristico": "característico", "clasica": "clásica", "clasico": "clásico",
    "basicamente": "básicamente", "practicamente": "prácticamente",
    "faciles": "fáciles", "debiles": "débiles", "debil": "débil",
    "brillantisimo": "brillantísimo", "brillantisima": "brillantísima",
    "muchisimo": "muchísimo", "muchisimas": "muchísimas", "carisimo": "carísimo",
    "termometro": "termómetro", "ultimo": "último", "proxima": "próxima",
    "proximo": "próximo", "proximos": "próximos", "proximamente": "próximamente",
    "retrogrado": "retrógrado", "volcan": "volcán", "patron": "patrón",
    "tunel": "túnel", "vaiven": "vaivén", "balon": "balón", "iman": "imán",
    "comun": "común", "ningun": "ningún", "millon": "millón", "mayoria": "mayoría",
    "luminica": "lumínica", "esferica": "esférica", "solida": "sólida",
    "solidos": "sólidos", "liquida": "líquida", "eliptica": "elíptica",
    "elipticas": "elípticas", "ecliptica": "eclíptica", "sincrona": "síncrona",
    "cumulo": "cúmulo", "cumulos": "cúmulos", "region": "región",
    "arcoiris": "arcoíris", "horoscopos": "horóscopos", "telarana": "telaraña",
    "combustion": "combustión", "transito": "tránsito", "transitos": "tránsitos",
    "imagenes": "imágenes", "cientifico": "científico",
    "tamano": "tamaño", "pequena": "pequeña", "pequeno": "pequeño",
    "pequenos": "pequeños", "montanas": "montañas", "senales": "señales",
    "disenados": "diseñados", "danar": "dañar",
    "jupiter": "júpiter", "andromeda": "andrómeda", "pluton": "plutón",
    "copernico": "copérnico", "nicolas": "nicolás", "orion": "orión",
    "descubrio": "descubrió", "empezo": "empezó", "fotografio": "fotografió",
    "mostro": "mostró", "formulo": "formuló", "lanzo": "lanzó",
    "recibio": "recibió", "describio": "describió", "salio": "salió",
    "abrio": "abrió", "cruzo": "cruzó", "choco": "chocó", "unio": "unió",
    "detecto": "detectó", "capto": "captó", "probo": "probó", "tardo": "tardó",
    "dejo": "dejó", "explico": "explicó", "logro": "logró", "ira": "irá",
    "conoceras": "conocerás", "veras": "verás",
    "podria": "podría", "podrian": "podrían", "saldria": "saldría",
    "flotaria": "flotaría", "pesaria": "pesaría", "permitiria": "permitiría",
    "fallaria": "fallaría", "separaria": "separaría", "desharian": "desharían",
    "titilarian": "titilarían",
    "pasara": "pasará", "chocara": "chocará", "chocaran": "chocarán",
    "fusionaran": "fusionarán", "alejaran": "alejarán", "explotara": "explotará",
    "formara": "formará", "ocurrira": "ocurrirá",
    # adverbios/adjetivos y verbos imperfectos que faltaban
    "demas": "demás", "aun": "aún", "detras": "detrás",
    "frio": "frío", "fria": "fría", "frios": "fríos", "frias": "frías",
    "rio": "río", "vacio": "vacío", "vacia": "vacía", "vacios": "vacíos",
    "vacias": "vacías",
    "envia": "envía", "envian": "envían", "envio": "envío",
    "creia": "creía", "tenia": "tenía", "venian": "venían", "existia": "existía",
    "cabrian": "cabrían", "desvia": "desvía", "enfria": "enfría",
}

_CUANTO = re.compile(r"\bcuant([oa]s?)\b(?!\s+(?:mas|más|menos|menor|mayor|antes|mejor|peor))", re.I)
_WORD = re.compile(r"[A-Za-zñÑ]+")
_CION = re.compile(r"^[a-zñ]+(cion|sion)$")
_ORBITA = re.compile(
    r"\b(una|la|su|sus|cada|esta|sola|misma|nueva|propia|primera|segunda|en)\s+orbita\b", re.I
)
_Q_INIT = re.compile(r"(^|[.!?]\s+|\n)(Que|Como|Cuando|Donde)\b")
_Q_MAP = {"Que": "Qué", "Como": "Cómo", "Cuando": "Cuándo", "Donde": "Dónde"}
_PORQUE = re.compile(r"\b([Pp])or que\b")
# "de que" interrogativo (de qué estan hechas / de qué color) -> con tilde;
# el conjuntivo ("evidencia de que...", "despues de que...") queda igual.
_DEQUE = re.compile(
    r"\b([Dd])e que\b(?=\s+(?:estan|están|esta|está|hecho|hecha|hechos|hechas|"
    r"nace|depende|color|parte)\b)",
    re.I,
)
# ", que" interrogativo (solo estas continuaciones); el relativo queda igual.
_COMAQUE = re.compile(r",(\s+)que\b(?=\s+(?:tapa|parece|otros|otro|otra|otras)\b)")


def _case(orig, repl):
    if orig.isupper():
        return repl.upper()
    if orig[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl


def _fix_word(m):
    w = m.group(0)
    low = w.lower()
    if low in CORR:
        return _case(w, CORR[low])
    if _CION.match(low):
        base = low[:-4] + ("ción" if low.endswith("cion") else "sión")
        return _case(w, base)
    return w


def fix(text):
    if not text:
        return text
    text = _PORQUE.sub(lambda m: m.group(1) + "or qué", text)
    text = _DEQUE.sub(lambda m: m.group(1) + "e qué", text)
    text = _COMAQUE.sub(lambda m: "," + m.group(1) + "qué", text)
    text = _Q_INIT.sub(lambda m: m.group(1) + _Q_MAP[m.group(2)], text)
    text = _CUANTO.sub(lambda m: _case(m.group(0), "cuánt" + m.group(1).lower()), text)
    text = _ORBITA.sub(lambda m: m.group(1) + " órbita", text)
    return _WORD.sub(_fix_word, text)


SPECS = [
    ("Category", ["name", "description"]),
    ("Lesson", ["title", "subtitle"]),
    ("Card", ["front", "back"]),
    ("Question", ["text", "explanation"]),
    ("Option", ["text"]),
    ("Achievement", ["name", "description"]),
    ("ShopItem", ["name", "description"]),
]


def apply_accents(apps, schema_editor):
    for model_name, fields in SPECS:
        Model = apps.get_model("astro", model_name)
        for obj in Model.objects.all():
            changed = []
            for f in fields:
                v = getattr(obj, f, None)
                if v:
                    nv = fix(v)
                    if nv != v:
                        setattr(obj, f, nv)
                        changed.append(f)
            if changed:
                obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [("astro", "0052_seed_gaps")]
    operations = [migrations.RunPython(apply_accents, migrations.RunPython.noop)]

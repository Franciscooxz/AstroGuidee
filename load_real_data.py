"""Carga datos reales extraidos del sitio Wix de Artistic Mold.
   Ejecutar: python manage.py shell < load_real_data.py"""

import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artisticmold.settings')
django.setup()

from apps.core.models import SiteConfig, HomeSection, AboutPage
from apps.faq.models import FAQ
from apps.testimonials.models import Testimonial
from apps.disciplines.models import DisciplineCategory, Discipline

# ── SITE CONFIG ──────────────────────────────────────────────────
cfg = SiteConfig.get()
cfg.phone = '+57 312 4408712'
cfg.whatsapp = '573124408712'
cfg.email = 'artisticmoldfad@gmail.com'
cfg.instagram = '@artisticmoldfad'
cfg.instagram_url = 'https://www.instagram.com/artisticmoldfad'
cfg.facebook = '@ArtisticMoldFAD'
cfg.facebook_url = 'https://www.facebook.com/ArtisticMoldFAD'
cfg.address = 'Localidad Kennedy, Bogota D.C., Colombia'
cfg.convenio = 'Convenio 552 del 2023 - Alcaldia Mayor de Bogota / UNODC'
cfg.tagline = 'Familia Artistico-Deportiva'
cfg.save()
print("SiteConfig actualizado")

# ── HOME SECTION ─────────────────────────────────────────────────
home = HomeSection.get()
home.title = 'Quienes Somos'
home.description = (
    'Artistic Mold es un Dispositivo de Base Comunitaria (DBC) y Centro de Escucha '
    'que nacio en abril de 2020 en Bogota, Colombia. Somos una Familia Artistico-Deportiva '
    'conformada por 10 cofundadores y mas de 30 integrantes activos, que impactamos a cientos '
    'de familias de la Localidad Kennedy. Usamos el arte y el deporte como herramientas '
    'de reconexion, prevencion y recuperacion integral.'
)
home.cta_text = 'Conocenos'
home.cta_url = '/nosotros/'
home.stat_1_number = '10+'
home.stat_1_label = 'Cofundadores'
home.stat_2_number = '30+'
home.stat_2_label = 'Integrantes'
home.stat_3_number = '50+'
home.stat_3_label = 'Disciplinas'
home.save()
print("HomeSection actualizado")

# ── ABOUT PAGE ───────────────────────────────────────────────────
about = AboutPage.get()
about.historia = (
    'Artistic Mold nacio en abril de 2020, en plena pandemia de COVID-19, cuando un grupo '
    'de jovenes bogotanos decidio transformar sus habilidades artisticas y deportivas en una '
    'herramienta de sanacion comunitaria. El nombre "Artistic Mold" (Molde Artistico) fue '
    'formalizado el 6 de diciembre de 2020, y el logo quedo definido el 27 de mayo de 2021. '
    'Hoy somos una familia de mas de 30 integrantes y 10 cofundadores, operando bajo el '
    'Convenio 552 del 2023 con la Alcaldia Mayor de Bogota, la Alcaldia Local de Kennedy '
    'y la Oficina de la ONU contra las Drogas y el Delito (UNODC).'
)
about.mision = (
    'Ayudar, impulsar, instruir y acompanar a quienes se atreven a luchar por su autenticidad, '
    'usando el arte y el deporte como herramientas primarias de reconexion consigo mismo y con '
    'la espiritualidad. Prevenimos y acompanamos procesos de recuperacion de enfermedades no '
    'transmisibles, adicciones y dificultades de salud mental, promoviendo el bienestar integral '
    'y la recuperacion de la dignidad en ninos, jovenes, adultos y adultos mayores.'
)
about.vision = (
    'Ser un referente mayor de los Dispositivos de Base Comunitaria en Bogota. Aspiramos a '
    'establecer multiples sedes, centros de alto rendimiento y espacios dedicados al arte, la '
    'vida, la salud mental y la promocion del bienestar integral, expandiendo nuestro impacto '
    'a mas localidades y comunidades de Colombia.'
)
about.frase_emblema = 'El opuesto de la adiccion no es la sobriedad, es la conexion'
about.save()
print("AboutPage actualizado")

# ── FAQS ─────────────────────────────────────────────────────────
FAQ.objects.all().delete()
faqs = [
    ("Que es Artistic Mold?",
     "Somos un Dispositivo de Base Comunitaria (DBC) y Centro de Escucha que nacio en abril de 2020 en Bogota. Somos una Familia Artistico-Deportiva que usa el arte y el deporte como herramientas de transformacion personal y comunitaria.", 1),
    ("Cuando y como nacio Artistic Mold?",
     "Nacio en abril de 2020, durante la pandemia de COVID-19, cuando nuestros cofundadores redirigieron sus habilidades artisticas y deportivas hacia la sanacion comunitaria. El nombre fue formalizado el 6 de diciembre de 2020.", 2),
    ("Que significa DBC?",
     "DBC significa Dispositivo de Base Comunitaria. Es el marco institucional bajo el cual operamos, en convenio con la Alcaldia Mayor de Bogota, la Alcaldia Local de Kennedy y la Oficina de la ONU contra las Drogas y el Delito (UNODC).", 3),
    ("Que convenios tienen?",
     "Operamos bajo el Convenio 552 del 2023, firmado con la Alcaldia Mayor de Bogota, la Alcaldia Local de Kennedy y la UNODC. Esto nos permite ofrecer muchos programas de manera gratuita a la comunidad.", 4),
    ("Que disciplinas ofrecen?",
     "Mas de 50 disciplinas: futbol, breaking, calistenia, pilates, spinning, graffiti, pintura, fotografia, musica, canto, teatro, oratoria, meditacion, neuroentrenamiento, danza, patinaje y mucho mas. El arte no tiene limites.", 5),
    ("Para que edades son los programas?",
     "Tenemos programas para todas las edades: ninos, adolescentes, jovenes, adultos y adultos mayores. El arte y el deporte no tienen fronteras de edad.", 6),
    ("Como puedo participar?",
     "Puedes contactarnos por WhatsApp al +57 312 4408712 o escribirnos a artisticmoldfad@gmail.com. Tambien siguenos en Instagram @artisticmoldfad para estar al tanto de todas las actividades.", 7),
    ("Cual es la filosofia de Artistic Mold?",
     "El opuesto de la adiccion no es la sobriedad, es la conexion. Creemos que el arte, el deporte y la espiritualidad son los pilares de la transformacion individual y comunitaria. Somos moldeados por Dios, el mayor artista.", 8),
]
for q, a, o in faqs:
    FAQ.objects.create(question=q, answer=a, order=o, is_active=True)
print(f"FAQs: {FAQ.objects.count()}")

# ── TESTIMONIALS ─────────────────────────────────────────────────
Testimonial.objects.all().delete()
testimonials = [
    ("Angie Ximena Rubio", "Integrante AM",
     "Tengo que aceptar que algo me esta afectando, que algo no esta bien en mi vida y estoy en ese proceso... Artistic Mold me ha dado ese espacio para reconocerme y avanzar.",
     True, 1),
    ("Julian Salazar", "Integrante AM",
     "La disciplina forma, la disciplina no es regimen, es distinto; si yo me propongo algo y lo trabajo, y me voy por eso, lo consigo. Aqui aprendi que el arte y el deporte son una misma cosa.",
     True, 2),
    ("Willie Alejandro Quinones", "Integrante AM",
     "Desde que volvi a ser Nano, gracias a Dios, a Mamita Maria y a mi familia... Todos los dias son y los vivo como si fuera el ultimo, a veces algunos son mas lokos que otros, pero todos son CHIMBAS.",
     True, 3),
    ("Barbara Quinones", "Integrante AM",
     "Poder decirle TE AMO, sin sentir de pronto miedo o pena... Aqui aprendi que el amor propio es el primer paso de todo.",
     True, 4),
    ("Valentina Velasquez", "Integrante AM",
     "Es como sentir el amor genuino, un amor que no tiene limites, un amor que es tan puro y sencillo... Eso es lo que encuentro cada vez que llego aqui.",
     True, 5),
    ("Tania Jurado", "Artista AM",
     "Me gusta pintar y reflejar criticas, emociones y pensamientos. El arte es mi forma de hablar cuando las palabras no alcanzan.",
     False, 6),
    ("Astrid Velasquez", "Integrante AM",
     "Los abusos, miedos, defectos de caracter no pudieron cortar mis alas, pues soy ARTE.",
     True, 7),
    ("Sonia Jurado", "Guerrera — Fibromialgia",
     "Decidi apostarle... apostarle a que mis musculos, a que mis arterias, a que mi cuerpo, si podia moverse nuevamente. Artistic Mold me devolvio la fe en mi propio cuerpo.",
     False, 8),
]
for name, role, quote, featured, order in testimonials:
    Testimonial.objects.create(
        name=name, role=role, quote=quote,
        is_featured=featured, is_active=True, order=order
    )
print(f"Testimonials: {Testimonial.objects.count()}")

# ── DISCIPLINAS — reales del Wix ─────────────────────────────────
DisciplineCategory.objects.all().delete()
Discipline.objects.all().delete()

cats_raw = [
    ("Danza y Movimiento",       "danza-movimiento",  "fa-music",         "#7c3aed", 1),
    ("Artes Visuales",           "artes-visuales",    "fa-paint-brush",   "#0891b2", 2),
    ("Artes Escenicas y Oratoria","artes-escenicas",  "fa-theater-masks", "#d97706", 3),
    ("Musica",                   "musica",            "fa-guitar",        "#6d28d9", 4),
    ("Actividad Fisica y Deporte","actividad-fisica", "fa-dumbbell",      "#e11d48", 5),
    ("Bienestar y Desarrollo",   "bienestar",         "fa-brain",         "#059669", 6),
    ("Creacion y Oficios",       "creacion-oficios",  "fa-hands",         "#dc2626", 7),
]
cats = {}
for name, slug, icon, color, order in cats_raw:
    cats[slug] = DisciplineCategory.objects.create(name=name, slug=slug, icon=icon, color=color, order=order)
print(f"Categorias: {DisciplineCategory.objects.count()}")

discs = [
    # Danza y Movimiento
    ("Breaking",                  "breaking",               "danza-movimiento",  "Danza urbana que incluye footwork, freeze, power moves y top rock. Cultura Hip-Hop autentica.", True),
    ("Danza",                     "danza",                  "danza-movimiento",  "Expresion corporal a traves del movimiento. Multiples estilos, una sola emocion.", True),
    ("Baile",                     "baile",                  "danza-movimiento",  "Baile social y recreativo para todas las edades. Nos mueve la alegria.", False),
    ("Ritmo Latino",              "ritmo-latino",           "danza-movimiento",  "Salsa, bachata, merengue y mas. La identidad latinoamericana en movimiento.", False),
    ("Dance Strong Jungle Fusion","dance-strong",           "danza-movimiento",  "Fusion de estilos de danza con entrenamiento fisico intenso. Energia pura.", False),
    # Artes Visuales
    ("Graffiti",                  "graffiti",               "artes-visuales",    "Arte urbano en espacios publicos. Estilos, tipografia, muralismo y aerosol.", True),
    ("Pintura",                   "pintura",                "artes-visuales",    "Tecnicas de pintura: acrilico, acuarela, oleo. Expresion plastica libre.", True),
    ("Dibujo",                    "dibujo",                 "artes-visuales",    "Fundamentos del dibujo artistico, tecnica y composicion visual.", False),
    ("Fotografia",                "fotografia",             "artes-visuales",    "Arte de capturar momentos. Tecnica, composicion y edicion digital.", False),
    ("Escultura",                 "escultura",              "artes-visuales",    "Creacion de obras tridimensionales. Modelado, talla y construccion.", False),
    ("Diseno y Edicion Audiovisual","diseno-audiovisual",   "artes-visuales",    "Diseno grafico, edicion de video y produccion audiovisual comunitaria.", False),
    # Artes Escenicas y Oratoria
    ("Interpretacion Escenica",   "interpretacion-escenica","artes-escenicas",   "Actuacion, improvisacion y logica escenica. El cuerpo como instrumento expresivo.", True),
    ("Oratoria",                  "oratoria",               "artes-escenicas",   "El arte de hablar en publico con confianza, claridad y poder de conviccion.", False),
    ("Poesia",                    "poesia",                 "artes-escenicas",   "La palabra como arte. Poesia urbana, slam poetry y escritura creativa.", False),
    ("Freestyle",                 "freestyle",              "artes-escenicas",   "Improvisacion verbal y musical. Creatividad sin limites en tiempo real.", True),
    # Musica
    ("Musica",                    "musica",                 "musica",            "Teoria musical, practica instrumental y apreciacion. El lenguaje universal.", True),
    ("Canto",                     "canto",                  "musica",            "Tecnica vocal, respiracion y desarrollo del oido musical. Tu voz es tu instrumento.", False),
    # Actividad Fisica y Deporte
    ("Futbol",                    "futbol",                 "actividad-fisica",  "El deporte rey. Futbol recreativo y formativo para todas las edades y niveles.", True),
    ("Calistenia",                "calistenia",             "actividad-fisica",  "Entrenamiento con peso corporal: dominadas, fondos, planchas y movimientos de habilidad.", True),
    ("Halterofilia",              "halterofilia",           "actividad-fisica",  "Levantamiento olimpico de pesas. Fuerza, tecnica y disciplina mental.", False),
    ("Spinning",                  "spinning",               "actividad-fisica",  "Ciclismo indoor de alta intensidad. Resistencia cardiovascular y quema calorica.", False),
    ("Pilates",                   "pilates",                "actividad-fisica",  "Fortalecimiento del nucleo, flexibilidad y conciencia corporal.", False),
    ("Running y Jogging",         "running-jogging",        "actividad-fisica",  "Carrera recreativa y formativa. Resistencia cardiovascular al aire libre.", False),
    ("Aerobics",                  "aerobics",               "actividad-fisica",  "Ejercicio aerobico con musica y movimiento. Salud cardiovascular y mucha diversion.", False),
    ("Patinaje",                  "patinaje",               "actividad-fisica",  "Patines de ruedas o en linea. Velocidad, equilibrio y libertad de movimiento.", False),
    ("Tabata",                    "tabata",                 "actividad-fisica",  "Entrenamiento de intervalos de alta intensidad (HIIT). 20 segundos de fuego, 10 de descanso.", False),
    ("Defensa Personal",          "defensa-personal",       "actividad-fisica",  "Tecnicas basicas de autodefensa adaptadas para toda la familia.", False),
    # Bienestar y Desarrollo
    ("Meditacion",                "meditacion",             "bienestar",         "Practica de atencion plena y silencio interior. Salud mental y espiritual.", True),
    ("Neuroentrenamiento",        "neuroentrenamiento",     "bienestar",         "Ejercicios que potencian las funciones cognitivas a traves del movimiento y el arte.", True),
    ("Escucha Activa",            "escucha-activa",         "bienestar",         "Habilidad fundamental de comunicacion y empatia. La base de toda conexion genuina.", False),
    ("Dialectica",                "dialectica",             "bienestar",         "El arte del debate y el pensamiento critico. Construimos argumentos con respeto.", False),
    ("Ludica y Didactica",        "ludica-didactica",       "bienestar",         "Metodologias de aprendizaje a traves del juego. El placer de aprender.", False),
    ("Fragmentacion",             "fragmentacion",          "bienestar",         "Tecnica de analisis y deconstruccion de movimientos y procesos creativos.", False),
    # Creacion y Oficios
    ("Manualidades y Decoraciones","manualidades",          "creacion-oficios",  "Creaciones en foami, carton, papel y mas. Arte aplicado a la vida cotidiana.", False),
    ("Nail Art y Spa de Unas",    "nail-art",               "creacion-oficios",  "Manicura, pedicura y arte en unas. Cuidado personal como expresion artistica.", False),
    ("Lectoescritura",            "lectoescritura",         "creacion-oficios",  "Fortalecimiento de la lectura y la escritura como herramientas de vida.", False),
    ("Juzgamiento Deportivo",     "juzgamiento-deportivo",  "creacion-oficios",  "Formacion en arbitraje y evaluacion deportiva. Liderazgo desde el conocimiento.", False),
]

for i, (name, slug, cat_slug, desc, featured) in enumerate(discs):
    Discipline.objects.create(
        name=name, slug=slug, category=cats[cat_slug],
        description=desc, is_featured=featured, is_active=True, order=i+1
    )
print(f"Disciplinas: {Discipline.objects.count()}")
print("\nDatos reales de Artistic Mold cargados correctamente!")

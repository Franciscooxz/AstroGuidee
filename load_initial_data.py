"""Run with: python manage.py shell < load_initial_data.py"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artisticmold.settings')
django.setup()

from apps.faq.models import FAQ
from apps.disciplines.models import DisciplineCategory, Discipline
from apps.resources.models import ResourceCategory
from apps.services.models import Service

# ── FAQs ────────────────────────────────────────────────
FAQ.objects.all().delete()
faqs = [
    ("Que es Artistic Mold?", "Somos una organizacion comunitaria DBC en Bogota que transforma vidas a traves del arte, el deporte y la cultura urbana.", 1),
    ("Como puedo participar?", "Puedes contactarnos por WhatsApp al +57 311 2856950. Ofrecemos inscripciones abiertas durante todo el ano.", 2),
    ("Que es DBC?", "DBC significa Deporte, Bienestar y Cultura. Es el marco de trabajo bajo el cual operamos, promoviendo el desarrollo integral.", 3),
    ("Hay costos para participar?", "Contamos con programas gratuitos gracias a convenios con la Alcaldia de Bogota. Algunos talleres tienen costos accesibles.", 4),
    ("Para que edades son los programas?", "Tenemos programas para todas las edades: ninos desde 5 anos, jovenes, adultos y adultos mayores.", 5),
    ("Donde estan ubicados?", "Operamos en Bogota D.C. con actividades en diferentes localidades. Contactanos para conocer el punto mas cercano.", 6),
    ("Que disciplinas ofrecen?", "Mas de 50 disciplinas: artes marciales, danza, capoeira, break dance, parkour, artes plasticas, teatro, musica y mas.", 7),
    ("Tienen convenio con entidades publicas?", "Si, contamos con convenio con la Alcaldia Mayor de Bogota, lo que nos permite ofrecer muchos programas de manera gratuita.", 8),
]
for q, a, o in faqs:
    FAQ.objects.create(question=q, answer=a, order=o, is_active=True)
print(f"FAQs: {FAQ.objects.count()}")

# ── Discipline Categories ────────────────────────────────
DisciplineCategory.objects.all().delete()
cats_raw = [
    ("Artes Marciales", "artes-marciales", "fa-fist-raised", "#dc2626", 1),
    ("Danza", "danza", "fa-music", "#7c3aed", 2),
    ("Artes Visuales", "artes-visuales", "fa-paint-brush", "#0891b2", 3),
    ("Artes Escenicas", "artes-escenicas", "fa-theater-masks", "#d97706", 4),
    ("Deportes Urbanos", "deportes-urbanos", "fa-running", "#059669", 5),
    ("Actividad Fisica", "actividad-fisica", "fa-dumbbell", "#e11d48", 6),
    ("Musica", "musica", "fa-guitar", "#6d28d9", 7),
    ("Otros", "otros", "fa-star", "#6b7280", 8),
]
cats = {}
for name, slug, icon, color, order in cats_raw:
    cats[slug] = DisciplineCategory.objects.create(name=name, slug=slug, icon=icon, color=color, order=order)
print(f"DisciplineCategories: {DisciplineCategory.objects.count()}")

# ── Disciplines ──────────────────────────────────────────
Discipline.objects.all().delete()
discs = [
    ("Karate Do", "karate-do", "artes-marciales", "Arte marcial japones que combina tecnicas de golpe, bloqueo y patadas.", True),
    ("Taekwondo", "taekwondo", "artes-marciales", "Arte marcial coreano enfocado en patadas de alta velocidad.", True),
    ("Judo", "judo", "artes-marciales", "Arte marcial japones basado en proyecciones y derribos.", False),
    ("Capoeira", "capoeira", "artes-marciales", "Arte marcial brasilena que combina lucha, danza y acrobacias con musica.", True),
    ("Muay Thai", "muay-thai", "artes-marciales", "Arte marcial tailandes conocido como el arte de los ocho miembros.", False),
    ("Kung Fu", "kung-fu", "artes-marciales", "Arte marcial chino con multiples estilos que combina tecnicas de ataque y filosofia.", False),
    ("Break Dance", "break-dance", "danza", "Danza urbana que incluye footwork, freeze, power moves y top rock. Cultura Hip-Hop.", True),
    ("Salsa", "salsa", "danza", "Baile latino lleno de ritmo y pasion con tecnicas cubanas y caleanas.", True),
    ("Reggaeton", "reggaeton", "danza", "Genero musical y estilo de baile urbano con raices caribenas.", False),
    ("Bachata", "bachata", "danza", "Baile romantico de origen dominicano con movimientos sensuales.", False),
    ("Hip Hop Dance", "hip-hop-dance", "danza", "Estilo de baile urbano que engloba breaking, locking, popping y krump.", True),
    ("Folklore", "folklore", "danza", "Danzas tradicionales colombianas y latinoamericanas. Patrimonio cultural.", False),
    ("Zumba", "zumba", "danza", "Programa de fitness que combina musica latina y movimientos de danza.", False),
    ("Pintura", "pintura", "artes-visuales", "Tecnicas de pintura al oleo, acrilico y acuarela. Expresion plastica.", True),
    ("Graffiti", "graffiti", "artes-visuales", "Arte urbano en espacios publicos. Estilos, tipografia, muralismo y aerosol.", True),
    ("Dibujo", "dibujo", "artes-visuales", "Fundamentos del dibujo artistico, tecnica y composicion.", False),
    ("Fotografia", "fotografia", "artes-visuales", "Arte de capturar momentos a traves del lente. Tecnica y edicion digital.", False),
    ("Escultura", "escultura", "artes-visuales", "Creacion de obras tridimensionales. Modelado, talla y construccion.", False),
    ("Teatro", "teatro", "artes-escenicas", "Expresion dramatica que combina actuacion, improvisacion y puesta en escena.", True),
    ("Teatro Fisico", "teatro-fisico", "artes-escenicas", "Integra cuerpo, teatro, danza y artes marciales.", False),
    ("Circo", "circo", "artes-escenicas", "Malabares, acrobacias, contorsion y equilibrio. Arte de la destreza.", True),
    ("Parkour", "parkour", "deportes-urbanos", "Desplazarse por el entorno urbano de manera eficiente. Saltos y escaladas.", True),
    ("Skateboard", "skateboard", "deportes-urbanos", "Deporte sobre patineta con trucos, freestyle y rampa.", False),
    ("BMX", "bmx", "deportes-urbanos", "Ciclismo de acrobacias en bicicleta en rampas y calles.", False),
    ("Patinaje", "patinaje", "deportes-urbanos", "Deporte en patines de ruedas o en linea. Velocidad y freestyle.", False),
    ("Calistenia", "calistenia", "actividad-fisica", "Entrenamiento con peso corporal. Dominadas, fondos y movimientos de habilidad.", True),
    ("Gimnasia Acrobatica", "gimnasia-acrobatica", "actividad-fisica", "Acrobacias, equilibrios y coreografias. Fuerza, flexibilidad y coordinacion.", False),
    ("Crossfit", "crossfit", "actividad-fisica", "Entrenamiento funcional de alta intensidad.", False),
    ("Yoga", "yoga", "actividad-fisica", "Practica que une cuerpo, mente y espiritu a traves de posturas y respiracion.", False),
    ("Natacion", "natacion", "actividad-fisica", "Deporte acuatico completo que trabaja todos los grupos musculares.", False),
    ("Guitarra", "guitarra", "musica", "Aprendizaje de guitarra acustica y electrica. Tecnica y teoria musical.", False),
    ("Percusion", "percusion", "musica", "Bateria, congas, bongos y percusion menor. Ritmo y coordinacion.", False),
    ("Canto", "canto", "musica", "Tecnica vocal, respiracion y desarrollo del oido musical.", False),
    ("Produccion Musical", "produccion-musical", "musica", "Creacion y produccion de musica urbana: Hip-Hop, Rap y electronica.", True),
]

for i, (name, slug, cat_slug, desc, featured) in enumerate(discs):
    Discipline.objects.create(
        name=name, slug=slug, category=cats[cat_slug],
        description=desc, is_featured=featured, is_active=True, order=i+1
    )
print(f"Disciplines: {Discipline.objects.count()}")

# ── Resource Categories ──────────────────────────────────
ResourceCategory.objects.all().delete()
ResourceCategory.objects.create(slug='dbc', title='DBC (Deporte, Bienestar y Cultura)', intro='Todo lo relacionado con la metodologia DBC de Artistic Mold.', icon='fa-star')
ResourceCategory.objects.create(slug='manual', title='Manual TFA', intro='Manual de la metodologia Tecnica de Formacion Artistica.', icon='fa-book')
ResourceCategory.objects.create(slug='bienestar', title='Bienestar y Salud', intro='Recursos para el cuidado integral de nuestra comunidad.', icon='fa-heart')
print(f"ResourceCategories: {ResourceCategory.objects.count()}")

# ── Services ─────────────────────────────────────────────
Service.objects.all().delete()
services = [
    ("Talleres Artisticos", "Talleres formativos en artes marciales, danza, musica, artes plasticas y artes escenicas para todas las edades.", "fa-palette", 1),
    ("Eventos y Muestras", "Organizacion de eventos culturales, muestras artisticas y presentaciones de nuestros participantes.", "fa-calendar-alt", 2),
    ("Formacion Docente", "Capacitacion para lideres y formadores en metodologias DBC y TFA.", "fa-chalkboard-teacher", 3),
    ("Actividad Fisica", "Programas de acondicionamiento fisico, deporte urbano y bienestar para la comunidad.", "fa-dumbbell", 4),
    ("Consultoria Comunitaria", "Asesoria a organizaciones comunitarias en implementacion de programas culturales y deportivos.", "fa-hands-helping", 5),
    ("Campamentos Urbanos", "Campamentos urbanos de verano con actividades artisticas, deportivas y culturales.", "fa-campground", 6),
]
for title, desc, icon, order in services:
    Service.objects.create(title=title, description=desc, icon=icon, order=order, is_active=True)
print(f"Services: {Service.objects.count()}")

print("\nDatos iniciales cargados correctamente!")

# -*- coding: utf-8 -*-
from django.db import migrations

# Preguntas nuevas para que cada unidad llegue a su cupo segun dificultad:
# nivel 2 -> 6 preg, nivel 3 -> 7, nivel 4 -> 8, nivel 5 -> 10.
# Formato: slug_leccion: [ (texto, tipo, [(opcion, correcta), ...]), ... ]
ADD = {
    # ---- Nivel 2 (llegar a 6): +1 ----
    'que-es-una-estrella': [
        ("Que mantiene a una estrella estable sin colapsar?", 'single',
         [("El equilibrio entre su gravedad y la presion de la fusion", True),
          ("El viento solar", False), ("Su campo magnetico", False), ("Su rotacion", False)]),
    ],
    'tipos-de-estrellas': [
        ("De que color se ve una estrella mas caliente?", 'single',
         [("Azul", True), ("Roja", False), ("Amarilla", False), ("Naranja", False)]),
    ],
    'vida-y-muerte-de-una-estrella': [
        ("Como se llama la fase en que una estrella como el Sol se hincha al final de su vida?", 'single',
         [("Gigante roja", True), ("Enana blanca", False), ("Supernova", False), ("Nebulosa", False)]),
    ],
    'la-via-lactea': [
        ("Aproximadamente cuantas estrellas tiene la Via Lactea?", 'single',
         [("Cientos de miles de millones", True), ("Unos pocos miles", False),
          ("Alrededor de un millon", False), ("Exactamente mil", False)]),
    ],
    'tipos-de-galaxias': [
        ("Que tipo de galaxia no tiene una forma definida?", 'single',
         [("Irregular", True), ("Espiral", False), ("Eliptica", False), ("Lenticular", False)]),
    ],

    # ---- Nivel 3 (llegar a 7): +2 ----
    'que-es-un-exoplaneta': [
        ("Un exoplaneta es un planeta que orbita...", 'single',
         [("Una estrella distinta al Sol", True), ("El Sol", False),
          ("La Tierra", False), ("Un agujero negro", False)]),
        ("Se han confirmado miles de exoplanetas.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'como-se-descubren': [
        ("El metodo del transito detecta un exoplaneta cuando...", 'single',
         [("El planeta pasa por delante de su estrella y la atenua un poco", True),
          ("El planeta emite luz propia", False), ("El planeta choca con su estrella", False),
          ("La estrella desaparece", False)]),
        ("Que revela el metodo de velocidad radial?", 'single',
         [("El leve bamboleo de la estrella por la gravedad del planeta", True),
          ("El color del planeta", False), ("La temperatura de la estrella", False),
          ("El tamano de la galaxia", False)]),
    ],
    'mundos-famosos': [
        ("Por que es interesante un planeta en la zona habitable?", 'single',
         [("Podria tener agua liquida en su superficie", True),
          ("Siempre tiene vida", False), ("Esta hecho de oro", False),
          ("No tiene estrella", False)]),
        ("Los planetas de TRAPPIST-1 orbitan una estrella...", 'single',
         [("Enana roja, pequena y fria", True), ("Gigante azul", False),
          ("Igual que el Sol", False), ("De neutrones", False)]),
    ],
    'andromeda-y-el-grupo-local': [
        ("Que le pasara a Andromeda y la Via Lactea en miles de millones de anos?", 'single',
         [("Chocaran y se fusionaran", True), ("Se alejaran para siempre", False),
          ("Andromeda explotara", False), ("No pasara nada", False)]),
        ("El Grupo Local es...", 'single',
         [("El cumulo de galaxias al que pertenece la Via Lactea", True),
          ("Un cumulo de estrellas", False), ("Un tipo de planeta", False),
          ("Una nebulosa cercana", False)]),
    ],
    'galaxias-asombrosas': [
        ("Que es un cuasar?", 'single',
         [("El nucleo brillantisimo de una galaxia con un agujero negro activo", True),
          ("Una estrella cercana", False), ("Un planeta gigante", False), ("Un cometa", False)]),
        ("Existen galaxias mucho mas grandes que la Via Lactea.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'que-es-un-agujero-negro': [
        ("Un agujero negro es una region donde la gravedad es tan fuerte que...", 'single',
         [("Ni la luz puede escapar", True), ("Todo se congela", False),
          ("El tiempo desaparece", False), ("No hay gravedad", False)]),
        ("Los agujeros negros estelares se forman cuando...", 'single',
         [("Colapsa el nucleo de una estrella muy masiva", True),
          ("Chocan dos planetas", False), ("Se apaga una estrella pequena", False),
          ("Explota un cometa", False)]),
    ],
    'el-horizonte-de-sucesos': [
        ("Que es el horizonte de sucesos?", 'single',
         [("El limite del que ya nada puede escapar", True),
          ("La superficie solida del agujero", False), ("Un anillo de planetas", False),
          ("El centro exacto", False)]),
        ("Como se llama el punto central de densidad extrema de un agujero negro?", 'single',
         [("Singularidad", True), ("Nucleo", False), ("Corona", False), ("Fotosfera", False)]),
    ],

    # ---- Nivel 4 (llegar a 8): +3 ----
    'tipos-de-agujeros-negros': [
        ("Que clase de agujero negro hay en el centro de casi todas las galaxias grandes?", 'single',
         [("Supermasivo", True), ("Estelar", False), ("Primordial", False), ("Enano", False)]),
        ("Como se llama el agujero negro del centro de la Via Lactea?", 'single',
         [("Sagitario A*", True), ("M87*", False), ("Cygnus X-1", False), ("Proxima b", False)]),
        ("Los agujeros negros supermasivos tienen millones o miles de millones de veces la masa del Sol.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'famosos-y-ondas-gravitacionales': [
        ("Que son las ondas gravitacionales?", 'single',
         [("Ondulaciones en el espacio-tiempo", True), ("Ondas de sonido del espacio", False),
          ("Luz muy intensa", False), ("Viento estelar", False)]),
        ("Que detector capto por primera vez ondas gravitacionales en 2015?", 'single',
         [("LIGO", True), ("Hubble", False), ("Kepler", False), ("Voyager", False)]),
        ("Las primeras ondas gravitacionales detectadas venian de...", 'single',
         [("La fusion de dos agujeros negros", True), ("Una supernova cercana", False),
          ("El Sol", False), ("Un cometa", False)]),
    ],
    'el-big-bang': [
        ("Que describe la teoria del Big Bang?", 'single',
         [("El origen y la expansion del universo hace unos 13.800 millones de anos", True),
          ("La explosion de una estrella", False), ("El nacimiento del Sol", False),
          ("El choque de dos galaxias", False)]),
        ("Que radiacion es el eco que dejo el Big Bang?", 'single',
         [("El fondo cosmico de microondas", True), ("Los rayos X del Sol", False),
          ("La luz de las estrellas", False), ("Las ondas de radio de la Tierra", False)]),
        ("El Big Bang fue una explosion dentro de un espacio vacio que ya existia.", 'truefalse',
         [("Falso", True), ("Verdadero", False)]),
    ],
    'la-expansion-del-universo': [
        ("Que observacion mostro que el universo se expande?", 'single',
         [("Las galaxias lejanas se alejan de nosotros (corrimiento al rojo)", True),
          ("Las estrellas cambian de color al azar", False), ("El Sol se enfria", False),
          ("La Luna se acerca", False)]),
        ("Quien descubrio que las galaxias mas lejanas se alejan mas rapido?", 'single',
         [("Edwin Hubble", True), ("Isaac Newton", False), ("Galileo", False), ("Kepler", False)]),
        ("Que parece acelerar la expansion del universo?", 'single',
         [("La energia oscura", True), ("La gravedad", False), ("El viento solar", False),
          ("Los agujeros negros", False)]),
    ],
    'materia-y-energia-oscura': [
        ("Como se detecta sobre todo la materia oscura?", 'single',
         [("Por su efecto gravitatorio sobre galaxias y estrellas", True),
          ("Por la luz que emite", False), ("Por su color oscuro", False),
          ("Por el sonido que hace", False)]),
        ("Aproximadamente que fraccion del universo es materia normal (la que vemos)?", 'single',
         [("Alrededor del 5%", True), ("El 50%", False), ("El 95%", False), ("El 100%", False)]),
        ("La energia oscura parece empujar al universo a expandirse cada vez mas rapido.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'telescopios-que-cambiaron-todo': [
        ("Que ventaja tiene el telescopio Hubble por estar en el espacio?", 'single',
         [("Evita la distorsion de la atmosfera terrestre", True),
          ("Esta mas cerca de las estrellas", False), ("No necesita energia", False),
          ("Puede tocar los planetas", False)]),
        ("En que tipo de luz observa sobre todo el telescopio James Webb?", 'single',
         [("Infrarrojo", True), ("Rayos X", False), ("Ultravioleta", False), ("Ondas de radio", False)]),
        ("Observar en infrarrojo le permite al James Webb...", 'single',
         [("Ver a traves del polvo y captar objetos muy lejanos y antiguos", True),
          ("Ver solo la Luna", False), ("Medir el sonido del espacio", False),
          ("Ver solo de dia", False)]),
    ],
    'misiones-que-exploran': [
        ("Que sonda es el objeto humano mas lejano, ya en el espacio interestelar?", 'single',
         [("Voyager 1", True), ("Apollo 11", False), ("Hubble", False), ("Curiosity", False)]),
        ("Que explora el rover Perseverance?", 'single',
         [("La superficie de Marte", True), ("La Luna", False), ("Venus", False), ("Jupiter", False)]),
        ("Las sondas Voyager llevan un disco con sonidos e imagenes de la Tierra.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'grandes-descubrimientos': [
        ("Que logro el proyecto Event Horizon Telescope en 2019?", 'single',
         [("La primera imagen real de un agujero negro", True), ("Hallar un planeta nuevo", False),
          ("Encontrar vida en Marte", False), ("Predecir el fin del universo", False)]),
        ("El primer exoplaneta alrededor de una estrella como el Sol (1995) lo hallaron...", 'single',
         [("Michel Mayor y Didier Queloz", True), ("Newton y Halley", False),
          ("Galileo y Kepler", False), ("Hubble y Einstein", False)]),
        ("Hoy sabemos que casi todas las estrellas tienen al menos un planeta.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],

    # ---- Nivel 5 (llegar a 10): +5 ----
    'la-gravedad': [
        ("Quien formulo la ley de la gravitacion universal?", 'single',
         [("Isaac Newton", True), ("Albert Einstein", False), ("Galileo Galilei", False),
          ("Nicolas Copernico", False)]),
        ("Segun Newton, la gravedad entre dos cuerpos es mayor cuando...", 'single',
         [("Tienen mas masa y estan mas cerca", True), ("Estan mas lejos", False),
          ("Son mas frios", False), ("Giran mas rapido", False)]),
        ("Que mantiene a los planetas orbitando el Sol?", 'single',
         [("La gravedad del Sol", True), ("El viento solar", False),
          ("El magnetismo de la Tierra", False), ("La luz", False)]),
        ("Como describe Einstein la gravedad en la relatividad general?", 'single',
         [("Como la curvatura del espacio-tiempo por la masa", True),
          ("Como una fuerza magnetica", False), ("Como una ilusion optica", False),
          ("Como una forma de calor", False)]),
        ("Sin aire, dos objetos de distinta masa caen con la misma aceleracion.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'la-luz-y-el-espectro': [
        ("La luz visible es una pequena parte de...", 'single',
         [("El espectro electromagnetico", True), ("El sonido", False),
          ("La gravedad", False), ("El viento solar", False)]),
        ("Que tipo de radiacion tiene mas energia?", 'single',
         [("Los rayos gamma", True), ("Las ondas de radio", False),
          ("La luz roja", False), ("El infrarrojo", False)]),
        ("Al analizar el espectro de la luz de una estrella podemos saber...", 'single',
         [("De que esta hecha y su temperatura", True), ("Solo su nombre", False),
          ("Su edad exacta en dias", False), ("El sonido que emite", False)]),
        ("Que instrumento separa la luz en sus colores o longitudes de onda?", 'single',
         [("Un espectroscopio", True), ("Un termometro", False),
          ("Una brujula", False), ("Un reloj", False)]),
        ("La luz roja tiene mayor longitud de onda que la luz azul.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
    'nociones-de-relatividad': [
        ("Segun la relatividad, nada puede viajar mas rapido que...", 'single',
         [("La luz", True), ("El sonido", False), ("Un cohete", False), ("La Tierra", False)]),
        ("Que expresa la ecuacion E=mc2?", 'single',
         [("Que la energia y la masa son equivalentes", True), ("Que la Tierra es plana", False),
          ("Que la luz no existe", False), ("Que el tiempo es fijo", False)]),
        ("Cerca de un objeto muy masivo, el tiempo...", 'single',
         [("Pasa mas lento", True), ("Pasa mas rapido", False),
          ("Se detiene para siempre", False), ("No cambia jamas", False)]),
        ("La relatividad general predice que la luz se curva al pasar cerca de...", 'single',
         [("Un objeto muy masivo", True), ("Un espejo", False),
          ("El aire", False), ("Un iman", False)]),
        ("La velocidad de la luz es la misma para todos los observadores.", 'truefalse',
         [("Verdadero", True), ("Falso", False)]),
    ],
}


def forwards(apps, schema_editor):
    Lesson = apps.get_model('astro', 'Lesson')
    Question = apps.get_model('astro', 'Question')
    Option = apps.get_model('astro', 'Option')

    for slug, questions in ADD.items():
        try:
            lesson = Lesson.objects.get(slug=slug)
        except Lesson.DoesNotExist:
            continue
        base = lesson.questions.count()
        for qi, (text, qtype, options) in enumerate(questions, start=base + 1):
            if Question.objects.filter(lesson=lesson, text=text).exists():
                continue
            q = Question.objects.create(lesson=lesson, text=text, qtype=qtype, order=qi)
            for oi, (otext, correct) in enumerate(options, start=1):
                Option.objects.create(question=q, text=otext, is_correct=correct, order=oi)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    texts = [q[0] for qs in ADD.values() for q in qs]
    Question.objects.filter(text__in=texts).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0032_order_and_difficulty'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

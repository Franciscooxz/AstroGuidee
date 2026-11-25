"""Ruta pedagógica de AstroGuide: 6 etapas y 24 unidades.

Las unidades 1 a 8 se publican con lecciones redactadas a partir de páginas
consultadas el 24 de noviembre de 2026. Las unidades 9 a 24 quedan en borrador:
no tienen lecciones activas ni se presentan como verificadas.

Esta ruta es una propuesta de la app. No es un currículo de la NASA ni de la UAI.
Ninguna lección se marca como revisada por una persona experta.
"""

from datetime import date

CHECKED = date(2026, 11, 24)

# Páginas abiertas ese día. La nota conserva el límite de lo que dicen.
S = {
    "sistema": (
        "NASA Science: Solar System",
        "https://science.nasa.gov/solar-system/",
        "Consultada el 2026-11-24. Las cantidades de asteroides y cometas de esa página cambian: no se usan como pregunta.",
    ),
    "datos": (
        "NASA Science: Solar System Facts",
        "https://science.nasa.gov/solar-system/solar-system-facts/",
        "Consultada el 2026-11-24. La nube de Oort se presenta ahí como modelo, no como imagen.",
    ),
    "oort": (
        "NASA Science: Oort Cloud",
        "https://science.nasa.gov/solar-system/oort-cloud/",
        "Consultada el 2026-11-24. NASA dice que no tiene imágenes directas de la nube.",
    ),
    "planetas": (
        "NASA Science: About the Planets",
        "https://science.nasa.gov/solar-system/planets/",
        "Consultada el 2026-11-24. El número de exoplanetas confirmados de esa página no se pregunta: cambia.",
    ),
    "tierra": (
        "NASA Science: Facts About Earth",
        "https://science.nasa.gov/earth/facts/",
        "Consultada el 2026-11-24. La inclinación que usa esta lección es 23,4°, la de esta ficha.",
    ),
    "fases": (
        "NASA Science: Moon Phases",
        "https://science.nasa.gov/moon/moon-phases/",
        "Consultada el 2026-11-24. El gráfico de fases de esa página está marcado como no a escala.",
    ),
    "eclipses": (
        "NASA Science: Eclipses",
        "https://science.nasa.gov/eclipses/",
        "Consultada el 2026-11-24. Incluye la advertencia de no mirar el Sol sin filtro seguro.",
    ),
    "mareas": (
        "NASA Science: Tides",
        "https://science.nasa.gov/moon/tides/",
        "Consultada el 2026-11-24. Los esquemas de esa página están marcados como no a escala.",
    ),
    "meteoros": (
        "NASA Science: Meteors and Meteorites",
        "https://science.nasa.gov/solar-system/meteors-meteorites/",
        "Consultada el 2026-11-24. No se pregunta la masa diaria estimada: es una cifra variable.",
    ),
    "anio": (
        "NASA Space Place: What Is a Light-Year?",
        "https://spaceplace.nasa.gov/light-year/en/",
        "Página actualizada el 2020-08-27 y consultada el 2026-11-24. No se usa su ejemplo de la galaxia más lejana: esa marca ya no está vigente.",
    ),
    "cielo": (
        "NASA Space Place: What Are Constellations?",
        "https://spaceplace.nasa.gov/constellations/en/",
        "Página actualizada el 2022-12-06 y consultada el 2026-11-24.",
    ),
    "ideas": (
        "UAI: Grandes Ideas de la Astronomía",
        "https://astro4edu.org/es/bigideas/bigideas/",
        "Consultado el índice el 2026-11-24. Solo se usan los títulos visibles de las grandes ideas, no el folleto completo.",
    ),
}


def _line(src):
    title, url, note = S[src]
    return f"{title} — {url} — {note}"


def _refs(*keys):
    return "\n".join(_line(key) for key in keys)


def Q(kind, text, explanation, payload):
    return {"kind": kind, "text": text, "explanation": explanation, "payload": payload}


def L(slug, title, hook, objective, prior, summary, connections, refs, cards, questions, minutes=4, icon="orbit"):
    return {
        "slug": slug,
        "title": title,
        "subtitle": hook,
        "objective": objective,
        "prerequisites": prior,
        "summary": summary,
        "connections": connections,
        "references": refs,
        "cards": cards,
        "questions": questions,
        "minutes": minutes,
        "icon": icon,
    }


def C(title, subtitle, summary, fact="", icon="orbit"):
    return {"title": title, "subtitle": subtitle, "summary": summary, "fact": fact, "icon": icon}


STAGES = [
    ("e1", 1, "Descubre el cielo", "Reconocer escalas, el cielo y cómo se mueve la Tierra."),
    ("e2", 2, "Explora nuestro vecindario", "La Luna, los eclipses, los planetas y los cuerpos pequeños."),
    ("e3", 3, "Entiende las reglas del espacio", "Distancias, gravedad, órbitas y cómo nacen los sistemas planetarios."),
    ("e4", 4, "Aprende a leer la luz", "La luz, los telescopios, los espectros y el Sol."),
    ("e5", 5, "La vida de las estrellas", "Tipos de estrellas, su cambio y la gravedad extrema."),
    ("e6", 6, "Investiga el universo", "Otros sistemas, galaxias, la expansión y lo que sigue abierto."),
]

# Unidades 9-24: solo estructura. Sin lecciones publicadas.
DRAFTS = [
    (9, "e3", "u09", "Distancias enormes", "orbit", "Kilómetros, unidad astronómica, año luz y el tiempo que tarda la luz. Borrador, sin lecciones publicadas."),
    (10, "e3", "u10", "Gravedad y movimiento", "planet", "Masa, peso, atracción, inercia y caída libre. Borrador, sin lecciones publicadas."),
    (11, "e3", "u11", "Cómo funcionan las órbitas", "orbit", "Leyes de Kepler, elipses, periodos y satélites. Borrador, sin lecciones publicadas."),
    (12, "e3", "u12", "Cómo nacen los sistemas planetarios", "sun", "Nubes, discos, acreción y la formación del sistema solar. Borrador, sin lecciones publicadas."),
    (13, "e4", "u13", "La luz trae información", "star", "Ondas, longitud de onda, frecuencia y el espectro. Borrador, sin lecciones publicadas."),
    (14, "e4", "u14", "Nuestros ojos tecnológicos", "target", "Telescopios, detectores y observatorios. Borrador, sin lecciones publicadas."),
    (15, "e4", "u15", "Descifrar una estrella", "star", "Espectros, elementos, temperatura y el efecto Doppler. Borrador, sin lecciones publicadas."),
    (16, "e4", "u16", "Conoce al Sol", "sun", "Estructura, fusión, actividad solar y la relación con la Tierra. Borrador, sin lecciones publicadas."),
    (17, "e5", "u17", "Estrellas diferentes", "star", "Color, temperatura, luminosidad y brillo aparente. Borrador, sin lecciones publicadas."),
    (18, "e5", "u18", "Nacer, vivir y cambiar", "galaxy", "Nebulosas, protoestrellas, secuencia principal y el diagrama H-R. Borrador, sin lecciones publicadas."),
    (19, "e5", "u19", "El destino de las estrellas", "star", "Evolución según la masa. Borrador, sin lecciones publicadas."),
    (20, "e5", "u20", "Gravedad extrema", "blackhole", "Relatividad introductoria, agujeros negros y ondas gravitacionales. Borrador, sin lecciones publicadas."),
    (21, "e6", "u21", "Otros sistemas planetarios", "planet", "Exoplanetas, tránsitos, velocidad radial y habitabilidad. Borrador, sin lecciones publicadas."),
    (22, "e6", "u22", "Galaxias y distancias cósmicas", "galaxy", "La Vía Láctea, tipos de galaxias y la escalera de distancias. Borrador, sin lecciones publicadas."),
    (23, "e6", "u23", "Un universo que evoluciona", "galaxy", "Expansión, corrimiento al rojo, Big Bang y el fondo cósmico. Borrador, sin lecciones publicadas."),
    (24, "e6", "u24", "Las preguntas abiertas", "atom", "Materia oscura, energía oscura, vida y los límites de lo que sabemos. Borrador, sin lecciones publicadas."),
]


def _units():
    """Unidades 1-8 con lecciones listas para publicar."""
    none = "Ninguno: es el inicio de la ruta."
    return [
        {
            "code": "u01",
            "stage": "e1",
            "order": 1,
            "name": "Tu lugar en el universo",
            "slug": "tu-lugar-en-el-universo",
            "icon": "orbit",
            "difficulty": 1,
            "subtitle": "De la Tierra a la galaxia, sin perder la escala.",
            "description": "Tierra, Sol, sistema solar, galaxia y universo: qué es cada cosa y cómo se contienen.",
            "lessons": [
                L(
                    "u01-escalas",
                    "Cinco escalas",
                    "¿La Tierra, el Sol y la galaxia son lo mismo en tamaños distintos?",
                    "Ordenar Tierra, Sol, sistema solar, galaxia y universo, y decir cuál contiene a cuál.",
                    none,
                    "La Tierra es un planeta. El Sol es la estrella del sistema solar. Ese sistema está en la Vía Láctea, y la Vía Láctea es una galaxia entre muchas en el universo.",
                    "Esta es la primera lección.",
                    _refs("sistema", "datos", "ideas"),
                    [
                        C("De menor a mayor", "Un planeta no es una galaxia", "La Tierra orbita al Sol. El Sol, con los planetas y otros cuerpos, forma el sistema solar. El sistema solar está dentro de la Vía Láctea. El universo incluye esa galaxia y las demás.", icon="earth"),
                        C("Una estrella, ocho planetas", "El Sol no es un planeta", "Nuestro sistema tiene una estrella, el Sol, y ocho planetas. También hay cinco planetas enanos con nombre oficial, cientos de lunas y muchos cuerpos menores. Un dibujo del sistema no suele estar a escala.", "Los esquemas habituales agrandan los planetas.", icon="sun"),
                    ],
                    [
                        Q("single", "¿Cuál es el orden correcto, de lo más pequeño a lo más grande?", "La Tierra pertenece al sistema solar, el sistema solar a la galaxia y la galaxia al universo. Invertir galaxia y sistema solar es el error más común.", [("El universo, la galaxia, el sistema solar y la Tierra", False), ("La Tierra, el sistema solar, la galaxia y el universo", True), ("La Tierra, la galaxia, el Sol y el sistema solar", False)]),
                        Q("tf", "El Sol es un planeta muy luminoso.", "El Sol es la estrella del sistema solar. Los planetas, en la ficha de NASA, son los ocho mundos que lo orbitan.", False),
                        Q("single", "¿Dónde está el sistema solar?", "NASA sitúa el sistema solar en la Vía Láctea, una galaxia espiral barrada. El universo es el conjunto, no un barrio de la galaxia.", [("Dentro de la Vía Láctea", True), ("Fuera de cualquier galaxia", False), ("Dentro de la Luna", False)]),
                    ],
                    icon="earth",
                ),
                L(
                    "u01-vecindario",
                    "Nuestro barrio en la galaxia",
                    "¿La Vía Láctea es el universo entero?",
                    "Ubicar el Sol en el brazo de Orión de la Vía Láctea y distinguir galaxia de universo.",
                    "Cinco escalas.",
                    "El Sol está en un brazo parcial de la Vía Láctea llamado brazo de Orión. La galaxia tiene muchos más sistemas. El universo contiene muchísimas galaxias.",
                    "Sigue a las cinco escalas.",
                    _refs("sistema", "datos"),
                    [
                        C("Brazo de Orión", "No estamos en el centro", "NASA describe la Vía Láctea como una galaxia espiral barrada. El Sol está en el brazo de Orión, entre los brazos de Sagitario y Perseo.", icon="galaxy"),
                        C("Una vuelta larga", "Una cifra aproximada", "El sistema solar tarda unos 230 millones de años en dar una vuelta al centro de la galaxia, según la ficha de NASA consultada en 2026. Es una escala de tiempo, no un dato para memorizar al año.", "Cifra aproximada de NASA Science, 2026-11-24.", icon="orbit"),
                    ],
                    [
                        Q("single", "¿Qué es la Vía Láctea?", "Es la galaxia donde está el sistema solar. Llamarla universo deja fuera a las demás galaxias.", [("La galaxia que contiene al sistema solar", True), ("Otro nombre del sistema solar", False), ("El conjunto de todos los universos", False)]),
                        Q("tf", "El Sol está en el centro de la Vía Láctea.", "Está en el brazo de Orión, un brazo parcial entre Sagitario y Perseo, no en el centro.", False),
                        Q("single", "Unos 230 millones de años, en la ficha de NASA, miden…", "Miden el tiempo aproximado de una órbita del sistema solar alrededor del centro galáctico. No es la edad de la Tierra ni un año luz.", [("Una vuelta del sistema solar al centro de la galaxia", True), ("La edad de la Tierra", False), ("Lo que tarda la luz en llegar del Sol", False)]),
                    ],
                    icon="galaxy",
                ),
                L(
                    "u01-ano-luz",
                    "El año luz mide distancia",
                    "Si algo está a un año luz, ¿tardó un año en crearse?",
                    "Reconocer que un año luz es distancia y que la luz del Sol tarda minutos, no años.",
                    "Las escalas y el barrio galáctico.",
                    "Un año luz es la distancia que recorre la luz en un año terrestre. La luz del Sol, a unos 150 millones de kilómetros, tarda unos 8 minutos. Ver lejos es ver el pasado de ese objeto.",
                    "Prepara la unidad de distancias, que sigue en borrador.",
                    _refs("anio", "tierra"),
                    [
                        C("No es un reloj", "Es una regla", "Space Place define el año luz como la distancia que la luz recorre en un año de la Tierra. Por eso no se dice que una estrella tenga cuatro años luz de edad cuando está a cuatro años luz.", icon="star"),
                        C("El Sol, en minutos", "La estrella más cercana", "La luz del Sol tarda unos 8 minutos en llegar. La siguiente estrella está a unos 4,3 años luz: la vemos como era hace ese tiempo. Esas dos cifras vienen de Space Place, página actualizada en 2020.", "No uses esta tarjeta como mapa a escala.", icon="sun"),
                    ],
                    [
                        Q("single", "Un año luz es…", "Es distancia. Confundirlo con tiempo es el error que esta lección quiere cortar.", [("La distancia que la luz recorre en un año", True), ("El tiempo que tarda la Tierra en orbitar el Sol", False), ("La edad de una estrella", False)]),
                        Q("tf", "La luz del Sol tarda un año luz en llegar a la Tierra.", "Tarda unos 8 minutos. Un año luz es muchísimo más largo que la distancia Tierra-Sol.", False),
                        Q("text", "Escribe la palabra que falta: el año luz es una unidad de ____.", "La respuesta es distancia. Space Place lo define así para no usarlo como si fuera un periodo.", ["distancia"]),
                    ],
                    icon="star",
                ),
                L(
                    "u01-casa",
                    "Por ahora, la vida conocida está aquí",
                    "¿Haber agua o un planeta parecido demuestra que hay vida?",
                    "Separar «la Tierra alberga la vida que conocemos» de «ya sabemos que no hay vida en ningún otro sitio».",
                    "Las escalas anteriores.",
                    "NASA dice que, hasta ahora, la Tierra es el único lugar del sistema solar donde hemos encontrado vida. Eso no es una prueba de que el resto del universo esté vacío: es el límite de lo encontrado.",
                    "Cierra la primera unidad y deja abierta la búsqueda, que se estudia más adelante.",
                    _refs("sistema", "tierra", "ideas"),
                    [
                        C("Un dato y un límite", "No es lo mismo", "La ficha de la Tierra dice que es el único mundo conocido con seres vivos. La ficha del sistema solar dice que, por ahora, solo conocemos vida en la Tierra y que NASA la busca en otros mundos.", icon="earth"),
                        C("Una idea, no un sello", "La ruta no es un currículo oficial", "El índice de Grandes Ideas de la UAI incluye que vivimos en un planeta pequeño del sistema solar y que quizá no estemos solos. Es un marco pedagógico, no un aval de esta app.", icon="cards"),
                    ],
                    [
                        Q("single", "¿Qué afirma con más cuidado la ficha de NASA consultada?", "«Hasta ahora solo conocemos vida en la Tierra» no significa «está demostrado que no existe en otro lugar».", [("Hasta ahora, la vida conocida del sistema solar está en la Tierra", True), ("Está demostrado que no hay vida fuera de la Tierra", False), ("Todos los planetas tienen vida", False)]),
                        Q("tf", "Encontrar un mundo parecido a la Tierra demuestra que allí hay vida.", "Parecerse o tener alguna condición favorable no es lo mismo que detectar vida. Esta lección solo afirma dónde la hemos encontrado.", False),
                        Q("single", "Esta ruta de AstroGuide es…", "Es una propuesta de la app para ordenar el aprendizaje. No es un plan oficial de la NASA ni de la UAI.", [("Una propuesta pedagógica de la app", True), ("El currículo oficial de la NASA", False), ("Un examen de la Unión Astronómica Internacional", False)]),
                    ],
                    icon="earth",
                ),
            ],
        },
        {
            "code": "u02",
            "stage": "e1",
            "order": 2,
            "name": "¿Qué estudia la astronomía?",
            "slug": "que-estudia-la-astronomia",
            "icon": "cards",
            "difficulty": 1,
            "subtitle": "Evidencias, modelos y lo que no es astronomía.",
            "description": "Qué observa la astronomía, en qué se diferencia de la astrología y cómo se reconoce un modelo.",
            "lessons": [
                L(
                    "u02-ciencia",
                    "Astronomía no es astrología",
                    "¿Mirar el horóscopo es hacer astronomía?",
                    "Distinguir la astronomía, que usa evidencias, de la astrología, que no las aporta para sus predicciones personales.",
                    "Saber que el sistema solar está en una galaxia.",
                    "La astronomía estudia el espacio con observaciones y datos. La astrología afirma que las posiciones del cielo describen a las personas o predicen su futuro, y esa afirmación no se apoya en evidencia científica.",
                    "Usa el cielo de la unidad anterior como objeto de estudio, no como oráculo.",
                    _refs("cielo", "ideas"),
                    [
                        C("Dos palabras parecidas", "No estudian lo mismo", "Space Place define la astronomía como el estudio científico de lo que hay en el espacio. La astrología, dice esa página, se basa en la creencia de que esas posiciones predicen el futuro o describen a una persona, y sus afirmaciones no se apoyan en evidencia científica.", icon="star"),
                        C("Una ciencia antigua", "Solo el título", "En el índice de Grandes Ideas, la idea 1 dice que la astronomía es una de las ciencias más antiguas, y la idea 4 que estudia los objetos celestes y los fenómenos del universo. No citamos aquí el desarrollo de esas ideas: no se abrió el folleto.", icon="cards"),
                    ],
                    [
                        Q("single", "¿Cuál de estas tareas es astronomía?", "Medir y contrastar datos del cielo es astronomía. Decir cómo será la semana de una persona según su signo no lo es.", [("Comparar observaciones del cielo con un modelo", True), ("Predecir la personalidad por la constelación del nacimiento", False), ("Elegir un número de la suerte con la Luna", False)]),
                        Q("tf", "La astrología y la astronomía son dos nombres de la misma ciencia.", "Space Place las separa: una exige evidencia y la otra no sostiene con evidencia sus claims sobre personas.", False),
                        Q("text", "Escribe el nombre de la ciencia que estudia el espacio con evidencias.", "La respuesta es astronomía. Astrología no se acepta en esta pregunta.", ["astronomia"]),
                    ],
                    icon="cards",
                ),
                L(
                    "u02-modelos",
                    "Ver no es lo mismo que modelar",
                    "Si nadie ha fotografiado algo, ¿puede seguir siendo una idea científica?",
                    "Clasificar un enunciado como observación o como modelo, usando la nube de Oort como caso.",
                    "Astronomía y evidencia.",
                    "Una observación es algo medido o visto. Un modelo organiza datos cuando el objeto no se ha visto directamente. La nube de Oort es un modelo: explica cometas, y NASA dice que no la hemos observado de forma directa.",
                    "El año luz ya enseñó a no tomar una palabra por lo que parece.",
                    _refs("datos", "oort"),
                    [
                        C("La nube que no se ha visto", "Modelo, no foto", "La ficha del sistema solar dice que la nube de Oort no se ha observado directamente. Su existencia se predice con modelos y con cometas que probablemente vienen de allí. La página específica repite que NASA no tiene imágenes directas.", icon="orbit"),
                        C("Cómo reconocerlo", "La frase importa", "Si el texto dice «vemos», «medimos» o «esta foto muestra», es una observación. Si dice «los científicos piensan» o «el modelo predice», todavía no es una foto. Las dos cosas pueden ser ciencia.", icon="target"),
                    ],
                    [
                        Q("single", "Según las fichas de NASA consultadas, la nube de Oort es…", "Es una predicción a partir de modelos y de cometas. Tratarla como una fotografía inventa una observación.", [("Un modelo todavía no observado de forma directa", True), ("Una foto tomada por un telescopio en órbita", False), ("Otro nombre del cinturón de asteroides", False)]),
                        Q("tf", "Un modelo científico es lo mismo que una opinión sin datos.", "Un modelo se contrasta con observaciones. La nube de Oort se propone para explicar cometas, no como una preferencia personal.", False),
                        Q("single", "¿Cuál de estas frases marca una observación?", "La observación señala lo registrado. Las otras anuncian una interpretación.", [("Una sonda midió partículas del viento solar en ese lugar", True), ("Un modelo predice un depósito lejano de cometas", False), ("Se cree que allí hay una nube", False)]),
                    ],
                    icon="target",
                ),
                L(
                    "u02-constelaciones",
                    "Figuras en el cielo, no objetos unidos",
                    "¿Las estrellas de una constelación están pegadas entre sí?",
                    "Explicar que una constelación es una región o figura del cielo y que sus estrellas pueden estar a distancias muy distintas.",
                    "Escalas y la idea de modelo.",
                    "Hoy hay 88 constelaciones reconocidas. Las estrellas de una figura no forman un objeto físico: unas están cerca y otras muy lejos. Sirven como mapa para nombrar regiones del cielo.",
                    "El año luz explica por qué dos estrellas vecinas en el dibujo pueden no ser vecinas de verdad.",
                    _refs("cielo"),
                    [
                        C("Un dibujo, no una familia", "Distancias distintas", "Space Place dice que las estrellas de una constelación no están conectadas. Algunas están relativamente cerca y otras muy lejos. La figura aparece si imaginamos líneas entre ellas.", icon="star"),
                        C("88 oficiales", "El mapa cambió según la cultura", "Hoy se reconocen 88 constelaciones. Otras culturas vieron otras figuras y otros nombres. Los astrónomos usan las oficiales para nombrar estrellas, nebulosas y lluvias de meteoros.", "Página de Space Place actualizada en 2022.", icon="cards"),
                    ],
                    [
                        Q("tf", "Las estrellas de una constelación forman un grupo físico a la misma distancia.", "Pueden verse juntas y estar a distancias muy diferentes. La figura es una perspectiva desde la Tierra.", False),
                        Q("single", "¿Para qué usan hoy las constelaciones los astrónomos, según Space Place?", "Sirven de mapa para nombrar objetos y lluvias. No demuestran que esas estrellas nacieron juntas.", [("Como referencia para nombrar regiones y objetos del cielo", True), ("Para demostrar que esas estrellas están unidas", False), ("Para predecir la personalidad", False)]),
                        Q("text", "¿Cuántas constelaciones oficiales menciona Space Place? Escribe el número.", "La página dice 88. Es un convenio de nombres, no el número de estrellas.", ["88"]),
                    ],
                    icon="star",
                ),
                L(
                    "u02-nombres",
                    "Quién pone los nombres",
                    "¿Por qué Plutón dejó de contarse entre los planetas?",
                    "Explicar que la definición de planeta usada en esta ruta es la de la UAI en 2006, y que los nombres oficiales no son un descubrimiento nuevo del objeto.",
                    "Astronomía, modelos y constelaciones.",
                    "En 2006 la Unión Astronómica Internacional adoptó una definición de planeta para el sistema solar. Con ella hay ocho planetas y cinco planetas enanos con nombre oficial. Poner nombre o clasificar no cambia lo que el objeto es físicamente.",
                    "Prepara la unidad de planetas y la de mundos pequeños.",
                    _refs("planetas"),
                    [
                        C("Ocho, no nueve", "Una decisión de 2006", "NASA explica que en 2006 la UAI definió planeta para nuestro sistema solar. Plutón pasó a planeta enano. Los cinco con nombre oficial son Ceres, Plutón, Haumea, Makemake y Eris.", icon="planet"),
                        C("Clasificar no es inventar", "El objeto ya estaba ahí", "Plutón no desapareció en 2006. Cambió de categoría porque la definición nueva separa planeta y planeta enano. Esta lección no copia el texto completo de la resolución: usa el resumen de la ficha de NASA.", icon="flag"),
                    ],
                    [
                        Q("single", "¿Qué ocurrió con Plutón en 2006, según NASA?", "Fue reclasificado como planeta enano. No se desintegró ni se descubrió ese año.", [("La UAI lo clasificó como planeta enano", True), ("Dejó de existir", False), ("Se convirtió en una estrella", False)]),
                        Q("tf", "Cambiar el nombre o la categoría de un cuerpo hace que cambie su masa.", "La clasificación es un acuerdo sobre cómo llamarlo. La masa no depende de la palabra.", False),
                        Q("single", "¿Cuántos planetas reconoce esa definición en nuestro sistema solar?", "Ocho. Los cinco planetas enanos oficiales van aparte.", [("Ocho", True), ("Nueve", False), ("Cinco", False)]),
                    ],
                    icon="flag",
                ),
            ],
        },
    ]


def _units_sky_and_moon():
    return [
        {
            "code": "u03",
            "stage": "e1",
            "order": 3,
            "name": "Mira hacia arriba",
            "slug": "mira-hacia-arriba",
            "icon": "star",
            "difficulty": 1,
            "subtitle": "Qué se mueve de verdad y qué solo lo parece.",
            "description": "Estrellas, planetas, la Luna y el cambio del cielo con la órbita y el lugar.",
            "lessons": [
                L(
                    "u03-fijos",
                    "Patrones que casi no cambian",
                    "Si las estrellas salen cada noche, ¿se están moviendo ellas?",
                    "Explicar que las figuras estelares se mantienen durante años y que su desplazamiento en el cielo se debe a nuestro movimiento.",
                    "Constelaciones y escalas.",
                    "Space Place dice que las estrellas permanecen casi en el mismo sitio durante muchísimos años. Parecen moverse porque la Tierra se mueve. Cada noche se ven un poco más al oeste.",
                    "El mapa de 88 constelaciones es la herramienta de esta lección.",
                    _refs("cielo"),
                    [
                        C("El mismo dibujo", "Años, no minutos", "Las constelaciones sirven de referencia porque sus estrellas no reordenan la figura de un año para otro. Lo que cambia es la porción de cielo que mira la noche.", icon="star"),
                        C("Un paso al oeste", "La órbita de la Tierra", "Como la Tierra avanza alrededor del Sol, el cielo nocturno cambia a lo largo del año. De una noche a la siguiente, las estrellas aparecen un poco más al oeste.", icon="orbit"),
                    ],
                    [
                        Q("single", "¿Por qué el cielo de la noche no es idéntico en enero y en julio?", "Porque la Tierra está en otro punto de su órbita y mira hacia otra dirección del espacio. No porque las constelaciones se desarmen.", [("Porque la Tierra ha avanzado en su órbita", True), ("Porque las estrellas cambian de figura cada mes", False), ("Porque la Luna apaga unas estrellas", False)]),
                        Q("tf", "Las estrellas de una constelación cruzan el sistema solar cada semana.", "Se quedan, a escala humana, en el mismo patrón. Quien se desplaza es la Tierra.", False),
                        Q("single", "De una noche a la siguiente, las estrellas parecen…", "Space Place dice que aparecen un poco más al oeste.", [("Un poco más al oeste", True), ("En un orden distinto", False), ("Más cerca de la Tierra", False)]),
                    ],
                    icon="star",
                ),
                L(
                    "u03-planetas",
                    "Los que cambian de sitio",
                    "¿Por qué algunos puntos brillantes no respetan las figuras?",
                    "Distinguir un planeta de una estrella por su desplazamiento respecto de las constelaciones.",
                    "Patrones del cielo y la definición de planeta.",
                    "La palabra planeta viene del griego y significa errante. Un planeta cambia de posición respecto de las estrellas. Una constelación no se reordena así.",
                    "Une el mapa fijo con los ocho planetas.",
                    _refs("planetas", "cielo"),
                    [
                        C("Errantes", "La palabra ya lo dice", "NASA recuerda que planeta viene del griego planētēs, errante. Vistos desde la Tierra, cambian de lugar entre las estrellas a lo largo de días o semanas.", icon="planet"),
                        C("No son estrellas que parpadean", "Otra pista, con límite", "La pista de esta lección es el movimiento respecto del fondo de estrellas. El titileo lo produce el aire y no basta para clasificar un punto.", icon="star"),
                    ],
                    [
                        Q("single", "Durante varias semanas, un punto brillante cruza de una constelación a otra. Lo más coherente es que sea…", "Ese desplazamiento contra el fondo fijo es el comportamiento de un planeta. Una estrella de la figura no hace ese viaje.", [("Un planeta", True), ("Una estrella de esa constelación", False), ("Un año luz", False)]),
                        Q("tf", "Los planetas están pintados en la constelación y se quedan en el dibujo.", "Se mueven respecto de las figuras. Por eso los antiguos los llamaron errantes.", False),
                        Q("text", "Escribe qué significa, según NASA, la palabra griega de la que viene planeta.", "Significa errante. También se acepta vagabundo o wanderer no: la lección pide la idea en español.", ["errante"]),
                    ],
                    icon="planet",
                ),
                L(
                    "u03-luna",
                    "Una luz que no es suya",
                    "Si la Luna brilla, ¿tiene luz propia?",
                    "Explicar que la luz lunar que vemos es luz solar reflejada y que la Luna es el satélite natural de la Tierra.",
                    "Estrellas, planetas y el Sol como estrella.",
                    "La Luna no produce la luz con la que la vemos: refleja luz del Sol. Es el satélite natural de la Tierra. El Sol ilumina siempre la mitad de la Luna.",
                    "Abre la unidad de la Luna.",
                    _refs("fases", "tierra"),
                    [
                        C("Reflejo, no faro", "La mitad iluminada", "NASA dice que la luz de la Luna es luz solar reflejada. El Sol ilumina siempre una mitad de la Luna; la otra queda en noche. Cuánto vemos de esa mitad depende de la posición.", icon="moon"),
                        C("Nuestro satélite", "Una luna, no un anillo", "La Tierra tiene una luna. NASA la llama el objeto más brillante y familiar del cielo nocturno. Un satélite natural es un cuerpo que orbita un planeta.", icon="earth"),
                    ],
                    [
                        Q("single", "La luz con la que vemos la Luna es…", "Es luz del Sol que rebota en la superficie. Decir que la Luna está encendida confunde reflejo con luz propia.", [("Luz del Sol reflejada", True), ("Luz que la Luna produce como una estrella", False), ("La sombra de la Tierra", False)]),
                        Q("tf", "El Sol ilumina a la vez toda la superficie de la Luna.", "Ilumina una mitad. La otra permanece a oscuras, igual que el lado nocturno de la Tierra.", False),
                        Q("single", "La Luna, respecto de la Tierra, es…", "Es su satélite natural. No es un planeta del sistema ni una estrella.", [("Su satélite natural", True), ("Una estrella pequeña", False), ("El centro del sistema solar", False)]),
                    ],
                    icon="moon",
                ),
                L(
                    "u03-lugar",
                    "No todo el mundo ve el mismo cielo",
                    "¿Una constelación famosa se ve desde cualquier país?",
                    "Predecir que la fecha y el hemisferio cambian las constelaciones visibles.",
                    "Figuras fijas y el movimiento de la Tierra.",
                    "El cielo depende de la fecha y del lugar. Quien está en el hemisferio norte no apunta hacia la misma región del espacio que quien está en el sur. Una constelación puede estar en el cielo de día, tapada por la luz del Sol.",
                    "Prepara la rotación y la traslación.",
                    _refs("cielo"),
                    [
                        C("Fecha y hemisferio", "Dos filtros", "Space Place dice que las constelaciones visibles dependen de la época del año y de la posición en la Tierra. El norte y el sur no miran en la misma dirección.", icon="earth"),
                        C("De día también están", "El Sol las tapa", "El ejemplo de esa página: hacia el 21 de septiembre, desde el hemisferio norte, puede verse Piscis de noche, mientras Virgo queda del lado del Sol y no se ve.", "Ejemplo del hemisferio norte, no un calendario universal.", icon="sun"),
                    ],
                    [
                        Q("single", "Dos personas, una en el norte y otra en el sur, miran el cielo la misma noche. ¿Qué cabe esperar?", "Pueden ver constelaciones distintas porque apuntan a regiones distintas del espacio.", [("Que no vean exactamente las mismas constelaciones", True), ("Que vean el mismo cielo, estrella por estrella", False), ("Que no vean ninguna estrella si no es luna llena", False)]),
                        Q("tf", "Si una constelación no se ve esta noche, ha desaparecido.", "Puede estar sobre el horizonte de día, o no elevarse desde ese hemisferio. No tiene que haberse apagado.", False),
                        Q("single", "¿Qué dos datos necesitas para anticipar una constelación?", "La fecha y el lugar. La personalidad del observador no entra.", [("La fecha y el lugar de la Tierra", True), ("Solo la hora del reloj de pulsera, en cualquier país", False), ("El signo del observador", False)]),
                    ],
                    icon="earth",
                ),
            ],
        },
        {
            "code": "u04",
            "stage": "e1",
            "order": 4,
            "name": "La Tierra en movimiento",
            "slug": "la-tierra-en-movimiento",
            "icon": "earth",
            "difficulty": 1,
            "subtitle": "Rotación, traslación e inclinación, cada una con su efecto.",
            "description": "Día y noche, el año y las estaciones, sin mezclar las causas.",
            "lessons": [
                L(
                    "u04-rotacion",
                    "Un giro y aparece el día",
                    "¿El Sol se apaga de noche?",
                    "Atribuir el día y la noche a la rotación de la Tierra, no a que el Sol se mueva alrededor nuestro cada 24 horas.",
                    "El cielo que cambia y la luz del Sol.",
                    "La Tierra da una vuelta sobre sí misma en unas 23,9 horas. Esa rotación produce el día y la noche. El Sol sigue iluminando: entra en noche la cara que queda de espaldas.",
                    "Separa este giro de la vuelta alrededor del Sol, que es la lección siguiente.",
                    _refs("tierra"),
                    [
                        C("Sobre sí misma", "Unas 23,9 horas", "NASA mide el día de rotación en 23,9 horas. Mientras una mitad mira al Sol, la otra está en noche. No hace falta que el Sol se apague.", icon="earth"),
                        C("No es la órbita", "Dos movimientos", "Orbitar el Sol es la traslación y tarda un año. Confundirla con la rotación hace creer que el día dura 365 días. Son movimientos distintos.", icon="orbit"),
                    ],
                    [
                        Q("single", "¿Qué movimiento explica el día y la noche?", "La rotación. La traslación explica el año y, junto con la inclinación, las estaciones.", [("La rotación de la Tierra", True), ("La vuelta de la Tierra alrededor del Sol", False), ("Que la Luna tape el Sol cada noche", False)]),
                        Q("tf", "De noche, el Sol deja de emitir luz.", "Ilumina el otro lado del planeta. La noche es la cara que no lo está mirando.", False),
                        Q("single", "Una vuelta de la Tierra sobre su eje dura, según la ficha de NASA…", "Unas 23,9 horas. 365,25 días es la traslación.", [("Unas 23,9 horas", True), ("365,25 días", False), ("29,5 días", False)]),
                    ],
                    icon="earth",
                ),
                L(
                    "u04-traslacion",
                    "Una vuelta y pasa un año",
                    "¿Por qué febrero tiene a veces un día más?",
                    "Relacionar la traslación de 365,25 días con el año bisiesto, sin usarla para explicar el día y la noche.",
                    "Rotación y día.",
                    "La Tierra tarda 365,25 días en orbitar el Sol. El calendario cuenta 365, así que cada cuatro años añade un día. Esa vuelta es la traslación, no la rotación.",
                    "El cielo que cambia a lo largo del año viene de este movimiento.",
                    _refs("tierra"),
                    [
                        C("365,25 días", "El cuarto que sobra", "NASA da 365,25 días a la órbita. Como el calendario usa 365, cada cuatro años se añade un 29 de febrero. Ese año se llama bisiesto.", icon="orbit"),
                        C("No produce la noche", "Otra vez los dos relojes", "Si la traslación durara un día, el año y el día serían lo mismo. No lo son: 23,9 horas es el giro, y 365,25 días es la órbita.", icon="sun"),
                    ],
                    [
                        Q("single", "¿Por qué existe el año bisiesto, según la ficha de la Tierra?", "Porque la órbita dura unos 365,25 días y el calendario, 365. El día extra recupera el cuarto acumulado.", [("Para ajustar el calendario a una órbita de 365,25 días", True), ("Porque la rotación a veces dura 48 horas", False), ("Porque la Luna completa trece vueltas", False)]),
                        Q("tf", "La traslación es el giro de la Tierra sobre su eje.", "Ese giro es la rotación. La traslación es la órbita alrededor del Sol.", False),
                        Q("text", "Escribe el movimiento que lleva a la Tierra alrededor del Sol.", "Se llama traslación. Órbita también describe el camino, pero la lección pide el movimiento con este nombre.", ["traslacion"]),
                    ],
                    icon="orbit",
                ),
                L(
                    "u04-eje",
                    "El eje inclinado hace las estaciones",
                    "¿Hace calor en verano porque estamos más cerca del Sol?",
                    "Predecir la estación de cada hemisferio a partir de hacia dónde se inclina el eje, no de la distancia al Sol.",
                    "Rotación y traslación.",
                    "El eje está inclinado unos 23,4° respecto del plano de la órbita. Cuando un hemisferio se inclina hacia el Sol, allí es verano y en el otro es invierno. Medio año después se invierte.",
                    "Corrige la idea de que la cercanía al Sol decide la estación.",
                    _refs("tierra"),
                    [
                        C("23,4 grados", "No es la distancia", "NASA atribuye el ciclo anual de estaciones a esta inclinación. Si el norte se inclina hacia el Sol, el Sol sube más en ese cielo y calienta más. Al sur le llega menos de lleno y es invierno.", "La ficha de la Luna menciona 23,5° en otro contexto. Aquí se usa 23,4°, el de la ficha de la Tierra.", icon="earth"),
                        C("Seis meses después", "Los dos hemisferios no coinciden", "Medio año más tarde, el sur es el que se inclina hacia el Sol. Por eso diciembre puede ser verano en un hemisferio e invierno en el otro. En el inicio de la primavera y del otoño, los dos reciben un calor parecido.", icon="sun"),
                    ],
                    [
                        Q("single", "El hemisferio norte está inclinado hacia el Sol. ¿Qué estación le corresponde?", "Verano en el norte e invierno en el sur. No es verano en todo el planeta.", [("Verano en el norte e invierno en el sur", True), ("Verano en los dos hemisferios", False), ("Invierno en el norte, porque está más lejos", False)]),
                        Q("tf", "Las estaciones ocurren porque la Tierra se acerca y se aleja mucho del Sol.", "La ficha de NASA las explica por la inclinación del eje, no por ese acercamiento.", False),
                        Q("single", "¿Por qué no es verano a la vez en Argentina y en España?", "Porque los hemisferios se inclinan en sentidos opuestos respecto del Sol.", [("Porque cuando un hemisferio mira más al Sol, el otro mira menos", True), ("Porque Argentina gira al revés", False), ("Porque el año bisiesto solo afecta al sur", False)]),
                    ],
                    icon="sun",
                ),
                L(
                    "u04-reto",
                    "Tres causas, tres efectos",
                    "¿Puedes repartir día, año y estaciones sin mezclarlos?",
                    "Asignar rotación, traslación e inclinación a su efecto, en casos nuevos.",
                    "Las tres lecciones anteriores de esta unidad.",
                    "La rotación hace el día y la noche. La traslación marca el año. La inclinación del eje hace que las estaciones de los dos hemisferios vayan al revés.",
                    "Cierra la etapa del cielo que se ve y del movimiento propio.",
                    _refs("tierra", "cielo"),
                    [
                        C("La tabla corta", "Una causa cada vez", "Día y noche: rotación. Año y calendario: traslación. Estaciones opuestas entre hemisferios: eje inclinado. Si una frase mezcla dos, sepáralas antes de responder.", icon="cards"),
                        C("El cielo de cada mes", "Ya tiene causa", "Que en una fecha se vea una constelación y en otra no viene de la traslación: la noche mira hacia otro lado del espacio. No hace falta una estación para explicarlo.", icon="star"),
                    ],
                    [
                        Q("single", "Quieres explicar por qué a las 22:00 ya es de noche. ¿Qué movimiento usas?", "El día y la noche vienen de la rotación. La estación no decide que exista la noche.", [("La rotación", True), ("Solo la inclinación del eje", False), ("Que la Tierra esté más lejos del Sol", False)]),
                        Q("single", "En el sur es verano. ¿Qué cabe decir del norte, según este modelo?", "El hemisferio contrario está en la estación opuesta.", [("Que en el norte es invierno", True), ("Que en el norte también es verano", False), ("Que el norte no tiene estaciones", False)]),
                        Q("tf", "El año bisiesto corrige la rotación de 23,9 horas.", "Corrige el cuarto de día de la órbita de 365,25 días. La rotación ya está contada en el día.", False),
                    ],
                    minutes=5,
                    icon="target",
                ),
            ],
        },
        {
            "code": "u05",
            "stage": "e2",
            "order": 5,
            "name": "Nuestra Luna",
            "slug": "nuestra-luna",
            "icon": "moon",
            "difficulty": 2,
            "subtitle": "Fases, tiempos y la cara que siempre vemos.",
            "description": "Luz reflejada, posiciones, fases, el mes lunar y la rotación sincronizada.",
            "lessons": [
                L(
                    "u05-luz",
                    "Luz propia y luz reflejada",
                    "¿La parte oscura de la Luna está apagada para siempre?",
                    "Explicar que el Sol ilumina siempre media Luna y que la fase es la porción de esa mitad que vemos.",
                    "La Luna refleja luz solar.",
                    "La Luna tiene un lado de día y un lado de noche, y esos lados cambian porque la Luna gira. La fase no es una mancha fija: es cuánto de la mitad iluminada queda de cara a la Tierra.",
                    "Repite el reflejo y lo usa para las fases.",
                    _refs("fases"),
                    [
                        C("Siempre media", "Cambia lo que vemos", "NASA dice que el Sol ilumina la mitad de la Luna. A veces vemos casi toda esa mitad, a veces una franja y a veces nada. La Luna no enciende y apaga trozos.", icon="moon"),
                        C("Día y noche lunares", "También gira", "Como la Tierra, la Luna tiene día y noche, y cambian al rotar. La cara oscura de una fase es noche lunar, no un terreno que no exista.", icon="sun"),
                    ],
                    [
                        Q("single", "Durante un cuarto creciente, la mitad que no vemos iluminada…", "Sigue existiendo. El Sol la ilumina o es su lado de noche, pero nuestra vista solo alcanza una parte de la mitad iluminada.", [("Sigue ahí: la fase es un efecto de perspectiva", True), ("Ha desaparecido hasta la luna llena", False), ("Es la sombra permanente de la Tierra", False)]),
                        Q("tf", "La Luna produce la luz de la zona blanca y apaga la zona oscura.", "Toda la luz que vemos es reflejo del Sol. La zona oscura es la que no estamos viendo iluminada, no un interruptor.", False),
                        Q("single", "¿Qué fracción de la Luna ilumina el Sol en cualquier momento?", "Una mitad. Ver solo una franja no significa que el Sol ilumine solo esa franja.", [("Una mitad", True), ("Solo el cuerno blanco", False), ("Toda la superficie a la vez", False)]),
                    ],
                    icon="moon",
                ),
                L(
                    "u05-posiciones",
                    "Dónde están el Sol, la Tierra y la Luna",
                    "En la luna nueva, ¿la Luna está del mismo lado que el Sol?",
                    "Relacionar luna nueva y luna llena con la posición de la Luna respecto del Sol, sin llamar eclipse a esa posición.",
                    "Luz reflejada y el eje de la Tierra.",
                    "En luna nueva, el lado iluminado mira al Sol y el lado de noche mira a la Tierra: la Luna está en la zona del cielo del Sol. En luna llena está del lado contrario y vemos su lado de día. Ninguna de las dos es, por sí sola, un eclipse.",
                    "La inclinación, que ya salió con las estaciones, impide que cada alineación sea un eclipse.",
                    _refs("fases"),
                    [
                        C("Nueva: del lado del Sol", "Casi nunca lo tapa", "NASA dice que en luna nueva el lado iluminado mira al Sol. La Luna sale y se pone con el Sol. Por la inclinación de su órbita, normalmente no pasa justo delante del Sol.", icon="sun"),
                        C("Llena: al otro lado", "Sale al atardecer", "En luna llena, vista desde la Tierra, la Luna está frente al Sol y vemos el lado de día. Sale hacia el atardecer y se pone hacia el amanecer.", icon="moon"),
                    ],
                    [
                        Q("single", "En luna nueva, ¿hacia qué lado del cielo está la Luna?", "Hacia la zona del Sol. Por eso no la vemos de noche como un disco brillante.", [("Hacia la misma zona del cielo que el Sol", True), ("En el lado opuesto al Sol", False), ("Detrás de la Tierra, en la sombra, siempre", False)]),
                        Q("tf", "Toda luna nueva es un eclipse de Sol.", "NASA dice que, por la inclinación de la órbita, normalmente no cruza justo por delante del Sol. El eclipse es el caso especial.", False),
                        Q("single", "Una luna llena sale, aproximadamente…", "Al atardecer, porque está frente al Sol.", [("Al atardecer", True), ("Al mediodía, junto al Sol", False), ("Solo durante un eclipse", False)]),
                    ],
                    icon="sun",
                ),
                L(
                    "u05-fases",
                    "Cómo se producen las fases",
                    "¿Cuarto creciente significa que solo existe un cuarto de Luna?",
                    "Ordenar las ocho fases y explicar que en los cuartos vemos la mitad del disco iluminado.",
                    "Posiciones de luna nueva y luna llena.",
                    "El orden es: nueva, creciente, cuarto creciente, gibosa creciente, llena, gibosa menguante, cuarto menguante y menguante. En el cuarto vemos la mitad del lado iluminado, no un cuarto del disco.",
                    "Los nombres en español corresponden a la lista de NASA: new, waxing crescent, first quarter, waxing gibbous, full, waning gibbous, third quarter y waning crescent.",
                    _refs("fases"),
                    [
                        C("Ocho pasos", "Creciente y menguante", "Creciente: cada día vemos más de la mitad iluminada. Menguante: vemos menos. Llena es cuando el lado de día mira hacia la Tierra. Nueva es cuando nos mira el lado de noche.", icon="moon"),
                        C("El cuarto no es un cuarto de disco", "Media cara iluminada", "NASA pide no llamar a esa fase simplemente media Luna sin matiz: vemos la mitad de la mitad iluminada. El disco se ve medio claro y medio oscuro. El nombre cuarto viene del punto en el recorrido del mes.", icon="cards"),
                    ],
                    [
                        Q("single", "¿Qué fase sigue a la luna nueva?", "La creciente. El cuarto creciente viene después, cuando el disco ya se ve medio iluminado.", [("Creciente", True), ("Llena", False), ("Menguante", False)]),
                        Q("single", "En cuarto creciente, lo que se ve iluminado es…", "La mitad del disco, que es la mitad de la cara de día. No es un cuarto del disco ni la Luna entera.", [("La mitad del disco", True), ("Un cuarto del disco", False), ("Toda la cara de día", False)]),
                        Q("tf", "Después de la luna llena, la fase siguiente del ciclo es la luna nueva.", "Antes pasan la gibosa menguante, el cuarto menguante y la menguante.", False),
                    ],
                    minutes=5,
                    icon="moon",
                ),
                L(
                    "u05-tiempos",
                    "Dos cuentas del mes",
                    "Si la Luna tarda 27 días en orbitar, ¿por qué las fases repiten a los 29?",
                    "Distinguir los 27,3 días de una vuelta orbital de los 29,5 días de luna nueva a luna nueva.",
                    "El orden de las fases.",
                    "NASA da unos 27,3 días para una revolución y unos 29,5 días de luna nueva a luna nueva. El ciclo de fases es el que repetimos en el cielo. Mientras la Luna da la vuelta, la Tierra también avanza, así que hace falta un poco más para volver a alinearse con el Sol.",
                    "La traslación de la Tierra, ya vista, es la pieza que alarga el ciclo.",
                    _refs("fases", "tierra"),
                    [
                        C("27,3 y 29,5", "No son un error", "27,3 días es la vuelta de la Luna alrededor de la Tierra. 29,5 días es el tiempo para repetir la fase. NASA publica los dos. El de las fases es el mes que se ve en el calendario lunar.", "238 855 millas es la distancia media en esa página. No hace falta memorizarla.", icon="orbit"),
                        C("Por qué no coinciden", "La Tierra no se queda quieta", "En 27 días la Tierra también se ha movido alrededor del Sol. La Luna tiene que recorrer un tramo más para que el Sol, la Tierra y ella vuelvan a la misma fase. Por eso el ciclo visible es más largo.", icon="earth"),
                    ],
                    [
                        Q("single", "¿Qué intervalo usa el ciclo de las fases?", "Unos 29,5 días, de luna nueva a luna nueva. 27,3 días es la órbita.", [("Unos 29,5 días", True), ("Unos 27,3 días", False), ("365,25 días", False)]),
                        Q("tf", "27,3 días y 29,5 días son dos medidas del mismo intervalo.", "Miden cosas distintas: una vuelta orbital y la repetición de la fase.", False),
                        Q("single", "¿Por qué la fase tarda más que una vuelta?", "Porque la Tierra avanza en su órbita y la alineación con el Sol pide un tramo extra.", [("Porque la Tierra también se mueve alrededor del Sol", True), ("Porque la Luna se detiene dos días", False), ("Porque el año bisiesto alarga la Luna", False)]),
                    ],
                    icon="orbit",
                ),
                L(
                    "u05-sincronizada",
                    "Rotación sincronizada",
                    "Si siempre vemos la misma cara, ¿la Luna no gira?",
                    "Explicar que la Luna gira una vez por cada órbita y que por eso desde la Tierra se ve un solo lado.",
                    "Los dos tiempos del mes.",
                    "La Luna está en rotación sincronizada: da una vuelta sobre sí misma en el mismo tiempo que orbita la Tierra. Gira. Desde aquí no vemos la cara lejana. Eso no significa que esa cara esté siempre de noche.",
                    "La rotación de la Tierra fue el modelo. Aquí el periodo de giro y el de órbita coinciden.",
                    _refs("fases"),
                    [
                        C("Gira, al mismo ritmo", "Una vuelta por órbita", "NASA llama a esto rotación sincronizada. El giro dura lo mismo que la órbita, así que la misma cara apunta a la Tierra. No es una Luna quieta.", icon="moon"),
                        C("La cara lejana existe", "No es la cara oscura de una fase", "Desde la Tierra no se ve la cara lejana. Esa cara recibe día y noche a lo largo del giro. Llamarla siempre oscura mezcla la cara oculta con la fase.", icon="star"),
                    ],
                    [
                        Q("tf", "Como vemos siempre el mismo lado, la Luna no rota.", "Rota una vez por órbita. Si no rotara, iríamos viendo toda la superficie.", False),
                        Q("single", "Rotación sincronizada significa que…", "El periodo de giro y el de órbita coinciden, y por eso nos mira el mismo lado.", [("Gira una vez cada vez que completa una órbita", True), ("No tiene rotación", False), ("La Tierra deja de girar cuando hay luna llena", False)]),
                        Q("single", "La cara lejana de la Luna…", "No se ve desde la Tierra, pero no es una noche permanente. El Sol la ilumina en su día.", [("No se ve desde la Tierra, y también tiene día y noche", True), ("Está siempre a oscuras", False), ("Es la luna nueva", False)]),
                    ],
                    icon="moon",
                ),
                L(
                    "u05-reto",
                    "Fase no es eclipse",
                    "¿Puedes tener luna llena sin que la Tierra le haga sombra?",
                    "Resolver casos que mezclan fases, cara oculta y eclipses, y acertar el que corresponde.",
                    "Fases, tiempos y rotación sincronizada.",
                    "La fase depende de cuánta mitad iluminada vemos. El eclipse ocurre solo cuando, además, hay una alineación precisa. La cara lejana es un efecto de la rotación sincronizada, no una fase.",
                    "Deja la explicación completa de eclipses y mareas para la unidad siguiente.",
                    _refs("fases", "eclipses"),
                    [
                        C("Tres ideas distintas", "No las juntes", "Fase: qué porción iluminada vemos. Eclipse: una sombra cuando la alineación es precisa. Cara lejana: el lado que la rotación sincronizada no enseña. Una luna nueva normal no es un eclipse.", icon="cards"),
                        C("El caso especial", "Inclinación", "La propia página de fases dice que en luna nueva la Luna normalmente no pasa justo delante del Sol, por la inclinación de su órbita. El eclipse pide ese paso justo.", icon="target"),
                    ],
                    [
                        Q("single", "Hay luna llena y no hay eclipse. ¿Es posible?", "Sí. La luna llena ocurre cada ciclo. El eclipse lunar solo si, además, entra en la sombra de la Tierra.", [("Sí. La fase no exige el eclipse", True), ("No. Toda luna llena es un eclipse lunar", False), ("No. La luna llena solo existe durante un eclipse solar", False)]),
                        Q("single", "Alguien llama cara oscura a la cara lejana. ¿Qué corrección cabe?", "La cara lejana no se ve desde aquí, pero tiene día. La oscuridad de una fase es otra cosa.", [("Que no la vemos, pero no está siempre de noche", True), ("Que es la luna nueva", False), ("Que es el eclipse de cada mes", False)]),
                        Q("tf", "El cuarto creciente es un eclipse parcial de Sol.", "Es una fase. El Sol no está tapado: vemos media cara iluminada de la Luna.", False),
                    ],
                    minutes=5,
                    icon="target",
                ),
            ],
        },
    ]


def published_units():
    from .path_build import neighborhood_units

    return _units() + _units_sky_and_moon() + neighborhood_units()

"""Unidades 6 a 8 y la carga idempotente de toda la ruta."""

from .learning_path import (
    CHECKED,
    C,
    DRAFTS,
    L,
    Q,
    STAGES,
    _refs,
)


def neighborhood_units():
    return [
        {
            "code": "u06",
            "stage": "e2",
            "order": 6,
            "name": "Alineaciones y mareas",
            "slug": "alineaciones-y-mareas",
            "icon": "sun",
            "difficulty": 2,
            "subtitle": "Cuándo una alineación hace sombra y cuándo mueve el mar.",
            "description": "Eclipses solares y lunares, y una introducción a las mareas.",
            "lessons": [
                L(
                    "u06-alineacion",
                    "Alineados, no en cada fase",
                    "Si ya hay luna nueva, ¿falta algo para el eclipse?",
                    "Explicar que el eclipse exige alinear Sol, Tierra y Luna, y decir en qué fase ocurre cada uno.",
                    "Fases de la Luna, sobre todo nueva y llena.",
                    "El eclipse se ve cuando Sol, Tierra y Luna se alinean. El de Sol ocurre en luna nueva y el de Luna en luna llena. La fase sola no basta: la órbita de la Luna está inclinada y casi siempre pasa por encima o por debajo.",
                    "Cierra el reto de la unidad anterior con la regla de las fases.",
                    _refs("eclipses", "fases"),
                    [
                        C("Dos eclipses", "Fase distinta", "NASA lo resume así: los eclipses lunares ocurren en luna llena y los solares en luna nueva. En el solar, la Luna pasa entre la Tierra y el Sol. En el lunar, la Tierra queda entre el Sol y la Luna.", icon="sun"),
                        C("No cada mes", "La órbita va inclinada", "Hay dos temporadas de eclipses al año, cada una de unos 35 días, separadas por poco menos de seis meses. Fuera de ellas, la luna nueva y la llena no dan en la sombra.", "35 días es una duración aproximada de NASA, no una fecha de calendario.", icon="orbit"),
                    ],
                    [
                        Q("single", "Un eclipse de Sol ocurre en fase de…", "Luna nueva. En luna llena la Luna está al otro lado y no puede tapar el Sol.", [("Luna nueva", True), ("Luna llena", False), ("Cuarto creciente", False)]),
                        Q("single", "Un eclipse de Luna ocurre en fase de…", "Luna llena, cuando puede entrar en la sombra de la Tierra.", [("Luna llena", True), ("Luna nueva", False), ("Creciente", False)]),
                        Q("tf", "Hay eclipse de Sol en cada luna nueva.", "No. La inclinación de la órbita hace que la mayoría de lunas nuevas no crucen el Sol. Los eclipses se concentran en dos temporadas al año.", False),
                    ],
                    icon="sun",
                ),
                L(
                    "u06-tipos",
                    "No hay un solo eclipse de Sol",
                    "¿Por qué a veces el Sol queda como un anillo?",
                    "Distinguir eclipse total, anular, parcial e híbrido, y relacionar el anular con la distancia de la Luna.",
                    "En qué fase ocurre cada eclipse.",
                    "NASA describe cuatro tipos de eclipse solar: total, parcial, híbrido y anular. El tipo depende de cómo se alinean y de lo lejos que esté la Luna. Si no llega a cubrir todo el disco, el anillo que queda es un eclipse anular, no una fase lunar.",
                    "La distancia ya apareció como idea de escala. Aquí cambia el tipo de sombra.",
                    _refs("eclipses"),
                    [
                        C("Cuatro solares", "Tres lunares", "Solares: total, parcial, híbrido y anular. Lunares: total, parcial y penumbral. El híbrido se ve total desde unos lugares y anular desde otros.", icon="sun"),
                        C("La distancia decide el anillo", "No es una fase", "Si la Luna está más lejos, su disco aparente no cubre el Sol y queda un anillo. Eso es un eclipse anular. No es un cuarto creciente: el Sol sigue siendo la fuente y hay que proteger la vista.", icon="moon"),
                    ],
                    [
                        Q("single", "Un anillo de Sol alrededor de la Luna es…", "Un eclipse anular: la Luna no cubre todo el disco solar. No es una fase de la Luna.", [("Un eclipse anular de Sol", True), ("Un cuarto creciente", False), ("Una luna llena", False)]),
                        Q("tf", "El tipo de eclipse solar no depende de la distancia de la Luna.", "NASA dice que el tipo depende de la alineación y de lo lejos que esté la Luna.", False),
                        Q("single", "Un eclipse híbrido…", "Puede verse como total o como anular según el lugar del observador.", [("Se ve total o anular según desde dónde se mire", True), ("Es otra forma de llamar a la luna nueva", False), ("Solo ocurre en luna llena", False)]),
                    ],
                    icon="sun",
                ),
                L(
                    "u06-seguridad",
                    "Cuál se puede mirar",
                    "¿Valen las gafas de sol para un eclipse solar?",
                    "Decidir si hace falta protección para mirar un eclipse de Sol o uno de Luna, y decir cuándo se puede apartar el filtro.",
                    "Tipos de eclipse.",
                    "Salvo el breve tramo de totalidad, no se mira el Sol sin un filtro seguro. Las gafas de sol no sirven. En la totalidad se puede mirar solo mientras el Sol está completamente cubierto. Un eclipse de Luna se puede mirar sin esa protección.",
                    "No es un dato de memoria: es una regla de seguridad de la página de eclipses.",
                    _refs("eclipses"),
                    [
                        C("El Sol, con filtro", "Las gafas de sol no bastan", "NASA dice que, fuera del breve periodo de totalidad, no se mire el Sol sin protección como unas gafas de eclipse. Esas gafas no son gafas de sol. En las fases parciales el filtro sigue puesto.", icon="sun"),
                        C("La Luna, sin ese riesgo", "Incluido el eclipse lunar", "La misma página dice que es seguro mirar la Luna a simple vista, o con telescopio, en cualquier tipo y momento de un eclipse lunar.", icon="moon"),
                    ],
                    [
                        Q("single", "Durante la fase parcial de un eclipse de Sol, ¿qué hay que hacer para mirarlo?", "Usar gafas de eclipse u otro filtro seguro, o un método indirecto como un proyector de agujero. Las gafas de sol no alcanzan.", [("Usar un filtro solar seguro o verlo de forma indirecta", True), ("Usar gafas de sol oscuras", False), ("Mirarlo sin nada, porque la Luna ya tapa una parte", False)]),
                        Q("tf", "Un eclipse de Luna exige las mismas gafas que uno de Sol.", "No. NASA dice que el eclipse lunar se puede mirar sin esa protección.", False),
                        Q("single", "En un eclipse total de Sol, las gafas se pueden quitar…", "Solo durante la totalidad, cuando la Luna cubre por completo el Sol, y hay que volver a ponerlas en cuanto reaparece.", [("Solo durante la totalidad", True), ("Durante todo el eclipse", False), ("Nunca, ni en la totalidad", False)]),
                    ],
                    minutes=5,
                    icon="flag",
                ),
                L(
                    "u06-mareas",
                    "Dos abultamientos, no una flecha",
                    "Si la Luna está sobre el mar, ¿por qué también hay marea alta al otro lado?",
                    "Explicar las dos pleamares, y cuándo la marea es viva o muerta, sin prometer la hora local.",
                    "Alineaciones del Sol, la Tierra y la Luna.",
                    "La gravedad de la Luna deforma el océano en dos abultamientos: el lado cercano y el lejano. La mayoría de las costas tienen dos pleamares al día. Cuando Sol, Tierra y Luna se alinean, en luna nueva o llena, las mareas vivas son más extremas. En los cuartos, las mareas muertas son más moderadas.",
                    "La fase dice el tipo de marea, no la hora de tu playa.",
                    _refs("mareas", "fases"),
                    [
                        C("Dos altas", "Cerca y lejos", "NASA describe un abultamiento del lado de la Luna y otro del lado opuesto. Al rotar, la costa pasa por los dos. De una pleamar a la siguiente pasa un poco más de 12 horas. Los continentes, el viento y la forma de la costa cambian la hora y la altura.", "Los dibujos de esa página no están a escala.", icon="moon"),
                        C("Vivas y muertas", "La fase avisa el tipo", "Con el Sol y la Luna alineados, en luna nueva o llena, las mareas se llaman vivas: más altas y más bajas. Con el Sol y la Luna en ángulo recto, hacia los cuartos, son las muertas, más moderadas. NASA las llama spring y neap. No sustituyen el pronóstico local.", icon="earth"),
                    ],
                    [
                        Q("single", "¿Por qué puede haber marea alta también en el lado opuesto a la Luna?", "Porque el océano se abulta en los dos lados, el cercano y el lejano, no solo debajo de la Luna.", [("Porque hay un abultamiento a cada lado de la Tierra", True), ("Porque el Sol apaga la gravedad de ese lado", False), ("Porque esa costa está siempre en luna llena", False)]),
                        Q("single", "¿En qué fases caben las mareas más extremas?", "En luna nueva y luna llena, cuando Sol, Tierra y Luna se alinean.", [("Luna nueva y luna llena", True), ("Solo en los cuartos", False), ("En cualquier fase, con la misma altura", False)]),
                        Q("tf", "Con la posición de la Luna basta para saber la hora exacta de la pleamar en tu playa.", "No. NASA dice que continentes, profundidad, viento y tormentas cambian la marea, y que hace falta el pronóstico local.", False),
                    ],
                    minutes=5,
                    icon="earth",
                ),
            ],
        },
        {
            "code": "u07",
            "stage": "e2",
            "order": 7,
            "name": "Los planetas",
            "slug": "los-planetas",
            "icon": "planet",
            "difficulty": 2,
            "subtitle": "Orden, grupos y tamaños, sin memorizar diámetros.",
            "description": "Los ocho planetas, rocosos y gigantes, y qué hace distinta a la Tierra.",
            "lessons": [
                L(
                    "u07-orden",
                    "Ocho, en este orden",
                    "¿Plutón entra en la fila?",
                    "Ordenar los ocho planetas desde el Sol y dejar fuera a los planetas enanos.",
                    "La definición de 2006 y el sistema solar.",
                    "Desde el Sol: Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano y Neptuno. Plutón no va en esa fila. Es un planeta enano.",
                    "Recupera la clasificación de la segunda unidad.",
                    _refs("planetas"),
                    [
                        C("La fila", "Cuatro y cuatro", "Los cuatro primeros son Mercurio, Venus, Tierra y Marte. Después vienen Júpiter, Saturno, Urano y Neptuno. Neptuno es el planeta más lejano.", icon="planet"),
                        C("Plutón, aparte", "No es el noveno", "La ficha de NASA lo cuenta entre los planetas enanos desde la definición de 2006. Ponerlo entre Marte y Júpiter, o al final de los ocho, desordena otro grupo.", icon="orbit"),
                    ],
                    [
                        Q("single", "¿Cuál es el orden correcto desde el Sol?", "Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano y Neptuno.", [("Mercurio, Venus, Tierra, Marte, Júpiter, Saturno, Urano, Neptuno", True), ("Mercurio, Venus, Marte, Tierra, Júpiter, Saturno, Neptuno, Urano", False), ("Sol, Tierra, Luna, Marte, Júpiter", False)]),
                        Q("tf", "Plutón es el noveno planeta de esa fila.", "No entra en los ocho. Es un planeta enano.", False),
                        Q("text", "Escribe el planeta más cercano al Sol.", "Mercurio.", ["mercurio"]),
                    ],
                    icon="planet",
                ),
                L(
                    "u07-grupos",
                    "Roca, gas y hielo",
                    "¿Los planetas grandes tienen suelo como la Tierra?",
                    "Clasificar los ocho en rocosos, gigantes gaseosos y gigantes helados.",
                    "El orden de los ocho.",
                    "Mercurio, Venus, Tierra y Marte son rocosos y tienen superficie sólida. Júpiter y Saturno son gigantes gaseosos. Urano y Neptuno son gigantes helados. Los gigantes no tienen una superficie sólida como la de la Tierra.",
                    "El lugar donde se formaron se cuenta con más detalle en una unidad que sigue en borrador.",
                    _refs("planetas", "datos"),
                    [
                        C("Interiores de roca", "Los cuatro primeros", "NASA los llama también planetas terrestres. Tienen superficie sólida. La Tierra es el mayor de esos cuatro.", icon="earth"),
                        C("Exteriores sin ese suelo", "Gas y hielo", "Júpiter y Saturno son los gigantes gaseosos. Urano y Neptuno, los helados. Por fuera hay gas en movimiento, sobre un núcleo. No se puede hablar de un suelo como el terrestre.", icon="jupiter"),
                    ],
                    [
                        Q("single", "¿Cuál es un planeta rocoso?", "Marte está entre los cuatro de superficie sólida. Júpiter no.", [("Marte", True), ("Júpiter", False), ("Neptuno", False)]),
                        Q("single", "Urano y Neptuno se describen como…", "Gigantes helados. Júpiter y Saturno son los gaseosos.", [("Gigantes helados", True), ("Planetas rocosos", False), ("Estrellas pequeñas", False)]),
                        Q("tf", "Júpiter tiene una superficie sólida parecida a la de la Tierra.", "No. Los gigantes no tienen esa superficie. Hay gases sobre un núcleo.", False),
                    ],
                    icon="jupiter",
                ),
                L(
                    "u07-tamanos",
                    "El mayor y el menor",
                    "¿El más lejano es también el más grande?",
                    "Comparar tamaños relativos sin usar diámetros: Júpiter el mayor, Mercurio el menor, la Tierra el mayor de los rocosos.",
                    "Grupos de planetas.",
                    "Júpiter es el mayor y Mercurio el menor. La Tierra es el mayor de los cuatro rocosos y el quinto del sistema. Neptuno es el más lejano y el cuarto en tamaño, así que lejos no significa grande.",
                    "Evita cifras que no hacen falta para comparar.",
                    _refs("planetas", "tierra"),
                    [
                        C("Extremos claros", "Sin memorizar kilómetros", "Mercurio es el más pequeño y el más cercano. Júpiter es el más grande. Saturno es el segundo en tamaño. Urano el tercero. Neptuno el cuarto.", icon="jupiter"),
                        C("La Tierra, en su grupo", "Quinta del sistema", "Es el mayor mundo rocoso y el quinto planeta en tamaño. Venus es un poco menor. Ser el quinto no la hace mediana en todo: es el mayor de los que tienen suelo sólido.", icon="earth"),
                    ],
                    [
                        Q("single", "¿Cuál es el planeta más grande?", "Júpiter.", [("Júpiter", True), ("Saturno", False), ("Neptuno", False)]),
                        Q("single", "Neptuno es el más lejano. En tamaño es…", "El cuarto, no el mayor. La distancia no ordena el tamaño.", [("El cuarto", True), ("El mayor", False), ("Más pequeño que Mercurio", False)]),
                        Q("tf", "Mercurio es el planeta más grande porque está cerca del Sol.", "Es el más pequeño. La cercanía no aumenta el tamaño.", False),
                    ],
                    icon="jupiter",
                ),
                L(
                    "u07-tierra",
                    "Qué hace reconocible a la Tierra",
                    "¿Un planeta con hielo o con nubes ya es otro mundo habitado?",
                    "Señalar rasgos de la Tierra que NASA usa para describirla, sin convertirlos en prueba de vida en otros planetas.",
                    "Tamaños, grupos y la lección sobre la vida conocida.",
                    "La Tierra es el tercer planeta, tiene una luna y, según su ficha, es el único del sistema solar con agua líquida en la superficie y el único donde conocemos vida. Esas frases no demuestran que un mundo parecido esté habitado.",
                    "Habitabilidad y vida se separan de nuevo. La unidad de exoplanetas sigue en borrador.",
                    _refs("tierra", "sistema"),
                    [
                        C("Agua en la superficie", "No basta con decir agua", "La ficha dice que la Tierra es el único planeta del sistema solar con agua líquida en la superficie, y que por eso es habitable para la vida que conocemos. Hielo en otras lunas no es lo mismo que ese océano.", icon="earth"),
                        C("Una luna", "Mercurio y Venus, ninguna", "De los ocho planetas, Mercurio y Venus son los únicos sin lunas. La Tierra tiene una. Venus tiene un cuasisatélite, Zoozve, que no es una luna.", "Zoozve evita el error de contar una luna en Venus.", icon="moon"),
                    ],
                    [
                        Q("single", "Según la ficha de la Tierra, el agua líquida de su superficie…", "La distingue, en esa ficha, del resto de planetas del sistema solar.", [("No se conoce en la superficie de los otros planetas del sistema", True), ("Está también en todos los gigantes", False), ("Prueba que Marte tiene ciudades", False)]),
                        Q("tf", "Venus tiene una luna.", "No. NASA dice que Mercurio y Venus no tienen lunas. Zoozve es un cuasisatélite, no una luna.", False),
                        Q("single", "Saber que la Tierra alberga vida permite afirmar que…", "Que aquí hay vida conocida. No que cualquier planeta con nubes también la tenga.", [("La vida que conocemos está aquí", True), ("Todo planeta rocoso está habitado", False), ("Los gigantes helados tienen océanos con peces", False)]),
                    ],
                    icon="earth",
                ),
            ],
        },
        {
            "code": "u08",
            "stage": "e2",
            "order": 8,
            "name": "Otros mundos pequeños",
            "slug": "otros-mundos-pequenos",
            "icon": "rocket",
            "difficulty": 2,
            "subtitle": "Lunas, enanos, restos y la piedra que cambia de nombre.",
            "description": "Lunas, planetas enanos, asteroides, cometas y la diferencia entre meteoroide, meteoro y meteorito.",
            "lessons": [
                L(
                    "u08-lunas",
                    "No solo la nuestra",
                    "¿Cuántas lunas tiene el sistema: una?",
                    "Reconocer que hay cientos de lunas y que Mercurio y Venus no tienen ninguna.",
                    "La Luna de la Tierra y los ocho planetas.",
                    "El sistema solar tiene cientos de lunas, alrededor de planetas, planetas enanos y algunos asteroides. Mercurio y Venus no tienen. Júpiter y Saturno son los que más acumulan.",
                    "La nuestra sirvió de modelo. Ahora es un caso entre muchos.",
                    _refs("datos", "sistema"),
                    [
                        C("Cientos", "No hace falta el número exacto", "Las fichas hablan de cientos de lunas, no de una lista cerrada para memorizar. El recuento cambia cuando se confirman más. Por eso esta lección no pregunta una cifra.", icon="moon"),
                        C("Dos planetas sin luna", "El resto, no", "Mercurio y Venus no tienen lunas. Los gigantes tienen muchas. Plutón, más pequeño que nuestra Luna, tiene cinco, entre ellas Caronte.", icon="planet"),
                    ],
                    [
                        Q("single", "¿Qué planeta no tiene lunas?", "Mercurio, y también Venus. Júpiter tiene muchas.", [("Mercurio", True), ("Júpiter", False), ("La Tierra", False)]),
                        Q("tf", "La Tierra es el único mundo con una luna.", "Es el único planeta con exactamente una, según su ficha, pero no el único mundo con lunas. Hay cientos.", False),
                        Q("single", "¿Por qué esta lección no pide el número exacto de lunas?", "Porque las fichas dicen cientos y el recuento sigue cambiando.", [("Porque la cifra confirmada cambia", True), ("Porque solo existe la Luna", False), ("Porque las lunas no se pueden contar", False)]),
                    ],
                    icon="moon",
                ),
                L(
                    "u08-enanos",
                    "Planeta enano no es un planeta pequeño",
                    "¿Ceres está en el mismo grupo que Júpiter?",
                    "Nombrar los cinco planetas enanos oficiales y situar a Ceres en el cinturón de asteroides.",
                    "La definición de 2006 y el orden de los planetas.",
                    "Los cinco con nombre oficial son Ceres, Plutón, Haumea, Makemake y Eris. Ceres es el mayor objeto del cinturón de asteroides, entre Marte y Júpiter, y el único planeta enano del sistema solar interior.",
                    "Plutón ya se reclasificó. Aquí se ve el grupo completo.",
                    _refs("planetas"),
                    [
                        C("Cinco nombres", "No son el noveno planeta", "Ceres, Plutón, Haumea, Makemake y Eris. NASA los llama planetas enanos reconocidos. Añadir un sexto, o devolver a Plutón a los ocho, contradice esa ficha.", icon="planet"),
                        C("Ceres, entre Marte y Júpiter", "El interior", "Es el objeto más grande del cinturón de asteroides y el único planeta enano del sistema solar interior. Los otros cuatro están mucho más lejos.", icon="orbit"),
                    ],
                    [
                        Q("single", "¿Cuál de estos es un planeta enano oficial?", "Ceres. Marte es uno de los ocho planetas.", [("Ceres", True), ("Marte", False), ("Titán", False)]),
                        Q("tf", "Ceres orbita más allá de Neptuno.", "Está en el cinturón de asteroides, entre Marte y Júpiter.", False),
                        Q("single", "¿Cuántos planetas enanos con nombre oficial lista la ficha consultada?", "Cinco. No se pregunta cuántos candidatos hay todavía sin ese estatus.", [("Cinco", True), ("Ocho", False), ("Uno, solo Plutón", False)]),
                    ],
                    icon="planet",
                ),
                L(
                    "u08-restos",
                    "Lo que no llegó a ser planeta",
                    "¿El cinturón de asteroides es una foto de la nube de Oort?",
                    "Distinguir asteroide, cometa, cinturón de Kuiper y la nube de Oort como modelo.",
                    "Planetas enanos y la diferencia entre ver y modelar.",
                    "Los asteroides del cinturón son restos que no formaron un planeta. Más allá de Neptuno está el cinturón de Kuiper, de cuerpos helados. La nube de Oort es un modelo esférico, no una imagen: no se ha observado directamente.",
                    "El modelo de la segunda unidad vuelve con nombre y lugar.",
                    _refs("datos", "oort", "meteoros"),
                    [
                        C("Asteroides y cometas", "Restos distintos", "La ficha del sistema solar dice que el cinturón de asteroides son piezas de la época de formación que no se juntaron en un planeta. Los cometas son cuerpos helados. Una lluvia de meteoros aparece cuando la Tierra cruza el polvo que dejó un cometa.", icon="rocket"),
                        C("Kuiper sí, Oort como modelo", "No los iguales", "El cinturón de Kuiper está pasado Neptuno y Plutón es su objeto más conocido. La nube de Oort se sitúa mucho más lejos. NASA dice que no la ha fotografiado y que su idea viene de modelos y de cometas.", "No hay foto de la nube de Oort.", icon="orbit"),
                    ],
                    [
                        Q("single", "El cinturón de asteroides, según la ficha consultada, son…", "Restos que no llegaron a formar un planeta.", [("Piezas que no se reunieron en un planeta", True), ("Una foto de la nube de Oort", False), ("Los anillos de Saturno", False)]),
                        Q("tf", "La nube de Oort y el cinturón de Kuiper están igual de fotografiados.", "De la nube de Oort, NASA dice que no tiene imágenes directas. El cinturón de Kuiper es la región donde está Plutón.", False),
                        Q("single", "Una lluvia de meteoros se relaciona, en la página de meteoros, con…", "Polvo dejado por un cometa, que la Tierra atraviesa.", [("Restos de polvo de un cometa", True), ("La sombra de un eclipse", False), ("El año bisiesto", False)]),
                    ],
                    icon="rocket",
                ),
                L(
                    "u08-piedra",
                    "Tres nombres, tres lugares",
                    "¿Una estrella fugaz es una estrella que cae?",
                    "Asignar meteoroide, meteoro y meteorito al espacio, a la atmósfera y al suelo.",
                    "Asteroides, cometas y la luz que no es propia.",
                    "El meteoroide está en el espacio. El meteoro es el brillo al entrar en la atmósfera. El meteorito es lo que llega al suelo. No es una estrella. Casi todo se evapora antes de tocar tierra.",
                    "Cierra el vecindario. Las reglas del movimiento quedan como borrador.",
                    _refs("meteoros", "tierra"),
                    [
                        C("Dónde está", "El nombre cambia", "Meteoroide: todavía en el espacio, de un grano de polvo a un asteroide pequeño. Meteoro: el destello en el aire, la llamada estrella fugaz. Meteorito: el trozo que sobrevive y llega al suelo.", icon="star"),
                        C("No es una estrella", "El aire hace el brillo", "La ficha de la Tierra dice que la atmósfera frena meteoroides y que la mayoría se quema: eso es el meteoro. Llamarlo estrella que cae mezcla una estrella, que es un sol lejano, con una piedra de paso.", icon="rocket"),
                    ],
                    [
                        Q("single", "Una roca acaba de llegar al suelo. Se llama…", "Meteorito. En el aire era un meteoro y, antes, un meteoroide.", [("Meteorito", True), ("Meteoroide", False), ("Constelación", False)]),
                        Q("single", "La raya luminosa del cielo es…", "Un meteoro: el brillo del meteoroide en la atmósfera.", [("Un meteoro", True), ("Una estrella que se apaga", False), ("Un eclipse anular", False)]),
                        Q("tf", "Todo meteoroide llega al suelo y se convierte en meteorito.", "No. La mayoría se vaporiza en la atmósfera. Solo el que sobrevive es meteorito.", False),
                    ],
                    minutes=5,
                    icon="star",
                ),
            ],
        },
    ]


def _write_question(Question, Option, lesson, index, spec):
    question, _ = Question.objects.update_or_create(
        lesson=lesson,
        order=index,
        defaults={
            "text": spec["text"],
            "qtype": "truefalse" if spec["kind"] == "tf" else spec["kind"],
            "explanation": spec["explanation"],
            "is_active": True,
        },
    )
    question.options.all().delete()
    if spec["kind"] == "tf":
        answer = spec["payload"]
        Option.objects.create(question=question, text="Verdadero", is_correct=answer is True, order=1)
        Option.objects.create(question=question, text="Falso", is_correct=answer is False, order=2)
    elif spec["kind"] == "text":
        for n, word in enumerate(spec["payload"], start=1):
            Option.objects.create(question=question, text=word, is_correct=True, order=n)
    else:
        for n, (label, ok) in enumerate(spec["payload"], start=1):
            Option.objects.create(question=question, text=label, is_correct=ok, order=n)
    return question


def load_learning_path(apps=None, schema_editor=None):
    """Crea o actualiza la ruta. No borra lecciones antiguas ni su progreso."""
    if apps is None:
        from django.apps import apps as django_apps

        apps = django_apps
    from .learning_path import published_units

    Stage = apps.get_model("astro", "Stage")
    Category = apps.get_model("astro", "Category")
    Lesson = apps.get_model("astro", "Lesson")
    Card = apps.get_model("astro", "Card")
    Question = apps.get_model("astro", "Question")
    Option = apps.get_model("astro", "Option")

    stages = {}
    for code, order, name, summary in STAGES:
        stage, _ = Stage.objects.update_or_create(
            code=code, defaults={"name": name, "order": order, "summary": summary}
        )
        stages[code] = stage

    for unit in published_units():
        category, _ = Category.objects.update_or_create(
            code=unit["code"],
            defaults={
                "name": unit["name"],
                "slug": unit["slug"],
                "stage": stages[unit["stage"]],
                "subtitle": unit["subtitle"],
                "description": unit["description"],
                "icon": unit["icon"],
                "order": unit["order"],
                "difficulty": unit["difficulty"],
                "status": "published",
                "is_active": True,
                "accent": "#7c4dff",
            },
        )
        for index, item in enumerate(unit["lessons"], start=1):
            lesson, _ = Lesson.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "category": category,
                    "title": item["title"],
                    "subtitle": item["subtitle"],
                    "objective": item["objective"],
                    "prerequisites": item["prerequisites"],
                    "summary": item["summary"],
                    "connections": item["connections"],
                    "references": item["references"],
                    "source_checked": CHECKED,
                    "review_state": "sources_checked",
                    "duration_min": item["minutes"],
                    "icon": item["icon"],
                    "order": index,
                    "is_active": True,
                },
            )
            for n, card in enumerate(item["cards"], start=1):
                Card.objects.update_or_create(
                    lesson=lesson,
                    order=n,
                    defaults={
                        "category": category,
                        "title": card["title"],
                        "slug": f"{lesson.slug}-c{n}",
                        "subtitle": card["subtitle"],
                        "summary": card["summary"],
                        "fun_fact": card["fact"],
                        "icon": card["icon"] or "orbit",
                        "is_active": True,
                    },
                )
            Card.objects.filter(lesson=lesson, order__gt=len(item["cards"])).update(is_active=False)
            for n, spec in enumerate(item["questions"], start=1):
                _write_question(Question, Option, lesson, n, spec)
            Question.objects.filter(lesson=lesson, order__gt=len(item["questions"])).update(is_active=False)

    for order, stage_code, code, name, icon, description in DRAFTS:
        Category.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "slug": code,
                "stage": stages[stage_code],
                "subtitle": "Próximamente",
                "description": description,
                "icon": icon,
                "order": order,
                "difficulty": 3 if order < 17 else 4,
                "status": "draft",
                "is_active": False,
                "accent": "#7c4dff",
            },
        )

    Category.objects.filter(code__isnull=True).update(is_active=False, status="archived")
    problems = validate_learning_path(apps)
    if problems:
        raise RuntimeError("Ruta inválida:\n" + "\n".join(problems))


def validate_learning_path(apps=None):
    """Devuelve una lista de problemas. Vacía si la estructura cierra."""
    if apps is None:
        from django.apps import apps as django_apps

        apps = django_apps
    Stage = apps.get_model("astro", "Stage")
    Category = apps.get_model("astro", "Category")
    Lesson = apps.get_model("astro", "Lesson")
    problems = []
    if Stage.objects.count() != 6:
        problems.append("Se esperaban 6 etapas.")
    units = list(Category.objects.exclude(code__isnull=True).order_by("order"))
    codes = [unit.code for unit in units]
    if codes != [f"u{n:02d}" for n in range(1, 25)]:
        problems.append("Las 24 unidades no están en orden.")
    published = [unit for unit in units if unit.status == "published"]
    drafts = [unit for unit in units if unit.status == "draft"]
    if [unit.order for unit in published] != list(range(1, 25)):
        problems.append("Las publicadas no son las unidades 1 a 24.")
    if drafts:
        problems.append("Quedan unidades en borrador.")
    for unit in drafts:
        if unit.is_active:
            problems.append(f"{unit.code} está en borrador y sigue activa.")
        if unit.lessons.filter(is_active=True).exists():
            problems.append(f"{unit.code} tiene lecciones publicadas.")
    for unit in published:
        if not unit.is_active:
            problems.append(f"{unit.code} publicada está inactiva.")
        lessons = list(unit.lessons.filter(is_active=True).order_by("order"))
        if not 4 <= len(lessons) <= 6:
            problems.append(f"{unit.code} tiene {len(lessons)} lecciones.")
        for lesson in lessons:
            if lesson.review_state == "expert_reviewed":
                problems.append(f"{lesson.slug} figura como revisión experta.")
            if lesson.review_state != "sources_checked" or not lesson.source_checked:
                problems.append(f"{lesson.slug} sin comprobación de fuentes.")
            if not lesson.objective or not lesson.summary or "http" not in (lesson.references or ""):
                problems.append(f"{lesson.slug} incompleta.")
            if lesson.cards.filter(is_active=True).count() < 2:
                problems.append(f"{lesson.slug} sin tarjetas.")
            questions = lesson.questions.filter(is_active=True)
            if questions.count() < 3:
                problems.append(f"{lesson.slug} sin ejercicios.")
            for question in questions:
                if not question.explanation:
                    problems.append(f"Pregunta sin explicación en {lesson.slug}.")
                correct = question.options.filter(is_correct=True).count()
                if question.qtype == "text" and correct < 1:
                    problems.append(f"Respuesta escrita sin aceptadas en {lesson.slug}.")
                if question.qtype != "text" and correct != 1:
                    problems.append(f"La pregunta de {lesson.slug} no tiene una sola correcta.")
    first = (
        Lesson.objects.filter(is_active=True, category__is_active=True)
        .order_by("category__order", "order")
        .first()
    )
    if first is None or first.slug != "u01-escalas":
        problems.append("La primera lección activa no es u01-escalas.")
    return problems

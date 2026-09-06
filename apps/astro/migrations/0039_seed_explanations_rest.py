# -*- coding: utf-8 -*-
from django.db import migrations

# Explicaciones para el resto del contenido (unidades 3-11).
# { lesson_slug: { texto_pregunta: explicacion } }
EXPL = {
    'que-es-una-estrella': {
        'De que estan hechas principalmente las estrellas?':
            "Las estrellas son enormes bolas de gas, sobre todo hidrogeno y helio, comprimido por su propia gravedad.",
        'Que proceso da energia a una estrella?':
            "La fusion nuclear en su nucleo: une nucleos de hidrogeno y libera enormes cantidades de energia.",
        'Que elemento fusiona una estrella como el Sol en su nucleo?':
            "Fusiona hidrogeno y lo convierte en helio. Ese es el motor durante casi toda su vida.",
        'Escribe el nombre de la estrella mas cercana a la Tierra.':
            "El Sol es nuestra estrella y la mas cercana; la siguiente esta a mas de 4 anos luz.",
        'Las estrellas tienen luz propia.':
            "Verdadero. A diferencia de los planetas, generan su propia luz gracias a la fusion nuclear.",
        'Que mantiene a una estrella estable sin colapsar?':
            "El equilibrio entre la gravedad, que la comprime, y la presion de la fusion, que empuja hacia afuera.",
    },
    'tipos-de-estrellas': {
        'Que color de estrella es el mas caliente?':
            "Las azules son las mas calientes; el color de una estrella depende de su temperatura.",
        'Las estrellas rojas son las mas frias.':
            "Verdadero. En las estrellas el rojo indica menor temperatura y el azul, mayor.",
        'Que determina el color de una estrella?':
            "Su temperatura superficial: cuanto mas caliente, mas azul; cuanto mas fria, mas roja.",
        'Una estrella mucho mas grande que el Sol es una...':
            "Una gigante o supergigante. Betelgeuse, por ejemplo, es una supergigante roja.",
        'Cuanto mas masiva es una estrella, mas rapido vive y muere.':
            "Verdadero. Las masivas queman su combustible mucho mas rapido: viven millones de anos, no miles de millones.",
        'De que color se ve una estrella mas caliente?':
            "Azul. La temperatura marca el color, del azul (caliente) al rojo (frio).",
    },
    'vida-y-muerte-de-una-estrella': {
        'Donde nacen las estrellas?':
            "En las nebulosas, nubes de gas y polvo que se contraen por gravedad hasta encender la fusion.",
        'Como se llama la explosion de una estrella muy masiva al morir?':
            "Supernova: una explosion brillantisima que por un tiempo puede eclipsar a toda su galaxia.",
        'En que termina una estrella como el Sol?':
            "En una enana blanca: un nucleo denso y caliente que se ira enfriando lentamente.",
        'Que puede quedar tras la supernova de una estrella muy masiva?':
            "Un agujero negro o una estrella de neutrones, segun cuanta masa tenia la estrella.",
        'Escribe como se llaman las nubes de gas donde nacen las estrellas.':
            "Nebulosas: autenticas cunas de estrellas hechas de gas y polvo.",
        'Como se llama la fase en que una estrella como el Sol se hincha al final de su vida?':
            "Gigante roja: al agotar el hidrogeno, la estrella se expande enormemente y se enfria en su superficie.",
    },
    'la-via-lactea': {
        'Como se llama nuestra galaxia?':
            "La Via Lactea, una galaxia espiral con cientos de miles de millones de estrellas.",
        'Que forma tiene la Via Lactea?':
            "Espiral: un disco con brazos que giran alrededor de un centro abultado.",
        'Donde esta el Sol dentro de la Via Lactea?':
            "En uno de sus brazos espirales, lejos del centro, a unos 26.000 anos luz.",
        'Que hay en el centro de la Via Lactea?':
            "Un agujero negro supermasivo llamado Sagitario A*, con millones de veces la masa del Sol.",
        'Escribe el nombre de nuestra galaxia.':
            "Via Lactea. Su nombre viene de la banda lechosa que forma en el cielo oscuro.",
        'Aproximadamente cuantas estrellas tiene la Via Lactea?':
            "Cientos de miles de millones de estrellas.",
    },
    'tipos-de-galaxias': {
        'Cual de estos NO es un tipo de galaxia?':
            "No existen galaxias cuadradas. Los tipos principales son espiral, eliptica e irregular.",
        'Dos galaxias pueden chocar entre si.':
            "Verdadero. Las colisiones son comunes; la Via Lactea y Andromeda se fusionaran en el futuro.",
        'Que tipo de galaxia tiene brazos que giran?':
            "Las espirales, como la Via Lactea, con brazos de estrellas que giran alrededor del centro.",
        'Las galaxias con forma de balon y estrellas viejas son...':
            "Elipticas: con forma de balon, poco gas y estrellas mayormente viejas.",
        'La Via Lactea chocara con la galaxia de Andromeda en el futuro.':
            "Verdadero. Ocurrira dentro de unos 4.500 millones de anos, formando una galaxia mayor.",
        'Que tipo de galaxia no tiene una forma definida?':
            "Las irregulares, sin forma espiral ni eliptica clara, a menudo por interacciones con otras galaxias.",
    },
    'que-es-un-exoplaneta': {
        'Que es un exoplaneta?':
            "Un planeta que orbita otra estrella distinta al Sol.",
        'Que es la zona habitable?':
            "La distancia a la estrella donde la temperatura permitiria agua liquida en la superficie.",
        'Ya se han descubierto miles de exoplanetas.':
            "Verdadero. Se han confirmado miles, y hay muchos mas candidatos por confirmar.",
        'En que ano se hallo el primer exoplaneta en una estrella como el Sol?':
            "En 1995, alrededor de la estrella 51 Pegasi; su hallazgo recibio el Nobel de Fisica.",
        'Escribe como se llaman los planetas fuera del Sistema Solar (una palabra).':
            "Exoplanetas: planetas que orbitan otras estrellas.",
        'Un exoplaneta es un planeta que orbita...':
            "Una estrella distinta al Sol; por eso el prefijo exo, fuera del Sistema Solar.",
        'Se han confirmado miles de exoplanetas.':
            "Verdadero. Misiones como Kepler dispararon el numero de confirmaciones.",
    },
    'como-se-descubren': {
        'En que consiste el metodo del transito?':
            "Se mide como la estrella pierde un poquito de brillo cuando el planeta pasa por delante.",
        'Que telescopios se dedican a cazar exoplanetas?':
            "Kepler y TESS, disenados para vigilar el brillo de miles de estrellas y detectar transitos.",
        'La gravedad de un planeta puede hacer que su estrella se bambolee.':
            "Verdadero. Es el metodo de velocidad radial: el planeta tira de su estrella y la hace oscilar.",
        'Como delata un planeta a su estrella en el metodo del bamboleo?':
            "Su gravedad hace que la estrella se mueva un poco, un vaiven que podemos medir.",
        'Escribe el telescopio cazador de planetas que empieza por K.':
            "Kepler, que descubrio miles de exoplanetas observando transitos.",
        'El metodo del transito detecta un exoplaneta cuando...':
            "El planeta pasa por delante de su estrella y la atenua ligeramente.",
        'Que revela el metodo de velocidad radial?':
            "El leve bamboleo de la estrella causado por la gravedad del planeta que la orbita.",
    },
    'mundos-famosos': {
        'Que tiene de especial el sistema TRAPPIST-1?':
            "Tiene siete planetas del tamano de la Tierra, varios en la zona habitable.",
        'Que es una super-Tierra?':
            "Un planeta rocoso mas grande que la Tierra pero menor que los gigantes gaseosos.",
        'Analizando su atmosfera se pueden buscar senales de vida en un exoplaneta.':
            "Verdadero. Ciertos gases en la atmosfera podrian ser biofirmas, indicios de vida.",
        'Que telescopio analiza atmosferas de exoplanetas?':
            "El James Webb, capaz de estudiar la luz que atraviesa la atmosfera de un exoplaneta.",
        'Cuantos planetas tiene el sistema TRAPPIST-1? (numero)':
            "Siete planetas rocosos, un caso unico para estudiar mundos parecidos a la Tierra.",
        'Por que es interesante un planeta en la zona habitable?':
            "Porque a esa distancia podria haber agua liquida en su superficie, clave para la vida como la conocemos.",
        'Los planetas de TRAPPIST-1 orbitan una estrella...':
            "Una enana roja, pequena y fria; por eso sus planetas caben muy cerca de ella.",
    },
    'andromeda-y-el-grupo-local': {
        'Que es Andromeda?':
            "La gran galaxia espiral mas cercana a la Via Lactea.",
        'A que distancia esta Andromeda, aproximadamente?':
            "A unos 2,5 millones de anos luz; la luz que vemos de ella salio hace millones de anos.",
        'Andromeda chocara con la Via Lactea en el futuro lejano.':
            "Verdadero. Se acercan y se fusionaran dentro de unos 4.500 millones de anos.",
        'Que es el Grupo Local?':
            "El grupo de galaxias al que pertenece la Via Lactea, dominado por ella y Andromeda.",
        'Escribe la galaxia grande mas cercana a la nuestra.':
            "Andromeda, visible a simple vista como una mancha tenue en cielos oscuros.",
        'Que le pasara a Andromeda y la Via Lactea en miles de millones de anos?':
            "Chocaran y se fusionaran en una sola galaxia mayor.",
        'El Grupo Local es...':
            "El cumulo de galaxias al que pertenece la Via Lactea, con varias decenas de miembros.",
    },
    'galaxias-asombrosas': {
        'Que es un cumulo de galaxias?':
            "Un grupo de cientos o miles de galaxias unidas por la gravedad.",
        'Como se distribuyen las galaxias a gran escala?':
            "En filamentos y enormes vacios, formando una red cosmica parecida a una telarana.",
        'Que es un cuasar?':
            "El nucleo brillantisimo de una galaxia lejana, alimentado por un agujero negro que devora materia.",
        'Los cuasares estan entre los objetos mas brillantes del universo.':
            "Verdadero. Pueden brillar mas que toda su galaxia junta.",
        'La estructura a gran escala del universo se parece a una...':
            "A una telarana o red cosmica: filamentos de galaxias separados por grandes vacios.",
        'Existen galaxias mucho mas grandes que la Via Lactea.':
            "Verdadero. Algunas galaxias gigantes tienen muchisimas mas estrellas que la nuestra.",
        'Que separa a unas galaxias de otras en el espacio?':
            "Enormes vacios casi sin materia; el universo esta practicamente vacio entre estructuras.",
    },
    'que-es-un-agujero-negro': {
        'Que puede escapar de un agujero negro?':
            "Nada, ni siquiera la luz: por eso es negro y no podemos verlo directamente.",
        'Como nace la mayoria de los agujeros negros?':
            "Al colapsar el nucleo de una estrella muy masiva al final de su vida.",
        'Un agujero negro aspira absolutamente todo lo que hay a su alrededor.':
            "Falso. Solo atrapa lo que cruza su horizonte de sucesos; a distancia actua como cualquier masa.",
        'Por que se llama "negro"?':
            "Porque no emite ni refleja luz: nada escapa de el, ni la propia luz.",
        'Escribe que fuerza es la responsable de un agujero negro.':
            "La gravedad, tan intensa que ni la luz puede escapar.",
        'Un agujero negro es una region donde la gravedad es tan fuerte que...':
            "Ni la luz puede escapar de ella.",
        'Los agujeros negros estelares se forman cuando...':
            "Colapsa el nucleo de una estrella muy masiva tras agotar su combustible.",
    },
    'el-horizonte-de-sucesos': {
        'Que es el horizonte de sucesos?':
            "El punto de no retorno: una vez cruzado, nada puede volver a salir.",
        'Una vez cruzas el horizonte de sucesos, puedes volver.':
            "Falso. Es el limite del que ya nada, ni la luz, puede escapar.",
        'Que hay en el centro de un agujero negro?':
            "Una singularidad: un punto donde la materia se concentra con densidad extrema.",
        'Que muestra la imagen de 2019 de un agujero negro?':
            "La luz de la materia caliente girando a su alrededor, con la sombra oscura del agujero en el centro.",
        'En que ano se publico la primera imagen de un agujero negro? (numero)':
            "En 2019: la del agujero negro de la galaxia M87, por el Event Horizon Telescope.",
        'Como se llama el punto central de densidad extrema de un agujero negro?':
            "La singularidad, donde las leyes fisicas conocidas dejan de funcionar.",
        'Visto desde fuera, que parece pasarle al tiempo cerca del horizonte de sucesos?':
            "Parece transcurrir cada vez mas lento por el intenso campo gravitatorio.",
    },
    'tipos-de-agujeros-negros': {
        'Cuales son los tipos de agujero negro por su masa?':
            "Estelares, intermedios y supermasivos, de menor a mayor masa.",
        'Donde suele haber un agujero negro supermasivo?':
            "En el centro de casi todas las galaxias grandes.",
        'De que nace un agujero negro estelar?':
            "Del colapso de una estrella masiva al morir.",
        'Un agujero negro supermasivo puede tener miles de millones de veces la masa del Sol.':
            "Verdadero. Los hay con millones y hasta miles de millones de masas solares.",
        'El agujero negro del centro de una galaxia es de tipo...':
            "Supermasivo, con millones o miles de millones de veces la masa del Sol.",
        'Que clase de agujero negro hay en el centro de casi todas las galaxias grandes?':
            "Supermasivo, como Sagitario A* en la Via Lactea.",
        'Como se llama el agujero negro del centro de la Via Lactea?':
            "Sagitario A*, con unos 4 millones de veces la masa del Sol.",
        'Los agujeros negros supermasivos tienen millones o miles de millones de veces la masa del Sol.':
            "Verdadero. De ahi el nombre supermasivo.",
    },
    'famosos-y-ondas-gravitacionales': {
        'Que es Sagitario A*?':
            "El agujero negro supermasivo del centro de la Via Lactea.",
        'Que se fotografio por primera vez en 2019?':
            "El agujero negro de la galaxia M87, la primera imagen real de uno.",
        'Que son las ondas gravitacionales?':
            "Ondulaciones del espacio-tiempo que se propagan, por ejemplo al chocar dos agujeros negros.",
        'Las ondas gravitacionales se detectaron por primera vez en 2015.':
            "Verdadero. Las detecto LIGO, confirmando una prediccion de Einstein de un siglo antes.",
        'En que ano se fotografio Sagitario A*? (numero)':
            "En 2022 se publico la imagen de Sagitario A*, el agujero negro de nuestra galaxia.",
        'Que detector capto por primera vez ondas gravitacionales en 2015?':
            "LIGO, dos enormes detectores en forma de L en Estados Unidos.",
        'Las primeras ondas gravitacionales detectadas venian de...':
            "La fusion de dos agujeros negros a mas de mil millones de anos luz.",
        'Ademas de agujeros negros, que otros objetos al fusionarse emiten ondas gravitacionales?':
            "Las estrellas de neutrones, cuya fusion tambien se ha detectado.",
    },
    'el-big-bang': {
        'Que describe el Big Bang?':
            "El inicio y la expansion del universo desde un estado extremadamente denso y caliente.",
        'El Big Bang fue una explosion en un punto concreto del espacio.':
            "Falso. No fue una explosion en el espacio, sino una expansion del propio espacio en todas partes.",
        'Que edad tiene el universo aproximadamente?':
            "Unos 13.800 millones de anos.",
        'Que es la radiacion de fondo de microondas?':
            "El resplandor que sobro del universo primitivo, hoy enfriado hasta las microondas; es la mejor prueba del Big Bang.",
        'Desde el Big Bang, el universo esta...':
            "Expandiendose: el espacio crece y las galaxias se alejan unas de otras.",
        'Que describe la teoria del Big Bang?':
            "El origen y la expansion del universo hace unos 13.800 millones de anos.",
        'Que radiacion es el eco que dejo el Big Bang?':
            "El fondo cosmico de microondas, un resplandor que llena todo el cielo.",
        'El Big Bang fue una explosion dentro de un espacio vacio que ya existia.':
            "Falso. Fue el propio espacio el que empezo a expandirse, no una explosion dentro de el.",
    },
    'la-expansion-del-universo': {
        'Que hacen las galaxias en el universo?':
            "Se alejan unas de otras porque el espacio entre ellas se expande.",
        'Quien descubrio la expansion del universo?':
            "Edwin Hubble, al ver que las galaxias lejanas se alejan de nosotros.",
        'El universo tiene un centro desde el que todo se aleja.':
            "Falso. No hay centro: desde cualquier galaxia se ve a las demas alejarse.",
        'Cuanto mas lejos esta una galaxia...':
            "Mas rapido se aleja; es la ley de Hubble.",
        'Escribe el apellido del astronomo que descubrio la expansion.':
            "Hubble; el telescopio espacial lleva su nombre en su honor.",
        'Que observacion mostro que el universo se expande?':
            "Que las galaxias lejanas se alejan (su luz se corre al rojo), tanto mas cuanto mas lejos estan.",
        'Quien descubrio que las galaxias mas lejanas se alejan mas rapido?':
            "Edwin Hubble, relacionando la distancia con la velocidad de alejamiento.",
        'Que parece acelerar la expansion del universo?':
            "La energia oscura, una forma de energia que empuja la expansion.",
    },
    'materia-y-energia-oscura': {
        'Cuanto del universo es materia y energia oscura?':
            "La mayor parte: mas del 90%. La materia normal es solo una pequena fraccion.",
        'Que hace la materia oscura?':
            "Su gravedad mantiene unidas las galaxias y los cumulos; sin ella se desharian.",
        'Que hace la energia oscura?':
            "Acelera la expansion del universo, empujando las galaxias a separarse cada vez mas rapido.",
        'Todo lo que vemos (estrellas, planetas) es la mayor parte del universo.':
            "Falso. La materia visible es apenas un 5%; el resto es materia y energia oscura.",
        'La materia invisible que une a las galaxias se llama materia...':
            "Oscura: no emite luz, pero la detectamos por su gravedad.",
        'Como se detecta sobre todo la materia oscura?':
            "Por su efecto gravitatorio sobre galaxias y estrellas, ya que no emite luz.",
        'Aproximadamente que fraccion del universo es materia normal (la que vemos)?':
            "Alrededor del 5%; el resto es materia oscura y energia oscura.",
        'La energia oscura parece empujar al universo a expandirse cada vez mas rapido.':
            "Verdadero. Su descubrimiento en 1998 fue una gran sorpresa.",
    },
    'telescopios-que-cambiaron-todo': {
        'Desde cuando esta en orbita el telescopio Hubble?':
            "Desde 1990. Lleva decadas enviando imagenes que cambiaron la astronomia.",
        'Que capta el telescopio James Webb?':
            "Luz infrarroja, que le permite ver las primeras galaxias y a traves del polvo.",
        'Los telescopios espaciales ven mejor porque no tienen la atmosfera estorbando.':
            "Verdadero. Sin la atmosfera que distorsiona y absorbe la luz, la imagen es mucho mas nitida.",
        'En que ano se lanzo el telescopio James Webb?':
            "En 2021; empezo a enviar imagenes en 2022.",
        'Escribe el famoso telescopio espacial que empieza por H.':
            "Hubble, en orbita desde 1990.",
        'Que ventaja tiene el telescopio Hubble por estar en el espacio?':
            "Evita la distorsion de la atmosfera terrestre, logrando imagenes muy nitidas.",
        'En que tipo de luz observa sobre todo el telescopio James Webb?':
            "En infrarrojo, ideal para ver objetos muy lejanos y antiguos.",
        'Observar en infrarrojo le permite al James Webb...':
            "Ver a traves del polvo y captar objetos muy lejanos y antiguos, casi del universo joven.",
    },
    'misiones-que-exploran': {
        'Que hacen hoy las sondas Voyager?':
            "Viajan por el espacio interestelar, mas alla del Sistema Solar, y aun envian datos.",
        'Que hace el rover Perseverance?':
            "Explora Marte buscando senales de vida pasada y recoge muestras.",
        'Voyager 1 es el objeto hecho por humanos mas lejano.':
            "Verdadero. Lanzada en 1977, es la nave que mas lejos ha llegado.",
        'En que ano se lanzaron las sondas Voyager?':
            "En 1977; siguen funcionando decadas despues.",
        'En que planeta trabaja el rover Perseverance?':
            "En Marte, en el crater Jezero, un antiguo lecho de rio.",
        'Que sonda es el objeto humano mas lejano, ya en el espacio interestelar?':
            "Voyager 1, que cruzo al espacio interestelar en 2012.",
        'Que explora el rover Perseverance?':
            "La superficie de Marte, buscando indicios de vida y preparando muestras.",
        'Las sondas Voyager llevan un disco con sonidos e imagenes de la Tierra.':
            "Verdadero. El Disco de Oro, un mensaje para quien pudiera encontrarlo.",
    },
    'grandes-descubrimientos': {
        'Donde se ha encontrado agua, ademas de la Tierra?':
            "En la Luna, Marte y lunas heladas de Jupiter y Saturno como Europa y Encelado.",
        'Que abrio la deteccion de ondas gravitacionales en 2015?':
            "Una forma nueva de estudiar el universo, escuchando choques que la luz no revela.",
        'El agua en el espacio es mas comun de lo que se creia antes.':
            "Verdadero. Se ha hallado agua o hielo en muchos lugares del Sistema Solar.",
        'Como avanza nuestro conocimiento del universo?':
            "Con nuevos telescopios y sondas que ven mas lejos y con mas detalle.",
        'En que ano se detectaron por primera vez las ondas gravitacionales? (numero)':
            "En 2015, un siglo despues de que Einstein las predijera.",
        'Que logro el proyecto Event Horizon Telescope en 2019?':
            "La primera imagen real de un agujero negro, el de la galaxia M87.",
        'El primer exoplaneta alrededor de una estrella como el Sol (1995) lo hallaron...':
            "Michel Mayor y Didier Queloz, que recibieron el Nobel de Fisica por ello.",
        'Hoy sabemos que casi todas las estrellas tienen al menos un planeta.':
            "Verdadero. Los planetas son la norma, no la excepcion, en la galaxia.",
    },
    'la-gravedad': {
        'Que hace la gravedad?':
            "Atrae la materia hacia otra materia: cuanta mas masa, mas atraccion.",
        'La gravedad mantiene a los planetas...':
            "En orbita alrededor del Sol, evitando que salgan disparados al espacio.",
        'Quien describio la ley clasica de la gravedad?':
            "Isaac Newton, con su ley de la gravitacion universal.",
        'Segun Einstein, la gravedad es...':
            "La curvatura del espacio-tiempo producida por la masa; los objetos siguen esa curvatura.",
        'Escribe el apellido del cientifico de la manzana y la gravedad.':
            "Newton, cuya ley explico tanto la caida de una manzana como la orbita de la Luna.",
        'Quien formulo la ley de la gravitacion universal?':
            "Isaac Newton, en el siglo XVII.",
        'Segun Newton, la gravedad entre dos cuerpos es mayor cuando...':
            "Tienen mas masa y estan mas cerca.",
        'Que mantiene a los planetas orbitando el Sol?':
            "La gravedad del Sol, que curva sus trayectorias en orbitas cerradas.",
        'Como describe Einstein la gravedad en la relatividad general?':
            "Como la curvatura del espacio-tiempo causada por la masa y la energia.",
        'Sin aire, dos objetos de distinta masa caen con la misma aceleracion.':
            "Verdadero. Sin resistencia del aire, una pluma y un martillo caen igual, como se probo en la Luna.",
    },
    'la-luz-y-el-espectro': {
        'Que nos permite saber la luz de las estrellas?':
            "De que estan hechas: cada elemento deja una huella caracteristica en su luz.",
        'Que es el espectro de la luz?':
            "La luz descompuesta en sus colores, como un arcoiris, que revela informacion del objeto.",
        'Existe luz que el ojo humano no puede ver, como los rayos X o el infrarrojo.':
            "Verdadero. La luz visible es solo una franja del espectro electromagnetico.",
        'Como supimos de que estan hechas las estrellas sin viajar a ellas?':
            "Analizando su luz y su espectro, que muestra las huellas de sus elementos.",
        'Como se llama la luz descompuesta en colores? (una palabra)':
            "Espectro. Analizarlo se llama espectroscopia.",
        'La luz visible es una pequena parte de...':
            "El espectro electromagnetico, que incluye radio, infrarrojo, ultravioleta, rayos X y gamma.",
        'Que tipo de radiacion tiene mas energia?':
            "Los rayos gamma, en el extremo mas energetico del espectro.",
        'Al analizar el espectro de la luz de una estrella podemos saber...':
            "De que esta hecha y su temperatura, entre otras cosas.",
        'Que instrumento separa la luz en sus colores o longitudes de onda?':
            "Un espectroscopio, base de la espectroscopia astronomica.",
        'La luz roja tiene mayor longitud de onda que la luz azul.':
            "Verdadero. El rojo es la luz visible de mayor longitud de onda; el azul, de menor.",
    },
    'nociones-de-relatividad': {
        'Que unio Einstein en un solo concepto?':
            "El espacio y el tiempo, en un unico tejido: el espacio-tiempo.",
        'Donde pasa el tiempo un poco mas lento?':
            "Donde la gravedad es mas fuerte; tambien va mas lento cuanto mas rapido te mueves.",
        'Algo con masa puede viajar mas rapido que la luz.':
            "Falso. La velocidad de la luz es el limite del universo; nada con masa la alcanza.",
        'Por que el GPS necesita la relatividad?':
            "Porque el tiempo pasa distinto en los satelites; sin corregirlo, el GPS fallaria por kilometros.",
        'Cual es el limite de velocidad del universo?':
            "La velocidad de la luz, unos 300.000 km por segundo.",
        'Segun la relatividad, nada puede viajar mas rapido que...':
            "La luz, el limite de velocidad del universo.",
        'Que expresa la ecuacion E=mc2?':
            "Que la energia y la masa son equivalentes: una puede convertirse en la otra.",
        'Cerca de un objeto muy masivo, el tiempo...':
            "Pasa mas lento, un efecto llamado dilatacion gravitatoria del tiempo.",
        'La relatividad general predice que la luz se curva al pasar cerca de...':
            "Un objeto muy masivo, cuya gravedad curva el espacio-tiempo por el que viaja la luz.",
        'La velocidad de la luz es la misma para todos los observadores.':
            "Verdadero. Es el postulado central de la relatividad: midas como midas, la luz va igual de rapido.",
    },
}


def forwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    for slug, mapping in EXPL.items():
        for text, exp in mapping.items():
            Question.objects.filter(lesson__slug=slug, text=text).update(explanation=exp)


def backwards(apps, schema_editor):
    Question = apps.get_model('astro', 'Question')
    texts = [t for m in EXPL.values() for t in m]
    Question.objects.filter(text__in=texts).update(explanation='')


class Migration(migrations.Migration):

    dependencies = [
        ('astro', '0038_questionreport'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

<div align="center">

# 🌌 AstroGuide

**Aprende astronomía como si fuera un juego.**
Una app estilo Duolingo para *entender el universo, no solo memorizarlo.*

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Tests](https://img.shields.io/badge/tests-70%20passing-3ddc84)
![PWA](https://img.shields.io/badge/PWA-installable-b18bff)
![Status](https://img.shields.io/badge/status-en%20desarrollo-ffce4d)

</div>

---

## ✨ Qué es

**AstroGuide** es una aplicación web educativa que enseña astronomía y astrofísica con **tarjetas y quizzes gamificados**, siguiendo una progresión pedagógica del cielo a simple vista hasta la cosmología. En vez de acumular datos sueltos, cada respuesta incorrecta se convierte en aprendizaje: explicaciones, repaso espaciado y práctica dirigida a tus puntos flojos.

Construida con **Django** (server-rendered) + **JavaScript vanilla**, con diseño *glassmorphism* azul/morado sobre un fondo espacial e iconos SVG propios.

> **Contenido actual:** 10 unidades · 44 lecciones · 284 preguntas, organizadas en niveles del 0 (curiosidad por el cielo) al 8 (cosmología).

---

## 📸 Capturas

> _Añade tus capturas en `docs/screenshots/` y descomenta las líneas de abajo._

<!--
| Ruta de aprendizaje | Quiz con explicación | Estadísticas |
|---|---|---|
| ![ruta](docs/screenshots/ruta.png) | ![quiz](docs/screenshots/quiz.png) | ![stats](docs/screenshots/stats.png) |

| Ligas con divisiones | Perfil / social | PWA en móvil |
|---|---|---|
| ![ligas](docs/screenshots/ligas.png) | ![perfil](docs/screenshots/perfil.png) | ![movil](docs/screenshots/movil.png) |
-->

---

## 🚀 Características

### 🎓 Aprendizaje
- **Ruta por niveles** con desbloqueo secuencial (roadmap 0 → 8).
- **Tarjetas** (flip) + **quizzes** de 3 tipos: opción múltiple, verdadero/falso y escribir la respuesta (comparación sin acentos).
- **Explicaciones en cada pregunta** — el *porqué* de la respuesta.
- **Dificultad progresiva**: el umbral de aprobado y el nº de preguntas escalan por nivel (60 % → 90 %).
- **Repaso inteligente (repetición espaciada, algoritmo SM-2)** y **práctica de temas flojos**.
- **Examen final por unidad** + **certificado** (con sello "con honores").
- **Explorar / glosario** con buscador sobre todo el contenido.

### 🎮 Gamificación
- **XP**, **racha** con congeladores, moneda **Cosmos** + tienda y cosméticos.
- **Vidas/corazones**, **meta diaria configurable**, **logros** y **rangos**.
- **Misiones semanales**, **cofres por hitos de racha**.
- **Ligas con divisiones** (Cometa → Cosmos) y **ascenso/descenso** semanal.

### 👥 Social
- **Seguir usuarios** y **perfiles públicos**.
- **Certificados verificables** por enlace público, compartibles.
- **Duelos 1v1** asíncronos (mismo set de preguntas, gana quien más acierte).

### 📊 Progreso y calidad
- **Estadísticas personales** con gráficas (precisión por unidad, actividad, temas flojos).
- **Centro de notificaciones** + toasts.
- **Reportar preguntas** + panel de calidad (preguntas más falladas).

### 📱 Plataforma
- **PWA instalable + offline** (manifest + service worker).
- **Tema claro/oscuro**, **audio** (lectura de tarjetas con Web Speech API).
- **Responsive** para móvil. Imagen astronómica del día vía **API de la NASA**.

### 🛠️ Panel de gestión propio (`/gestion/`)
CRUD de unidades, lecciones, tarjetas, quizzes, tienda y logros; estadísticas, calidad y anuncios — sin depender del admin de Django.

---

## 🧰 Stack

| Capa | Tecnología |
|---|---|
| Backend | Django 5.2 · Python 3.14 |
| Base de datos | SQLite (desarrollo) |
| Frontend | Templates de Django + JavaScript vanilla (sin build step) |
| Estilos | CSS con custom properties · iconos SVG propios |
| PWA | Service worker + Web App Manifest |
| Imágenes | Pillow |
| APIs / navegador | NASA APOD · Web Speech API · Web Share API |
| Tests | Django test framework (70 tests) |

---

## 💡 Decisiones técnicas destacadas

- **Repetición espaciada (SM-2):** cada pregunta se reprograma según aciertes o falles, priorizando lo que estás a punto de olvidar — memoria a largo plazo real, no repetición ciega.
- **Calificación en el servidor:** el cliente nunca decide si aciertas; toda la corrección y las recompensas se validan en el backend (anti-trampa).
- **Contenido como migraciones de datos idempotentes:** el contenido es reproducible en cualquier entorno con `migrate`, versionado junto al código.
- **Ligas con cierre semanal como *management command*** (`leagues_rollover`), pensado para ejecutarse por cron en producción.
- **Sin *build step*:** JavaScript vanilla + render en servidor. Decisión pragmática que prioriza velocidad de desarrollo y simplicidad de despliegue.
- **Seguridad:** `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` por variables de entorno; *cache-busting* de assets por versión.

---

## 🗂️ Estructura

```
apps/astro/
├── models.py            # dominio: Category, Lesson, Card, Question, Profile,
│                        #   ReviewItem (SRS), Duel, Follow, UnitExam, ...
├── views.py             # rutas de la app (quiz, repaso, examen, ligas, social...)
├── panel_views.py       # panel de gestión propio (/gestion/)
├── management/commands/
│   └── leagues_rollover.py   # cierre semanal de ligas (cron)
├── migrations/          # esquema + contenido sembrado (idempotente)
└── tests.py             # 70 tests
templates/astro/         # HTML (base, ruta, quiz, panel, PWA sw.js...)
static/astro/            # CSS, JS vanilla, iconos e imágenes
```

---

## ⚙️ Puesta en marcha (local)

```bash
git clone https://github.com/Franciscooxz/AstroGuidee.git
cd AstroGuidee

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # opcional, para el panel /gestion/
python manage.py runserver
```

Abre **http://localhost:8000**. En desarrollo funciona con valores por defecto; para producción define `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` y `DJANGO_ALLOWED_HOSTS`.

### 🧪 Tests

```bash
python manage.py test apps.astro
```

---

## 🗺️ Contenido por niveles

| Nivel | Unidad |
|:---:|---|
| 0 | Bienvenido al universo |
| 1 | El cielo a simple vista |
| 2 | Observación |
| 3 | Sistema Solar · Exoplanetas |
| 4 | Las estrellas |
| 5 | Galaxias y el cosmos |
| 7 | Objetos extremos (agujeros negros, neutrones, relatividad) |
| 8 | Cosmología |

---

## 📌 Estado y próximos pasos

🚧 **En desarrollo activo.** Próximo: despliegue con enlace público, CI (GitHub Actions), y andamiaje de plan **Premium** (freemium).

---

## 👤 Autor

**Francisco** — [@Franciscooxz](https://github.com/Franciscooxz)

> Proyecto personal de aprendizaje y portfolio. Si quieres definir una licencia, añade un archivo `LICENSE` (por ejemplo, MIT).

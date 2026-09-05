# Artistic Mold — Sitio Web Oficial

Sitio web de **Artistic Mold**, Familia Artístico-Deportiva y Dispositivo de Base Comunitaria (DBC) de Bogotá, Colombia (Convenio 552 del 2023). Fundada en abril de 2020, usa el arte y el deporte como herramientas de reconexión, prevención y recuperación integral.

El proyecto es una aplicación **Django** completa: sitio público (frontend) + panel de administración propio (backoffice) + admin de Django.

---

## Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.14 |
| Framework | Django 5.2.4 |
| Base de datos | SQLite (`db.sqlite3`) |
| Imágenes | Pillow |
| CSS/UI | Bootstrap 5.3 (CDN) + CSS propio (`static/site/css/style.css`) |
| Iconos | Font Awesome 6.4 (CDN) |
| Tipografía | Poppins (Google Fonts) |
| Editor de texto enriquecido | TinyMCE 7 (CDN, licencia GPL) — solo en el panel |

> Nota: Bootstrap, Font Awesome, Google Fonts y TinyMCE se cargan desde CDN, por lo que el panel y el sitio necesitan conexión a internet para verse completos.

## Instalación y Puesta en Marcha

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Aplicar migraciones
python manage.py migrate

# 3. Crear usuario administrador (si no existe)
python manage.py createsuperuser

# 4. (Opcional) Cargar datos iniciales del sitio
python load_real_data.py

# 5. Iniciar el servidor de desarrollo
python manage.py runserver
```

El sitio queda en `http://localhost:8000/` y el panel en `http://localhost:8000/panel/`.

---

## Estructura del Proyecto

```
E:\Artistic
├── manage.py
├── requirements.txt
├── db.sqlite3               # Base de datos SQLite
├── load_initial_data.py     # Script de datos de ejemplo
├── load_real_data.py        # Script de datos reales del sitio
│
├── artisticmold/            # Configuración del proyecto
│   ├── settings.py          # Configuración general (apps, BD, email, media)
│   ├── urls.py              # Rutas raíz + robots.txt + manejadores 404/500
│   ├── wsgi.py / asgi.py
│
├── apps/                    # Aplicaciones Django (una por dominio)
│   ├── core/                # Config del sitio, home, nosotros, contacto, política, fundadores, PANEL
│   ├── slider/              # Slides del carrusel del home
│   ├── blog/                # Posts y categorías del blog
│   ├── disciplines/         # Artes & Disciplinas y sus categorías
│   ├── faq/                 # Preguntas frecuentes
│   ├── testimonials/        # Testimonios
│   ├── gallery/             # Álbumes y fotos (fototeca)
│   ├── services/            # Servicios (con detalle) y PDF de catálogo
│   └── resources/           # Centro de recursos y sus categorías
│
├── templates/               # HTML (Django Templates)
│   ├── base.html            # Layout del sitio público (navbar, footer, favicon)
│   ├── home/ nosotros/ contacto/ politica/
│   ├── artes/ blog/ galeria/ servicios/ recursos/
│   ├── 404.html / 500.html
│   └── panel/               # Backoffice completo (base propia + una carpeta por módulo)
│
├── static/site/             # Archivos estáticos propios
│   ├── css/style.css        # Todos los estilos del sitio público
│   ├── js/main.js
│   └── img/
│
└── media/                   # Archivos subidos por el panel (imágenes, PDFs)
```

---

## Backend

### Apps y Modelos

**`apps/core`** — el corazón del sitio:
- `SiteConfig` (singleton): nombre del sitio, tagline, logo, **favicon**, teléfono, WhatsApp, email, redes sociales, dirección, convenio.
- `HomeSection` (singleton): sección "Quiénes Somos" del home con estadísticas (cofundadores, integrantes, disciplinas).
- `AboutPage` (singleton): contenido de la página Nosotros (historia, misión, visión, preceptos, símbolos, frase emblema).
- `Founder`: fundadores (nombre, rol, foto, biografía enriquecida, orden, activo). Se muestran en Nosotros.
- `PolicyPage` (singleton): política de privacidad con interruptor `is_active` (si está apagado, `/politica/` devuelve 404).

> Los "singleton" fuerzan `pk=1` en `save()`: solo existe un registro, se edita siempre el mismo.

**`apps/slider`** — `Slide`: imagen, título, subtítulo, link, orden, activo.

**`apps/blog`** — `BlogCategory` (nombre, slug, orden) y `Post` (título, slug único, categoría, portada, extracto, contenido enriquecido, autor, publicado/destacado, fechas).

**`apps/disciplines`** — `DisciplineCategory` (nombre, slug, icono FA, color, orden) y `Discipline` (nombre, slug único, descripción enriquecida, imagen, destacada en home, activa, orden). Tienen página de detalle por slug.

**`apps/faq`** — `FAQ`: pregunta, respuesta, orden, activa. Se muestran en acordeón en el home.

**`apps/testimonials`** — `Testimonial`: nombre, rol, cita, evento, foto, destacado, activo, orden. Los destacados+activos aparecen en el home (máx. 3).

**`apps/gallery`** — `Album` (título, año, portada, descripción) y `Photo` (imagen, pie, orden). Subida múltiple de fotos desde el panel.

**`apps/services`** — `Service`: título, **slug único** (URL de detalle), descripción enriquecida, icono FA, imagen, orden, activo. `ServicePDF`: catálogo descargable. Cada servicio tiene página de detalle con **formulario de contacto** integrado.

**`apps/resources`** — `ResourceCategory` (título, slug automático, intro, icono, orden) y `Resource` (título, contenido enriquecido, imagen, **archivo PDF descargable opcional**, orden, activo).

### Rutas Públicas

| URL | Contenido |
|---|---|
| `/` | Home: slider, quiénes somos, disciplinas destacadas, FAQ, testimonios, blog reciente, CTA |
| `/nosotros/` | Historia, misión/visión, preceptos, símbolos y fundadores |
| `/artes/` y `/artes/<slug>/` | Listado (con filtro por categoría `?cat=`) y detalle de disciplinas |
| `/servicios/` y `/servicios/<slug>/` | Listado y detalle de servicios (detalle con formulario de contacto) |
| `/blog/` y `/blog/<slug>/` | Listado y detalle de posts |
| `/galeria/` y `/galeria/<id>/` | Álbumes y fotos |
| `/recursos/` | Centro de recursos por categorías (con PDFs descargables) |
| `/contacto/` | Información de contacto + formulario |
| `/politica/` | Política de privacidad (solo si está activada) |
| `/sitemap.xml` y `/robots.txt` | SEO (sitemap incluye posts, disciplinas, servicios y álbumes) |

### Formulario de Contacto y Correo

- Los formularios de `/contacto/` y del detalle de cada servicio envían POST a la vista `contacto()` en `apps/core/views.py`, que arma y envía el correo a `CONTACT_EMAIL`.
- **Estado actual**: `EMAIL_BACKEND` es el de **consola** — los correos se imprimen en la terminal del servidor, **no se envían de verdad**. Para producción hay que configurar SMTP (ver "Pendientes para producción").

### Panel de Administración (`/panel/`)

Backoffice propio (no confundir con el admin de Django) con login exclusivo para usuarios *staff*. Módulos:

- **Dashboard**: contadores generales y últimos posts.
- **Configuración** (3 pestañas): Sitio General (datos de contacto, logo, favicon), Home (sección principal y estadísticas) y Nosotros.
- **Inicio / Slider**: CRUD de slides.
- **Artes & Disciplinas** + **Categorías**: CRUD completo con slug automático.
- **Servicios**: CRUD (el slug del detalle se genera automáticamente del título).
- **Recursos** + categorías: CRUD con editor enriquecido y subida de PDF.
- **Galería / Fototeca**: álbumes con subida múltiple de fotos.
- **Blog** + **Categorías**: CRUD de posts (extracto, portada, publicar/destacar).
- **Fundadores**: CRUD con foto y biografía enriquecida.
- **Testimonios**, **FAQ**, **Política de Privacidad**.

Detalles técnicos del panel:
- Los campos de texto largo usan **TinyMCE** (clase `textarea.rich-editor`, inicializado en `templates/panel/base.html`) con subida de imágenes vía `/panel/upload/` y botón propio para insertar videos de YouTube.
- Las vistas están en `apps/core/panel_views.py` y las rutas en `apps/core/panel_urls.py` (namespace `panel:`). No usan Django Forms: leen `request.POST`/`request.FILES` directamente.
- Utilidades: `_unique_slug()` (slugs sin colisiones) y `_int()` (conversión segura de números).

### Admin de Django (`/django-admin/`)

Disponible como respaldo con todos los modelos registrados. El día a día se maneja desde `/panel/`.

---

## Frontend

### Sistema de diseño

Definido en `static/site/css/style.css` con variables CSS:

```css
--black: #0d0d0d    /* fondo principal */
--black3: #1c1c1c   /* tarjetas */
--yellow: #F5C518   /* color de marca */
--grey: #8a8a8a     /* texto secundario */
--radius: 12px
```

Estética: **fondo negro + acentos amarillos**, tipografía Poppins, tarjetas con hover elevado, secciones con etiqueta (`section-label`) y títulos con palabra resaltada en amarillo.

### Templates

- `templates/base.html`: layout público — navbar fija, mensajes flash, footer con datos de `SiteConfig` (disponible en todos los templates gracias al context processor `apps/core/context_processors.py`), favicon dinámico.
- Cada sección tiene su carpeta (`home/`, `artes/`, `blog/`…) con `index.html`/`list.html` y `detail.html` cuando aplica.
- Los contenidos creados con el editor enriquecido se renderizan con `|safe` dentro de `.rich-content`; en tarjetas/resúmenes se usa `|striptags|truncatewords:N` para mostrar texto plano recortado.
- `templates/panel/base.html`: layout del backoffice (sidebar oscura, tablas, formularios, alertas) con bloque `extra_css` para estilos por página.

### Contenido dinámico del Home (orden de secciones)

1. Slider (slides activos)
2. Quiénes Somos (`HomeSection` + estadísticas)
3. Disciplinas destacadas (máx. 6, `is_featured=True`)
4. Preguntas Frecuentes (acordeón)
5. Testimonios (máx. 3 destacados)
6. Últimas publicaciones del blog (máx. 3 publicadas)
7. CTA final de contacto

---

## Archivos Subidos (`media/`)

| Carpeta | Contenido |
|---|---|
| `site/` | Logo y favicon |
| `slider/`, `home/`, `nosotros/` | Imágenes de secciones |
| `disciplines/`, `services/`, `blog/`, `resources/` | Imágenes de contenido |
| `services/pdf/`, `resources/pdf/` | PDFs descargables |
| `gallery/covers/`, `gallery/photos/` | Fototeca |
| `founders/` | Fotos de fundadores |
| `editor/` | Imágenes subidas desde el editor enriquecido |

En desarrollo los sirve Django (`DEBUG=True`); en producción deben servirse por el servidor web (Nginx/Apache) o un storage externo.

---

## Pendientes para Producción

Antes de publicar el sitio en internet hay que:

1. **Correo real**: cambiar `EMAIL_BACKEND` a SMTP en `settings.py` (Gmail requiere una *contraseña de aplicación*). Hoy los mensajes del formulario solo se imprimen en consola.
2. **`DEBUG = False`** y configurar `ALLOWED_HOSTS` con el dominio real.
3. **`SECRET_KEY`**: mover a variable de entorno (actualmente está escrita en el código).
4. **Estáticos**: ejecutar `python manage.py collectstatic` y servir `static/` y `media/` desde el servidor web.
5. Considerar migrar de SQLite a PostgreSQL si crece el tráfico.
6. Activar la **Política de Privacidad** desde el panel cuando el texto esté listo.

"""Aplica tildes a las tarjetas.

La migracion 0053 corrigio Lesson, Question y Option, pero en Card buscaba
los campos front/back, que ya no existen. El texto visible esta en title,
subtitle, summary, fun_fact y content.
"""

import importlib
import re

from django.db import migrations

_DE_DONDE = re.compile(r"^(De) donde\b")
_EXTRA = {
    "numeros": "números",
    "pequenas": "pequeñas",
    "lineas": "líneas",
    "tamanos": "tamaños",
}
_EXTRA_WORD = re.compile(r"\b(" + "|".join(_EXTRA) + r")\b", re.I)
_FIELDS = ["title", "subtitle", "summary", "fun_fact", "content"]


def _case(orig, repl):
    if orig.isupper():
        return repl.upper()
    if orig[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl


def _extra(text):
    return _EXTRA_WORD.sub(lambda m: _case(m.group(0), _EXTRA[m.group(0).lower()]), text)


def apply_card_accents(apps, schema_editor):
    fix = importlib.import_module("apps.astro.migrations.0053_fix_accents").fix
    Card = apps.get_model("astro", "Card")
    for obj in Card.objects.all().iterator():
        changed = []
        for name in _FIELDS:
            value = getattr(obj, name) or ""
            updated = _extra(fix(value))
            if name in ("title", "subtitle"):
                updated = _DE_DONDE.sub(r"\1 dónde", updated)
            if updated != value:
                setattr(obj, name, updated)
                changed.append(name)
        if changed:
            obj.save(update_fields=changed)

    Question = apps.get_model("astro", "Question")
    for obj in Question.objects.all().iterator():
        changed = []
        for name in ("text", "explanation"):
            value = getattr(obj, name) or ""
            updated = _DE_DONDE.sub(r"\1 dónde", _extra(fix(value)))
            if updated != value:
                setattr(obj, name, updated)
                changed.append(name)
        if changed:
            obj.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [("astro", "0053_fix_accents")]
    operations = [migrations.RunPython(apply_card_accents, migrations.RunPython.noop)]

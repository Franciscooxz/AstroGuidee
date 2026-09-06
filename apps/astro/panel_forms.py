from django import forms
from django.forms import inlineformset_factory
from .models import Category, Lesson, Card, Question, Option, ShopItem, Achievement

ICON_CHOICES = [
    ('', '— sin icono —'),
    ('sun', 'Sol'), ('mercury', 'Mercurio'), ('venus', 'Venus'), ('earth', 'Tierra'),
    ('mars', 'Marte'), ('jupiter', 'Jupiter'), ('saturn', 'Saturno'), ('uranus', 'Urano'),
    ('neptune', 'Neptuno'), ('orbit', 'Orbita'), ('star', 'Estrella'), ('galaxy', 'Galaxia'),
    ('blackhole', 'Agujero negro'), ('atom', 'Atomo'), ('planet', 'Planeta'),
    ('cards', 'Tarjetas'), ('quiz', 'Quiz'), ('progress', 'Progreso'), ('rocket', 'Cohete'),
    ('coin', 'Moneda'), ('flame', 'Llama'),
]


class StyledForm(forms.ModelForm):
    """Aplica la clase .field a todos los widgets del panel."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            css = w.attrs.get('class', '')
            if isinstance(w, forms.CheckboxInput):
                w.attrs['class'] = (css + ' check').strip()
            else:
                w.attrs['class'] = (css + ' field').strip()
            if isinstance(w, forms.Textarea):
                w.attrs.setdefault('rows', 4)


class UnitForm(StyledForm):
    class Meta:
        model = Category
        fields = ['name', 'subtitle', 'description', 'icon', 'accent', 'order', 'difficulty', 'is_active']
        widgets = {'icon': forms.Select(choices=ICON_CHOICES)}


class LessonForm(StyledForm):
    class Meta:
        model = Lesson
        fields = ['category', 'title', 'subtitle', 'icon', 'order', 'is_active']
        widgets = {'icon': forms.Select(choices=ICON_CHOICES)}


class CardForm(StyledForm):
    class Meta:
        model = Card
        fields = ['lesson', 'title', 'subtitle', 'summary', 'content', 'fun_fact',
                  'icon', 'image', 'image_credit', 'order', 'is_active']
        widgets = {'icon': forms.Select(choices=ICON_CHOICES)}


class QuestionForm(StyledForm):
    class Meta:
        model = Question
        fields = ['lesson', 'text', 'qtype', 'explanation', 'image', 'order', 'is_active']


class OptionForm(StyledForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct', 'order']


OptionFormSet = inlineformset_factory(
    Question, Option, form=OptionForm,
    extra=4, can_delete=True, min_num=2, validate_min=True,
)


class ShopItemForm(StyledForm):
    class Meta:
        model = ShopItem
        fields = ['name', 'key', 'description', 'icon', 'price', 'effect', 'order', 'is_active']
        widgets = {'icon': forms.Select(choices=ICON_CHOICES)}


class AchievementForm(StyledForm):
    class Meta:
        model = Achievement
        fields = ['name', 'key', 'description', 'icon', 'condition_type', 'threshold',
                  'order', 'is_active']
        widgets = {'icon': forms.Select(choices=ICON_CHOICES)}

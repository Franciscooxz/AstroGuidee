import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (Achievement, Card, Category, Lesson, LessonProgress,
                     Option, Profile, Question, ShopItem, UserAchievement)


class AstroBaseTest(TestCase):
    def setUp(self):
        # Aislar: desactivar el contenido sembrado por migraciones para tener
        # una ruta deterministica solo con la unidad de prueba.
        self.user = User.objects.create_user('tester', password='Cosmos2026xyz')
        self.cat = Category.objects.create(name='Unidad Test', slug='unidad-test',
                                           order=1, accent='#8b5cff', is_active=True)
        Category.objects.exclude(pk=self.cat.pk).update(is_active=False)

        self.l1 = Lesson.objects.create(category=self.cat, title='Leccion 1', slug='l1', order=1)
        self.l2 = Lesson.objects.create(category=self.cat, title='Leccion 2', slug='l2', order=2)
        Card.objects.create(lesson=self.l1, category=self.cat, title='Carta A',
                            summary='Resumen A', order=1)

        # Quiz de l1: una de opcion y una de texto
        self.q1 = Question.objects.create(lesson=self.l1, text='Pregunta?', qtype='single', order=1)
        self.o_ok = Option.objects.create(question=self.q1, text='Correcta', is_correct=True, order=1)
        Option.objects.create(question=self.q1, text='Incorrecta', is_correct=False, order=2)
        self.q2 = Question.objects.create(lesson=self.l1, text='Escribe Sol', qtype='text', order=2)
        Option.objects.create(question=self.q2, text='Sol', is_correct=True, order=1)

    def login(self):
        self.assertTrue(self.client.login(username='tester', password='Cosmos2026xyz'))

    def complete_l1(self, text_answer='sol'):
        answers = {str(self.q1.id): self.o_ok.id, str(self.q2.id): text_answer}
        return self.client.post(
            reverse('astro:finish_quiz', args=[self.l1.slug]),
            data=json.dumps({'answers': answers}), content_type='application/json')


class AuthTests(AstroBaseTest):
    def test_home_public(self):
        self.assertEqual(self.client.get(reverse('astro:home')).status_code, 200)

    def test_register_creates_and_logs_in(self):
        resp = self.client.post(reverse('astro:register'), {
            'username': 'newbie', 'email': 'a@b.com',
            'password1': 'Cosmos2026xyz', 'password2': 'Cosmos2026xyz',
        })
        self.assertTrue(User.objects.filter(username='newbie').exists())
        self.assertEqual(resp.status_code, 302)

    def test_ruta_requires_login(self):
        resp = self.client.get(reverse('astro:ruta'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/entrar/', resp.url)


class LessonUnlockTests(AstroBaseTest):
    def test_first_unlocked_second_locked(self):
        self.login()
        self.assertEqual(self.client.get(reverse('astro:lesson', args=['l1'])).status_code, 200)
        # l2 bloqueada -> redirige a la ruta
        self.assertEqual(self.client.get(reverse('astro:lesson', args=['l2'])).status_code, 302)

    def test_completing_unlocks_next(self):
        self.login()
        self.complete_l1()
        self.assertTrue(LessonProgress.objects.filter(
            user=self.user, lesson=self.l1, completed=True).exists())
        self.assertEqual(self.client.get(reverse('astro:lesson', args=['l2'])).status_code, 200)


class QuizTests(AstroBaseTest):
    def test_perfect_awards_xp_and_completes(self):
        self.login()
        data = self.complete_l1(text_answer='sol').json()
        self.assertEqual(data['correct'], 2)
        self.assertTrue(data['passed'])
        self.assertGreater(data['xp_earned'], 0)
        self.assertGreater(Profile.objects.get(user=self.user).xp, 0)

    def test_text_answer_ignores_accents_and_case(self):
        self.login()
        data = self.complete_l1(text_answer='SÓL').json()  # con acento y mayusculas
        self.assertEqual(data['correct'], 2)

    def test_text_answer_wrong(self):
        self.login()
        data = self.complete_l1(text_answer='luna').json()
        self.assertEqual(data['correct'], 1)


class StoreTests(AstroBaseTest):
    def setUp(self):
        super().setUp()
        self.item = ShopItem.objects.create(key='freeze-test', name='Congelar',
                                            effect='streak_freeze', price=30)

    def test_buy_deducts_and_applies(self):
        self.login()
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.coins = 50
        p.save()
        self.client.post(reverse('astro:buy_item', args=['freeze-test']))
        p.refresh_from_db()
        self.assertEqual(p.coins, 20)
        self.assertEqual(p.streak_freezes, 1)

    def test_buy_blocked_without_coins(self):
        self.login()
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.coins = 5
        p.save()
        self.client.post(reverse('astro:buy_item', args=['freeze-test']))
        p.refresh_from_db()
        self.assertEqual(p.coins, 5)
        self.assertEqual(p.streak_freezes, 0)


class AchievementTests(AstroBaseTest):
    def test_achievement_awarded_on_completion(self):
        ach = Achievement.objects.create(key='primer-test', name='Primero',
                                         condition_type='lessons_completed', threshold=1)
        self.login()
        self.complete_l1()
        self.assertTrue(UserAchievement.objects.filter(user=self.user, achievement=ach).exists())


class LeagueAndProfileTests(AstroBaseTest):
    def test_weekly_xp_and_league(self):
        self.login()
        self.complete_l1()
        self.assertGreater(Profile.objects.get(user=self.user).weekly_xp, 0)
        resp = self.client.get(reverse('astro:league'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'tester')

    def test_settings_updates_profile(self):
        self.login()
        self.client.post(reverse('astro:settings'),
                         {'save_profile': '1', 'email': 'new@x.com', 'avatar': 'saturn'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@x.com')
        self.assertEqual(Profile.objects.get(user=self.user).avatar, 'saturn')

    def test_settings_rejects_invalid_avatar(self):
        self.login()
        self.client.post(reverse('astro:settings'),
                         {'save_profile': '1', 'email': 'new@x.com', 'avatar': 'malicioso'})
        self.assertEqual(Profile.objects.get(user=self.user).avatar, '')


class PanelTests(AstroBaseTest):
    def test_panel_requires_staff(self):
        self.login()  # usuario normal
        self.assertEqual(self.client.get('/gestion/').status_code, 302)

    def test_panel_ok_for_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.login()
        self.assertEqual(self.client.get('/gestion/').status_code, 200)
        self.assertEqual(self.client.get('/gestion/estadisticas/').status_code, 200)

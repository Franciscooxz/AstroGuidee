import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (Achievement, Card, Category, Lesson, LessonProgress,
                     Notification, Option, Profile, Question, ReviewItem,
                     ShopItem, UserAchievement)


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


class NotificationTests(AstroBaseTest):
    def test_achievement_creates_notification(self):
        Achievement.objects.create(key='n-test', name='Primero',
                                   condition_type='lessons_completed', threshold=1)
        self.login()
        self.complete_l1()
        self.assertTrue(Notification.objects.filter(
            user=self.user, text__icontains='Logro desbloqueado').exists())

    def test_center_lists_and_marks_read(self):
        self.login()
        Notification.push(self.user, 'Hola cosmos', icon='star')
        self.assertEqual(Notification.objects.filter(user=self.user, is_read=False).count(), 1)
        resp = self.client.get(reverse('astro:notifications'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hola cosmos')
        # abrir el centro marca todo como leido
        self.assertEqual(Notification.objects.filter(user=self.user, is_read=False).count(), 0)

    def test_clear_deletes_history(self):
        self.login()
        Notification.push(self.user, 'A')
        Notification.push(self.user, 'B')
        self.client.post(reverse('astro:clear_notifications'))
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 0)


class DifficultyTests(AstroBaseTest):
    def _add_singles(self, n):
        """Agrega n preguntas single (1 correcta) a l1 y devuelve el mapa de respuestas correctas."""
        answers = {str(self.q1.id): self.o_ok.id, str(self.q2.id): 'sol'}
        for i in range(n):
            q = Question.objects.create(lesson=self.l1, text=f'Extra {i}?', qtype='single', order=10 + i)
            ok = Option.objects.create(question=q, text='Si', is_correct=True, order=1)
            Option.objects.create(question=q, text='No', is_correct=False, order=2)
            answers[str(q.id)] = ok.id
        return answers

    def test_high_difficulty_requires_more(self):
        # l1 con 5 preguntas y unidad nivel 5 -> aprobar exige 5/5 (ceil(0.9*5))
        self.cat.difficulty = 5
        self.cat.save()
        answers = self._add_singles(3)  # ahora 5 preguntas en total
        self.login()
        # Fallar 1 (respuesta de texto mal) -> 4/5, no aprueba en nivel 5
        wrong = dict(answers); wrong[str(self.q2.id)] = 'mal'
        data = self.client.post(reverse('astro:finish_quiz', args=[self.l1.slug]),
                                data=json.dumps({'answers': wrong}),
                                content_type='application/json').json()
        self.assertEqual(data['correct'], 4)
        self.assertEqual(data['needed'], 5)
        self.assertFalse(data['passed'])
        self.assertFalse(LessonProgress.objects.filter(
            user=self.user, lesson=self.l1, completed=True).exists())

    def test_low_difficulty_passes_with_60(self):
        # nivel 1 (default) con 5 preguntas -> basta 3/5
        self.cat.difficulty = 1
        self.cat.save()
        answers = self._add_singles(3)
        self.login()
        wrong = dict(answers)
        wrong[str(self.q2.id)] = 'mal'
        wrong[str(self.q1.id)] = 0  # 2 fallos -> 3/5
        data = self.client.post(reverse('astro:finish_quiz', args=[self.l1.slug]),
                                data=json.dumps({'answers': wrong}),
                                content_type='application/json').json()
        self.assertEqual(data['correct'], 3)
        self.assertEqual(data['needed'], 3)
        self.assertTrue(data['passed'])


class ReviewTests(AstroBaseTest):
    def test_completion_seeds_reviews(self):
        self.login()
        self.complete_l1()
        # l1 tiene 2 preguntas -> se crean 2 items de repaso, vencen manana
        items = ReviewItem.objects.filter(user=self.user)
        self.assertEqual(items.count(), 2)
        tomorrow = timezone.localdate() + timedelta(days=1)
        self.assertTrue(all(it.due == tomorrow for it in items))

    def test_review_page_shows_due(self):
        self.login()
        self.complete_l1()
        # forzar vencimiento a hoy
        ReviewItem.objects.filter(user=self.user).update(due=timezone.localdate())
        resp = self.client.get(reverse('astro:review'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'quizStage')

    def test_correct_review_pushes_due_and_awards_xp(self):
        self.login()
        self.complete_l1()
        ReviewItem.objects.filter(user=self.user).update(due=timezone.localdate())
        xp_before = Profile.objects.get(user=self.user).xp
        answers = {str(self.q1.id): self.o_ok.id, str(self.q2.id): 'sol'}
        data = self.client.post(
            reverse('astro:finish_review'),
            data=json.dumps({'answers': answers}), content_type='application/json').json()
        self.assertEqual(data['correct'], 2)
        self.assertGreater(data['xp_earned'], 0)
        self.assertGreater(Profile.objects.get(user=self.user).xp, xp_before)
        # acertadas: due pasa a futuro (>= hoy+1)
        for it in ReviewItem.objects.filter(user=self.user):
            self.assertGreater(it.due, timezone.localdate())
            self.assertEqual(it.reps, 1)

    def test_wrong_review_keeps_due_soon(self):
        self.login()
        self.complete_l1()
        ReviewItem.objects.filter(user=self.user).update(due=timezone.localdate(), reps=3, interval=20)
        answers = {str(self.q1.id): 'x', str(self.q2.id): 'mal'}
        self.client.post(reverse('astro:finish_review'),
                         data=json.dumps({'answers': answers}), content_type='application/json')
        for it in ReviewItem.objects.filter(user=self.user):
            self.assertEqual(it.reps, 0)
            self.assertEqual(it.interval, 1)
            self.assertEqual(it.lapses, 1)


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

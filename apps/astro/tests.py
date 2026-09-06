import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (Achievement, Card, Category, Lesson, LessonProgress,
                     Notification, Option, Profile, Question, QuestionReport,
                     QuestionStat, ReviewItem, ShopItem, UserAchievement)


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


class ExplanationTests(AstroBaseTest):
    def test_explanation_rendered_in_quiz(self):
        self.q1.explanation = 'Porque el Sol fusiona hidrogeno.'
        self.q1.save()
        self.login()
        resp = self.client.get(reverse('astro:quiz', args=[self.l1.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'q-explain')
        self.assertContains(resp, 'Porque el Sol fusiona hidrogeno.')

    def test_no_explanation_no_block(self):
        # q1 y q2 sin explicacion -> no aparece el bloque
        self.login()
        resp = self.client.get(reverse('astro:quiz', args=[self.l1.slug]))
        self.assertNotContains(resp, 'q-explain')


class ReportTests(AstroBaseTest):
    def test_report_creates_record(self):
        self.login()
        resp = self.client.post(reverse('astro:report_question', args=[self.q1.id]),
                                data=json.dumps({'reason': 'datos'}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        r = QuestionReport.objects.get(user=self.user, question=self.q1)
        self.assertEqual(r.reason, 'datos')
        self.assertFalse(r.resolved)

    def test_report_is_idempotent_per_user(self):
        self.login()
        for reason in ('confusa', 'opcion'):
            self.client.post(reverse('astro:report_question', args=[self.q1.id]),
                             data=json.dumps({'reason': reason}),
                             content_type='application/json')
        self.assertEqual(QuestionReport.objects.filter(
            user=self.user, question=self.q1).count(), 1)
        self.assertEqual(QuestionReport.objects.get(
            user=self.user, question=self.q1).reason, 'opcion')

    def test_invalid_reason_falls_back(self):
        self.login()
        self.client.post(reverse('astro:report_question', args=[self.q1.id]),
                         data=json.dumps({'reason': 'hackeo'}),
                         content_type='application/json')
        self.assertEqual(QuestionReport.objects.get(
            user=self.user, question=self.q1).reason, 'otro')

    def test_panel_shows_hardest_questions(self):
        # q1 muy fallada por varios usuarios -> aparece en "mas falladas"
        for i in range(6):
            u = User.objects.create_user(f'u{i}', password='Cosmos2026xyz')
            QuestionStat.objects.create(user=u, question=self.q1, seen=1, correct=0)
        self.user.is_staff = True
        self.user.save()
        self.login()
        resp = self.client.get(reverse('gestion:quality'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Preguntas mas falladas')
        self.assertContains(resp, self.q1.text)

    def test_panel_quality_and_resolve(self):
        QuestionReport.objects.create(user=self.user, question=self.q1, reason='datos')
        self.user.is_staff = True
        self.user.save()
        self.login()
        resp = self.client.get(reverse('gestion:quality'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.q1.text)
        self.client.post(reverse('gestion:resolve_reports', args=[self.q1.id]))
        self.assertTrue(QuestionReport.objects.get(question=self.q1).resolved)


class QuestionImageTests(AstroBaseTest):
    # PNG 1x1 valido (base64) para probar el ImageField sin ficheros externos.
    PNG = (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
           b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
           b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

    def test_quiz_renders_image(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        self.q1.image = SimpleUploadedFile('p.png', self.PNG, content_type='image/png')
        self.q1.save()
        self.login()
        resp = self.client.get(reverse('astro:quiz', args=[self.l1.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'q-image')

    def test_no_image_no_tag(self):
        self.login()
        resp = self.client.get(reverse('astro:quiz', args=[self.l1.slug]))
        self.assertNotContains(resp, 'q-image')


class UnitExamTests(AstroBaseTest):
    def _complete_unit(self):
        # completar l1 y l2 de la unidad de prueba
        LessonProgress.objects.update_or_create(
            user=self.user, lesson=self.l1, defaults={'completed': True})
        LessonProgress.objects.update_or_create(
            user=self.user, lesson=self.l2, defaults={'completed': True})

    def test_exam_locked_until_unit_complete(self):
        self.login()
        self.assertEqual(self.client.get(reverse('astro:exam', args=['unidad-test'])).status_code, 302)

    def test_exam_available_when_complete(self):
        self._complete_unit()
        self.login()
        resp = self.client.get(reverse('astro:exam', args=['unidad-test']))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Examen final')

    def test_pass_exam_records_and_rewards(self):
        from apps.astro.models import UnitExam
        self._complete_unit()
        self.login()
        coins0 = Profile.objects.get_or_create(user=self.user)[0].coins
        answers = {str(self.q1.id): self.o_ok.id, str(self.q2.id): 'sol'}  # 2/2 = 100%
        data = self.client.post(
            reverse('astro:finish_exam', args=['unidad-test']),
            data=json.dumps({'answers': answers}), content_type='application/json').json()
        self.assertTrue(data['passed'])
        self.assertTrue(data['honors'])
        self.assertEqual(data['pct'], 100)
        ex = UnitExam.objects.get(user=self.user, category=self.cat)
        self.assertTrue(ex.passed)
        self.assertEqual(ex.best_score, 100)
        self.assertEqual(Profile.objects.get(user=self.user).coins, coins0 + 50)

    def test_fail_exam_no_reward(self):
        from apps.astro.models import UnitExam
        self._complete_unit()
        self.login()
        answers = {str(self.q1.id): 0, str(self.q2.id): 'mal'}  # 0/2
        data = self.client.post(
            reverse('astro:finish_exam', args=['unidad-test']),
            data=json.dumps({'answers': answers}), content_type='application/json').json()
        self.assertFalse(data['passed'])
        self.assertFalse(UnitExam.objects.get(user=self.user, category=self.cat).passed)


class DailyGoalTests(AstroBaseTest):
    def test_change_daily_goal(self):
        self.login()
        self.client.post(reverse('astro:settings'), {'save_goal': '1', 'daily_goal': '3'})
        self.assertEqual(Profile.objects.get(user=self.user).daily_goal, 3)

    def test_invalid_goal_ignored(self):
        self.login()
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.daily_goal = 2
        p.save()
        self.client.post(reverse('astro:settings'), {'save_goal': '1', 'daily_goal': '99'})
        self.assertEqual(Profile.objects.get(user=self.user).daily_goal, 2)


class StreakChestTests(AstroBaseTest):
    def test_milestone_leaves_pending_chest(self):
        from apps.astro.views import _check_streak_chest
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.streak = 7
        _check_streak_chest(p)
        p.save()
        self.assertEqual(p.pending_chest, 7)
        self.assertEqual(p.streak_reward_max, 7)

    def test_open_chest_grants_reward(self):
        self.login()
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.pending_chest = 7
        p.streak_reward_max = 7
        coins0, freezes0 = p.coins, p.streak_freezes
        p.save()
        self.client.post(reverse('astro:open_chest'))
        p.refresh_from_db()
        self.assertEqual(p.coins, coins0 + 30)       # recompensa de 7 dias
        self.assertEqual(p.streak_freezes, freezes0 + 1)  # >=7 da congelador
        self.assertEqual(p.pending_chest, 0)

    def test_no_double_reward_same_milestone(self):
        from apps.astro.views import _check_streak_chest
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.streak = 5
        _check_streak_chest(p)  # hito 3 alcanzado
        p.pending_chest = 0     # simula que ya lo abrio
        _check_streak_chest(p)  # no debe volver a dar el hito 3
        self.assertEqual(p.pending_chest, 0)


class MissionTests(AstroBaseTest):
    def _set_week_xp(self, xp):
        from django.utils import timezone
        p = Profile.objects.get_or_create(user=self.user)[0]
        p.weekly_xp = xp
        p.week_key = timezone.localdate().strftime('%G-%V')
        p.save()

    def test_missions_page_ok(self):
        self.login()
        resp = self.client.get(reverse('astro:missions'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Coleccionista de XP')

    def test_claim_grants_reward_once(self):
        self.login()
        self._set_week_xp(200)  # cumple mision xp150 (reward 20)
        coins0 = Profile.objects.get(user=self.user).coins
        self.client.post(reverse('astro:claim_mission', args=['xp150']))
        self.assertEqual(Profile.objects.get(user=self.user).coins, coins0 + 20)
        # segundo intento no vuelve a pagar
        self.client.post(reverse('astro:claim_mission', args=['xp150']))
        self.assertEqual(Profile.objects.get(user=self.user).coins, coins0 + 20)

    def test_claim_blocked_if_not_done(self):
        self.login()
        self._set_week_xp(10)  # no cumple xp150
        coins0 = Profile.objects.get(user=self.user).coins
        self.client.post(reverse('astro:claim_mission', args=['xp150']))
        self.assertEqual(Profile.objects.get(user=self.user).coins, coins0)

    def test_perfect_quiz_counts_weekly(self):
        self.login()
        self.complete_l1()  # quiz perfecto (2/2)
        p = Profile.objects.get(user=self.user)
        self.assertEqual(p.week_perfect, 1)


class LeagueDivisionTests(AstroBaseTest):
    def test_league_shows_division(self):
        self.login()
        self.complete_l1()
        resp = self.client.get(reverse('astro:league'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Liga Cometa')  # division 0 por defecto

    def test_rollover_promotes_and_relegates(self):
        from django.core.management import call_command
        from django.utils import timezone
        wk = timezone.localdate().strftime('%G-%V')
        # 16 usuarios en division 1 (Luna) con XP distinta
        profs = []
        for i in range(16):
            u = User.objects.create_user(f'lg{i}', password='Cosmos2026xyz')
            p = Profile.objects.get_or_create(user=u)[0]
            p.division = 1
            p.weekly_xp = 100 - i  # lg0 el mejor, lg15 el peor
            p.week_key = wk
            p.save()
            profs.append(p)
        call_command('leagues_rollover')
        best = Profile.objects.get(user__username='lg0')
        worst = Profile.objects.get(user__username='lg15')
        middle = Profile.objects.get(user__username='lg8')
        self.assertEqual(best.division, 2)    # top 7 ascienden
        self.assertEqual(worst.division, 0)   # ultimos 7 bajan
        self.assertEqual(middle.division, 1)  # zona media se queda
        self.assertEqual(best.weekly_xp, 0)   # semana reiniciada


class WeakPracticeTests(AstroBaseTest):
    def test_weak_lists_missed_questions(self):
        self.login()
        self.complete_l1(text_answer='mal')  # q2 falla -> queda como floja
        resp = self.client.get(reverse('astro:review_weak'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'quizStage')
        self.assertContains(resp, 'Temas flojos')
        self.assertContains(resp, self.q2.text)   # la fallada aparece
        self.assertNotContains(resp, self.q1.text)  # la acertada no

    def test_weak_empty_when_all_correct(self):
        self.login()
        self.complete_l1()  # todo correcto
        resp = self.client.get(reverse('astro:review_weak'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Sin temas flojos')

    def test_finish_review_grades_and_schedules_submitted(self):
        self.login()
        self.complete_l1(text_answer='mal')
        # practicar la floja q2 y ahora acertarla
        data = self.client.post(reverse('astro:finish_review'),
                                data=json.dumps({'answers': {str(self.q2.id): 'sol'}}),
                                content_type='application/json').json()
        self.assertEqual(data['correct'], 1)
        self.assertEqual(data['total'], 1)
        st = QuestionStat.objects.get(user=self.user, question=self.q2)
        self.assertEqual((st.seen, st.correct), (2, 1))  # 1 del quiz + 1 del repaso
        self.assertTrue(ReviewItem.objects.filter(user=self.user, question=self.q2).exists())


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


class StatsTests(AstroBaseTest):
    def test_finish_quiz_records_question_stats(self):
        self.login()
        self.complete_l1()  # q1 correcta, q2 texto 'sol' correcta
        s1 = QuestionStat.objects.get(user=self.user, question=self.q1)
        self.assertEqual((s1.seen, s1.correct), (1, 1))
        s2 = QuestionStat.objects.get(user=self.user, question=self.q2)
        self.assertEqual((s2.seen, s2.correct), (1, 1))

    def test_wrong_answer_lowers_accuracy(self):
        self.login()
        self.complete_l1(text_answer='mal')  # q2 falla
        s2 = QuestionStat.objects.get(user=self.user, question=self.q2)
        self.assertEqual((s2.seen, s2.correct), (1, 0))
        self.assertEqual(s2.accuracy, 0)

    def test_stats_page_ok(self):
        self.login()
        self.complete_l1()
        resp = self.client.get(reverse('astro:stats'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Precision por unidad')

    def test_stats_empty_state(self):
        self.login()
        resp = self.client.get(reverse('astro:stats'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Aun no hay datos')


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

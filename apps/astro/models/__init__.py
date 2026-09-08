"""Modelos de AstroGuide, organizados por dominio.

Se re-exportan todos aqui para que `from apps.astro.models import X` siga
funcionando y Django registre los modelos.
"""

from .content import Card, Category, Lesson, Option, Question
from .gamification import (
    Achievement,
    MissionClaim,
    Notification,
    Profile,
    Purchase,
    ShopItem,
    UserAchievement,
)
from .progress import CardProgress, LessonProgress, QuestionStat, ReviewItem, UnitExam
from .social import Duel, Follow, QuestionReport

__all__ = [
    "Card",
    "Category",
    "Lesson",
    "Option",
    "Question",
    "Achievement",
    "MissionClaim",
    "Notification",
    "Profile",
    "Purchase",
    "ShopItem",
    "UserAchievement",
    "CardProgress",
    "LessonProgress",
    "QuestionStat",
    "ReviewItem",
    "UnitExam",
    "Duel",
    "Follow",
    "QuestionReport",
]

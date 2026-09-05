from django.contrib import admin
from .models import (Category, Lesson, Card, CardProgress, LessonProgress,
                     Question, Option, Profile, ShopItem, Achievement, UserAchievement)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['order', 'title', 'icon', 'is_active']
    ordering = ['order']
    prepopulated_fields = {'slug': ('title',)}


class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    fields = ['order', 'title', 'subtitle', 'icon', 'is_active']
    ordering = ['order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'lesson_count', 'card_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'card_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CardInline]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'category', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'lesson', 'is_active']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CardProgress)
class CardProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'card', 'known', 'updated_at']
    list_filter = ['known', 'card__category']
    search_fields = ['user__username', 'card__title']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed', 'lesson__category']
    search_fields = ['user__username', 'lesson__title']


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'lesson', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['lesson__category', 'lesson', 'is_active']
    search_fields = ['text']
    inlines = [OptionInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'xp', 'streak', 'best_streak', 'coins', 'last_active']
    search_fields = ['user__username']


@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'effect', 'price', 'order', 'is_active']
    list_editable = ['price', 'order', 'is_active']
    prepopulated_fields = {'key': ('name',)}


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'condition_type', 'threshold', 'order', 'is_active']
    list_editable = ['threshold', 'order', 'is_active']
    prepopulated_fields = {'key': ('name',)}


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['achievement']
    search_fields = ['user__username']

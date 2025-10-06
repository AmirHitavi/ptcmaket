from modeltranslation.translator import TranslationOptions, register

from .models import Blog, Category, History, Project


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ["title"]


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ["title", "description", "slug"]


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ["title", "description", "summary", "body", "slug"]


@register(History)
class HistoryTranslationOptions(TranslationOptions):
    fields = ["event"]

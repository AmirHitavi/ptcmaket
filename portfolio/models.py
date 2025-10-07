from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Category(BaseModel):
    title = models.CharField(
        verbose_name=_("عنوان دسته‌بندی"), max_length=255, unique=True
    )

    class Meta:
        verbose_name = _("دسته‌بندی")
        verbose_name_plural = _("دسته‌بندی‌ها")
        ordering = ["title"]

    def __str__(self):
        return self.title


class Project(BaseModel):

    class ProjectStatus(models.TextChoices):
        FINISHED = "F", _("پایان‌یافته")
        ONGOING = "O", _("در حال انجام")

    title = models.CharField(verbose_name=_("عنوان پروژه"), max_length=255)
    slug = AutoSlugField(
        verbose_name=_("اسلاگ پروژه"),
        populate_from="title",
        unique=True,
        always_update=True,
    )
    description = models.TextField(verbose_name=_("توضیحات پروژه"))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("دسته‌بندی پروژه"),
        related_name="projects",
    )
    size = models.CharField(verbose_name=_("اندازه پروژه"))
    dimensions = models.CharField(max_length=255, verbose_name=_("ابعاد پروژه"))
    creation_year = models.CharField(max_length=4, verbose_name=_("سال ایجاد پروژه"))
    scale = models.CharField(verbose_name=_("مقیاس پروژه"))
    status = models.CharField(
        verbose_name=_("وضعیت پروژه"),
        max_length=1,
        choices=ProjectStatus.choices,
        default=ProjectStatus.FINISHED,
    )

    class Meta:
        verbose_name = _("پروژه")
        verbose_name_plural = _("پروژه‌ها")
        ordering = ["-created_at", "title"]

    def __str__(self):
        return self.title

    @property
    def is_finished(self):
        return self.status == self.ProjectStatus.FINISHED


class GalleryItem(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name=_("پروژه آیتم گالری"),
        related_name="gallery_items",
    )
    image = models.ImageField(verbose_name=_("تصویر آیتم گالری"), upload_to="projects/")

    class Meta:
        verbose_name = _("آیتم گالری")
        verbose_name_plural = _("آیتم‌های گالری")
        ordering = ["created_at"]


class Blog(BaseModel):
    class BlogStatus(models.TextChoices):
        PUBLISHED = "P", _("منتشر شده")
        ARCHIVED = "A", _("آرشیو شده")

    title = models.CharField(verbose_name=_("عنوان بلاگ"), max_length=255)
    slug = AutoSlugField(
        verbose_name=_("اسلاگ بلاگ"),
        populate_from="title",
        unique=True,
        always_update=True,
    )

    description = models.CharField(verbose_name=_("توضیحات بلاگ"), max_length=255)
    summary = models.CharField(verbose_name=_("خلاصه بلاگ"), max_length=255)
    body = RichTextUploadingField(verbose_name=_("محتوای بلاگ"), config_name="default")
    cover = models.ImageField(verbose_name=_("کاور بلاگ"), upload_to="blogs/")
    status = models.CharField(
        verbose_name=_("وضعیت بلاگ"),
        choices=BlogStatus.choices,
        default=BlogStatus.PUBLISHED,
    )

    updated_at = models.DateTimeField(verbose_name=_("تاریخ بروزرسانی"), auto_now=True)

    class Meta:
        verbose_name = _("بلاگ")
        verbose_name_plural = _("بلاگ‌ها")
        ordering = ["-updated_at", "-created_at", "title"]

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == self.BlogStatus.PUBLISHED


class Comment(BaseModel):
    class CommentStatusChoice(models.TextChoices):
        APPROVED = "A", _("تأیید شده")
        REJECTED = "R", _("رد شده")

    name = models.CharField(verbose_name=_("نام"), max_length=255)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=255)
    text = models.TextField(verbose_name=_("متن"))
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name=_("بلاگ"),
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("والد"),
        related_name="replies",
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("وضعیت نظر"),
        max_length=1,
        choices=CommentStatusChoice.choices,
        default=CommentStatusChoice.APPROVED,
    )

    class Meta:
        verbose_name = _("نظر")
        verbose_name_plural = _("نظرات")
        ordering = ["-created_at"]

    def __str__(self):
        return ""

    @property
    def is_approved(self):
        return self.status == self.CommentStatusChoice.APPROVED

    @property
    def is_reply(self):
        return self.parent is not None


class History(BaseModel):
    event = models.CharField(verbose_name=_("رویداد تاریخ"), max_length=255)
    date = models.DateField(verbose_name=_("تاریخ رویداد"))
    url = models.URLField(verbose_name=_("آدرس تاریخ"), null=True, blank=True)

    class Meta:
        verbose_name = _("تاریخچه")
        verbose_name_plural = _("تاریخچه‌ها")
        ordering = ["-created_at"]

    def __str__(self):
        return self.event

from autoslug import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Category(BaseModel):
    title = models.CharField(
        verbose_name=_("Category Title"), max_length=255, unique=True
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["title"]

    def __str__(self):
        return self.title


class Project(BaseModel):

    class ProjectStatus(models.TextChoices):
        FINISHED = "F", _("Finished")
        ONGOING = "O", _("Ongoing")

    title = models.CharField(verbose_name=_("Project Title"), max_length=255)
    slug = AutoSlugField(
        verbose_name=_("Project Slug"),
        populate_from="title",
        unique=True,
        always_update=True,
    )
    description = models.TextField(verbose_name=_("Project Description"))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Project Category"),
        related_name="projects",
    )
    size = models.CharField(verbose_name=_("Project Size"))
    dimensions = models.CharField(max_length=255, verbose_name=_("Project dimensions"))
    creation_year = models.CharField(
        max_length=4, verbose_name=_("Project Creation Year")
    )
    scale = models.CharField(verbose_name=_("Project Scale"))
    status = models.CharField(
        verbose_name=_("Project Status"),
        max_length=1,
        choices=ProjectStatus.choices,
        default=ProjectStatus.FINISHED,
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
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
        verbose_name=_("Gallery Item Project"),
        related_name="gallery_items",
    )
    image = models.ImageField(
        verbose_name=_("Gallery Item Image"), upload_to="projects/"
    )

    class Meta:
        verbose_name = _("Gallery Item")
        verbose_name_plural = _("Gallery Items")
        ordering = ["created_at"]


class Blog(BaseModel):
    class BlogStatus(models.TextChoices):
        PUBLISHED = "P", _("Published")
        ARCHIVED = "A", _("Archived")

    title = models.CharField(verbose_name=_("Blog Title"), max_length=255)
    slug = AutoSlugField(
        verbose_name=_("Blog Slug"),
        populate_from="title",
        unique=True,
        always_update=True,
    )

    description = models.CharField(verbose_name=_("Blog Description"), max_length=255)
    summary = models.CharField(verbose_name=_("Blog Summary"), max_length=255)
    body = RichTextUploadingField(verbose_name=_("Blog Content"), config_name="default")
    cover = models.ImageField(verbose_name=_("Blog Cover"), upload_to="blogs/")
    status = models.CharField(
        verbose_name=_("Blog Status"),
        choices=BlogStatus.choices,
        default=BlogStatus.PUBLISHED,
    )

    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        ordering = ["-updated_at", "-created_at", "title"]

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == self.BlogStatus.PUBLISHED


class Comment(BaseModel):
    class CommentStatusChoice(models.TextChoices):
        APPROVED = "A", _("Approved")
        REJECTED = "R", _("Rejected")

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    email = models.EmailField(verbose_name=_("Email"), max_length=255)
    text = models.TextField(verbose_name=_("Text"))
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name=_("Blog"),
        related_name="comments",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("Parent"),
        related_name="replies",
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("Comment Status"),
        max_length=1,
        choices=CommentStatusChoice.choices,
        default=CommentStatusChoice.APPROVED,
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    @property
    def is_approved(self):
        return self.status == self.CommentStatusChoice.APPROVED

    @property
    def is_reply(self):
        return self.parent is not None

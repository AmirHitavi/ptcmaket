import factory
import factory.random
from faker import Faker as FakerFactory

from ..models import Blog, Category, Comment, GalleryItem, History, Project

faker = FakerFactory()


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    title = factory.LazyAttribute(lambda x: f"Category {faker.word()}")


class ProjectFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Project

    title = factory.LazyAttribute(lambda x: f"Project {faker.word()}")
    description = factory.LazyAttribute(lambda x: faker.sentence())
    category = factory.SubFactory(CategoryFactory)
    size = factory.LazyAttribute(
        lambda x: faker.random_element(["1", "1.25", "1.5", "1.75", "2"])
    )
    dimensions = factory.LazyAttribute(
        lambda x: f"{faker.random_int(1, 10)}*{faker.random_int(1, 10)}"
    )
    creation_year = factory.LazyAttribute(lambda x: f"{faker.year()}")
    scale = factory.LazyAttribute(
        lambda x: faker.random_element(["1:00", "1:1", "1:2", "1:5"])
    )
    status = factory.LazyAttribute(
        lambda x: faker.random_element(
            [Project.ProjectStatus.FINISHED, Project.ProjectStatus.ONGOING]
        )
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        gallery_items_count = kwargs.pop("gallery_items", None)

        project = super()._create(model_class, *args, **kwargs)

        if gallery_items_count is not None:
            for _ in range(gallery_items_count):
                GalleryItemFactory(project=project)
        else:
            for _ in range(faker.random_int(min=1, max=10)):
                GalleryItemFactory(project=project)

        return project


class GalleryItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = GalleryItem

    project = factory.SubFactory(ProjectFactory)
    image = factory.django.ImageField()


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.Sequence(lambda n: faker.name())
    description = factory.LazyAttribute(lambda x: "".join(faker.words(5)))
    summary = factory.LazyAttribute(lambda x: "".join(faker.sentences(nb=5)))
    body = factory.LazyAttribute(lambda x: "<p>Simple test content</p>")
    cover = factory.django.ImageField()
    status = factory.LazyAttribute(lambda x: Blog.BlogStatus.PUBLISHED)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        comments_count = kwargs.pop("comments", None)

        blog = super()._create(model_class, *args, **kwargs)

        if comments_count is not None:
            for _ in range(comments_count):
                CommentFactory(blog=blog)
        else:
            for _ in range(faker.random_int(1, 5)):
                CommentFactory(blog=blog)

        return blog


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment

    name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    text = factory.LazyAttribute(lambda x: faker.sentence())
    blog = factory.SubFactory(BlogFactory)
    status = factory.LazyAttribute(lambda x: Comment.CommentStatusChoice.APPROVED)


class HistoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = History

    event = factory.LazyAttribute(lambda x: f"Event {faker.word()}")
    date = factory.LazyAttribute(lambda x: faker.date())

from rest_framework import serializers

from ..models import Blog, Comment, Project


class ProjectSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source="category.title")
    banner_image = serializers.SerializerMethodField()
    gallery_items = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "description",
            "category",
            "size",
            "dimensions",
            "creation_year",
            "scale",
            "banner_image",
            "gallery_items",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "context") and self.context.get("view"):
            view = self.context["view"]
            if hasattr(view, "action"):
                if view.action == "list":

                    allowed_fields = {
                        "title",
                        "slug",
                        "category",
                        "creation_year",
                        "banner_image",
                    }

                    existing_fields = set(self.fields)

                    for field_name in existing_fields - allowed_fields:
                        self.fields.pop(field_name)
                elif view.action == "retrieve":

                    not_allowed_fields = ["banner_image", "category"]
                    for field in not_allowed_fields:
                        self.fields.pop(field)

    def get_banner_image(self, obj: Project):
        has_images = obj.gallery_items.exists()
        if has_images:
            first_gallery_item = obj.gallery_items.first()

            if first_gallery_item:
                return first_gallery_item.image.url
        return None

    def get_gallery_items(self, obj: Project):
        return [item.image.url for item in obj.gallery_items.all()]


class BlogSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "title",
            "slug",
            "description",
            "summary",
            "body",
            "cover",
            "comments",
        ]

    def get_comments(self, obj: Blog) -> list:
        all_approved_comments = getattr(obj, "all_approved_comments", [])

        top_level_comments = [
            comment for comment in all_approved_comments if comment.parent is None
        ]

        context = self.context.copy()
        context["all_approved_comments"] = all_approved_comments

        return CommentSerializer(
            top_level_comments,
            many=True,
            context=context,
        ).data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if hasattr(self, "context") and self.context.get("view"):
            view = self.context.get("view")
            if hasattr(view, "action"):
                if view.action == "list":
                    allowed_fields = {
                        "title",
                        "slug",
                        "description",
                        "summary",
                        "cover",
                    }
                    all_fields = set(self.fields)

                    for field in all_fields - allowed_fields:
                        self.fields.pop(field)
                if view.action == "retrieve":

                    not_allowed_fields = ["description"]

                    for field in not_allowed_fields:
                        self.fields.pop(field)


class CommentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), allow_null=True, required=False
    )
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "name", "email", "text", "parent", "replies"]

    def get_replies(self, obj: Comment) -> list:
        all_approved_comments = self.context.get("all_approved_comments", [])

        replies = [
            comment for comment in all_approved_comments if comment.parent_id == obj.id
        ]

        return CommentSerializer(replies, many=True, context=self.context).data

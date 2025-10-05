from rest_framework import serializers

from .models import Blog, Comment, Project


class ProjectListSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source="category.title")
    banner_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ["title", "slug", "category", "creation_year", "banner_image"]

    def get_banner_image(self, obj: Project):
        has_images = obj.gallery_items.exists()
        if has_images:
            first_gallery_item = obj.gallery_items.first()

            if first_gallery_item:
                return first_gallery_item.image.url
        return None


class ProjectDetailsSerializer(serializers.ModelSerializer):

    gallery_items = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "size",
            "dimensions",
            "creation_year",
            "scale",
            "gallery_items",
        ]

    def get_gallery_items(self, obj: Project):
        if obj.gallery_items:
            return [item.image.url for item in obj.gallery_items.all()]
        return []


class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ["title", "slug", "description", "summary", "cover"]


class CommentSerializer(serializers.ModelSerializer):

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "name", "email", "text", "parent", "replies"]
        read_only_fields = ["parent"]

    def get_replies(self, obj: Comment) -> list:
        all_approved_comments = self.context.get("all_approved_comments", [])

        replies = [
            comment for comment in all_approved_comments if comment.parent_id == obj.id
        ]

        return CommentSerializer(replies, many=True, context=self.context).data


class BlogDetailsSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ["title", "summary", "body", "cover", "comments"]

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


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["name", "email", "text"]

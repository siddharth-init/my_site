from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.


class Author(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def author_details(self):
        return f"{self.firstname} {self.lastname} "

    def __str__(self):
        return self.author_details()


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def tag_details(self):
        return f"{self.caption}"

    def __str__(self):
        return self.tag_details()


class Post(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.TextField()
    content = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "Author", on_delete=models.SET_NULL, related_name="posts", null=True
    )
    tags = models.ManyToManyField("Tag")
    image_name = models.CharField(max_length=100, null=True, blank=True, default="")

    def post_details(self):
        return f"{self.title} ({self.date})"

    def __str__(self):
        return self.post_details()

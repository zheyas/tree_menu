from django.db import models
from django.urls import reverse, NoReverseMatch

class Page(models.Model):
    slug = models.CharField(max_length=200, unique=True)   # например, "about" или "contacts" или "info/company"
    title = models.CharField(max_length=200)
    page_title = models.CharField(max_length=200, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=200, blank=True)

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        return self.url or "#"

    def __str__(self):
        return self.title

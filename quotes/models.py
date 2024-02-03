from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'text', 'author')

    def __str__(self):
        return f'{self.text[:50]} by {self.author}'

class SavedQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote_text = models.TextField()
    quote_author = models.CharField(max_length=100)
    class Meta:
        unique_together = ('user', 'quote_text', 'quote_author')
    def get_absolute_url(self):
        return reverse('delete_saved_quote', args=[str(self.id)])
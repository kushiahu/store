# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


class User(AbstractUser):

	GENDER = (
		('F', 'Femenino'),
		('M', 'Masculino'),
		('O', 'Otros'),
	)

	slug = models.SlugField(unique=True, editable=False)
	avatar = models.ImageField(upload_to='users/avatars', null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
	is_verified = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELD = ['email']

	def __str__(self):
		return f'@{self.username}'

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.username)
		super(User, self).save(*args, **kwargs)
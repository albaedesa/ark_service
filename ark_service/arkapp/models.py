from django.db import models
from django.conf import settings
import arkpy

# Create your models here.

class Minter(models.Model):

	name = models.CharField(max_length=256)
	prefix = models.CharField(max_length=7)
	template = models.CharField(max_length=25)
	active = models.BooleanField(default=True)
	date_created = models.DateField(auto_now_add=True)
	description = models.TextField()

	def __repr__(self):
		return '<Minter: {}>'.format(self.name)

	def _ark_exists(self, key):
		if len(Ark.objects.filter(key=key)) > 0:
			return True
		else:
			return False

	def mint(self, quantity):
		ark_list = []

		for item in range(quantity):
			key = arkpy.mint(authority=settings.NAAN, prefix=self.prefix, template = self.template)

			while self._ark_exists(key) is False:
				ark = Ark.objects.create(key=key, minter=self)
				ark.save()
				ark_list.append(ark)

		if quantity == 1:
			return ark_list[0]
		else:
			return ark_list 
				


class Ark(models.Model):

	key = models.CharField(max_length=25, unique=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	minter = models.ForeignKey('Minter', on_delete=models.CASCADE)
	target = models.URLField(max_length=200, null=True, blank=True)

	def __repr__(self):
		return '<Ark: {}>'.format(self.key)

	def bind(self, target):
		target = Ark.objects.get(key=self.key)
		ark.target = target
		ark.save()
		return self.target


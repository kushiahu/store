import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse

from apls.carts.models import Cart


class Order(models.Model):

	STATUS = (
		('CR', 'CREATED'),
		('PY', 'PAYED'),
		('CP', 'COMPLETED'),
		('CN', 'CANCELED'),
	)

	id_uuid = models.CharField(default=uuid.uuid4, max_length=36, editable=False)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, related_name='orders',
		null=True, blank=True, on_delete=models.CASCADE
	)
	cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
	subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	shipping_total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
	#shipping_address = models.ForeignKey(Address)
	status = models.CharField(max_length=2, choices=STATUS, default='CR')

	def __str__(self):
		return f'Orden: {self.id_uuid}'

	@property
	def total(self):
		return float(self.subtotal) + float(self.shipping_total)

	def update_subtotal(self):
		self.subtotal = self.cart.total
		self.save()

	def get_absolute_url(self):
		return reverse('order:confirm', args=[str(self.id_uuid)])

	def payed(self):
		self.status = 'PY'
		self.cart.completed()
		self.save()
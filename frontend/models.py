from django.db import models
from django.contrib.auth.models import User

# Product model
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.product_name  # Return product_name for this model


# Scheme model
class Scheme(models.Model):
    scheme_name = models.CharField(max_length=200)
    ministry = models.CharField(max_length=200)
    scheme_link = models.CharField(max_length=200, default='http://example.com')
    scheme_summary = models.CharField(max_length=1000, default='No Data Available')
    scheme_image = models.ImageField(upload_to='products/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Print the scheme_link in the console before saving
        print(f'Saving scheme with link: {self.scheme_link}')
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.scheme_name


# User Profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Custom Phone and Address model using a raw table (frontend_userprofile)
class PhoneAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    class Meta:
        db_table = 'frontend_userprofile'  # Reference the table name directly
        managed = False  # Managed as an unmanaged model


# In models.py
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def total_price(self):
        return self.product.product_price * self.quantity

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy
import uuid


class CartItems(models.Model):
    user_cart_id = models.IntegerField()
    product_id = models.IntegerField()
    amount = models.IntegerField(null=False, default=0)

    class Meta:
        managed = False
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class UserCart(models.Model):
    user_id = models.IntegerField()
    cart_hash = models.CharField(max_length=36, unique=True, default=None, null=False)
    is_bought = models.BooleanField()

    class Meta:
        managed = False
        db_table = "user_cart"
        verbose_name = "User Cart"
        verbose_name_plural = "User Carts"

    def save(self, *args, **kwargs):
        if not self.cart_hash:
            self.cart_hash = uuid.uuid4().hex
        super().save(*args, **kwargs)


class Roles(models.TextChoices):
    USER = "user", gettext_lazy("User")
    MANAGER = "manager", gettext_lazy("Manager")
    ADMIN = "admin", gettext_lazy("Admin")
    SUPERADMIN = "superadmin", gettext_lazy("Superadmin")


class Users(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    chat_id = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(
        max_length=255,
        null=False,
        default=Roles.USER,
        choices=Roles.choices
    )

    class Meta:
        managed = False
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name="subcategories")
    name = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = "subcategories"
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return f"{self.name} {self.category.name}"


class Products(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    picture_path = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.BigIntegerField()
    telegram_has = models.BooleanField(null=False, default=False)
    web_has = models.BooleanField(null=False, default=False)
    discount = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    article = models.CharField(max_length=36, unique=True, default=None, null=False)

    def save(self, *args, **kwargs):
        if not self.article:
            self.article = uuid.uuid4().hex

        if not self.id:
            self.price = self.price * 100

        if self.picture_path:
            self.web_has = True

        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class YooInvoice(models.Model):
    id = models.AutoField(primary_key=True)
    service_id = models.CharField(max_length=255, null=True)
    cart_id = models.IntegerField(null=True)
    status = models.CharField(max_length=255, null=True)
    value = models.CharField(max_length=255, null=True)
    currency = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    paid = models.BooleanField(null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "yoo_invoices"
        verbose_name = "YooInvoice"
        verbose_name_plural = "YooInvoices"


class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField(null=False)
    answer = models.TextField(null=False)

    class Meta:
        managed = False
        db_table = "faq"
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class Broadcast(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    picture_path = models.CharField(max_length=255, null=False)
    telegram_has = models.BooleanField(null=False, default=False)
    web_has = models.BooleanField(null=False, default=False)
    sent_at = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = "broadcasts"


class BroadcastSent(models.Model):
    id = models.AutoField(primary_key=True)
    broadcast_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "broadcasts_sent"
        managed = False

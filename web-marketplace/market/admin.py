from django.contrib import admin
from django import forms
from .models import CartItems, Users, UserCart, Products, Subcategory, Category, Faq, BroadcastSent, Broadcast
from django.core.files.storage import FileSystemStorage


class PicsStorage(FileSystemStorage):
    location = 'market/static/pics'


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 3


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "chat_id", "role")
    search_fields = ("name", "chat_id",)


class FaqAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer')
    list_filter = ('question',)
    search_fields = ('question', 'answer')


class ProductForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Products
        fields = (
            "name",
            "picture",
            "description", 
            "price", 
            "discount", 
            "is_visible", 
            "article"
        )
        readonly_fields = ("created_at",)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data["picture"]:
            fs = FileSystemStorage(location='market/static/pics')
            filename = fs.save(self.cleaned_data['picture'].name, self.cleaned_data['picture'])
            instance.picture_path = filename

        if commit:
            instance.save()

        return instance
    

class ProductsAdmin(admin.ModelAdmin):
    list_display = ("name", "total_price", "discount", "created_at", "is_visible")
    list_filter = ("is_visible",)
    search_fields = ("name",)
    form = ProductForm
    fields = ("name", "subcategory", "picture", "description", "price", "discount", "is_visible", "created_at", "article")
    readonly_fields = ("created_at", "article",)

    @classmethod
    def total_price(cls, obj):
        if obj.discount > 0:
            return str(int(obj.price - (obj.price * (obj.discount / 100)))//100)

        return str(int(obj.price / 100))


class BroadcastForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Broadcast
        fields = (
            "text",
            "picture",
            "sent_at",
        )


class BroadcastAdmin(admin.ModelAdmin):
    list_display = ("text", "picture_path", "sent_at",)
    form = BroadcastForm


admin.site.register(CartItems)
admin.site.register(Users, UserAdmin)
admin.site.register(UserCart)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Faq, FaqAdmin)
admin.site.register(BroadcastSent)
admin.site.register(Broadcast, BroadcastAdmin)

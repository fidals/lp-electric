from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.html import format_html

from lp_electric.models import Category, Product, CategoryPage, ProductPage
from pages.models import CustomPage, FlatPage
from images.models import Image


def after_action_message(updated_rows):
    if updated_rows == 1:
        return '1 item was'
    else:
        return '{} items were'.format(updated_rows)


class ProductInline(admin.StackedInline):
    model = Product
    can_delete = False
    fieldsets = ((None, {
        'classes': ('primary-chars', ),
        'fields': (
            ('name', 'id'),
            ('category', 'correct_category_id'),
            ('in_stock', 'is_popular'),
        )
    }),)

    def correct_category_id(self, obj):
        """Needed for correct short_description attr"""
        return obj.category_id
    correct_category_id.short_description = 'Category ID'

    readonly_fields = ['id', 'correct_category_id']


class CategoryInline(admin.StackedInline):
    model = Category
    can_delete = False
    fieldsets = ((None, {
        'classes': ('primary-chars', ),
        'fields': (
            # 'slug',TODO in dev-775
            ('name', 'id'),
            ('parent', 'correct_parent_id'),
        )
    }),)

    def correct_parent_id(self, obj):
        """Needed for correct short_description attr"""
        return obj.parent_id
    correct_parent_id.short_description = 'Parent ID'

    readonly_fields = ['id', 'correct_parent_id']


class ImageInline(GenericStackedInline):
    model = Image
    extra = 1
    readonly_fields = ['picture']
    verbose_name = 'Image'
    fieldsets = (
        (None, {
            'classes': ('primary-chars', ),
            'fields': (
                ('picture', 'image'),
                # 'slug', TODO in dev-775
                ('_title', 'is_main'),
                ('description', ),
            ),
        }),
    )

    def picture(self, obj):
        return format_html(
            '<img src="{url}" class="images-item">',
            url=obj.image.url
        )


# --------------------- Model admin classes ---------------------
class PageAdmin(admin.ModelAdmin):
    save_on_top = True #  https://goo.gl/al9CEc

    list_filter = ['is_active']
    list_display = ['id', 'h1', 'is_active']
    list_display_links = ['h1']

    inlines = [ImageInline]

    search_fields = ['id', 'h1', 'parent__h1']

    readonly_fields = ['id']

    actions = ['make_items_active', 'make_items_non_active']

    fieldsets = (
        ('Дополнительные характеристики', {
            'classes': ('seo-chars',),
            'fields': (
                ('id', 'is_active'),
                'date_published',
                # 'slug', TODO in dev-775
                '_menu_title',
                'seo_text',
                'position',
            )
        }),
        ('Параметры страницы', {
            'classes': ('secondary-chars',),
            'fields': (
                ('h1', '_title'),
                'keywords',
                'description',
                'content'
            )
        })
    )

    def make_items_active(self, request, queryset):
        updated_rows = queryset.update(is_active=1)
        message_prefix = after_action_message(updated_rows)

        self.message_user(request,
                          '{} marked as active.'.format(message_prefix))

    make_items_active.short_description = 'Make active'

    def make_items_non_active(self, request, queryset):
        updated_rows = queryset.update(is_active=0)
        message_prefix = after_action_message(updated_rows)

        self.message_user(request,
                          '{} marked as non-active.'.format(message_prefix))

    make_items_non_active.short_description = 'Make inactive'


class CustomPageAdmin(PageAdmin):
    # Fieldsets
    fieldsets = (
        ('Дополнительные характеристики', {
            'classes': ('seo-chars',),
            'fields': (
                'is_active',
                'date_published',
                '_menu_title',
                'seo_text',
                'position',
                ('parent', 'correct_parent_id')
            )
        }),
        ('Параметры страницы', {
            'classes': ('secondary-chars',),
            'fields': (
                ('h1', '_title'),
                ('keywords', 'id'),
                'description',
                'content'
            )
        })
    )

    def correct_parent_id(self, obj):
        """Needed for correct short_description attr"""
        return obj.parent_id
    correct_parent_id.short_description = 'Parent ID'

    readonly_fields = ['id', 'correct_parent_id']

    def custom_parent(self, obj):
        if not obj.parent:
            return

        parent = obj.parent
        url = reverse('admin:pages_custompage_change', args=(parent.id,))

        return format_html(
            '<a href="{url}">{parent}</a>',
            parent=parent,
            url=url
        )

    custom_parent.short_description = 'Parent'
    custom_parent.admin_order_field = 'parent__h1'


class FlatPageAdmin(PageAdmin):
    fieldsets = (
        ('Дополнительные характеристики', {
            'classes': ('seo-chars',),
            'fields': (
                ('id', 'is_active'),
                'date_published',
                # 'slug', TODO in dev-775
                '_menu_title',
                'seo_text',
                'position',
                ('parent', 'correct_parent_id')
            )
        }),
        ('Параметры страницы', {
            'classes': ('secondary-chars',),
            'fields': (
                ('h1', '_title'),
                'keywords',
                'description',
                'content'
            )
        })
    )

    def correct_parent_id(self, obj):
        """Needed for correct short_description attr"""
        return obj.parent_id
    correct_parent_id.short_description = 'Parent ID'

    readonly_fields = ['id', 'correct_parent_id']

    def custom_parent(self, obj):
        if not obj.parent:
            return

        parent = obj.parent
        url = reverse('admin:pages_flatpage_change', args=(parent.id,))

        return format_html(
            '<a href="{url}">{parent}</a>',
            parent=parent,
            url=url
        )

    custom_parent.short_description = 'Parent'
    custom_parent.admin_order_field = 'parent__h1'


class ProductPageAdmin(PageAdmin):
    inlines = [
        ProductInline,
        ImageInline,
    ]

    list_filter = ['is_active']

    list_display = ['product_id', 'h1', 'custom_parent', 'price', 'links', 'is_active']

    search_fields = ['lp_electric_product__id', 'h1', 'parent__h1']

    def product_id(self, obj):
        return obj.model.id

    product_id.short_description = 'Id'
    product_id.admin_order_field = 'lp_electric_product__id'

    def price(self, obj):
        return obj.model.price

    price.short_description = 'Price'
    price.admin_order_field = 'lp_electric_product__price'

    def custom_parent(self, obj):
        if not obj.parent:
            return

        parent = obj.parent
        url = reverse('admin:lp_electric_categorypage_change', args=(parent.id,))

        return format_html(
            '<a href="{url}">{parent}</a>',
            parent=parent,
            url=url
        )

    custom_parent.short_description = 'Category'
    custom_parent.admin_order_field = 'parent__h1'

    def links(self, model):
        context = {
            'site_url': model.url,
        }

        return render_to_string('admin/includes/items_list_row.html', context)

    links.short_description = 'Link'


class CategoryPageAdmin(PageAdmin):
    inlines = [
        CategoryInline,
        ImageInline
    ]

    search_fields = ['h1', 'parent__h1']

    list_display = ['category_model_id', 'h1', 'custom_parent', 'is_active']

    # Custom fields
    def category_model_id(self, obj):
        return obj.model.id

    category_model_id.short_description = 'Id'
    category_model_id.admin_order_field = 'lp_electric_category__id'

    def custom_parent(self, obj):
        if not obj.parent_id:
            return
        try:
            url = reverse('admin:lp_electric_categorypage_change', args=(obj.parent_id,))
        except:
            url = reverse('admin:pages_custompage_change', args=(obj.parent_id,))

        return format_html(
            '<a href="{url}">{parent_id}</a>',
            parent_id=obj.parent,
            url=url
        )

    custom_parent.short_description = 'Parent'
    custom_parent.admin_order_field = 'parent__h1'

admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(ProductPage, ProductPageAdmin)
admin.site.register(CategoryPage, CategoryPageAdmin)
admin.site.register(FlatPage, FlatPageAdmin)

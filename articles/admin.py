from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope


admin.site.register(Tag)


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_quantity = 0
        for form in self.forms:
            for k, v in form.cleaned_data.items():
                if k == 'is_main' and v == True:
                    is_main_quantity += 1
        if is_main_quantity != 1:
            raise ValidationError('IS_MAIN==TRUE should be the only ONE')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

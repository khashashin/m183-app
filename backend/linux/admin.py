from django.contrib import admin
from linux.models import Command, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    fields = ('option', 'name', 'description')


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

    # List available options inline
    inlines = [
        OptionInline,
    ]

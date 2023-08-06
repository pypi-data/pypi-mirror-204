from typing import Type

from django.contrib.admin import SimpleListFilter
from django.db.models import Model, ForeignKey


def foreign_key_filter(model: Type[Model], field_name: str):
    field: ForeignKey = getattr(model, field_name).field

    class ForeignKeyFilter(SimpleListFilter):
        title = field.verbose_name.capitalize()
        parameter_name = field_name

        def lookups(self, request, model_admin):
            # noinspection PyUnresolvedReferences
            return [(instance.pk, str(instance)) for instance in field.related_model.objects.all()]

        def queryset(self, request, queryset):
            if not self.value():
                return queryset

            query = {
                f"{field_name}__pk": self.value()
            }

            return queryset.filter(**query)

    return ForeignKeyFilter


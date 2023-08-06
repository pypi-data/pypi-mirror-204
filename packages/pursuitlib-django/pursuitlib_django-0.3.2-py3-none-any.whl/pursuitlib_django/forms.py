from typing import List, Optional, Dict, Type

import django.forms as dforms
from django.conf import settings
from django.contrib import messages
from django.db.models import Model
from django.forms import BoundField
from django.forms.utils import ErrorDict, ErrorList
from django.forms.widgets import CheckboxInput, TextInput, Select
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.safestring import SafeText
from django_select2.forms import Select2Mixin
from pursuitlib.utils import is_null_or_empty, get_oneline_string
from pursuitlib_django.utils import get_verbose_name, is_feminine

# Read the Django configuration
FORM_DEFAULT_TEMPLATE = getattr(settings, "FORM_DEFAULT_TEMPLATE")


DEFAULT_LIST_HTML = "<ul><li>&nbsp;</li></ul>"
DEFAULT_FORM_SECTION = "main"


class Form(dforms.Form):
    @classmethod
    def handle_request(cls, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.method == 'POST':
            form = cls(data=request.POST, files=request.FILES, **kwargs)

            if not form.is_valid():
                form.display_errors(request)
            else: return form.submit(request)
        else: form = cls(**kwargs)

        return form.show(request)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self:
            self.transform_field(field)
        for field in self.get_text_list_fields():
            if field not in self.initial:
                self.initial.setdefault(field, DEFAULT_LIST_HTML)
            elif is_null_or_empty(self.initial[field]):
                self.initial[field] = DEFAULT_LIST_HTML

    def order_fields(self, field_order):
        super().order_fields(field_order)
        self.add_dynamic_fields()

    def add_dynamic_fields(self):
        pass

    def transform_field(self, field: BoundField):
        field.section = DEFAULT_FORM_SECTION
        for sname, sfields in self.get_sections().items():
            if field.name in sfields:
                field.section = sname
                break

        field.visible = self.is_visible_by_default(field)

        if field.widget_type == "checkbox":
            field.display_label = False
            field.display_icon = False
        elif field.widget_type == "ckeditor" or field.widget_type == "ckeditoruploading":
            field.display_label = True
            field.display_icon = False
        else:
            field.display_label = True
            field.display_icon = True

        field.icon = self.get_icon_for_field(field)

        widget = field.field.widget

        if isinstance(widget, CheckboxInput):
            widget.attrs["class"] = "form-check-input"
        else:
            if isinstance(widget, TextInput):
                widget.attrs["autocomplete"] = "off"

            if isinstance(widget, Select):
                widget.attrs["class"] = "form-select"
            else:
                widget.attrs["class"] = "form-control"

            if isinstance(widget, Select2Mixin):
                # noinspection PyUnresolvedReferences
                widget.attrs["data-placeholder"] = self.get_field_placeholder(field)
            else: widget.attrs["placeholder"] = self.get_field_placeholder(field)

    # noinspection PyUnresolvedReferences
    def full_clean(self):
        super().full_clean()
        for field in self.get_text_list_fields():
            if get_oneline_string(self.cleaned_data[field]) == DEFAULT_LIST_HTML:
                self.cleaned_data[field] = ""
                if hasattr(self.instance, field):
                    setattr(self.instance, field, "")

    def get_title(self) -> str:
        return "Formulaire"

    def get_page_title(self) -> str:
        return self.get_title()

    def get_header(self) -> Optional[str or SafeText]:
        return None

    def get_submit_text(self) -> str:
        return "Envoyer"

    def get_sections(self) -> Dict[str, List[str]]:
        return {}

    def get_section(self, section: str) -> List[BoundField]:
        fields = []
        for field in self:
            if field.section == section:
                fields.append(field)
        return fields

    def is_visible_by_default(self, field: BoundField) -> bool:
        return True

    def get_icon_for_field(self, field: BoundField) -> str:
        return "fas fa-arrow-right"

    def get_field_placeholder(self, field: BoundField) -> str:
        return field.label + " ..."

    def get_text_list_fields(self) -> List[str]:
        return []

    def get_context(self) -> dict:
        return {
            "form": self
        }

    def show(self, request: HttpRequest) -> HttpResponse:
        return render(request, FORM_DEFAULT_TEMPLATE, context=self.get_context())

    def submit(self, request: HttpRequest) -> HttpResponse:
        return HttpResponseRedirect("/")

    def display_errors(self, request: HttpRequest):
        errors: ErrorDict = self.errors
        for key, value in errors.items():
            field_name = self[key].label
            elist: ErrorList = value
            elist_txt = "<br />".join([str(e) for e in elist])
            messages.error(request, SafeText(f"<strong>{field_name}</strong><br />{elist_txt}"))


class ModelForm(Form, dforms.ModelForm):
    @classmethod
    def fetch_instance_from_id(cls) -> bool:
        return True

    # noinspection PyShadowingBuiltins
    @classmethod
    def handle_request(cls, request: HttpRequest, id=None, **kwargs) -> HttpResponse:
        if id is not None:
            # noinspection PyUnresolvedReferences
            model_type = cls.Meta.model
            try:
                kwargs["instance"] = model_type.objects.get(pk=id)
            except model_type.DoesNotExist:
                model_name = get_verbose_name(model_type)
                raise Http404(f"Unable to find {model_name} instance")

        return super().handle_request(request, **kwargs)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        self.edit_form = instance is not None and instance.pk is not None

    def is_edit_form(self) -> bool:
        return self.edit_form

    def get_title(self) -> str:
        if self.is_edit_form():
            return f"Modification de {self.instance}"
        else:
            model_name = get_verbose_name(self._meta.model)
            pronoun = "une" if is_feminine(self._meta.model) else "un"
            return f"Création d'{pronoun} {model_name}"

    def get_submit_text(self) -> str:
        verb = "Modifier" if self.is_edit_form() else "Créer"
        pronoun = "la" if is_feminine(self._meta.model) else "le"
        model_name = get_verbose_name(self._meta.model)
        return f"{verb} {pronoun} {model_name}"

    def save(self, commit=True):
        result = super().save(commit=False)
        self.set_result_fields(result)
        if commit:
            result.save()
            self.save_m2m()
        return result

    # This can be overriden to statically set some resulting fields
    def set_result_fields(self, result):
        pass

    def submit(self, request: HttpRequest) -> HttpResponse:
        self.save()
        return super().submit(request)

    def send_confirmation_message(self, request: HttpRequest):
        model_name = get_verbose_name(self._meta.model).capitalize()
        verb_suffix = "e" if is_feminine(self._meta.model) else ""
        if self.is_edit_form():
            messages.info(request, f"{model_name} modifié avec succès")
        else:
            messages.success(request, f"{model_name} créé{verb_suffix} avec succès")

    def get_delete_url(self) -> Optional[str]:
        return None


class DeleteModelForm(Form):
    @classmethod
    def get_model_type(cls) -> Type[Model]:
        raise NotImplemented()

    # noinspection PyMethodOverriding,PyShadowingBuiltins,PyUnresolvedReferences
    @classmethod
    def handle_request(cls, request: HttpRequest, id: int, **kwargs) -> HttpResponse:
        model_type = cls.get_model_type()
        try:
            instance = model_type.objects.get(pk=id)
            return super().handle_request(request, instance=instance, **kwargs)
        except model_type.DoesNotExist:
            raise Http404(f"Unable to find {model_type.__name__} instance with ID {id}")

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance

    def get_title(self) -> str:
        model_type = self.get_model_type()
        model_name = get_verbose_name(model_type)
        pronoun = "une" if is_feminine(model_type) else "un"
        return f"Suppression d'{pronoun} {model_name}"

    def get_header(self) -> Optional[str or SafeText]:
        return SafeText(f"Souhaitez vous vraiment supprimer {self.instance} ? <strong>Cette action est irréversible</strong>.")

    def get_submit_text(self) -> str:
        return "Confirmer la suppression"

    def submit(self, request: HttpRequest) -> HttpResponse:
        # Delete the instance when the form is submitted
        self.instance.delete()
        return super().submit(request)

    def send_confirmation_message(self, request: HttpRequest):
        model_type = self.get_model_type()
        model_name = get_verbose_name(model_type).capitalize()
        verb_suffix = "e" if is_feminine(model_type) else ""
        messages.info(request, f"{model_name} supprimé{verb_suffix} avec succès")

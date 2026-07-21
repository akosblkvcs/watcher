from typing import ClassVar

from django import forms

from watch.models import Target


class TargetForm(forms.ModelForm[Target]):
    """Create/edit form for a watch target."""

    class Meta:
        model = Target
        fields = [
            "name",
            "url",
            "selector_type",
            "selector",
            "processor_type",
            "processor_config",
            "active",
        ]
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "selector": forms.TextInput(),
            "processor_config": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "processor_config": 'Optional JSON, e.g. {"decimal_sep": ","}',
        }

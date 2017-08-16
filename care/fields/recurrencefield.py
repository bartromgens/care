import recurrence.forms
import recurrence.fields


class RecurrenceWidget(recurrence.forms.RecurrenceWidget):
    class Media:
        css = {
            'all': ('css/django-recurrent-fixes.css', ),
        }


class RecurrenceField(recurrence.fields.RecurrenceField):
    def formfield(self, **kwargs):
        defaults = {
            'widget': RecurrenceWidget,
        }
        defaults.update(kwargs)
        return super(RecurrenceField, self).formfield(**defaults)

from django.forms import DateTimeInput
from django.forms import DateTimeInput
from django.forms import Select
from django.templatetags.static import static

class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = 'widgets/bootstrap_datetimepicker.html'

    def get_context(self, name, value, attrs):
        datetimepicker_id = 'datetimepicker_{name}'.format(name=name)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        return context

class BootstrapSelect(Select):
    class Media:
        css = {
          'all': ['//cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/css/bootstrap-select.min.css',  # noqa
                  static('bootstrap_select/bootstrap_select.css'), ]
        }
        js = ['//cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/js/bootstrap-select.min.js', ]  # noqa

    #return forms.Media(
    #        css=css,
    #        js=js,
    #)

    def __init__(self, attrs=None, choices=(), **kwargs):
        #assets = bootstrap_select_settings.BOOTSTRAP_SELECT_ASSETS
        #self.bootstrap_js = kwargs.get('bootstrap_js', assets['bootstrap_js'])
        #self.bootstrap_css = kwargs.get('bootstrap_css', assets['bootstrap_css'])
        #self.jquery_js = kwargs.get('jquery_js', assets['jquery_js'])

        if attrs is None:
            attrs = {'class': 'selectpicker'}
        else:
            try:
                attrs['class'] += ' selectpicker'
            except KeyError:
                attrs['class'] = 'selectpicker'
        super(BootstrapSelect, self).__init__(attrs=attrs, choices=choices)

    # Django 1.8
    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''

        html = '<option value="{}"'.format(option_value)
        html += ' data-content="{}"'.format(force_text(option_label))
        if self.attrs.get('data-live-search'):
            html += ' data-tokens="{}"'.format(option_value)
        html += '{}>{}</option>'.format(selected_html, force_text(option_label))
        return format_html(html)

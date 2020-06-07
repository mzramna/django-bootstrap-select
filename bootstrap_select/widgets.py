from django import forms
from django.forms import Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from . import settings as bootstrap_select_settings


class BootstrapSelect(Select):

    @property
    def media(self):
        css = {
          'all': ['//cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.17/css/bootstrap-select.min.css',  # noqa
                  static('bootstrap_select/bootstrap_select.css'), ]
        }
        js = ['//cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.17/js/bootstrap-select.min.js', ]  # noqa

        if self.bootstrap_css:
            css['all'] = ['//maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'] + css['all']  # noqa
        if self.bootstrap_js:
            js = ['//maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js'] + js
        if self.jquery_js:
            js = ['//ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'] + js

        return forms.Media(
            css=css,
            js=js,
        )

    def __init__(self, attrs=None, choices=(), **kwargs):
        assets = bootstrap_select_settings.BOOTSTRAP_SELECT_ASSETS
        self.bootstrap_js = kwargs.get('bootstrap_js', assets['bootstrap_js'])
        self.bootstrap_css = kwargs.get('bootstrap_css', assets['bootstrap_css'])
        self.jquery_js = kwargs.get('jquery_js', assets['jquery_js'])

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

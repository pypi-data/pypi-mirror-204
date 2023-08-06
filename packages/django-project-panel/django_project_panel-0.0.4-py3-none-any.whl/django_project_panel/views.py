import copy
from datetime import datetime, timedelta, date

from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic

from .models import *
from .project_panel import ProjectPanel


class Panel(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    permission_required = ['project_panel_app.view_panel']
    template_name = 'project_panel/panel.html'
    extra_context = {
        'title': 'Мониторинг-панель проекта',
    }

    def get_context_data(self, **kwargs):
        panel = ProjectPanel()
        ctx = super(Panel, self).get_context_data(**kwargs)
        ctx['virtual_memory'] = panel.virtual_memory()
        ctx['hard_memory'] = panel.hard_disk()
        ctx['folders_files'] = panel.folders_files()
        ctx['db'] = panel.databases()
        return ctx


class CleanTable(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    permission_required = ['project_panel_app.edit_panel']
    template_name = 'project_panel/clean_table.html'
    extra_context = {
        'title': 'Мониторинг-панель проекта',
    }
    result = ''

    def dispatch(self, request, *args, **kwargs):
        self.alias = kwargs['alias']
        self.table = kwargs['table']
        self.db = copy.copy(settings.DATABASES[self.alias])
        self.clean_settings = copy.copy(settings.PROJECT_PANEL.get('clean_model', {}).get(f'{self.alias}.{self.table}'))
        if self.clean_settings is None:
            raise Exception(f'В блоке clean_model нет сведений о таблице {self.alias}.{self.table} (settings.py)')
        self.panel = ProjectPanel()
        self.table_info = self.panel.get_db_report(self.alias, self.table)[0]
        self.filter_value = (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        return super(CleanTable, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.filter_value = self.request.POST.get('filter_value', self.filter_value)
        if self.request.POST.get('run_sql_query') == 'run':
            try:
                self.panel.clean_table(self.alias, self.table, self.clean_settings['filter_field_lt'], self.filter_value)
                self.result = 'Запрос выполнен'
                self.table_info = self.panel.get_db_report(self.alias, self.table)[0]
            except Exception as e:
                self.result = f'Запрос не выполнен: {e}'
        return super(CleanTable, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CleanTable, self).get_context_data(**kwargs)
        ctx['title'] = f'{self.alias}.{self.table}'
        ctx['alias'] = self.alias
        ctx['db'] = self.db['NAME']
        ctx['table'] = self.table
        ctx['table_info'] = self.table_info
        ctx['sql'] = self.panel.clean_table(self.alias, self.table, self.clean_settings['filter_field_lt'], self.filter_value, bild_sql=True)
        ctx['filter_value'] = self.filter_value
        ctx['result'] = self.result
        return ctx




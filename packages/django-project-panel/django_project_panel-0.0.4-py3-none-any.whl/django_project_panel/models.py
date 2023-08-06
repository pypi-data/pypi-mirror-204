from django.db import models


class ProjectPanelModel(models.Model):
    KB, MB, GB, TB = 'kb', 'mb', 'gb', 'tb'
    UNIT_SIZE = {KB: 1, MB: 2, GB: 3, TB: 4}

    name = models.CharField(max_length=255, verbose_name='')

    class Meta:
        managed = True
        db_table = 'ProjectPanelModel'
        verbose_name = 'Панель управления проектом'
        default_permissions = ()
        permissions = (
            ('view_panel', 'Панель управления проектом - просмотр'),
            ('manage_panel', 'Панель управления проектом - управление'),
        )

    def __str__(self):
        return f"{self.id} {self.name}"




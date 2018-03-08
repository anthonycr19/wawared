from django.db import models


# Create your models here.
class CatalogoProcedimiento(models.Model):
    CHOISE_SEXO = (
        (None, 'No determinado'),
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    )
    codigo_cpt = models.CharField(max_length=20, null=True, blank=True)
    denominacion_procedimientos = models.TextField(null=True, blank=True)
    sexo = models.CharField(null=True, blank=True, choices=CHOISE_SEXO, default=None, max_length=1)

    def __unicode__(self):
        return u'({0}) {1}'.format(self.codigo_cpt, self.denominacion_procedimientos)

    @property
    def nombre_display(self):
        return self.denominacion_procedimientos

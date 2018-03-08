from django.db import models


class ICD10Manager(models.Manager):
    def get_queryset(self):
        return super(ICD10Manager, self) \
            .get_queryset().filter(is_familia=True, is_activo=True)


class ICD10ManagerMedical(models.Manager):
    def get_queryset(self):
        return super(ICD10ManagerMedical, self) \
            .get_queryset().filter(is_medico=True, is_activo=True)

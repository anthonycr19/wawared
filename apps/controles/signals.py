from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Control


@receiver(post_delete, sender=Control)
def post_delete_control(sender, instance, **kwargs):
    Control.order_by_date(instance.embarazo)


@receiver(post_save, sender=Control)
def post_save_control(sender, instance, created, **kwargs):
    if hasattr(instance, 'diagnostico') and instance.diagnostico:
        instance.diagnostico.tratamiento = '\n'.join(
            instance.generar_tratamiento())
        instance.diagnostico.save()
        # if created:
        #     from citas.models import Cita
        #     Cita.schedule_appointment(instance)

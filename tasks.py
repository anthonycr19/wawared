from invoke import task, run


@task(name='loaddata')
def load_data():
    fixtures = (
        'apps/cie/fixtures/*.json',
        'apps/pacientes/fixtures/*.json',
        'apps/controles/fixtures/*.json',
        'apps/ubigeo/fixtures/*.json',
        'apps/perfiles/fixtures/*.json',
        'apps/establecimientos/fixtures/*.json'
    )
    for fixture in fixtures:
        run('python manage.py loaddata {}'.format(fixture))

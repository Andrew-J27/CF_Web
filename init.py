from case_manager.models import SystemUser, Attorney, Assistant


def setup():
    admins = ['andrew', 'axel', 'amanda']
    attorneys = ['Edgar', 'Alex']
    assistants = ['Crista','Ester', 'Glenda', 'Jose', 'Laura', 'Michaell', 'Miguel', 'Victoria']

    for name in admins:
        user = SystemUser.objects.create(username=name)
        user.set_password("2127")
        user.role = "admin"
        user.save()

    for name in attorneys:
        user = SystemUser.objects.create(username=name)
        user.set_password("2127")
        user.role = "attorney"
        user.save()
        attorney = Attorney.objects.create(name=name, user=user) 
        attorney.save()

    for name in assistants:
        user = SystemUser.objects.create(username=name)
        user.set_password("2127")
        user.role = "assistant"
        user.save()
        assistant = Assistant.objects.create(name=name, user=user) 
        assistant.save() 
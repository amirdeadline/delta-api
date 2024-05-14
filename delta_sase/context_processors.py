#delta_api project context_processors.py
from django.conf import settings as django_settings
from delta_sase.settings import TENANT_SUBFOLDER_PREFIX

def settings(request):
    return {
        "settings": django_settings,
    }



def get_subfolder_code(request):
    subfolder_code = ""

    if request is None:
        return subfolder_code

    try:
        subfolder_code = "/" + TENANT_SUBFOLDER_PREFIX + "/" + request.tenant.name
    except:
        pass
    return subfolder_code

#for template
def get_program_settings(request):
    subfolder_code = get_subfolder_code(request)
    context = {
        'subfolder_code': subfolder_code
    }
    return {"program_settings": context}
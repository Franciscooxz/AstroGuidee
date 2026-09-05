from .models import SiteConfig, PolicyPage


def site_config(request):
    return {
        'site_config': SiteConfig.get(),
        'policy_active': PolicyPage.get().is_active,
    }

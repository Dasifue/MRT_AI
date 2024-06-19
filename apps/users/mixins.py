from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class IsDoctorMixin(AccessMixin):
    redirect_url = "main:cabinet"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.position in ("DOCTOR", "ADMIN"):
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)



class IsPatientMixins(AccessMixin):
    redirect_url = "main:cabinet"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.position in ("PATIENT", "ADMIN"):
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

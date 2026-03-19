from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def callback(request):
    enterprise_token = request.GET.get("enterpriseToken", "").strip()
    signup_url_name = request.GET.get("signupUrlName", "").strip()
    if not enterprise_token:
        return JsonResponse(
            {
                "status": "missing_enterprise_token",
                "message": "Callback received without enterpriseToken query parameter.",
            },
            status=400,
        )
    return JsonResponse(
        {
            "status": "ok",
            "message": "AMAPI callback received.",
            "enterpriseToken": enterprise_token,
            "signupUrlName": signup_url_name,
            "next": "Use bootstrap_enterprise with --enterprise-token and --signup-url-name.",
        }
    )

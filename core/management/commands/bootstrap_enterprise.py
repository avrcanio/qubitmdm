from django.core.management.base import BaseCommand, CommandError

from amapi.services import amapi_service
from core.models import Enterprise


class Command(BaseCommand):
    help = "Bootstrap AMAPI enterprise via signup URL or enterprise token"

    def add_arguments(self, parser):
        parser.add_argument("--create-signup-url", action="store_true", help="Create signup URL")
        parser.add_argument("--enterprise-token", type=str, help="Enterprise token received from signup callback")
        parser.add_argument("--enterprise-name", type=str, default="QubitMDM Enterprise")
        parser.add_argument("--organization-id", type=str, default="default-org")
        parser.add_argument("--service-account-key-path", type=str, required=True)

    def handle(self, *args, **options):
        if options["create_signup_url"]:
            payload = amapi_service.create_signup_url()
            self.stdout.write(self.style.SUCCESS(f"signupUrl: {payload}"))

        token = options.get("enterprise_token")
        if token:
            enterprise_response = amapi_service.create_enterprise(
                enterprise_token=token,
                enterprise_name=options["enterprise_name"],
            )
            enterprise_id = enterprise_response.get("name")
            if not enterprise_id:
                raise CommandError("AMAPI response did not contain enterprise id in 'name'.")

            enterprise, _ = Enterprise.objects.update_or_create(
                enterprise_id=enterprise_id,
                defaults={
                    "enterprise_name": options["enterprise_name"],
                    "organization_id": options["organization_id"],
                    "service_account_key_path": options["service_account_key_path"],
                },
            )
            self.stdout.write(self.style.SUCCESS(f"Enterprise saved: {enterprise}"))

        if not options["create_signup_url"] and not token:
            raise CommandError("Provide --create-signup-url and/or --enterprise-token")

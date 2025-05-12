"""
Module containing the AdminPagesTestCase class.
"""

from django.contrib.admin.sites import site
from django.urls import reverse
from mixer.backend.django import mixer

from account.models import User
from core.mixins import BaseAPITestCase


class AdminPagesTestCase(BaseAPITestCase):
    """
    Class to test all the admin pages.

    This assert that all the admin pages and the code added to them works fine.
    """

    def _give_privilegies_to_user(self, user: User) -> None:
        user.is_staff = True
        user.is_superuser = True
        user.save()
        user.refresh_from_db()
        self.client.force_login(user)

    def test_should_load_all_admin_pages(self):
        """
        Assert all registered admin pages return a 200 response.
        """
        self._give_privilegies_to_user(self.user)

        skip_admin_page_names = ["auth_group", "authtoken_tokenproxy"]

        for model in site._registry:  # noqa: SLF001
            model_name = model._meta.model_name  # noqa: SLF001
            app_label = model._meta.app_label  # noqa: SLF001
            verbose_model_name = model._meta.verbose_name.capitalize()  # noqa: SLF001  # type: ignore

            admin_page_name = f"{app_label}_{model_name}"

            # SKIP DEFAULT ADMIN CLASSES - TESTING ONLY APP ONES
            if admin_page_name in skip_admin_page_names:
                continue

            with self.subTest(f"Testing {admin_page_name} - List View (Changelist)"):
                changelist_url = reverse(f"admin:{admin_page_name}_changelist")
                response = self.client.get(changelist_url)
                self.assertEqual(response.status_code, 200)

            with self.subTest(f"Testing {admin_page_name} - Add View"):
                add_url = reverse(f"admin:{app_label}_{model_name}_add")
                response = self.client.get(add_url)
                self.assertEqual(response.status_code, 200)

            with self.subTest(f"Testing {admin_page_name} - Edit View"):
                # Create one object to open its page
                obj = mixer.blend(model)
                change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[obj.pk])
                response = self.client.get(change_url)
                self.assertEqual(response.status_code, 200)
                self.assertIn("Base Fields", response.content.decode())
                self.assertIn(f"{verbose_model_name} details", response.content.decode())

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Create Default groups "

    def handle(self, *args, **options):
        try:
            content_type = ContentType.objects.get(app_label='contenttypes', model='contenttype')
            view_perm = Permission.objects.get(content_type=content_type, codename='view_contenttype')
            add_perm = Permission.objects.get(content_type=content_type, codename='add_contenttype')
            change_perm = Permission.objects.get(content_type=content_type, codename='change_contenttype')
            delete_perm = Permission.objects.get(content_type=content_type, codename='delete_contenttype')

            viewer_group, created = Group.objects.get_or_create(name='viewer')
            viewer_group.permissions.add(view_perm)
            staff_group, created = Group.objects.get_or_create(name='editor')
            staff_group.permissions.add(view_perm, add_perm, change_perm, delete_perm)

        except Exception as e:
            self.stderr.write(f"Error: {str(e)}")

        self.stdout.write(self.style.SUCCESS('Successfully initialized groups'))


# tree_menu/management/commands/fill_menus.py

from django.core.management.base import BaseCommand
from tree_menu.models import Menu, MenuItem, Page

class Command(BaseCommand):
    help = 'Заполняет БД тестовыми меню, пунктами меню и Page'

    def handle(self, *args, **kwargs):
        # --- Меню main_menu ---
        main_menu, _ = Menu.objects.get_or_create(name='main_menu')
        home = MenuItem.objects.create(menu=main_menu, title="Главная", url="/")
        about = MenuItem.objects.create(menu=main_menu, title="О нас", url="/about/")
        services = MenuItem.objects.create(menu=main_menu, title="Услуги", url="/services/")
        contact = MenuItem.objects.create(menu=main_menu, title="Контакты", url="/contact/")

        # Вложенный пункт в "Услуги"
        service1 = MenuItem.objects.create(menu=main_menu, title="Консультация", url="/services/consult/",
                                           parent=services)
        service2 = MenuItem.objects.create(menu=main_menu, title="Аудит", url="/services/audit/", parent=services)

        # --- Меню details_menu ---
        details_menu, _ = Menu.objects.get_or_create(name='details_menu')
        item1 = MenuItem.objects.create(menu=details_menu, title="Деталь 1", url="/details/1/")
        item2 = MenuItem.objects.create(menu=details_menu, title="Деталь 2", url="/details/2/")
        subitem = MenuItem.objects.create(menu=details_menu, title="Поддеталь", url="/details/2/sub/", parent=item2)

        # --- Меню help_menu ---
        help_menu, _ = Menu.objects.get_or_create(name="help_menu")
        faq = MenuItem.objects.create(menu=help_menu, title="FAQ", url="/help/faq/")
        support = MenuItem.objects.create(menu=help_menu, title="Поддержка", url="/help/support/")

        # >>> ДОБАВЛЯЕМ Page для всех урлов <<<

        urls_titles = [
            # (url, title)
            ("/about/", "О нас"),
            ("/services/", "Услуги"),
            ("/contact/", "Контакты"),
            ("/services/consult/", "Консультация"),
            ("/services/audit/", "Аудит"),
            ("/details/1/", "Деталь 1"),
            ("/details/2/", "Деталь 2"),
            ("/details/2/sub/", "Поддеталь"),
            ("/help/faq/", "FAQ"),
            ("/help/support/", "Поддержка"),
        ]

        for url, title in urls_titles:
            slug = url.strip("/")

            # Для главной страницы slug получается пустым, пропускаем
            if not slug:
                continue

            Page.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'page_title': title,
                    'content': f"<p>Тестовый контент для страницы <b>{title}</b> ({url})</p>"
                }
            )

        self.stdout.write(self.style.SUCCESS("Меню, пункты и страницы Page созданы!"))

from django.db import models
from datetime import datetime


class Base(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

    class Meta:
        abstract = True


class Region(Base):
    name = models.CharField(max_length=100, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регионы"
        verbose_name_plural = "Регионы"


class Brand(Base):
    name = models.CharField(max_length=100, verbose_name="Название")
    region = models.ForeignKey(Region, null=True, blank=False, on_delete=models.SET_NULL)
    uniq = models.CharField(max_length=100, verbose_name="Буква или номер", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Agent(Base):
    name = models.CharField(max_length=100, verbose_name="Имя")
    uniq = models.CharField(max_length=100, verbose_name="Буква или номер", null=True, blank=True)
    brand = models.ManyToManyField(Brand, verbose_name="Бренд")
    is_boss = models.BooleanField(default=False, verbose_name="Дополнительный функционал")
    is_permission = models.BooleanField(default=False, verbose_name="Выходные дни")
    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")

    def show_brand(self):
        return ",\n".join([g.name for g in self.brand.all()])

    show_brand.short_description = "Бренд"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Агент"
        verbose_name_plural = "Агенты"


class Project(Base):
    name = models.CharField(max_length=100, verbose_name="Название")
    uniq = models.CharField(max_length=100, verbose_name="Буква или номер")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд", related_name="project")
    signature = models.TextField(verbose_name="Тип документа")
    is_special = models.BooleanField(default=False, verbose_name="Спец пдф")
    file = models.FileField(verbose_name="Сертификат", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class Contract(Base):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Проект")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Агент")
    inn = models.CharField(max_length=50, verbose_name="ИНН")
    firm = models.CharField(max_length=50, verbose_name="Название фирмы", null=True)
    code = models.CharField(max_length=50, verbose_name="Номер")
    status = models.BooleanField(default=True, verbose_name="Подпись")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"


class Counter(Base):
    count = models.PositiveBigIntegerField(default=1, verbose_name="Счёт")
    year = models.PositiveIntegerField(default=int(datetime.now().strftime("%Y")))

    class Meta:
        verbose_name = "Счётчик для контрактов"
        verbose_name_plural = "Счётчик для контрактов"

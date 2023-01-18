from django.db import models
from django.db.models.manager import BaseManager
from django.utils import timezone
from django.db.models.query import QuerySet

from libs.db.models.fields import EnumField


class QuerySetNotDelete(QuerySet):
    def delete(self):
        # 级联软删 要打补丁，先不用
        self.update(is_deleted=True)


class NotDeleteManager(BaseManager.from_queryset(QuerySetNotDelete)):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def lock(self):
        """ Lock the table. """
        cursor = connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("LOCK TABLES %s WRITE" % table)
        row = cursor.fetchone()
        return row

    def unlock(self):
        """ Unlock the table. """
        cursor = connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("UNLOCK TABLES")
        row = cursor.fetchone()
        return row


class AbstractModels(models.Model):
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True

    def delete(self):
        # TODO 是否需要级连软删待定，。
        self.is_deleted = True
        self.save()

    objects = NotDeleteManager()
    all_objects = models.Manager()



class AbstractStatusModel():
    def __init__(self, status_transfer_map, status_attr, init_status,
                 enum_data):
        self.enum_data = enum_data
        self.status_transfer_map = status_transfer_map
        self.status_attr = status_attr
        self.init_status = init_status

    def __call__(self):
        status_transfer_map = self.status_transfer_map
        status_attr = self.status_attr
        enum_data = self.enum_data
        init_status = self.init_status

        def get_status_transfer_map_handled(attr_to_value_map, status_transfer_map):
            return {
                attr_to_value_map[k]: [attr_to_value_map[i] for i in v]
                for k, v in status_transfer_map.items()
            }

        class AnonymousModelClass(AbstractModels):
            # INIT_STATUS = init_status
            locals_instance = locals()
            # for k, v in status_settings.items():
            #     locals_instance[k] = v[0]
            # status_choice = tuple((v[0], v[1])
            #                       for k, v in status_settings.items())
            # RISK_STATUS_MAP = {v[0]: v[1] for k, v in status_settings.items()}

            # attr_to_value_map = {k: v[0] for k, v in status_settings.items()}

            status_transfer_map_handled = status_transfer_map

            # locals_instance[status_attr] = models.SmallIntegerField(
            #     choices=status_choice,
            #     default=init_status,
            #     help_text='状态'
            # )
            locals_instance[status_attr]  = EnumField(
                enum_data=enum_data,
                default=init_status,
                help_text='状态'
            )



            def __get_valid_status(self, status):
                return self.status_transfer_map_handled.get(status) or tuple()

            @property
            def valid_status(self):  # TODO:  动态属性
                return self.__get_valid_status(getattr(self, status_attr))

            def __setattr__(self, name, value):
                if name == status_attr and (getattr(self, '__status__', None) == None):
                    __status__ = self.__dict__.get(status_attr, None)
                    if __status__ != value:
                        self.__dict__['__status__'] = __status__
                return super().__setattr__(name, value)

            def save(self, force_insert=False, force_update=False, using=None,
                     update_fields=None):
                if self.__dict__.get('__status__', None):
                    assert getattr(self, status_attr) in \
                        self.__get_valid_status(
                            self.__status__), 'error {}'.format(status_attr)
                return super().save(force_insert, force_update,
                                    using, update_fields)

            class Meta:
                abstract = True

        return AnonymousModelClass

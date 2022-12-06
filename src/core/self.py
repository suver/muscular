from ..storage import StorageMapper
storageMapper = StorageMapper()


class Prop:
    pass


class Self(Prop):
    """
    Класс позволяющий добавить в объект ссылку на самого себя

    """

    _instance = None
    _name = None

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return self.app
    #
    # def __set__(self, obj, value):
    #     print('Updating %r to %r', obj, self.public_name, value)
    #     setattr(obj, self.private_name, value)

    # def __call__(self, *args, **kwargs):
    #
    #     import sys
    #     a = sys._getframe(1)
    #     print('---------------------->aaa', a)
    #     if 'self' in a.f_locals:
    #         print('---------------------->a.f_locals[self]', a.f_locals['self'])
    #     print('---------------------->a.f_globals', a.f_globals)
    #     name = inspect.stack()[1][3]
    #     print('====================')
    #     print(inspect.stack()[1])
    #     print('====================')
    #     print(inspect.stack()[1])
    #     print('====================')
    #     print(name)
    #     print('====================', globals())
    #     print(globals()[name])

    # def __str__(self) -> str:
    #     return self._instance.__name__

    def __deepcopy__(self, memo):
        return self.copy()

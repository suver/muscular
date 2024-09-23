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

    def __deepcopy__(self, memo):
        return self.copy()

from muscles import Model, Column, Key, String, Enum, Date, DateTime


class User(Model):
    id = Column(Key)
    name = Column(String, index=True)
    email = Column(String, index=True)
    status = Column(Enum(enum=['inactive', 'deleted', 'blocked', 'active']), index=True)
    birthday = Column(Date)
    created_at = Column(DateTime)

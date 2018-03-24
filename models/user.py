from flask import g
# from models import Model
from models import Model

Model = Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('username', str, ''),
            ('password', str, ''),
            ('nickname', str, ''),
            ('user_image', str, '/uploads/default.png'),
            ('bio', str, ''),
        ]
        return names

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        nickname = form['nickname']
        password = form['password']
        if len(name) > 2 and len(nickname)>2 and User.one(username=name) is None:
            password = User.salted_password(password)
            u = User.new(dict(
                username=name,
                password=password,
                nickname=nickname,
            ))
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(
            username=form['username'],
            password=User.salted_password(form['password'])
        )
        return user

    @classmethod
    def anonym(cls):
        u = User.one(username='Anonym')
        if u is None:
            form = dict(
                username='Anonym',
                password='Anonym',
                nickname='匿名用户',
            )
            u = User.new(form)
        return u

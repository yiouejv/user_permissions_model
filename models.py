from config import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from datetime import datetime

# 用户可能包括多个角色（运营，市场部人员），一个角色可能包含多个用户


class Permission(object):
    '''
      以255的二进制方式表示  1111 1111
    '''
    ALL_PERMISSION = 0b11111111
    # 1. 访问总权限
    VISITOR =        0b00000001  # 最后一位表示，访问权限
    # 2. 管理帖子权限
    POSTER =         0b00000010  # 倒数第二位
    # 3. 管理评论的权限
    COMMENTER =      0b00000100  # 倒数第三位
    # 4. 管理板块的权限
    BOARDER =        0b00001000  # 倒数第四位
    # 5. 管理前台用户的权限
    FRONTUSER =      0b00010000  # 倒数第五位
    # 6. 管理后台用户的权限
    ADMINUSER =      0b00100000  # 倒数第六位
    # 7. 管理后台管理员的权限
    ADMINER =        0b01000000  # 倒数第七位



role_user = Table(
    'role_user',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('user.id', Integer, ForeignKey('user.id'), primary_key=True)
)


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    desc = Column(String(200), nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    permissions = Column(Integer, default=Permission.VISITOR)
    users = relationship('User.id', secondary='role_user', backref=backref('roles'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    create_time = Column(DateTime, default=datetime.now)

    @property
    def permissions(self):
        if not self.roles:
            return 0
        else:
            all_permissions = 0
            for role in self.roles:
                all_permissions |= role.permissions
        return all_permissions

    def has_permissions(self, permissions):
        return self.permissions & permissions == permissions

    @property
    def is_developer(self):
        return self.has_permissions(Permission.ALL_PERMISSION)


def create_role():
    # 访问者（可以修改个人信息）
    visitor = Role(name='访问者', desc='只能访问相关数据不能修改')
    visitor.permissions = Permission.VISITOR

    # 运营人员
    operator = Role(name='运营', desc='可以管理帖子，评论, 管理前台用户')
    operator.permissions = Permission.VISITOR | Permission.POSTER | Permission.COMMENTER \
                           | Permission.BOARDER | Permission.FRONTUSER

    # 管理员(用户绝大部分权限)
    admin = Role(name='管理员', desc='拥有本系统所有权限。')
    admin.permissions = Permission.VISITOR | Permission.POSTER | Permission.COMMENTER \
                        | Permission.BOARDER | Permission.FRONTUSER | Permission.ADMINUSER

    # 开发者(拥有所有权限)
    developer = Role(name='开发者', desc='开发人员专用角色')
    developer.permissions = Permission.ALL_PERMISSION










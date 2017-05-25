# -*- coding: utf-8 -*-
import datetime
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

from . import BaseService
from guitar.models import UserModel, UserinfoModel, DynamicModel
from guitar.utils.tools import generate_uid


class UserService(BaseService):

    def get_users(self, id):
        users = self.session.query(UserModel).filter(
            UserModel.id!=id,
        ).all()
        return [user.to_dict() for user in users]

    def create_user(self, arguments):
        uid = 0
        while True:
            uid = generate_uid()
            user = self.session.query(UserModel).filter(
                UserModel.uid == uid).first()
            if user is None:
                uid = uid
                break
            continue
        user = UserModel(
            uid=uid,
            nickname=arguments.get('nickname'),
            email=arguments.get('email'),
            password=generate_password_hash(
                arguments.get('password')
            )
        )
        try:
            self.session.add(user)
            self.session.commit()
        except Exception as e:
            raise e
            self.session.rollback()
            self.session.close()
        return user.to_dict()

    def get_user_with_nickname(self, nickname):
        user = self.session.query(UserModel).filter(
            UserModel.nickname == nickname).first()
        self.session.close()

        if user is None:
            return None
        else:
            return user

    def get_user_with_email(self, email):
        user = self.session.query(UserModel).filter(
            UserModel.email == email).first()
        self.session.close()

        if user is None:
            return None
        else:
            return user

    def get_user_with_uid(self, uid):
        user = self.session.query(UserModel).filter(
            UserModel.uid == uid).first()
        self.session.close()

        if user is None:
            return None
        else:
            return user

    # 根据微信openid获取用户信息
    def get_user_with_openid(self, openid):
        user = self.session.query(UserModel).filter(
            UserModel.openid == openid).first()
        self.session.close()

        if user is None:
            return None
        else:
            return user

    def get_one_user(self, arguments):
        nickname_or_email = arguments.get('nickname_or_email')
        password = arguments.get('password')

        if '@' in nickname_or_email:
            user = self.get_user_with_email(nickname_or_email)
        else:
            user = self.get_user_with_nickname(nickname_or_email)

        if user and check_password_hash(user.password, password):
            return user
        else:
            return None

    def generate_confirmation_token(self, email, secret, password_salt):
        serializer = URLSafeTimedSerializer(secret)
        return serializer.dumps(
            email,
            salt=password_salt)

    def verify_email_token(self,
                           token, secret, password_salt, expiration=3600):
        serializer = URLSafeTimedSerializer(secret)
        try:
            email = serializer.loads(
                token,
                salt=password_salt,
                max_age=expiration)
        except:
            return False
        return email

    def update_user_state(self, email):
        user = self.session.query(UserModel).filter(
            UserModel.email == email).first()
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        self.session.add(user)
        self.session.commit()
        return user and user.to_dict()

    # 更改绑定学生信息状态
    def change_bind_school_status(self, uid):
        user = self.session.query(UserModel).filter(
            UserModel.uid == uid).first()
        user.is_bind_school = True
        self.session.add(user)
        self.session.commit()

    # 用户第一次登陆应用
    # 保存微信的用户信息
    def save_weixin_info(self, user_info={}):
        # 先保存uid
        uid = 0
        while True:
            uid = generate_uid()
            user = self.session.query(UserModel).filter(
                UserModel.uid == uid).first()
            if user is None:
                uid = uid
                break
            continue
        user = UserModel(
            confirmed=True,
            uid=uid,
            openid=user_info['openid'],
            avatar_url=user_info['headimgurl'].encode('utf8'),
            nickname=user_info['nickname'].encode('utf8')
        )
        self.session.add(user)
        self.session.commit()

        userInfo = self.session.query(UserinfoModel).filter(
            UserinfoModel.user == user).first()
        if userInfo is None:
            info = UserinfoModel(
                access_token=user_info['access_token'],
                token_refresh=user_info['refresh_token'],
                city=user_info['city'].encode('utf8'),
                user=user
            )
            self.session.add(info)
            self.session.commit()

    # 发表动态
    def publish_dynamic(self, uid, dynamic_content):
        user = self.session.query(UserModel).filter_by(
            uid=uid).first()
        dynamic = DynamicModel(
            content=dynamic_content['dynamicContent'],
            address_name=dynamic_content['addressName'],
            address_city=dynamic_content['addressCity'],
            img_url=dynamic_content['img_url'],
            user=user
        )
        try:
            self.session.add(dynamic)
            self.session.commit()
        except:
            self.session.rollback()
        else:
            return True
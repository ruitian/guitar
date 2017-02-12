# -*- coding: utf-8 -*-
from werkzeug import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

from . import BaseService
from guitar.models import UserModel


class UserService(BaseService):

    def get_users(self):
        users = self.session.query(UserModel).all()
        return [user.to_dict() for user in users]

    def create_user(self, arguments):
        user = UserModel(
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

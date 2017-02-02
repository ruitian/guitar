# -*- coding: utf-8 -*-


class Code(object):

    INTERNAL_ERROR = (10000, u'内部系统错误')
    API_REQUEST_ERROR = (10003, u'内部接口调用出错')
    RESOURCE_NOT_FOUND = (10004, u'资源没找到')

    COMMON_ERROR = (20000, u'服务通常错误')

    INPUT_ERROR = (20100, u'参数错误')
    INPUT_MISSING = (20101, u'缺少必需参数')
    INPUT_TYPE_INVALID = (20102, u'参数类型错误')
    INPUT_VALUE_INVALID = (20103, u'参数值不被允许')
    INPUT_REDUNDANT = (20104, u'参数多余')
    INPUT_TOO_MANY = (20105, u'输入参数过多')
    INPUT_LT_MIN = (20106, u'输入值小于最小允许值')
    INPUT_GT_MAX = (20107, u'输入值大于最大允许值')
    INPUT_LT_MIN_LEN = (20108, u'输入值不满足最小长度')
    INPUT_GT_MAX_LEN = (20109, u'输入值超过最大长度')
    INPUT_LT_MIN_LIST_LEN = (20110, u'输入数组长度不足')
    INPUT_GT_MAX_LIST_LEN = (20111, u'输入数组超长')
    INPUT_NOT_IN_CHOICES = (20112, u'输入值不在允许值范围')
    INPUT_GROUP_ERROR = (20113, u'输入不满足组合定义')


class BaseError(Exception):
    default = Code.INTERNAL_ERROR

    def __init__(self, code_tuple=None, msg=None, **kwargs):
        if not code_tuple:
            code_tuple = self.__class__.default
        self.code = code_tuple[0]

        if msg:
            if not isinstance(msg, unicode):
                msg = unicode(msg, 'utf-8', 'replace')

            if kwargs.get('combine_messages'):
                self.msg = u'%s: %s' % (code_tuple[1], msg)
            else:
                self.msg = msg
        else:
            self.msg = code_tuple[1]

        self.data = kwargs.get('data')

    def __unicode__(self):
        return u'%s: %s' % (self.code, self.msg)

    def __str__(self):
        return self.msg.encode('utf8')


class InternetError(BaseError):
    default = Code.INTERNAL_ERROR


class InternalError(BaseError):
    default = Code.INTERNAL_ERROR


class APIRequestError(InternetError):
    default = Code.API_REQUEST_ERROR

    def __init__(self,
                 code_tuple=Code.INTERNAL_ERROR, msg='',
                 request=None, response=None):
        self.request = request
        self.response = response
        super(self.__class__, self).__init__(code_tuple, msg)


class CommonError(BaseError):
    default = Code.COMMON_ERROR


class InputError(CommonError):
    default = Code.INPUT_ERROR

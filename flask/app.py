from flask import Flask, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
# 设置可以跨域访问
CORS(app, supports_credentials=True)


# key是用户名，value是token
username_tokens = {}


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    # 获取客户端发送的用户名、密码参数
    username = request.json.get('username')
    password = request.json.get('password')

    # TODO 正常做法：去数据库中查询用户名、密码是否正确
    if 'likeileen666' != username:
        return {
            'code': 4000,
            'msg': '用户名错误'
        }

    if '666666' != password:
        return {
            'code': 4001,
            'msg': '密码错误'
        }

    # 使用uuid作为token
    token = str(uuid.uuid1())
    username_tokens[username] = token
    return {
        'code': 0,
        'msg': '登录成功',
        'data': {
            'token': token
        }
    }


# 退出登录接口
@app.route('/logout', methods=['POST'])
def logout():
    # 从请求头中获取用户的token信息
    token = request.headers.get('Token')
    # 根据token找到用户名
    username = ''
    for key, value in username_tokens.items():
        if value == token:
            username = key
            break
    # 删除token
    del username_tokens[username]
    return {
        'code': 0,
        'msg': '退出登录成功'
    }


# 接收客户端发送的图片数据，进行图像解析
@app.route('/test', methods=['POST'])
def test():
    # 从请求头中获取用户的token信息
    token = request.headers.get('Token')
    exists = False
    for key, value in username_tokens.items():
        if value == token:
            exists = True
            break

    # token不存在
    if not exists:
        return {
            'code': 4002,
            'msg': 'Token无效'
        }

    # token存在
    # 获取客户端发送的图片数据
    image_base64 = request.json.get('image')

    # TODO 调用算法对图像进行解析

    return {
        'code': 0
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
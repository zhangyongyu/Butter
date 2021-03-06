from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
    abort,
    g,
)
from werkzeug.utils import secure_filename
from models.user import User
import os
import uuid

from routes import *
from utils import log
from models.topic import Topic
from models.board import Board

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    board_id = request.args.get('board_id', 'all')
    if board_id == 'all':
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)

    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user = u)


@main.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        # 用类函数来判断
        u = User.register(form)
        return redirect(url_for('index.login'))
    else:
        u = current_user()
        return render_template("register.html", user=u)


@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        u = User.validate_login(form)
        print('login u', u)
        if u is None:
            # 转到 topic.index 页面
            return redirect(url_for('topic.index'))
        else:
            # session 中写入 user_id
            session['user_id'] = u.id
            print('login', session)
            # 设置 cookie 有效期为 永久
            session.permanent = True
            return redirect(url_for('topic.index'))
    else:
        u = current_user()
        return render_template("login.html", user=u)

@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def valid_suffix(suffix):
    valid_type = ['jpg', 'png', 'jpeg','JPG','PNG','JPEG']
    return suffix in valid_type



@main.route('/user/<id>')
def user_detail(id):
    u = User.one(id)
    if u is None:
        abort(404)
    else:
        ts = sorted(User.topics(u), key=lambda x:x.ct, reverse=True)
        rs = sorted(User.replies(u), key=lambda x:x.ct, reverse=True)
        rts = []
        for r in rs:
            rts.append(r.topic())
        return render_template('profile.html', user=u, topics=ts, reply_titles=rts)


@main.route('/settings', methods=['GET', 'POST'])
def settings():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('settings.html', user=u)


@main.route('/changepsd', methods=["POST"])
def changepsd():
    u = current_user()
    old_psd = request.form['old_psd']
    form = dict(
        password=old_psd,
        username=u.username
    )
    if User.validate_login(form):
        User.update(u.id, dict(
            password=User.salted_password(request.form['psd'])
        ))
    return redirect(url_for(".settings"))



@main.route('/changeprofile', methods=["POST"])
def changeprofile():
    u = current_user()
    form = request.form
    User.update(u.id, dict(
        username=form['username'],
        bio=form['bio'],
    ))
    return redirect(url_for(".settings"))


@main.route('/image/add', methods=["POST"])
def add_img():
    # file 是一个上传的文件对象
    file = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    if valid_suffix(suffix):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        # filename = secure_filename(file.filename)
        filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
        file.save(os.path.join('user_image', filename))
        u = current_user()
        User.update(u.id, dict(
            user_image='/uploads/{}'.format(filename)
        ))
        log('u.img:::', u.user_image)

    return redirect(url_for(".settings"))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory('user_image', filename)

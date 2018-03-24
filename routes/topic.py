from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *
import json

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


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


@main.route('/<string:id>')
def detail(id):
    m = Topic.find(id=id)
    u = current_user()
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, user=u)


@main.route("/add", methods=["POST"])
# @login_required
@csrf_required
def add():
    form = request.form
    u = current_user()
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))


@main.route("/delete")
@csrf_required
def delete():
    id = request.args.get('id')
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = request.args.get('board_id')
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id, user=u)

import re
import uuid

from flask import abort, flash, redirect, render_template, request

from . import app, db
from .forms import URLMapForm
from .models import URL_map


PATTERN = re.compile("[A-Za-z0-9]+")


def get_unique_short_id():
    while True:
        short_link = str(uuid.uuid4())[:6]
        if not URL_map.query.filter_by(short=short_link).first():
            break

    return short_link


def check_short_id(short_id, api=False):
    if URL_map.query.filter_by(short=short_id).first():
        if api:
            return False, f'Имя "{short_id}" уже занято.'
        return False, f'Имя {short_id} уже занято!'
    if len(short_id) > 16 or not PATTERN.fullmatch(short_id):
        return False, 'Указано недопустимое имя для короткой ссылки'

    return True, ''


@app.route('/<string:id>')
def redirect_view(id):
    url_obj = URL_map.query.filter_by(short=id).first()

    if not url_obj:
        abort(404)

    original_link = url_obj.original
    return redirect(original_link)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()

    if form.validate_on_submit():
        short_id = form.custom_id.data

        if short_id:
            is_valid, message = check_short_id(short_id)
            if not is_valid:
                flash(message)
                return render_template('yacut.html', form=form)
        else:
            short_id = get_unique_short_id()

        url_map = URL_map(
            original=form.original_link.data,
            short=short_id
        )

        db.session.add(url_map)
        db.session.commit()

        flash_message = (f'Ваша новая ссылка готова:\n'
                         f'<a href="{request.url_root}{short_id}">'
                         f'{request.url_root}{short_id}</a>')

        flash(flash_message)
        return render_template('yacut.html', form=form)

    return render_template('yacut.html', form=form)

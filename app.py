from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

# app settings
app = Flask(__name__)
app.config['SECRET_KEY'] = '67cbe9e9-bdde-48f1-bf95-d0938e76713e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:A5x67!qw@localhost/bible?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# db models


class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    order = db.Column(db.Integer)
    books = db.relationship('Book')

    def __init__(self, name, order):
        self.name = name
        self.order = order


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    number = db.Column(db.Integer)
    volumeId = db.Column(db.Integer, db.ForeignKey('volume.id'))
    chapters = db.relationship('Chapter')

    def __init__(self, name, number, volumeId):
        self.name = name
        self.number = number
        self.volumeId = volumeId


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    subtext = db.Column(db.String(45))
    number = db.Column(db.Integer)
    bookId = db.Column(db.Integer, db.ForeignKey('book.id'))
    verses = db.relationship('Verse')

    def __init__(self, name, subtext, number, bookId):
        self.name = name
        self.subtext = subtext
        self.number = number
        self.bookId = bookId


class Verse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    title = db.Column(db.String(45))
    number = db.Column(db.Integer)
    chapterId = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def __init__(self, text, title, number, chapterId):
        self.text = text
        self.title = title
        self.number = number
        self.chapterId = chapterId


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'verb' in request.form.keys():
            rec = Volume.query.get(request.form['id'])
            if request.form['verb'] == 'delete':
                # delete
                db.session.delete(rec)
                db.session.commit()

                flash('Volume deleted!')
                return redirect(url_for('index'))
            else:
                # update
                rec.name = request.form['name']
                rec.order = request.form['order']

                db.session.commit()

                flash('Volume updated!')
                return redirect(url_for('index'))
        # add new
        rec = Volume(request.form['name'], request.form['order'])

        db.session.add(rec)
        db.session.commit()

        flash('Volume added!')
        return redirect(url_for('index'))

    data = Volume.query.order_by(Volume.order.asc()).all()
    breadcrumb = """<a href="/">Home</a>"""
    return render_template('index.html', data=data, breadcrumb=breadcrumb)


@app.route('/volume/<int:id>', methods=['GET', 'POST'])
def volume(id):
    if request.method == 'POST':
        if 'verb' in request.form.keys():
            rec = Book.query.get(request.form['id'])
            if request.form['verb'] == 'delete':
                # delete
                db.session.delete(rec)
                db.session.commit()

                flash('Book deleted!')
                return redirect(url_for('volume', id=id))
            else:
                # update
                rec.name = request.form['name']
                rec.number = request.form['number']

                db.session.commit()

                flash('Book updated!')
                return redirect(url_for('volume', id=id))
        # add new
        rec = Book(request.form['name'], request.form['number'], id)

        db.session.add(rec)
        db.session.commit()

        flash('Book added!')
        return redirect(url_for('volume', id=id))

    data = Volume.query.get(id)
    breadcrumb = """<a href="/">Home</a><span>></span><a href="/volume/""" + \
        str(id) + """">Volume</a>"""
    return render_template('volume.html', data=data, breadcrumb=breadcrumb)


@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book(id):
    if request.method == 'POST':
        if 'verb' in request.form.keys():
            rec = Chapter.query.get(request.form['id'])
            if request.form['verb'] == 'delete':
                # delete
                db.session.delete(rec)
                db.session.commit()

                flash('Chapter deleted!')
                return redirect(url_for('book', id=id))
            else:
                # update
                rec.name = request.form['name']
                rec.subtext = request.form['subtext']
                rec.number = request.form['number']

                db.session.commit()

                flash('Chapter updated!')
                return redirect(url_for('book', id=id))
        # add new
        rec = Chapter(
            request.form['name'], request.form['subtext'], request.form['number'], id)

        db.session.add(rec)
        db.session.commit()

        flash('Chapter added!')
        return redirect(url_for('book', id=id))

    data = Book.query.get(id)
    breadcrumb = """<a href="/">Home</a><span>></span><a href="/volume/""" + \
        str(data.volumeId) + """">Volume</a><span>></span><a href="/book/""" + \
        str(id) + """">Book</a>"""
    return render_template('book.html', data=data, breadcrumb=breadcrumb)


@app.route('/chapter/<int:id>', methods=['GET', 'POST'])
def chapter(id):
    if request.method == 'POST':
        if 'verb' in request.form.keys():
            rec = Verse.query.get(request.form['id'])
            if request.form['verb'] == 'delete':
                # delete
                db.session.delete(rec)
                db.session.commit()

                flash('Verse deleted!')
                return redirect(url_for('chapter', id=id))
            else:
                # update
                rec.text = request.form['text']
                rec.title = request.form['title']
                rec.number = request.form['number']

                db.session.commit()

                flash('Verse updated!')
                return redirect(url_for('chapter', id=id))
        # add new
        rec = Verse(
            request.form['text'], request.form['title'], request.form['number'], id)

        db.session.add(rec)
        db.session.commit()

        flash('Verse added!')
        return redirect(url_for('chapter', id=id))

    data = Chapter.query.get(id)
    book = Book.query.get(data.bookId)
    breadcrumb = """<a href="/">Home</a><span>></span><a href="/volume/""" + \
        str(book.volumeId) + """">Volume</a><span>></span><a href="/book/""" + \
        str(data.bookId) + """">Book</a><span>></span><a href="/chapter/""" + \
        str(id) + """">Chapter</a>"""
    return render_template('chapter.html', data=data, book=book, breadcrumb=breadcrumb)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)

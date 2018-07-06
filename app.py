from flask import Flask , render_template, request,redirect,url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'Your Database'
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
db = SQLAlchemy(app)

# models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime , nullable=False, default=datetime.utcnow)
    language_code = db.Column(db.String, db.ForeignKey('lang.code'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.relationship('Post', backref='project', lazy=True)  

class Lang(db.Model):
    code = db.Column(db.String(3),primary_key=True)
    name = db.Column(db.String(10),unique=True, nullable=False)
    post_id = db.relationship('Post', backref='translate', lazy=True)

    def __repr__(self):
        return f"Lang('{self.code}', '{self.name}')"

# Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for("index",lang="en"))

# routes
@app.route('/<string:lang>', methods=['GET', 'POST'])
def index(lang):  
    form = PostForm()
    if lang == 'en':
        posts = Post.query.filter(Post.language_code == 'en').order_by(Post.project_id.desc()) 
        if form.validate_on_submit():
                project_id = project.query.order_by(project.id.desc()).first().id
                title = form.title.data
                content = form.content.data
                pro = project(id=project_id+1)
                db.session.add(pro)
                db.session.commit()
                post = Post(title=title,content=content,language_code='en',project_id=project_id+1)
                db.session.add(post)
                db.session.commit()
                return redirect( url_for('index',lang='en') )
        return render_template('en/index.html', posts=posts,form=form,lang=lang)
    
    if lang == 'ar': 
        posts = Post.query.filter(Post.language_code == 'ar').order_by(Post.project_id.desc()) 
        if form.validate_on_submit():
                # return last project 
                project_id = project.query.order_by(project.id.desc()).first().id
                title = form.title.data
                content = form.content.data
                pro = project(id=project_id+1)
                db.session.add(pro)
                db.session.commit()
                post = Post(title=title,content=content,language_code='ar',project_id=project_id+1)
                db.session.add(post)
                db.session.commit()
                return redirect( url_for('index',lang='ar') )
        return render_template('ar/index.html', posts=posts,form=form,lang=lang)
    else:
        posts = Post.query.filter(Post.language_code == 'en').order_by(Post.id.desc()) 
        return render_template('en/index.html', posts=posts,form=form,lang=lang)

# translation page route
@app.route('/<string:lang>/translate/<int:post_id>', methods=['GET', 'POST'])
def translate(lang,post_id):
    form = PostForm()
    post=Post.query.get_or_404(post_id)
    # (ar) to (en)
    if lang == 'ar':
        if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                pro = project(id=post.project_id)
                post = Post(title=title,content=content,language_code='en',project_id=pro.id)
                db.session.add(post)
                db.session.commit()
        return render_template('ar/translate.html', form=form,post=post)
    else:
        #  (en) to (ar)
        if form.validate_on_submit():
                title = form.title.data
                content = form.content.data
                pro = project(id=post.project_id)
                post = Post(title=title,content=content,language_code='ar',project_id=pro.id)
                db.session.add(post)
                db.session.commit()
        return render_template('en/translate.html',form=form,post=post)


if __name__  == '__main__':
    app.run(debug=True)
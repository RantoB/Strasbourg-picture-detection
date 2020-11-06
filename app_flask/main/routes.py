import secrets
import os
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from main import app, db, bcrypt
from main.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from main.models import User, Post

infos_1 = [
    {
        'content': "Vous pouvez tester l'algorithme en postant une photo \
                    d'un de ces lieux. La photo doit être prise du sol. \
                    Le batiment ou la statue doivent être vus de \
                    face et doivent se trouver plus ou moins au centre \
                    de l'image."
    },
    {
        'content': "N'hésitez pas à tester avec d'autres images pour voir \
                    si l'algorithme remarque bien qu'il ne s'agit d'aucun \
                    des monuments qu'il connait."
    },
    {
        'content': "Note: c'est un projet en cours de développement. \
                    La collecte de données est en cours et le nombre \
                    de lieux identifiables va augmenter."
    },
]

infos_2 = [
    {
        'content':  "- L'application est développée en Python avec le framework \
                    Flask. L'image Docker de l'application est disponible sur \
                    Dockerhub: rantob/image_reco_stras. L'application est \
                    déployée sur Cloud Run de Google Cloud Platform."
    },
    {
        'content': "Autres projets: "
    },
    {
        'content': "- Dashboard de production d'électricité en France et modèle \
                    de prédiction de la demande d'électricité déployé en \
                    prototype sur Heroku: electricity demand model"
    },
    {
        'content': "- Jeux de piste géants au centre ville de Strasbourg: \
                    ENIGMA Strasbourg. Ainsi que son chatbot développé avec \
                    RASA et déployé avec docker-compose sur Google Compute \
                    Engine de Google Cloud Platform."
    },
    {
        'content': "Développé par Bertrand BURCKER"
    },
]


@app.route("/")
def accueil():
    return render_template('accueil.html',
                           infos_1=infos_1,
                           infos_2=infos_2)


@app.route("/articles")
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=2)
    return render_template('posts.html',
                           posts=posts,
                           title='Articles')

@app.route("/user/<string:username>")
def posted_by(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date.desc())\
        .paginate(page=page, per_page=2)
    return render_template('user_articles.html',
                           posts=posts,
                           title='Articles', user=user)


@app.route("/statues")
def page_statues():
    return render_template('page.html',
                           title='Statues de Strasbourg')


@app.route("/monuments")
def page_monuments():
    return render_template('page.html',
                           title='Monuments de Strasbourg')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'{form.username.data}, votre espace a bien été créé avec succès.', 'success')
        return redirect(url_for('accueil'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # to redirect to the page the user tried to access to
            next_page = request.args.get('next')
            flash('Vous êtes connecté à votre espace perso.', 'success')
            return redirect(next_page) if next_page else redirect(url_for("accueil"))
        else:
            flash(
                'Echec de la connextion, vérifiez votre adresse e-mail ou votre mot de passe.', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('accueil'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static',
                                'profile_pics', picture_filename)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Vos informations personnelles ont été mises à jour.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username # populate the form with current values
        form.email.data = current_user.email # populate the form with current values
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Mon espace perso',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, 
                    content=form.content.data, 
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Votre article a été posté avec succès', 'success')
        return redirect(url_for('posts'))
    return render_template('create_post.html',
                           title='Nouvel article', form=form,
                           legend='Nouvel article')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('article.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        db.session.commit()
        flash('Votre article a bien été mis à jour.', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title # populate the form with current values
        form.content.data = post.content # populate the form with current values
    return render_template('create_post.html',
                           title='Modifier l\'article', form=form, 
                           legend='Modifier l\'article')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Votre article a bien supprimé.', 'success')
    return redirect(url_for('accueil'))
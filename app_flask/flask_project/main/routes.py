import logging
import os
from flask import Blueprint, render_template, url_for, redirect, request
from flask_project.main.forms import PictureForm
from flask_project.main.utils import (infos_1, infos_2, pic_names, picture_examples,
                                        save_picture, result_for_user)

logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def accueil():

    picture_ex = picture_examples()
    form = PictureForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
        return redirect(url_for('main.image_reco', picture_filename=picture_filename))
    else:
        picture_filename = '1.cathedrale-15.jpeg'
        result = 'Voici la Cathédrale Notre Dame de Strasbourg'

    return render_template('accueil.html',
                            picture_ex=picture_ex,
                            picture_filename=picture_filename,
                            result=result,
                            form=form,
                            infos_1=infos_1,
                            infos_2=infos_2)

@main.route("/<string:picture_filename>", methods=["GET", "POST"])
def image_reco(picture_filename):
    picture_ex = picture_examples()

    result = result_for_user(picture_filename)

    form = PictureForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
        return redirect(url_for('main.image_reco', picture_filename=picture_filename))

    return render_template('accueil.html',
                            picture_ex=picture_ex,
                            picture_filename=picture_filename,
                            result=result,
                            form=form,
                            infos_1=infos_1,
                            infos_2=infos_2)

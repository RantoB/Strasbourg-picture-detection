from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

@pages.route("/bertrandburcker")
def page_statues():
    return render_template('bertrandburcker.html',
                           title='Bertrand BURCKER')

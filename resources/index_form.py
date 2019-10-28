from flask_wtf import Form
from wtforms import StringField,validators

class SearchForm(Form):
    searchstr = StringField('searchstr',validators=[validators.DataRequired()])
from wtforms import Form
from wtforms import StringField, HiddenField, validators, SelectField
from wtforms.validators import Required
from flask_babel import gettext

class UrlForm(Form):
	labelURL = gettext(u"Enter URL corresponding to the content: ")
	url = StringField (labelURL,
		[
			Required(message = gettext(u"Please, indicate a url.")),
			validators.length(min=4, message= gettext(u"Please, enter a valid value (it must be a URL)."))
		])

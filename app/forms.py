from flask_wtf import Form
from wtforms import FloatField, SubmitField, StringField, IntegerField, RadioField
from wtforms.validators import NumberRange, Required, AnyOf, Optional

#Slew to a user input RA Dec
class obs_stats(Form):
	exptime = StringField('Single Exptime (separated by commas if multiple)',default = '450,360,180',validators = [Required()]) 
	limmags = StringField('Single Exp lim. mag',default='21.0,20.5,19.5',validators = [Required()])
	tiling_times = StringField('Total time available for tiling (days)',default='2.0,3.0,4.0',validators = [Required()])
	frac_areas_covered = StringField('Localisation probabilities covered for each exptime')
	distance = FloatField('LIGO distance [Mpc]',default='150.0',validators = [Required()])
	submit_obsstats = SubmitField('Generate')


class results_fdets(Form):
	fdets = StringField('Detected Fraction',render_kw = {'readonly': True})
from app import app
from flask import Flask
from flask import render_template, request, flash, redirect, url_for, session
from .forms import obs_stats, results_fdets
from datetime import datetime
import time
import json
import os
from astropy.time import Time
import sys
sys.path.append('.')
import flask
from .calc_fdet import calc_fdets_grid, calculate_multiple_fdets
import numpy as np


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['JSON_FOLDER'] = os.path.join(APP_ROOT,'static/json/')
app.config['IMG_FOLDER'] = 'static/img/'
app.config['JSON_RELATIVE_FOLDER'] = 'static/json/'
print(app.config['JSON_FOLDER'])


@app.route('/', methods=['GET', 'POST'])
def index():
    form_calc_fdet = obs_stats(prefix='form_calc_fdet')
    form_fdets = results_fdets(prefix='form_fdets')

    fdets = []
    imagenames = []
    if form_calc_fdet.submit_obsstats.data and form_calc_fdet.validate():
        tiling_times = np.array(form_calc_fdet.tiling_times.data.split(','),dtype=float)
        exposure_times = np.array(form_calc_fdet.exptime.data.split(','),dtype=float)
        limmags = np.array(form_calc_fdet.limmags.data.split(','),dtype=float)
        frac_areas = form_calc_fdet.frac_areas_covered.data.split(',')
        if frac_areas[0]!='':
            frac_areas = np.array(frac_areas,dtype=float)
        else:
            frac_areas = None
        distance = float(form_calc_fdet.distance.data)

        fdets, imagenames = calculate_multiple_fdets(tiling_times,limmags,exposure_times,distance,locfracs_covered=frac_areas)
        print(fdets)
        form_fdets.fdets.data = fdets

    return render_template('index.html',form_calc_fdet = form_calc_fdet,form_fdets = form_fdets,imagenames=imagenames)


if __name__=='__main__':
	app.run(host='127.0.0.1',port='8000')
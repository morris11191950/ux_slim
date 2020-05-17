from flask import render_template, jsonify, json
from . import literature
from flask_login import login_required, current_user
from ..models import Queries

@literature.route('/literature/districts_all')
def districts_all():
    rows = Queries().districts_all()
    jsonStr = json.dumps(rows)
    j = jsonify(Districts=jsonStr)
    return j

@literature.route('/literature/categories_all')
def categories_all():
    rows = Queries().categories_all()
    #print('In literature views ', rows)
    jsonStr = json.dumps(rows)
    j = jsonify(Categories=jsonStr)
    return j

@literature.route('/literature/specialCollections_all')
def specialCollections_all():
    #print('I made it to special collections')
    rows = Queries().specialCollections_all()
    jsonStr = json.dumps(rows)
    j = jsonify(SpecialCollections=jsonStr)
    return j

@literature.route('/literature/references_by_district/<int:district_id>')
def references_by_district(district_id):
    #print('Views - References by district ', district_id)
    rows = Queries().references_by_district(district_id)
    jsonStr = json.dumps(rows)
    j = jsonify(Refs=jsonStr)
    return j

@literature.route('/literature/references_by_category/<int:category_id>')
def references_by_category(category_id):
    #print('In literature views: references by category ')
    rows = Queries().references_by_category(category_id)
    #print('In literature views: references by category ', rows)
    jsonStr = json.dumps(rows)
    j = jsonify(Refs=jsonStr)
    return j

@literature.route('/literature/references_by_specialCollection/<int:spcol_id>')
def references_by_specialCollection(spcol_id):
    #print('Views:references_by_specialCollection spcol_id', spcol_id)
    rows = Queries().references_by_specialCollection(spcol_id)
    jsonStr = json.dumps(rows)
    j = jsonify(Refs=jsonStr)
    return j

##########################################################################
##########################################################################
# LITERATURE EDITS
##########################################################################
##########################################################################



##########################################################################
##########################################################################
# LITERATURE PDFs
##########################################################################
##########################################################################
@literature.route('/literature/url_pdf/<id>')
def url_pdf(id):
    row = Queries().url_pdf(id)
    jsonStr = json.dumps(row)
    j = jsonify(Url=jsonStr)
    return j

# THIS MUST BE AT BOTTOM!
@literature.route('/literature')
@login_required
def literature():
    #print('In literature views ')
    return render_template('literature/literature.html')

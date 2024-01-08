from application import cache,user_datastore,db,bcrypt,Role
from flask import Blueprint,send_from_directory,jsonify
from application.configuration import root_path
from celery.result import AsyncResult

application=Blueprint('application',__name__,static_folder='static')

@cache.memoize(timeout=30)
@application.get('/svg/<filename>')
def svg_provider(filename):
    return send_from_directory('static',f'{filename}.svg')

@application.get('/csv/<id>')
def csv_provider(id):
    job_result=AsyncResult(id)
    path=f'{root_path}/temp/'
    if job_result.ready():
        filename=job_result.result
        return send_from_directory(path,filename)
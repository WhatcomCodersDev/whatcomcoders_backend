import collections 

collections.Iterable = collections.abc.Iterable 

from flask import Blueprint, jsonify, request
from flask.globals import request

from app.services import firestore_db

bp = Blueprint("directory", __name__)

@bp.route("/api/directory/getStudents")
def get_students():
    students = firestore_db.get_all_students()
    return jsonify(students)

@bp.route("/api/directory/getAlumni")
def get_alumni():
    alumni = firestore_db.get_all_alumni()
    return jsonify(alumni)

@bp.route("/api/directory/getMentors")
def get_mentors():
    mentors = firestore_db.get_all_mentors()
    return jsonify(mentors)

@bp.route("/api/directory/getMeetMeFor")
def get_meet_me_for():
    filter = request.args.get('filter')
    meet_me_for = firestore_db.get_all_meet_me_for(filter)
    return jsonify(meet_me_for)

@bp.route("/api/directory/getAreasOfExpertise")
def get_areas_of_expertise():
    filter = request.args.get('filter')
    areas_of_expertise = firestore_db.get_all_areas_of_expertise(filter)
    return jsonify(areas_of_expertise)

@bp.route("/api/directory/getSkills")
def get_skills():
    filter = request.args.get('filter')
    skills = firestore_db.get_all_skills(filter)
    return jsonify(skills)

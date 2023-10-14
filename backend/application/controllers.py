from flask import Flask, request, send_file
from flask import render_template
from main import app as app

from application import tasks
from flask_sse import sse

print("in controller app", app)



@app.route("/export_csv_venue/<venue_id>", methods=["GET", "POST"])
def export_csv_venue(venue_id):
    task =  tasks.export_csv_venues.delay(venue_id)
    result = task.get()
    if(result is None):
        return {"message" : "Venue not Found"}, 404
    return send_file(result, attachment_filename=f"venue_{venue_id}_details.csv", as_attachment=True)

@app.route("/export_csv_show/<show_id>", methods=["GET", "POST"])
def export_csv_show(show_id):
    task =  tasks.export_csv_shows.delay(show_id)
    result = task.get()
    if(result is None):
        return {"message" : "Show not Found"}, 404
    return send_file(result, attachment_filename=f"venue_{show_id}_details.csv", as_attachment=True)



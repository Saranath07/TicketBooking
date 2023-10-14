import time
from application.workers import celery
from flask import current_app as app
from .models import Users, Venue, Shows, ShowVenue, Bookings
from celery.schedules import crontab
from .database import db
from .send_email import send_email
from jinja2 import Template
import csv
from weasyprint import HTML
import time

print("crontab ", crontab)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    
    
    # sender.add_periodic_task(5.0, periodic_tasks.s(), name='add every 10')
    sender.add_periodic_task(20.0, send_monthly_reminder.s(), name='add every 20')
    sender.add_periodic_task(5.0, send_daily_reminder.s(), name='add every 5')
    # sender.add_periodic_task(15.0, check_movie_prices.s(), name='add every 15')

   
     
# @celery.task()
# def periodic_tasks():
#     # check_movie_prices()
#     send_monthly_reminder()
#     send_daily_reminder()
#     return "Tasks completed successfully"


@celery.task()
def check_movie_prices():
   
    showvenues = ShowVenue.query.all()
    for showvenue in showvenues:
        venue = Venue.query.filter_by(venue_id = showvenue.venue_id).first()
        total_seats = venue.capacity
        available_seats = showvenue.available_seats
        ratio = available_seats / total_seats
        print(ratio)
        if ratio < 0.6:
            showvenue.price += 0.01 * showvenue.price
            
        elif ratio < 0.75:
            showvenue.price += 0.025 * showvenue.price
        db.session.commit()
    return "Price check done successfully"

@celery.task()
def send_daily_reminder():
   
    now = time.time()
    threshold = now - 10 #now - 24 * 60 * 60

    print(threshold)
   
    inactive_users = Users.query.filter(Users.lastseen < threshold).all()
    template_file = "emails/example.html"
    for user in inactive_users:
        
        with open(template_file) as f:
            template = Template(f.read())
            message =  template.render(data = user)
        
        
        send_email(user.email, message, subject="Daily Remainder")

    return len(inactive_users)

def format_report(template_file, data={}, movies={}, venues={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data, movies = movies, venues = venues)

def create_pdf_report(data, template_html, movies, venues):
    message = format_report(template_html, data = data, movies = movies, venues = venues)
    html = HTML(string = message)
    file_name = f"PDF_files/{str(data.name)}.pdf"
    print(file_name)
    html.write_pdf(target = file_name)


def generate_monthly_reminder(user_id):
    
    bookings = Bookings.query.filter_by(user_id=user_id).all()
    movie_counts = {}
    venue_counts = {}

    for booking in bookings:
        showvenue_id = booking.showvenue_id
        showvenue = ShowVenue.query.filter_by(showvenue_id = showvenue_id).first()
        show = Shows.query.filter_by(show_id = showvenue.show_id).first()
        movie_name = show.show_name
        movie_counts[movie_name] = movie_counts.get(movie_name, 0) + 1
        venue = Venue.query.filter_by(venue_id = showvenue.venue_id).first()
        venue_counts[venue.venue_name] = venue_counts.get(venue.venue_name, 0) + 1



    
   
    return movie_counts, venue_counts


    


@celery.task()
def send_monthly_reminder():
    
    users = Users.query.all()
    
    for user in users:
        if user.role == 'user':
            shows, venues = generate_monthly_reminder(user.public_id)
            template_file = "templates/monthly_remainder.html"
            with open(template_file) as f:
                template = Template(f.read())
                message =  template.render(data = user, movies = shows, venues = venues)
            
            create_pdf_report(user, template_file, shows, venues)
            file_name = f"PDF_files/{str(user.name)}.pdf"
            
            print(file_name)
            send_email(user.email, message, subject=f"Monthly Report {user.name}", attachment_file=file_name)

    return len(users)



@celery.task()
def export_csv_venues(venue_id):
    venue = Venue.query.filter_by(venue_id = venue_id).first()
    showvenue = ShowVenue.query.filter_by(venue_id = venue_id).all()
    no_of_shows = len(showvenue) 
    
    filename = f"{venue.venue_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Venue Name', 'Location', 'Capacity', 'Description', 'No. of Shows'])
        
        writer.writerow([venue.venue_name, venue.region, venue.capacity, venue.venue_description, no_of_shows])
    return filename

@celery.task()
def export_csv_shows(show_id):
    show = Shows.query.filter_by(show_id = show_id).first()
    
    
    filename = f"{show.show_id}.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Show Name', 'Ratings', 'Tags', 'Description'])
        
        writer.writerow([show.show_name, show.ratings, show.tags, show.show_description])
    return filename




import os
from flask import Flask
from flask_restful import Api
from application.config import LocalDevelopmentConfig
from flask_cors import CORS
from application.database import db
from flask_jwt_extended import JWTManager
from application.models import Users
from application import workers
from celery.schedules import timedelta
from flask_sse import sse

app = None
api = None
celery = None
def create_app():
    
    app = Flask(__name__)
    if os.getenv("ENV","development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    
    api = Api(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    
    
    return app, api, celery

app, api, celery = create_app()

cors = CORS(app) # Allow cross-origin requests 
api = Api(app)

jwt = JWTManager(app)
with app.app_context():
    db.create_all()

app.register_blueprint(sse, url_prefix='/stream')

from application.controllers import *

from application.auth import *

from application.ratings import *

from application.user_api import UserApi

api.add_resource(UserApi, '/api/user')

from application.venue_api import *

api.add_resource(VenueApi, "/api/venue", "/api/venue/<venue_id>")

api.add_resource(VenueAnalyticsApi, "/api/venueanalytics")



from application.show_api import *

api.add_resource(ShowApi, "/api/show", "/api/show/<show_id>")

api.add_resource(ShowAnalyticsApi, "/api/showanalytics")


from application.bookings import BookingApi

api.add_resource(BookingApi, "/api/booking", "/api/booking/<showvenue_id>")

from application.show_venue_api import ShowVenueApi

api.add_resource(ShowVenueApi, "/api/showvenue/<show_id>")

from application.venue_show_api import VenueShowApi

api.add_resource(VenueShowApi, "/api/venueshow/<venue_id>")


from application.ticket_details import TicketDetails

api.add_resource(TicketDetails, "/api/bookingDetails")

from application.movie_search import *

api.add_resource(MovieSearchApi, "/api/search_movies")

api.add_resource(RegionSearchApi, "/api/search_region/<region>")

api.add_resource(LanguageSearchApi, "/api/search_lang/<lang>")

from application.region_lang import *

api.add_resource(RegionApi, "/api/regions")

api.add_resource(LanguageApi, "/api/languages")




if __name__ == "__main__":
    
    app.run(
        debug = True,
        
    )

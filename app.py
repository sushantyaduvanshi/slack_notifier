from flask import Flask, request 
from flask_restful import Resource, Api
from dotenv import load_dotenv
from main import send_message
import os

# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 
load_dotenv()
  
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class SlackSend(Resource): 
  
    # Corresponds to POST request 
    def get(self, *args): 
        try:
            if not request.args.get("message"):
                return "`message` is missing in parameters.", 400
            if not request.args.get("channel"):
                return "`channel` is missing in parameters.", 400
            channel = request.args["channel"]
            message = request.args["message"]
            status, error = send_message(message, channel)
            if not status:
                if error:
                    return error, 500
                return "Something went wrong!", 500
            return "Message sent successfully", 200
        except Exception as e:
            print("Got error while sending message to slack :::", e)
            return f"Got error while sending message to slack ::: {e}", 500
  
# adding the defined resources along with their corresponding urls 
api.add_resource(SlackSend, '/slack/send') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True, host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 8001)) 
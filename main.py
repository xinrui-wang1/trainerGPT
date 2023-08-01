from flask import Flask, request, render_template
from flask_cors import CORS
from functions import generate_prompt, generate_response
import os
from dotenv import load_dotenv
load_dotenv()

# openai_api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

class UserProfile:
    def __init__(self, user_data):
        self.days_per_week = user_data['days_per_week']
        self.goal = user_data['goal']
        self.intensity = user_data['intensity']
        self.gender = user_data['gender']
        self.weight = user_data['weight']
        self.height_ft = user_data['height_ft']
        self.height_in = user_data['height_in']
        self.age = user_data['age']
        self.experience = user_data['experience']
        self.equipment = user_data['equipment']
        self.duration_hr = user_data['duration_hr']
        self.duration_min = user_data['duration_min']

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    form_data = {}
    prompt = ""
    if request.method == 'POST':
        # get the form data
        form_data = {
            'days_per_week': request.form.get('days_per_week'),
            'goal': request.form.get('goal'),
            'intensity': request.form.get('intensity'),
            'gender': request.form.get('gender'),
            'weight': request.form.get('weight'),
            'height_ft': request.form.get('height_ft'),
            'height_in': request.form.get('height_in'),
            'age': request.form.get('age'),
            'experience': request.form.get('experience'),
            'equipment': request.form.get('equipment'),
            'duration_hr': request.form.get('duration_hr'),
            'duration_min': request.form.get('duration_min')
        }

        # generate the prompt
        prompt = generate_prompt(form_data)
        response = generate_response(prompt)
        
    return render_template('form.html', form_data=form_data, prompt=response)

if __name__ == '__main__':
    app.run(debug=True)

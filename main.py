from flask import Flask, render_template, request, redirect, url_for
import os
from flask_mail import Mail, Message
import json
import time
import cv2  # OpenCV for video recording
from candidate_processing import Candidate, generate_screening_questions, calculate_similarity
import mysql.connector
from flask import send_from_directory
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import flash
from ExtractingWordsVideo import extract_keywords_from_text,calculate_percentage_of_matches_ques1,calculate_percentage_of_matches_ques2,extract_words_from_audio,question1,question2,audio_path_Ques1,audio_path_Ques2
from wordExtraction import extract_text_from_pdf,extract_words_from_text1,calculate_percentage_of_matches,all_keywords

# Load configuration parameters from config.json
with open("/Users/mananmehra/Desktop/HR Optiflow/config.json", "r") as c:
    params = json.load(c)["params"]
    

local_server=True   

app = Flask(__name__)
app.secret_key = 'ABCD124'

if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
    
db = SQLAlchemy(app)

class Candidate(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(50), nullable=False)
    position=db.Column(db.String(50), nullable=False)
    selected=db.Column(db.String(20),nullable=True)

USERNAME = 'mehravirgo@gmail.com'
PASSWORD = 'Sabina@1976'

cv_data=[]

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password'],
)
mail = Mail(app)

# Set the duration of the interview recording in seconds (60 seconds = 1 minute)
interview_duration = 60

# Function to record a video for the specified duration
import os
from datetime import datetime

def record_video(duration):
    cap = cv2.VideoCapture(0)  # Open the default camera (0)
    codec = cv2.VideoWriter_fourcc(*'XVID')

    output_folder = '/Users/mananmehra/Desktop/HR Optiflow/audio_videos'

    # Ensure the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_folder, f'interview_video_{timestamp}.mov')

    out = cv2.VideoWriter(output_file, codec, 30, (640, 480))

    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return output_file

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'cv' not in request.files:
        return redirect(request.url)

    file = request.files['cv']
    candidate_name = request.form.get('candidate_name')  # Get the candidate's name
    candidate_email = request.form.get('candidate_email')  # Get the candidate's email
    candidate_position = request.form.get('candidate_position')  # Get the candidate's position
    
    cv_data.append({
        "name": candidate_name,
        "email": candidate_email,
        "position": candidate_position,
        "filename": file.filename,
    })

    if file.filename == '' or not all([candidate_name, candidate_email, candidate_position]):
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Save candidate information to the database
        if request.method == 'POST':
            entry = Candidate(name=candidate_name, email=candidate_email, position=candidate_position)
            db.session.add(entry)
            db.session.commit()

        recorded_video = record_video(interview_duration)

        subject = "CV Upload Notification"
        sender_email = params['gmail-user']
        recipient_email = "mumehra2827@gmail.com"  # Replace with the recipient's email
        message_body = "Your CV has been uploaded successfully."

        msg = Message(subject=subject,
                      sender=sender_email,
                      recipients=[recipient_email])
        msg.body = message_body
        mail.send(msg)
    return redirect(url_for('home'))

@app.route('/job')
def job():
    return render_template('job.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/pro')
def pro():
    return render_template('pro.html')

@app.route('/calculate_result', methods=['GET', 'POST'])
def calculate_result():
    if request.method == 'POST':
        # Get user input from the form
        name = request.form.get('name')
        email = request.form.get('email')

        # Perform the necessary calculations based on the input
        # You can use the existing functions or create new ones

        # Example: Calculate percentage for question 1
        result1 = extract_words_from_audio(audio_path_Ques1)
        keywords_result1 = extract_keywords_from_text(result1)
        percentage_Ques1 = calculate_percentage_of_matches_ques1(keywords_result1, question1)

        # Example: Calculate percentage for question 2
        result2 = extract_words_from_audio(audio_path_Ques2)
        keywords_result2 = extract_keywords_from_text(result2)
        percentage_Ques2 = calculate_percentage_of_matches_ques2(keywords_result2, question2)
        
        # Example: Calculate result of resume
        pdf_path = '/Users/mananmehra/Desktop/HR Optiflow/uploads/manan_cv.pdf'
        extracted_text = extract_text_from_pdf(pdf_path)
        extracted_words = extract_words_from_text1(extracted_text)
        print("Extracted Words from Resume:", extracted_words)
        percentage_resume = calculate_percentage_of_matches(extracted_words, all_keywords)
        print("Percentage for Resume:", percentage_resume)
        total_percentage = percentage_Ques1 + percentage_Ques2 + percentage_resume
        selected = total_percentage > 10

        # Update the database or perform other actions based on the result
        # Example: Update the database
        if selected:
            selected_candidate = Candidate.query.filter_by(email=email).first()
            if selected_candidate:
                # Update the candidate's selection status in the database
                selected_candidate.selected = 'Yes'  # Change to whatever indicator you prefer
                db.session.commit()

        # Redirect to the dashboard or another page with the result
        return redirect(url_for('dashboard'))

    return render_template('result.html')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    # Query the database to get candidate information
    
    candidates = Candidate.query.all()

    enrolled_candidates = len(candidates)
    selected_candidates = Candidate.query.filter_by(selected='Yes').count()
    not_selected_candidates = Candidate.query.filter_by(selected='No').count()  # You may need to modify this based on your selection criteria

    enrollment_selection_data = [
        go.Bar(
            x=['Enrolled', 'Selected', 'Not Selected'],
            y=[enrolled_candidates, selected_candidates, not_selected_candidates],
            marker=dict(color=['blue', 'green', 'red'])
        )
    ]

    enrollment_selection_layout = go.Layout(
        title='Enrollment and Selection Status',
        xaxis=dict(title='Status'),
        yaxis=dict(title='Number of Candidates')
    )

    enrollment_selection_fig = go.Figure(data=enrollment_selection_data, layout=enrollment_selection_layout)
    enrollment_selection_graph = enrollment_selection_fig.to_html(full_html=False)

    return render_template('dashboard.html', candidates=candidates, enrollment_selection_graph=enrollment_selection_graph)

    # return render_template('dashboard.html', cv_data=cv_data)

@app.route('/view_cv/<filename>')
def view_cv(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
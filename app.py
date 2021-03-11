'''
This program accepts .wav files and transcribes the audio to the closest matching text.
Clearer audio files will be accurately transcribed.
To filter out noise or interference, play with threshold values or filter through ambient noise adjustment.
Author: Delzad Bamji
'''

from flask import Flask, render_template, request, redirect
import speech_recognition as speech

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    # if post method is called after form submission
    if request.method == "POST":
        print("FORM DATA RECEIVED IN POST METHOD")
        # check if the file really exists and isn't empty
        if "file" not in request.files:
            print("NO FILES FOUND")
            redirect(request.url)
        # if user sends a blank submit without selecting a file
        file = request.files["file"]
        if file.filename == "":
            redirect(request.url)
        # start speech recognition
        if file:
            recognizer = speech.Recognizer()

            with speech.AudioFile(file) as sourceFile:
                # recognizer.adjust_for_ambient_noise(sourceFile, duration=2)
                data = recognizer.record(sourceFile)
                try:
                    transcript = recognizer.recognize_google(data, key=None)
                except LookupError:
                    transcript = "Audio cannot be deciphered. Please use a clearer file."

    else:
        redirect(request.url)
    return render_template('index.html', transcript=transcript)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)

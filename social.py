from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

class Check:

    def __init__(self):
        self.email = ""
        
    def print_linked(self):
        return f"{self.email} = Linked"

    def print_unlinked(self):
        return f"{self.email} = Unlinked"

    def twitter(self):
        # Your existing Twitter check logic goes here
        pass

    def instagram(self):
        # Your existing Instagram check logic goes here
        pass

    def snapchat(self):
        # Your existing Snapchat check logic goes here
        pass

    def run_checks(self):
        self.twitter()
        self.instagram()
        self.snapchat()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    email = request.json.get('email', '')
    
    # Perform social media checks
    checker = Check()
    checker.email = email
    checker.run_checks()
    
    result = {
        'twitter': checker.print_linked() if checker.twitter() else checker.print_unlinked(),
        'instagram': checker.print_linked() if checker.instagram() else checker.print_unlinked(),
        'snapchat': checker.print_linked() if checker.snapchat() else checker.print_unlinked()
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

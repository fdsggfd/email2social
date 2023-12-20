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

    def print_timeout(self):
        return f"{self.email} = Timeout: Too many tries, please wait"

    def twitter(self):
        r = requests.Session()
        url = "https://api.twitter.com/i/users/email_available.json?email=" + self.email
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        Host = "api.twitter.com"
        Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        r.headers = {'User-Agent': user_agent, 'Host': Host, 'Accept': Accept}
        req = r.get(url).json()
        text = str(req)
        print(text)
        print('')
        if text.find("'valid': False") == True:
            return True
        else:
            return False

    def instagram(self):
        r = requests.Session()
        url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        r.headers = {'user-agent': user_agent}
        r.headers.update({'X-CSRFToken': "missing"})
        data = {"email_or_username": self.email}
        req = r.post(url, data=data)
        print(req.text)
        print('')
        
        if req.text.find("We sent an email to") >= 0:
            return True
        elif req.text.find("Please wait") >= 0:
            return "timeout"
        else:
            return False

    def snapchat(self):
        url = "https://bitmoji.api.snapchat.com/api/user/find"
        r = requests.Session()
        r.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        req = r.post(url, headers=r.headers, json={"email": self.email})
        status = req.status_code
        print(status)
        print('')
        if status == 200:
            print(f"{self.email} = is linked to an account" + "\n")
            file = open("snapchat-linked.txt", "a")
            file.write(self.email + "\n")
            file.close()
            return True
        else:
            print(f"{self.email} = is not linked to an account" + "\n")
            return False

    def run_checks(self):
        # Call each method once
        twitter_result = self.twitter()
        instagram_result = self.instagram()
        snapchat_result = self.snapchat()

        return {
            'twitter': self.print_linked() if twitter_result else self.print_unlinked(),
            'instagram': self.print_linked() if instagram_result == True else self.print_timeout() if instagram_result == "timeout" else self.print_unlinked(),
            'snapchat': self.print_linked() if snapchat_result else self.print_unlinked()
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    email = request.json.get('email', '')

    # Perform social media checks
    checker = Check()
    checker.email = email
    result = checker.run_checks()

    # Handle the "timeout" case
    if result['instagram'] == 'timeout':
        result['instagram'] = 'timeout: Too many tries, please wait'

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

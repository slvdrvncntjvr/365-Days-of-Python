from flask import Flask, request, render_template
from cryptography.fernet import Fernet

SECRET_KEY = b'JrU0wJc_eJhD_R0I9p_JD_6z7rbdh6aD6Xghz23dFo4='
cipher = Fernet(SECRET_KEY)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def decrypt():
    decrypted_text = ""
    if request.method == "POST":
        encrypted_text = request.form.get("encrypted_text", "")
        try:
            decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            decrypted_text = f"Decryption failed: {e}"
    return render_template("decrypt.html", decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

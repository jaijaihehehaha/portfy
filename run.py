from flask import Flask, render_template
import os

# Absolute path to the folder containing run.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "app", "templates"),
    static_folder=os.path.join(BASE_DIR, "app", "static")
)

@app.route('/')
def home():
    # Look inside templates/public
    return render_template("public/index.html")

if __name__ == "__main__":
    # Ensure working directory is root
    os.chdir(BASE_DIR)
    app.run(host="0.0.0.0", port=2324, debug=True)

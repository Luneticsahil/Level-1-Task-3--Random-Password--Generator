from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

def generate_password(length, use_letters=True, use_numbers=True, use_symbols=True):
    character_pool = ""
    if use_letters:
        character_pool += string.ascii_letters  # A-Z, a-z
    if use_numbers:
        character_pool += string.digits  # 0-9
    if use_symbols:
        character_pool += string.punctuation  # Special characters
    
    if not character_pool:
        return None  # No character types selected
    
    return ''.join(random.choice(character_pool) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    error_message = ""

    if request.method == "POST":
        if "clear" in request.form:  # Clear button clicked
            return render_template("index.html")

        try:
            length = int(request.form.get("length", 8))
            use_letters = "use_letters" in request.form
            use_numbers = "use_numbers" in request.form
            use_symbols = "use_symbols" in request.form

            if length < 4 or length > 20:
                error_message = "Password length must be between 4 and 20!"
            else:
                password = generate_password(length, use_letters, use_numbers, use_symbols)
                if password is None:
                    error_message = "Please select at least one character type!"
        
        except ValueError:
            error_message = "Invalid input. Please enter a valid number."

    return render_template("index.html", password=password, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)

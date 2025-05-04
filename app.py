from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment

@app.route("/", methods=["GET", "POST"])
def index():
    quote_output = None
    pro_user = request.args.get("pro") == "true"

    if request.method == "POST":
        business_name = request.form.get("business_name", "Your Business")
        job_description = request.form.get("job_description", "")

        prompt = f"""
        Write a professional quote for a handyman business named {business_name} for the following job:
        {job_description}
        Include:
        - A polite greeting
        - An itemized service summary
        - A total price
        - Simple payment terms (e.g. payment due upon completion)
        - A friendly closing
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional assistant that writes client-ready service quotes."},
                {"role": "user", "content": prompt}
            ]
        )

        quote_output = response["choices"][0]["message"]["content"]

    return render_template("index.html", quote_output=quote_output, pro_user=pro_user)

if __name__ == "__main__":
    app.run(debug=True)

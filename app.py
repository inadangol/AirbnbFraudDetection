from flask import Flask, render_template, request
import pickle
import numpy as np # type: ignore

# Create a simple Flask application
app = Flask(__name__)

# Load the trained Logistic Regression model
lgr = pickle.load(open('Logistic_Regression.pkl','rb'))



#@app.route('/')
#def form():
   # return render_template('form.html')  # Create a simple index page

@app.route('/', methods=["GET", "POST"])
def handle_form():
    if request.method == "POST":
        try:
            host_response_rate = float(request.form['host_response_rate'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Host Response Rate")

        try:
            host_identity_verified = 1 if request.form['host_identity_verified'] == 'True' else 0
        except ValueError:
            return render_template('form.html', error="Invalid value for Host Identity Verified")

        try:
            host_total_listings_count = int(request.form['host_total_listings_count'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Host Total Listings Count")

        try:
            price = float(request.form['price'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Price")

        try:
            number_of_reviews = int(request.form['number_of_reviews'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Number of Reviews")

        try:
            review_scores_rating = float(request.form['review_scores_rating'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Review Scores Rating")

        try:
            instant_bookable = 1 if request.form['instant_bookable'] == 'True' else 0
        except ValueError:
            return render_template('form.html', error="Invalid value for Instant Bookable")

        try:
            cancellation_policy = int(request.form['cancellation_policy'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Cancellation Policy")

        try:
            reviews_per_month = float(request.form['reviews_per_month'])
        except ValueError:
            return render_template('form.html', error="Invalid value for Reviews Per Month")

        # Prepare input data for prediction
        input_data = np.array([[host_response_rate, host_identity_verified, host_total_listings_count,
                                price, number_of_reviews, review_scores_rating, instant_bookable,
                                cancellation_policy, reviews_per_month]])

        # Make the prediction
        prediction = lgr.predict(input_data)[0]

        # Interpret the prediction
        result = "Fraud" if prediction == 1 else "Not Fraud"

        return render_template('result.html', prediction=result)

    return render_template('form.html')
@app.route('/predict', methods=['POST'])
def predict():
    return handle_form()

if __name__ == "__main__":
    app.run(debug=True)

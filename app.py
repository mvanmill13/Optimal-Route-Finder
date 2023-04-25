from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import googlemaps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Define the routing function
def calculate_optimal_route(api_key, addresses):
    gmaps = googlemaps.Client(key=api_key)
    directions = gmaps.directions(addresses[0], addresses[-1], waypoints=addresses[1:-1], optimize_waypoints=True)
    route = [leg['start_address'] for leg in directions[0]['legs']]
    route.append(directions[0]['legs'][-1]['end_address'])
    return route

class AddressForm(FlaskForm):
    submit = SubmitField('Continue')
    num_addresses = StringField('How many addresses do you want to input?', validators=[DataRequired()])
    
    
@app.route('/', methods=['GET', 'POST'])
def index():

    form = AddressForm()
    if request.method == 'POST':
        num_addresses = int(request.form['num_addresses'])
        form.addresses = []
        for i in range(num_addresses):
            field_name = f"address{i+1}"
            setattr(AddressForm, field_name, StringField(f'Address {i+1}', validators=[DataRequired()]))
            form.addresses.append(getattr(form, field_name))
        if form.validate_on_submit():
            addresses = [field.data for field in form.addresses]
            # Call the routing function
            api_key = 'Your Key Goes Here'
            route = calculate_optimal_route(api_key, addresses)
            return render_template('route.html', route='Optimal Route: ' + ' -> '.join(route))
        
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

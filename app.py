from flask import Flask, flash, redirect, url_for, render_template, request
from wtforms import Form, TextField, SelectField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from utils import build_query, execute_query
import creds

app = Flask(__name__)
app.config['SECRET_KEY'] = creds.SECRET_KEY

previous = []
genres = ['literaryFiction']

class SuggestForm(FlaskForm):
    category = TextField('What you want (eg, book)')#, [validators.Required("Please enter your category.")])
    # category_samples = SelectField('Sample things', choices = [('book', 'Book'), 
      # ('show', 'TV Show')])

    similar = TextField('Similar book')
    genre = SelectField('Genre', choices=genres, default='')
    start = SelectField('Start year', coerce=int, choices=range(1990, 2021), default=1700)
    end = SelectField('End year', coerce=int, choices=range(1990, 2021), default=2020)
    submit = SubmitField("Go")

    # def validate_dates(self):
    #     start = self.start.data
    #     end = self.end.data

    #     if start and end and start > end:
    #         raise ValidationError(f'Start year {start} must be less than or equal to End year {end} \
    #         or one of them must be left blank')

@app.route('/')
def index():
    form = SuggestForm()
    return render_template('index.html', form=form)

@app.route("/suggest/", methods=['GET'])
def suggest():
    form = SuggestForm(request.form)
    if True:
    # if form.validate_on_submit():
    # category = form['category'].data.lower()
    # change hardcoded value back
    # genre = form.get('genre')
    # similar = form.get('similar')
    # start = form.get('from')
    # end = form.get('to')
        genre = form['genre'].data
        similar = form['similar'].data
        start = form['start'].data
        end = form['end'].data

        category = 'book'
        # if category in options.keys():
        # if not options[category]:
        #     suggestion = 'no more options to suggest for {}'.format(category)
        #     previous.append(None)
        # else:
        query = build_query(category, similar, genre, start, end)
        options = execute_query(query)
        # will always refresh options. shouldn't cache directly but rather save params and rsults in didct
        suggestion = options[0]
        options = options[1:]
        link = 'https://duckduckgo.com/?q=!amazon isbn {}&atb=v231-1&ia=web'.format(suggestion[2])
        suggestion[2] = link
        previous.append((category, suggestion[0], link))

        # else:
            # suggestion = 'could not find suggestion for {}'.format(category)

        return render_template('index.html', form=form, suggestion=suggestion, previous=previous)

    # else:
    #     # flash(form.errors)
    #     # flash(form.validate_on_submit())
    #     return render_template('index.html', form=form)
if __name__ == '__main__':
    app.run(debug=True)

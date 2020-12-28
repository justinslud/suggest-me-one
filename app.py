from flask import Flask, flash, redirect, url_for, render_template, request
from wtforms import Form, TextField, SelectField, SubmitField, validators, ValidationError
from flask_wtf import FlaskForm
from utils import build_query, execute_query
import creds
from data import GENRES, SUBJECTS

app = Flask(__name__)
app.config['SECRET_KEY'] = creds.SECRET_KEY

previous = []
results = {}

class SuggestForm(FlaskForm):
    category = TextField('What you want (eg, book)', default='book')#, [validators.Required("Please enter your category.")])
    # category_samples = SelectField('Sample things', choices = [('book', 'Book'), 
      # ('show', 'TV Show')])

    similar = TextField('Similar book')
    genre = SelectField('Genre', choices=GENRES, coerce=str)
    subject = SelectField('Subject', choices=SUBJECTS, coerce=str)
    start = SelectField('Start year', coerce=int, choices=range(1990, 2021))
    end = SelectField('End year', coerce=int, choices=range(1990, 2021))
    submit = SubmitField("Go")

    # def validate_dates(self):
    #     start = self.start.data
    #     end = self.end.data

    #     if start and end and start > end:
    #         raise ValidationError(f'Start year {start} must be less than or equal to End year {end} \
    #         or one of them must be left blank')
    def validate(self):
        return 0

@app.route('/')
def index():
    form = SuggestForm()
    return render_template('index.html', form=form)

@app.route("/suggest/", methods=['GET'])
def suggest():
    form = SuggestForm(request.form)
    if True:
    # if form.validate():
    # category = form['category'].data.lower()
    # change hardcoded value back
    # genre = form.get('genre')
    # similar = form.get('similar')
    # start = form.get('from')
    # end = form.get('to')
        print(form)
        category = form['category'].data
        genre = form['genre'].data
        subject = form['subject'].data
        similar = form['similar'].data
        start = form['start'].data
        end = form['end'].data
        print(category, similar, genre, subject, start, end)
        # category = 'book'
        # if category in options.keys():
        # if not options[category]:
        #     suggestion = 'no more options to suggest for {}'.format(category)
        #     previous.append(None)
        # else:
        query = build_query(category, similar, genre, subject, start, end)
        print(query)
        if query not in results.keys():
            res = execute_query(query)
            if res:
                results[query] = res
                options = [['Suggestion could not be gathered at this time. Try removing or broadening search criteria.']]
        
            else:
                options = results[query]

        else:
            options = results[query]

        if len(options[0]) > 1:
            suggestion = options[0]
            results[query] = results[query][1:]
            link = 'https://www.amazon.com/s?k=isbn+{}'.format(suggestion[2])
            suggestion[2] = link
            previous.append((category, suggestion[0], link))

            return render_template('index.html', form=form, suggestion=suggestion, previous=previous)
            # return redirect(url_for('index', form=form, suggestion=suggestion, previous=previous, _external=True))
    # else:
    #     # flash(form.errors)
    #     # flash(form.validate_on_submit())
        return render_template('index.html', form=form, suggestion=options[0], previous=previous)
if __name__ == '__main__':
    app.run(debug=True)

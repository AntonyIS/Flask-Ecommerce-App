from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, FileField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProductForm(FlaskForm):
    product_name = StringField('Product name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField(u'Category',choices=[("Women","women"),("Men","men"),("Kids","kids")])
    item = StringField('Item', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    size = IntegerField('Size', validators=[DataRequired()])
    size_number = IntegerField('Size number', validators=[DataRequired()])
    reviews = IntegerField('Size', validators=[DataRequired()])
    image = FileField("Product Image")
    user_id = StringField('user_id', validators=[DataRequired()])
    submit = SubmitField('Add Product')

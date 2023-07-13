from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_shop.models import User


class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    email_address = StringField('Email',
                                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                f'Username {username.data} was taken. Choose another one!')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError(
                f'Email address {email_address.data} was taken. Choose another one!')


class SignInForm(FlaskForm):
    email_address = StringField('Email',
                                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_description = StringField(
        'Product Description', validators=[DataRequired()])
    product_image = StringField('Product Image', validators=[DataRequired()])
    product_price = DecimalField('Product Price', validators=[DataRequired()])
    product_submit = SubmitField('Add Product')


class NewServiceForm(FlaskForm):
    service_description = StringField(
        'Product Description', validators=[DataRequired()])
    service_submit = SubmitField('Add Service')


class NewUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    email_address = StringField('Email',
                                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    phone_number = StringField('Phone Number',
                               validators=[Length(max=10)])
    address = StringField('Full Address',
                          validators=[Length(max=72)])
    submit = SubmitField('Add User')

class RemoveForm(FlaskForm):
    entry = SelectField('Object to be removed', validators=[DataRequired()])
    submit = SubmitField('Remove')

class ModifyUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    email_address = StringField('Email',
                                validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number',
                               validators=[Length(max=10)])
    address = StringField('Full Address',
                          validators=[Length(max=72)])
    submit = SubmitField('Change profile details')

class ModifyUser2Form(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=32)])
    email_address = StringField('Email',
                                validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number',
                               validators=[Length(max=10)])
    address = StringField('Full Address',
                          validators=[Length(max=72)])
    submit = SubmitField('Change profile details')

class ModifyProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Product Description', validators=[DataRequired()])
    image = StringField('Product Image', validators=[DataRequired()])
    price = StringField('Product Price', validators=[DataRequired()])
    submit = SubmitField('Change product details')
    
class ModifyServiceForm(FlaskForm):
    service = StringField(
        'Product Description', validators=[DataRequired()])
    submit = SubmitField('Change service details')

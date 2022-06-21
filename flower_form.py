from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
#librería para construir la estructura de cajones de entrada de datos en la 
#webapp
class FlowerForm(FlaskForm):
    SepalLengthCm = StringField('Sepal Length Cm')
    SepalWidthCm = StringField('Sepal Width Cm')
    PetalLengthCm = StringField('Petal Length Cm')
    PetalWidthCm = StringField('Petal Width Cm')

    submit = SubmitField("Predict")
#carga estas librerias de flask
from contextlib import redirect_stderr
from pydoc import render_doc
from flask import Flask, session, url_for, render_template, redirect
import joblib
#carga la clase creada en flower_form.py 
from flower_form import FlowerForm

#Cargamos los modelos guardados en saved_models
knn_loaded = joblib.load('saved_models/knn_iris_dataset.pkl')
encoder_loaded = joblib.load('saved_models/iris_label_encoder.pkl')

#creamos la función de predicción
def make_prediction(model, encoder, sample_json):
    SepalLengthCm = sample_json['SepalLengthCm']
    SepalWidthCm = sample_json['SepalWidthCm']
    PetalLengthCm = sample_json['PetalLengthCm']
    PetalWidthCm = sample_json['PetalWidthCm']
    
    # Creamos un vector de input
    flower = [[SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm]]

    # Predicción
    prediction_raw = model.predict(flower)

    #Convertimos los índices en labels de las clases:
    prediction_real = encoder.inverse_transform(prediction_raw)

    return prediction_real[0]

# creamos la app de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route('/', methods=['GET','POST']) # llamo a la página inicio, que por defecto de nombra solo así '/'
# coge el nombre de la aplicación creada
def index():  #definición de la página de inicio (index.html, la homepage)
    form = FlowerForm()

    if form.validate_on_submit():
        session['SepalLengthCm'] = form.SepalLengthCm.data #session viene de 
        session['SepalWidthCm'] = form.SepalWidthCm.data
        session['PetalLengthCm'] = form.PetalLengthCm.data
        session['PetalWidthCm'] = form.PetalWidthCm.data

        return redirect(url_for('prediction'))
    return render_template('home.html', form=form) #home.html, fichero que pondré en la carpeta 'templates'

@app.route('/prediction')   #llamo a la página prediction (la que quiero crear para que mustre los resultados)
def prediction():  #definición de la página donde se dará la predicción
    content = {'SepalLengthCm': float(session['SepalLengthCm']), 'SepalWidthCm': float(session['SepalWidthCm']),
               'PetalLengthCm': float(session['PetalLengthCm']), 'PetalWidthCm': float(session['PetalWidthCm'])}

    results = make_prediction(knn_loaded, encoder_loaded, content)

    return render_template('prediction.html', results=results) #prediction.html, fichero
                                                            # que pondré en la carpeta 'templates'

#ejecutamos la aplicación app.run()
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080) # '0.0.0.0' to Run the application on a local development server
                                    # `5000` to Run the application on a local development server
    app.run() #cuando lo hagamos en la nube, en remoto


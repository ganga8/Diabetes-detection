from flask import Flask,render_template,request
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import csv

app = Flask(__name__,template_folder='templates')
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/submit',methods=['GET','POST'])

def submit():
    print("I came here")

    preg = request.form.get('pregnancies')
    glucose = request.form.get('Glucose')
    bloodP =request.form.get('BloodPressure')
    skinT = request.form.get('Thickness')
    insulin = request.form.get('Insulin')
    bmi = request.form.get('BMI')
    Diabetes = request.form.get('Diabetes')
    age = request.form.get('Age')
    
    appendDataToCsv(preg,glucose,bloodP,skinT, insulin, bmi,Diabetes,age)
    print("===========Text excel saved==========")
    var = predictMe()
    var = var*100
    #******Result*******
    msg = ''
    if var < 150 and var >= 90:
        msg = "Your sugar level is normal! Keep up the good work"
        return render_template('display_data.html', message = msg)
    else:
        msg = "Your have diabetes follow the below diet"
        return render_template('display_data1.html', message = msg)

#appending data to excel sheet
def appendDataToCsv(preg,glucose,bloodP,skinT, insulin, bmi,Diabetes,age):
    print("Entered Append Function")

    fields = [preg,glucose,bloodP,skinT,insulin,bmi,Diabetes,age]
    names = ['Pregnancies', 'Glucose','BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Diabetes','Age'] 
    filename = "sugar.csv"
    with open(filename ,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)
        csvwriter.writerow(fields)
def predictMe():
    value = predictDiabetes()
    var = int(value)
    return var
def predictDiabetes():
    dataset=pd.read_csv("diabetes.csv")
    print((dataset[["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]]==0).sum())
    dataset[["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]]=dataset[["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]].replace(0,np.NaN)
    print((dataset[["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]]==0).sum())
    print(dataset.isnull().sum())
    dataset.fillna(dataset.mean(), inplace=True)
    array = dataset.values
    x_train = array[:,0:8]
    y_train = array[:,8]
    ols = LogisticRegression()
    model = ols.fit(x_train, y_train)
    # testring set
    database =pd.read_csv("sugar.csv")
    '''col_names = ['Pregnancies', 'Glucose','BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Diabetes','Age']
    per = 0.55
    plot = pd.DataFrame(col_names)
    pima = pd.read_csv(database, names=col_names)
    test = pima[((int)(len(plot) * per)):]
    xtest = test[['Pregnancies', 'Glucose','BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Diabetes','Age']]'''
    array = database.values
    xtest = array[:,0:8]
    predict = model.predict(xtest)
    print(predict)
    print("==Value of model predict===")
    length = 1-len(predict)
    print("length",length)
    print(predict[length])
    return predict[length]
    
if __name__ == '__main__':
    app.run(debug = True , use_reloader = False)
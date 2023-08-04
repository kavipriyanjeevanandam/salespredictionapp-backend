
from flask import Flask, request
from mongo import mongo
from flask_cors import CORS, cross_origin
import pickle
import gzip
import numpy as np
import pandas as pd
from math import floor
from pandas.tseries.offsets import DateOffset
from sklearn.metrics import mean_squared_error
from helper import list_to_json

app = Flask(__name__)
app.register_blueprint(mongo, url_prefix = "/db")
CORS(app)

month=''
target=''
filepath =''

@app.route('/')
def start():
  return '<h1>Welcome to Sales prediction app</h1>'

# Function to get input parameters from angular and saving them

@app.route('/predict/file', methods=['GET','POST'])
@cross_origin()
def fileRead():
  try:
    uploaded_file = request.files['file']

    global month, target, filepath
    month = request.form['month']
    target = request.form['parameter']
    
    filepath = r".\files\UserData.csv"
    uploaded_file.save(filepath)
    return {'post':'success'}
  except:
    return {'post' :'error'}

# Function to load trained model and give prediction results to angular

@app.route('/predict/results')
def results():
  try:
    results = pickle.load(gzip.open("./mlmodel/model.pkl.gz",'rb'))
    df = pd.read_csv(filepath)
    df.columns=["Month",target]

    dates_input = df['Month'].tolist()
    sales_input = df[target].tolist()

    df['Month']=pd.to_datetime(df['Month'])
    df.set_index('Month',inplace=True)
    df['forecast']=results.predict(start= floor(len(df)*0.8),end=len(df),dynamic=True)
    
    future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,int(month))]
    future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)  
    future_df=pd.concat([df,future_datest_df])
    future_df['forecast'] = results.predict(start = len(df), end = len(future_df), dynamic= True)  

    date_values = np.append(dates_input[:-1],pd.Series(future_dates).dt.strftime('%m/%d/%Y'))
    sales_data = np.append(sales_input,future_df['forecast'].tolist()[ len(df):])
      
    score = np.sqrt(mean_squared_error(df[target][floor(len(df)*0.8):len(df)-1], df['forecast'][floor(len(df)*0.8):len(df)-1]))
    return list_to_json(date_values,sales_data,future_df,score)
    
  except:
    return {'status':"error"}




if __name__ == '__main__':
  app.run(host='0.0.0.0',debug =True, port =5000)
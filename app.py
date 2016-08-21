from flask import Flask,render_template,request,redirect
import requests
import pandas as pd
from pandas import DataFrame, Series
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
app = Flask(__name__)


@app.route('/getStock')
def getStock():
  api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % app.stockname
  api_url += '?api_key=wuR-yRYttjYYAvzgNdM6'
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  r = session.get(api_url)
  name = r.json()['dataset']['name']
  name = name.split('(')[0]
  dat = r.json()['dataset']
  df = DataFrame(dat['data'], columns=dat['column_names'] )
  df = df.set_index(pd.DatetimeIndex(df['Date']))

  priceReq = 'Close'
  p = figure(x_axis_type="datetime", width=800, height=600)
  p.line(df.index, df[priceReq], legend=priceReq, line_width=3)
  p.title.text = app.stockname + ' ' + priceReq + ' prices'
  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  p.legend.location = "top_left"

  app.script, app.div = components(p)

  return redirect ('/plotpage')

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
        app.stockname = request.form['stockname']
        return redirect('/getStock')

@app.route('/plotpage', methods=['GET','POST'])
#@app.route('/plotpage')
def plotpage():
  if request.method == 'GET':
    return render_template('plot.html', script=app.script, div= app.div, ticker=app.stockname)
    #return render_template('plot-orig.html',stockname=app.stockname)
  else:
    return redirect('/index')    

if __name__ == "__main__":
    app.run(debug=True)
'''
Written By Isaiah Hanna 2024-09-18

Purpose: Create a webpage for the user to interact with program
'''

from flask import Flask,render_template,request,jsonify
from Main import Recommendation
import requests
from ImportData.api_Url import URL
from ExceptionsList import DataImportException
from waitress import serve

#Create instance of Recommendation object 
recommender = Recommendation()
#Extract relevant features and encode
features = recommender.features
titles = recommender.animes['titles'].apply(lambda x: x.strip("[]").split(",")[0].strip("'").title())
titlesDict = {"titles":list(titles)}

app = Flask(__name__) # Tells flask that everthing needed to run the site is in this file (hence '__name__')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userShow = request.form['watched-show']
        recommender.input(userShow)
        userAnime = recommender.userAnime # Saves a pd.Dataframe containing the userAnime's features 
        recommender.predict(numRows = 1) # Only ask for one row
        recID = recommender.prediction[0]  #Bring in the uid of the anime that the user should like based on their input. Note the [0] is due to it being a list
        try:
            response = requests.get(URL +  "/anime/" + str(int(recID)))
            if response.status_code == 400:
                raise DataImportException(error_code="2001",message="Request failed to retrieve data from jikan api.")
            data = response.json()['data']
            image = data['images']['jpg']['image_url']
        except Exception as e:
            print(e)

        recommendation = recommender.animes.loc[recommender.animes['uid'] == recID].iloc[0,1].strip("[]").split(",")[0].title() #Return the primary title for the predicted anime to watch based on the user's input
        return render_template('recommendation_index.html', recommended_show=f"{recommendation}", watched_show=userShow,image_url = image)

    return render_template('recommendation_index.html',titles = titles)


@app.route('/get-shows',methods = ['GET'])
def getShows():
    return jsonify(titlesDict)


serve(app,host = '0.0.0.0',port = 8080)


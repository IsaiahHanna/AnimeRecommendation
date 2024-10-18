'''
Written By Isaiah Hanna 2024-09-18

Purpose: Create a webpage for the user to interact with program
'''

from flask import Flask,render_template,request,jsonify
import Main as main

#Load in data
animeCopy = main.DataImport()

#Extract relevant features and encode
features = main.FeatureEncoding(animeCopy)
titles = animeCopy['titles'].apply(lambda x: x.strip("[]").split(",")[0].strip("'").title())
titlesDict = {"titles":list(titles)}

app = Flask(__name__) # Tells flask that everthing needed to run the site is in this file (hence '__name__')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userShow = request.form['watched-show']
        print(userShow)
        userAnime = main.UserInput(animeCopy,features,userShow,console = False) # Saves a pd.Dataframe containing the userAnime's features 
        print(userAnime.iloc[0,0])
        similarAnime = main.SimilarityScores(features,userAnime,3)  #Bring in the 3 indices of the 3 most similar anime to the user's input
        recIDX = similarAnime[0] #Uid of recommended show
        print(recIDX)
        recommendation = animeCopy.loc[animeCopy['uid'] == recIDX].iloc[0,1].strip("[]").split(",")[0].title() #Return the primary title for the most similar anime to the user's input
        print(recommendation)
        return render_template('recommendation_index.html', recommended_show=f"{recommendation}", watched_show=userShow)

    return render_template('recommendation_index.html',titles = titles)


@app.route('/get-shows',methods = ['GET'])
def getShows():
    return jsonify(titlesDict)

app.run(host = "0.0.0.0", port = 8080,debug=True) #Tells flask to run on my machine and which port


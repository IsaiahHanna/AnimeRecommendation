'''
Written By Isaiah Hanna 2024-09-18

Purpose: Create a webpage for the user to interact with program
'''

from flask import Flask,render_template,request,jsonify
from Main import Recommendation

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
        print(userShow)
        recommender.input(userShow)
        userAnime = recommender.userAnime # Saves a pd.Dataframe containing the userAnime's features 
        print(userAnime.iloc[0,0])
        recommender.predict()
        recID = recommender.predictions[0]  #Bring in the 5 uids of the anime that the user should like based on their input, then save the top anime
        print(recID)
        recommendation = recommender.animes.loc[recommender.animes['uid'] == recID].iloc[0,1].strip("[]").split(",")[0].title() #Return the primary title for the predicted anime to watch based on the user's input
        print(recommendation)
        return render_template('recommendation_index.html', recommended_show=f"{recommendation}", watched_show=userShow)

    return render_template('recommendation_index.html',titles = titles)


@app.route('/get-shows',methods = ['GET'])
def getShows():
    return jsonify(titlesDict)

app.run(host = "0.0.0.0", port = 8080,debug=True) #Tells flask to run on my machine and which port


from flask import Flask,render_template,request
import pickle
import numpy as np

app = Flask(__name__)

def load_model():
    with open('mobile.pkl','rb') as file:
        data = pickle.load(file)
    return data

obj = load_model()
sim = obj['similarity']
df = obj['data']


phone_names = df['name'].values

def recommend(new_phone):
    # obtaining the index of the new person from the dataframe
    ind = df[df['name'] == new_phone].index[0]
    #'cosine[ind]' obtains the similarity for the 'new person','list(enumerate())'  creates a list of an 
    # iterable that produces pairs of (index, value),'sorted' sorts the list, 'reverse=True' sorts
    # the list in descending order rather than default ascending order,'key = lambda x:x[1]' specifies that 
    # list should be sorted using the similarity not its index i.e [(3,0.98),(2,0.67),(1,0.45)]
    distance = sorted(list(enumerate(sim[ind])),reverse = True,key = lambda x: x[1])
    recos = []
    for i in distance[1:6]:
        recos.append(df['name'].iloc[i[0]])
        
    return recos

@app.route('/')
def homepage():
    return render_template('phone.html',phone_names = phone_names)

@app.route('/recommend',methods=['POST'])
def get_recommendation():
    final = {}
    name_of_phone = request.form.get('phone')
    recos = recommend(name_of_phone)
    for i in recos:
        matched_rows = df[df['name'] == i]
        for index, row in matched_rows.iterrows():
            final[i] =  row['imgURL']
            
    return render_template('phone.html',recommendations = final,phone_names = phone_names,name_of_phone = name_of_phone)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
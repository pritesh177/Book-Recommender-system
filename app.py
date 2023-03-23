from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
filtered_rating=pickle.load(open('filtered_rating.pkl','rb'))
similar_score=pickle.load(open('similar_score.pkl','rb'))

app=Flask(__name__,template_folder='Template')

@app.route('/')
def index():
    return render_template('index.html',
                            book_name=list(popular_df['Book-Title'].values),
                            author=list(popular_df['Publisher'].values),
                            image=list(popular_df['Image-URL-M'].values),
                            votes=list(popular_df['num_Rating'].values),
                            rating=list(popular_df['avg_Rating'].values)
                            )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input=request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar=sorted(list(enumerate(similar_score[index])),key=lambda x:x[1],reverse=True)[1:5]
    data=[]
    for i in similar:
        item=[]
        temp_df=filtered_rating[filtered_rating['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

if (__name__=='__main__'):
    app.run(debug=True)
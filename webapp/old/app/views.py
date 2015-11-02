from flask import render_template, request,flash, redirect, url_for
from app import app, db
from app.models import Post

@app.route('/')
def index():
  post = Post.query.all()
  return render_template('index.html', post=post)

@app.route('/add' , methods=['POST', 'GET'])
def add():
  if request.method == 'POST':
      post=Post(request.form['title'], request.form['body'])
      db.session.add(post)
      db.session.commit()
      flash('New entry was successfully posted')     

  return render_template('add.html')

@app.route('/edit/<id>' , methods=['POST', 'GET'])
def edit (id):
    #Getting user by primary key:
    post = Post.query.get(id)
    if request.method == 'POST':                
                post.title = request.form['title']
                post.text =  request.form['body']
                db.session.commit()
                return  redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/delete/<id>' , methods=['POST', 'GET'])
def delete (id):
     post = Post.query.get(id)
     db.session.delete(post)
     db.session.commit()
     flash ('deleted')
           
     return redirect(url_for('index'))

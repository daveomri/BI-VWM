from   flask import Flask, render_template, url_for, request, redirect
import database_handler as database_handler
import comparation as cmpa
import data_retrieval as dare

app = Flask(__name__)

#main destination of form page
@app.route('/')
def index():
    return render_template('index.html')

#getting data from form
@app.route('/', methods=['POST'])
def index_post():
    #POST - user sent data to process
    if request.method == 'POST':
        #remove old data
        dare.clean_old_data()
        #get first set of pictures
        firstSet  = request.files.getlist('firstDataset')
        #get second set of pictures
        secondSet = request.files.getlist('secondDataset')
        #get option how to process data
        option = request.form['similarity_function']
        #get number of keypoints to extract
        key_num = request.form['keypoint_num']
        #get feature extractor
        fea_ex = request.form['algorithm']
        #get witch function to use
        funct_data = request.form['func_data']
        #save data to database
        database_handler.store_names(firstSet, "ds1", int(key_num), fea_ex)
        database_handler.store_names(secondSet, "ds2", int(key_num), fea_ex)
        #compare two sets of pictures
        cmpa.compare_controller(option, funct_data)
        #return result
        return redirect(url_for('result'))
    #return main page
    return render_template('index.html')

@app.route('/result')
def result():
    #get first and second set of result pictures
    first_set, second_set = dare.data_retrieval()
    #return page with result
    return render_template('result.html', first_set=first_set, second_set=second_set)

#debug app if it is being run directly
if __name__ == "__main__":
    app.run(debug=True)
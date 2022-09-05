from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/details', methods=['POST'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if (request.method == 'POST'):
        try:
            usern = request.form['content']
            gfg_url = "https://auth.geeksforgeeks.org/user/" + usern
            response_website = urReq(gfg_url)
            data_gfg = response_website.read()
            response_website.close()
            final_url = requests.get(gfg_url)
            final_url.encoding = 'utf-8'
            beautifyed_html = bs(final_url.text, "html.parser")
            clg_name = beautifyed_html.find("div", {"class": "basic_details_data"}).a.text
            rank = beautifyed_html.find("div", {"class": "profile_rank_div tooltipped"}).text[2:]
            score = beautifyed_html.find("div", {"class": "row score_cards_container"})
            coding_score = score.find_all("div", {"class": "col xl3 l6 m6 s12"})[0].div.div.text.split("\n")[2]
            no_problem = score.find_all("div", {"class": "col xl3 l6 m6 s12"})[1].div.div.text.split("\n")[2]
            monthly_coding = score.find_all("div", {"class": "col xl3 l6 m6 s12"})[2].div.div.text.split("\n")[2]
            detail_problem = beautifyed_html.find("div", {"class": "solved_problem_section"})
            school = detail_problem.text.split("\n")[2]
            sc=""
            for d in school:
                if d.isdigit():
                    sc=sc+d
            basic = detail_problem.text.split("\n")[3]
            bsc = ""
            for d in basic:
                if d.isdigit():
                    bsc = bsc + d

            easy = detail_problem.text.split("\n")[4]
            es = ""
            for d in easy:
                if d.isdigit():
                    es = es + d

            medium = detail_problem.text.split("\n")[5]
            md = ""
            for d in medium:
                if d.isdigit():
                    md = md + d


            hard = detail_problem.text.split("\n")[6]
            hd = ""
            for d in hard:
                if d.isdigit():
                    hd = hd + d


            coders= []
            mydict = {"clg_name":clg_name,"rank":rank,"coding_score":coding_score,"monthly_coding": monthly_coding,"no_problem":no_problem,"school":sc,"basic":bsc,"easy":es,"medium":md,"hard":hd }
            coders.append(mydict)
            return render_template('result.html',coders=coders[0:len(coders)])
        except:
            return render_template('emp.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

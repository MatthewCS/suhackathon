from database_manager import DatabaseManager
from flask import Flask, json, render_template, request
from scoreboard import Scoreboard


app = Flask(__name__)
score = Scoreboard(3) # 300 seconds to update
db = DatabaseManager("./info.db") # handle our database


# update the scoreboard up to 60 seconds sooner/later than the base 300 seconds.
@score.update(2)
def update_scoreboard():

    ports = score.check_ports()
    print("PORTS:\t" + str(ports))
    db.update_scoreboard(ports)


@app.route("/")
def index_page():

    return render_template("index.html")


@app.route("/scoreboard")
def scoreboard():

    return render_template("scoreboard.html")


# We want to load this into /scoreboard, so that we can continually update
# that page.
@app.route("/scores")
def scores():

    sb = list(db.read_database())
    for sb_index in range(0, len(sb)):

        sb[sb_index] = list(sb[sb_index])

        for item_index in range(0, len(sb[sb_index]) - 1):

            if sb[sb_index][item_index] == 0:

                sb[sb_index][item_index] = "DOWN"

            elif sb[sb_index][item_index] == 1:

                sb[sb_index][item_index] = "UP"

    return render_template("scores.html", scoreboard=sb)


@app.route("/get_scoreboard")
def get_scoreboard():

    score_list = list(db.read_database())
    score_dict = {}

    for scores in score_list:
        score_dict[scores[0]] = {}
        score_dict[scores[0]]["ftp"] = bool(scores[1])
        score_dict[scores[0]]["ssh"] = bool(scores[2])
        score_dict[scores[0]]["smtp"] = bool(scores[3])
        score_dict[scores[0]]["http"] = bool(scores[4])
        score_dict[scores[0]]["rdp"] = bool(scores[5])
        score_dict[scores[0]]["points"] = scores[6]

    response = app.response_class(
        response=json.dumps(score_dict),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":

    db.upload_new_ips(score.ip_list)

    # run a check before the webapp goes up, don't wait for delay
    update_scoreboard()

    app.run(host='0.0.0.0', port=80)

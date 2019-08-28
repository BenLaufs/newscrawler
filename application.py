import os
import requests, json

from flask import Flask, jsonify, render_template, request, url_for
from flask_socketio import SocketIO, emit
from AURnewsticker import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

@socketio.on("search")
def search_trigger(data):
    print("received")
    stories = []

    trigger = data["trigger"]


    if trigger != "none":
        story_counter = 0

        # DataSources
        urlList = readUrlConfig("urls.txt")

        for u in urlList:

            url_stories_all = []
            url_stories_filtered = []
            url_stories_all = process(u)
            story_counter += len(url_stories_all)
            url_stories_filtered = filterStories(url_stories_all, trigger)
            for n in url_stories_filtered:
                stories_web = []
                summaries_web = []
                dates_web = []
                urls_web = []
                triggers_web = []
                triggers_web.append(trigger)
                stories_web.append(n.title)
                summaries_web.append(n.summary)
                dates_web.append(n.pubDate)
                urls_web.append(n.link)
                web_data = {'stories_name': stories_web, 'stories_summary': summaries_web, 'stories_date': dates_web, 'stories_url': urls_web, 'story_counter': story_counter, 'triggers': triggers_web}
                emit("show stories", web_data, broadcast=True)
                socketio.sleep(1)

    else:
        triggers = ["spin-off", "carve-out", "Abspaltung", "Restrukturierung", "Gewinnwarnung", "Teilverkauf", "short-seller", "insolven"]
        # DataSources
        urlList = readUrlConfig("urls.txt")
        story_counter = 0
        for u in urlList:
            url_stories = []
            filter_stories = []
            url_stories = process(u)
            story_counter += len(url_stories)
            for t in triggers:
                filter_stories = filterStories(url_stories, t)
                stories_web = []
                dates_web = []
                summaries_web = []
                urls_web = []
                triggers_web = []
                for n in filter_stories:
                    stories_web.append(n.title)
                    dates_web.append(n.pubDate)
                    summaries_web.append(n.summary)
                    urls_web.append(n.link)
                    triggers_web.append(t)
                web_data = {'stories_name': stories_web, 'stories_summary': summaries_web, 'stories_date': dates_web,'stories_url': urls_web, 'story_counter': story_counter, 'triggers': triggers_web}
                emit("show stories", web_data, broadcast=True)
                socketio.sleep(1)

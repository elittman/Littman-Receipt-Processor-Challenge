from math import ceil
import uuid
import flask
from flask import Flask, request

app = Flask(__name__)

pointsDict = {}

@app.route('/receipts/process', methods=["POST"])
def process_receipts():
    try:
        receipt = request.json
    except:
        return "The receipt is invalid", 400
    points = calculate_points(receipt)
    id = str(uuid.uuid1())
    # regenerate id if duplicate
    while id in pointsDict:
        id = str(uuid.uuid1())
    pointsDict[id] = points
    content = {
        "id": id,
    }
    return flask.jsonify(**content), 200
    
@app.route('/receipts/<id>/points', methods=["GET"])
def get_points(id):
    if id in pointsDict:
        content = {
            "points": pointsDict[id],
        }
        return flask.jsonify(**content), 200
    else:
        return "No receipt found for that id", 404

def calculate_points(receipt):
    points = 0
    # One point for every alphanumeric character in the retailer name
    points += sum(char.isalnum() for char in receipt["retailer"])

    # 50 points if the total is a round dollar amount with no cents
    if float(receipt["total"]).is_integer():
        points += 50

    # 25 points if the total is a multiple of 0.25
    if float(receipt["total"]) % 0.25 == 0 :
        points += 25

    # 5 points for every two items on the receipt
    points += (len(receipt["items"]) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer
    for item in receipt["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points += ceil(float(item["price"]) * 0.2)

    # 6 points if the day in the purchase date is odd
    purchase_date_number = int(receipt["purchaseDate"][-2:])

    if purchase_date_number % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time_hour_and_minutes = receipt["purchaseTime"].split(':')
    hour = int(purchase_time_hour_and_minutes[0])
    minutes = int(purchase_time_hour_and_minutes[1])
    if (hour == 14 and minutes > 0) or hour == 15:
        points += 10

    return points

if __name__ == '__main__':
    app.run()
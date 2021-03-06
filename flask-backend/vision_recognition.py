from flask import jsonify, request
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import keys
import json
import requests
import semantics


def custom_vision_endpoint(user_image_url):

    payload = {
      #  "Url": user_image_url
        "Url": user_image_url
    }
    headers = {
        "Content-Type": "application/json",
        "Prediction-Key": "66aaad81eed9481bba65df01dfe09420"
    }

    url = "https://southcentralus.api.cognitive.microsoft.com/customvision/v1.0/Prediction/91f2d2f7-5c8d-4eb3-a741-a9c75ab6fc41/url"
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response = response.json()
    # if custom model has high probability rate, return recommendations
    if response['Predictions'][0]['Probability'] > 0.75:
        val = response['Predictions'][0]['Tag']
        return json.dumps(semantics.get_recommendations(val))
    # call clarifai api otherwise
    else:
        k = keys.Keys()
        app = ClarifaiApp(api_key=k.get_clarifai_key())
        # Use apparel model
        model = app.models.get('apparel')
        image = ClImage(url = user_image_url)
        result= model.predict([image])
        concepts = result['outputs'][0]['data']['concepts']
        # check for high confidence
        if concepts[0]['value'] >= 0.9:
            val = concepts[0]['name']
            return json.dumps(semantics.get_recommendations(val))

        # otherwise provide the user with choice
        output = []
        for i in range(3):
            output.append(semantics.get_recommendations(concepts[i]['name']))
        return json.dumps(output)

#custom_vision_endpoint("http://viliflik.files.wordpress.com/2010/10/glasses-best.jpg")
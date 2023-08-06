import os
import requests
from urllib.parse import urlparse
from PIL import Image

class Classify:
    def __init__(self):
        self.LOCALHOST_URL = "http://127.0.0.1:8000/"
        self.URL = "http://ec2-18-142-227-173.ap-southeast-1.compute.amazonaws.com/"
    
    def imageClassify(self, paths=[]):
        """
        Classify an image, from path provided, if it contains nudity, or if it is sexy or safe.

        Args:
            paths (list): List of Image path
        Returns:
            dict: predictions
        """
        files = []
        for path in paths:
            if not os.path.exists(path):
                raise Exception("Path provided does not exists.")
            files.append(('files', open(path, 'rb')))

        response = requests.post(
            url=self.URL+"classify/", files=files).json()

        return response

    def imageClassifyUrl(self, urls=[]):
        """
        Classify an image, from url provided, if it contains nudity, or if it is sexy or safe.

        Args:
            paths (list): List of Image URL or data URI
        Returns:
            dict: predictions
        """
        json = []

        for url in urls:
            json.append({
                "source": url
            })

        response = requests.post(
            url=self.URL+"classify-url/", json=json).json()

        return response

class Detect:

    def __init__(self):
        self.URL = "http://127.0.0.1:8000/"
    
    def save_to_path(self, prediction, save_path):
        """
        Downloads image url and saves it to the save path provided.

        Args:
            prediction (dict): List of Image URL or data URI
            save_path (str): Save path
        """
        url = prediction['url']
        url_path = urlparse(url).path
        print(url_path)
        filename = url_path.split('/')[1]
        image = Image.open(requests.get(url, stream=True).raw)

        if os.path.exists(save_path):
            os.chdir(save_path)
            image.save(filename)
        else:
            raise Exception("Save path does not exist.")
    
    def detectExposed(self, paths=[]):
        """
        Detect exposed parts in an image, from path provided.

        Args:
            paths (list): List of Image path
        Returns:
            dict: predictions
        """
        files = []
        for path in paths:
            if not os.path.exists(path):
                raise Exception("Path provided does not exists.")
            files.append(('files', open(path, 'rb')))

        response = requests.post(
            url=self.URL+"detect/", files=files).json()

        return response
    
    def detectExposedFromUrl(self, urls=[]):
        """
        Detect exposed parts in an image, from url provided.

        Args:
            paths (list): List of Image URL or data URI
        Returns:
            dict: predictions
        """
        json = []

        for url in urls:
            json.append({
                "source": url
            })

        response = requests.post(
            url=self.URL+"detect-url/", json=json).json()

        return response
    
    def censorExposed(self, paths=[], save_path=None):
        """
        Detect exposed parts in an image, from path provided.
        If save path is provided the image URL of censored image
        will be saved in the provded save path.

        Args:
            paths (list): List of Image path
            save_path (str): Save path
        Returns:
            dict: predictions
        """
        files = []
        for path in paths:
            if not os.path.exists(path):
                raise Exception("Path provided does not exists.")
            files.append(('files', open(path, 'rb')))

        response = requests.post(
            url=self.URL+"censor/", files=files).json()

        predictions = response['Prediction']

        if not save_path == None:
            if not os.path.exists(save_path):
                raise Exception("Save Path provided does not exists.")
            for prediction in predictions:
                self.save_to_path(prediction, save_path)

        return response

    def censorExposedFromUrl(self, urls=[], save_path=None):
        """
        Detect exposed parts in an image, from url provided.
        If save path is provided the image URL of censored image
        will be saved in the provded save path.

        Args:
            paths (list): List of Image path
            save_path (str): Save path
        Returns:
            dict: predictions
        """
        json = []

        for url in urls:
            json.append({
                "source": url
            })

        response = requests.post(
            url=self.URL+"censor-url/", json=json).json()

        predictions = response['Prediction']

        if not save_path == None:
            if not os.path.exists(save_path):
                raise Exception("Save Path provided does not exists.")
            for prediction in predictions:
                self.save_to_path(prediction, save_path)

        return response

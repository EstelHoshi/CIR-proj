
class Detector:
    
    def __init__(self, model):
        self._model = model

    def _preprocess(self, image):
        return image

    def predict(self, image):
        image = self._preprocess(image)
        return self._model(image)
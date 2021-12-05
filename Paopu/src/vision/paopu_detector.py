import cv2
import torch
import torchvision
import numpy as np

import torch.nn.functional as F

from detector import Detector

class PaopuDetector(Detector):
    def __init__(self, model):
        mean = 255.0 * np.array([0.485, 0.456, 0.406])
        stdev = 255.0 * np.array([0.229, 0.224, 0.225])
        self._normalize = torchvision.transforms.Normalize(mean, stdev)
        self._device = torch.device('cuda')
        _model = torchvision.models.alexnet(pretrained=False)
        _model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 3)
        _model.load_state_dict(torch.load(model))
        super().__init__(_model.to(self._device))

    def _preprocess(self, image):
        x = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        x = x.transpose((2, 0, 1))
        x = self._normalize(torch.from_numpy(x).float()).to(self._device)
        return x[None, ...]

    def predict(self, image):
        y = super().predict(image)
        y = F.softmax(y, dim=1).flatten()
        return map(float, y)

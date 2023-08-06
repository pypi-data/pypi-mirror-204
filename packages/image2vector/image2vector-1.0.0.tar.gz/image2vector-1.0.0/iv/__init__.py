from typing import List, Union
from pathlib import Path
from io import BytesIO
import torch
import numpy
from PIL import Image
from numpy import ndarray
from torch import Tensor
from torch import device as TorchDevice
from torchvision import transforms
from torchvision.transforms.functional import InterpolationMode
from iv.cirtorch.networks.imageretrievalnet import ImageRetrievalNet
from iv.schemas import Device, Runtime


__version__ = '1.0.0'
VERSION = __version__

preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class ResNet:
    def __init__(
        self,
        # weight_file: Union[Path, str],
        device: Union[Device, str] = Device.CPU,
        runtime: Union[Runtime, str] = Runtime.ONNXRUNTIME,
        runtime_model: Union[Path, str, None] = None,
    ) -> None:
        assert isinstance(device, (Device, str))
        self.device = TorchDevice(
            device.value if isinstance(device, Device) else device)

        # if isinstance(weight_file, Path):
        #     weight_file = str(weight_file)

        # self.weight_file = weight_file

        assert isinstance(runtime, (Runtime, str))
        self.runtime = runtime.value if isinstance(
            runtime, Runtime) else runtime

        assert isinstance(runtime_model, (Path, str))
        self.runtime_model = str(runtime_model) if isinstance(
            runtime_model, Path) else runtime_model

        self.load_network()
        # self.init_transform()

    def load_network(self):

        if self.runtime == Runtime.PYTORCH.value:
            state: dict = torch.load(self.runtime_model)

            state['state_dict']['whiten.weight'] = state['state_dict']['whiten.weight'][0::4, ::]
            state['state_dict']['whiten.bias'] = state['state_dict']['whiten.bias'][0::4]

            network: ImageRetrievalNet = ImageRetrievalNet()

            # print(type(state['state_dict']))
            # print(len(state['state_dict']))

            # for key,value in state['state_dict'].items():
            #     print(key)

            network.load_state_dict(state['state_dict'])
            network.eval()
            network.to(self.device)
            self.network = network

        elif self.runtime == Runtime.ONNXRUNTIME.value:
            import onnxruntime
            ort_session = onnxruntime.InferenceSession(self.runtime_model)
            self.network = ort_session

        elif self.runtime == Runtime.PYTORCH_SCRIPT.value:
            loaded_model = torch.jit.load(self.runtime_model)
            loaded_model.eval()
            loaded_model.to(self.device)
            self.network = loaded_model

        elif self.runtime == Runtime.PYTORCH_TENSORRT.value:
            import torch_tensorrt
            trt_ts_module = torch.jit.load(self.runtime_model)
            trt_ts_module.to(self.device)

            self.network = trt_ts_module

        else:
            raise Exception(f'Unsupported runtime: {self.runtime}')

    def images_to_vectors(self, images: Tensor) -> Tensor:
        if self.runtime == Runtime.PYTORCH.value:
            with torch.no_grad():
                _img_tensor = images.to(self.device)
                features = self.network(_img_tensor)
                vectors = torch.transpose(features, 0, 1)
                return vectors
        elif self.runtime == Runtime.ONNXRUNTIME.value:
            ort_inputs = {
                self.network.get_inputs()[0].name:
                    images.cpu().numpy()
            }
            ort_outputs: list[numpy.ndarray] = self.network.run(
                None, ort_inputs)
            _ort_output = ort_outputs[0]
            _ort_output: ndarray
            _t = torch.from_numpy(_ort_output)
            t = torch.transpose(_t, 0, 1)
            return t

        elif self.runtime == Runtime.PYTORCH_SCRIPT.value:
            with torch.no_grad():
                _img_tensor = images.to(self.device)
                features = self.network(_img_tensor)
                vectors = torch.transpose(features, 0, 1)
                return vectors
        elif self.runtime == Runtime.PYTORCH_TENSORRT.value:
            _img_tensor = images.to(self.device)
            features = self.network(_img_tensor)
            vectors = torch.transpose(features, 0, 1)
            return vectors
        else:
            raise Exception('not support runtime')

    def gen_vector(
        self,
        image: Union[Image.Image, ndarray, Path, str, bytes],
        batch_size: int = 1,
        num_workers: int = 0
    ) -> List[float]:
        if isinstance(image, bytes):
            image_file_like = BytesIO(image)
            image = Image.open(image_file_like).convert('RGB')

        if isinstance(image, Image.Image):
            image = image.convert('RGB')

        if isinstance(image, Path) or isinstance(image, str):
            image = Image.open(str(image)).convert('RGB')

        if isinstance(image, ndarray):
            image = Image.fromarray(image).convert('RGB')

        assert isinstance(image, Image.Image)

        batch_size = 1

        preprocessed_image: torch.Tensor = preprocess(image)
        unsqueezed_image = preprocessed_image.unsqueeze(0)

        _images = torch.cat([unsqueezed_image]*batch_size, dim=0)

        vectors = self.images_to_vectors(_images)

        return vectors.squeeze(0).tolist()

    def gen_vectors(
        self,
        images: List[Union[Image.Image, ndarray, Path, str, bytes]],
        batch_size: int = 1,
        num_workers: int = 0
    ) -> List[List[float]]:

        _images = []

        assert isinstance(images, List)
        assert len(images) > 0

        for index, image in enumerate(images):
            if isinstance(image, bytes):
                image_file_like = BytesIO(image)
                image = Image.open(image_file_like).convert('RGB')
                # _images[index] = image
                _images.append(image)
                assert isinstance(image, Image.Image)

            elif isinstance(image, Image.Image):
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                # _images[index] = image
                _images.append(image)
                assert isinstance(image, Image.Image)

            elif isinstance(image, Path) or isinstance(image, str):
                image = Image.open(str(image)).convert('RGB')
                # _images[index] = image
                _images.append(image)
                assert isinstance(image, Image.Image)

            elif isinstance(image, ndarray):
                image = Image.fromarray(image).convert('RGB')
                # _images[index] = image
                _images.append(image)
                assert isinstance(image, Image.Image)
            else:
                raise Exception(f'Unsupported type: {type(image)}')

        assert isinstance(
            _images[0], Image.Image), f'images[0] type: {type(_images[0])}'

        for index, image in enumerate(_images):
            preprocessed_image: torch.Tensor = preprocess(image)
            unsqueezed_image = preprocessed_image.unsqueeze(0)
            _images[index] = unsqueezed_image

        _images = torch.cat(_images, dim=0)

        vectors = self.images_to_vectors(_images)

        return vectors.tolist()


def l2(vector1: List[float], vector2: List[float]) -> float:
    vector1 = numpy.array(vector1)
    vector2 = numpy.array(vector2)
    return float(numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2))))

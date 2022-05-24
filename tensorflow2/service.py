import bentoml
import numpy as np
import PIL.Image
from bentoml.io import Image, NumpyNdarray

mnist_runner = bentoml.tensorflow.get("tensorflow_mnist:latest").to_runner()

svc = bentoml.Service(
    "tensorflow_mnist_demo",
    runners=[
        mnist_runner,
    ],
)


@svc.api(
    input=NumpyNdarray(dtype="float32", enforce_dtype=True),
    output=NumpyNdarray(dtype="float32"),
)
async def predict_ndarray(inp: "np.ndarray") -> "np.ndarray":
    assert inp.shape == (28, 28)
    # We are using greyscale image and our PyTorch model expect one
    # extra channel dimension
    inp = np.expand_dims(inp, 2)
    return await mnist_runner.async_run(inp)


@svc.api(input=Image(), output=NumpyNdarray(dtype="float32"))
async def predict_image(f: PIL.Image) -> "np.ndarray":
    assert isinstance(f, PIL.Image.Image)
    arr = np.array(f) / 255.0
    assert arr.shape == (28, 28)

    # We are using greyscale image and our PyTorch model expect one
    # extra channel dimension
    arr = np.expand_dims(arr, 2).astype("float32")
    return await mnist_runner.async_run(arr)

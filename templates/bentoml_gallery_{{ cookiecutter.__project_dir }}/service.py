import typing as t

import bentoml
import numpy as np
import PIL.Image

from bentoml.io import Image, NumpyNdarray
from PIL.Image import Image as PILImage

{{ cookiecutter.__project_slug }}_runner = bentoml.{{ cookiecutter.__project_dir }}.load_runner(
    "{{ cookiecutter.__full_name }}",
    name="{{ cookiecutter.__project_slug }}_runner",
    predict_fn_name="predict",
)

svc = bentoml.Service(
    name="{{ cookiecutter.__full_name }}",
    runners=[
        {{ cookiecutter.__project_slug }}_runner,
    ],
)


@svc.api(
    input=NumpyNdarray(dtype="float32", enforce_dtype=True),
    output=NumpyNdarray(dtype="int64"),
)
async def predict_ndarray(inp: "np.ndarray") -> "np.ndarray":
    assert inp.shape == (28, 28)
    # We are using greyscale image and our PyTorch model expect one
    # extra channel dimension
    inp = np.expand_dims(inp, 0)
    output_tensor = await {{ cookiecutter.__project_slug }}_runner.async_run(inp)
    return output_tensor.numpy()


@svc.api(input=Image(), output=NumpyNdarray(dtype="int64"))
async def predict_image(f: PILImage) -> "np.ndarray":
    assert isinstance(f, PILImage)
    arr = np.array(f)/255.0
    assert arr.shape == (28, 28)

    # We are using greyscale image and our PyTorch model expect one
    # extra channel dimension
    arr = np.expand_dims(arr, 0).astype("float32")
    output_tensor = await {{ cookiecutter.__project_slug }}_runner.async_run(arr)
    return output_tensor.numpy()

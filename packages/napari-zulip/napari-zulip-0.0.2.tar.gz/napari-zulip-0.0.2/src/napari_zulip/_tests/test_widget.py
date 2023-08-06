import numpy as np

from napari_zulip import screenshot_to_zulip


def test_screenshot_to_zulip(make_napari_viewer):
    viewer = make_napari_viewer()
    layer = viewer.add_image(np.random.random((100, 100)))

    # this time, our widget will be a MagicFactory or FunctionGui instance
    my_widget = screenshot_to_zulip()


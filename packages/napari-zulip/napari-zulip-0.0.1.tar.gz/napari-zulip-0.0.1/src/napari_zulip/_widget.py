import tempfile
import time
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import zulip
from magicgui import magic_factory

if TYPE_CHECKING:
    import napari

from typing import Annotated

MultiLineStr = Annotated[
    str, (("widget_type", "TextEdit"), ("value", "test text"))
]


@magic_factory
def screenshot_to_zulip(
    viewer: "napari.viewer.Viewer",
    zulip_realm: str = "napari.zulipchat.com",
    stream: str = "randoms",
    topic: str = "napari-zulip",
    content: MultiLineStr = "Test message from napari-zulip",
    caption: MultiLineStr = "This is a screenshot from napari",
    canvas_only: bool = True,
):
    # Global parameters
    config_path = str(Path.home() / ".zulip.d" / f"{zulip_realm}.zuliprc")

    # Globals vars
    client = zulip.Client(config_file=config_path)

    tf = tempfile.NamedTemporaryFile(suffix=".png")
    local_path = tf.name

    # Save screenshot into temp file
    viewer.screenshot(path=local_path, canvas_only=canvas_only)

    with open(local_path, "rb") as fp:
        upload_result = client.upload_file(fp)

    message_content = f"{content} ![{caption}]({upload_result['uri']})"

    message_request = {
        "type": "stream",
        "to": stream,
        "topic": topic,
        "content": message_content,
    }

    client.send_message(message_request)


if __name__ == "__main__":
    import napari

    viewer = napari.Viewer()

    img = np.random.rand(256, 256)
    layer = viewer.add_image(img)

    widget = screenshot_to_zulip()
    widget.viewer.value = viewer
    widget.content.value = "Test message from napari-zulip"
    widget.caption.value = "This is a screenshot from napari"
    viewer.window.add_dock_widget(widget, name="napari-zulip")

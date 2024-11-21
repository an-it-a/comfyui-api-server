import functions_framework
import time

from call_comfyui_unsecure import CallComfyUI

server_address = "127.0.0.1:8188"


@functions_framework.http
def main_handle(request):
    request_json = request.get_json(silent=True)

    workflow = request_json['workflow']

    comfyui_call = CallComfyUI(server_address)

    images = comfyui_call.call(workflow)

    results = []
    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            filename = str(round(time.time()))
            image.save("/vol1/output/" + filename + ".png")
            results.append(filename)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    text = '{"results":"' + str(results) + '.png"}'
    return (text, 200, headers)
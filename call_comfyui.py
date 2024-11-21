from websocket import create_connection
import json
import urllib.request
import urllib.parse
import uuid

class CallComfyUI:
    def __init__(self, server_address, token):
        self.server_address = server_address
        self.token = token
        self.client_id = str(uuid.uuid4())

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request("https://{}/prompt".format(self.server_address), data=data)
        req.add_header("Authorization", "Bearer {}".format(self.token))
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        req = urllib.request.Request("https://{}/view?{}".format(self.server_address, url_values))
        req.add_header("Authorization", "Bearer {}".format(self.token))
        with urllib.request.urlopen(req) as response:
            return response.read()

    def get_history(self, prompt_id):
        req = urllib.request.Request("https://{}/history/{}".format(self.server_address, prompt_id))
        req.add_header("Authorization", "Bearer {}".format(self.token))
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())

    def get_images(self, ws, prompt):
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                # If you want to be able to decode the binary stream for latent previews, here is how you can do it:
                # bytesIO = BytesIO(out[8:])
                # preview_image = Image.open(bytesIO) # This is your preview in PIL image format, store it in a global
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

        return output_images

    def call(self, prompt):
        ws = create_connection("wss://{}/ws?clientId={}".format(self.server_address, self.client_id),
                               header=["Authorization: Bearer {}".format(self.token)]
                               )
        images = self.get_images(ws, prompt)
        ws.close()
        return images
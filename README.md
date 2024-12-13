# ComfyUI with HTTP API in Cloud Run

## To add models or custom nodes, update Dockerfile

## Request Curl
<i>Remember to replace your endpoint URL!</i>
```
curl -X POST -H 'Content-Type: application/json' \
-H "Authorization: Bearer $(gcloud auth print-identity-token)" \
-d '{"workflow": {"1":{"inputs":{"ckpt_name":"beautifulRealistic_v60.safetensors"},"class_type":"CheckpointLoaderSimple","_meta":{"title":"Load Checkpoint"}},"2":{"inputs":{"seed":866395120630463,"steps":20,"cfg":8,"sampler_name":"euler","scheduler":"normal","denoise":1,"model":["1",0],"positive":["4",0],"negative":["5",0],"latent_image":["6",0]},"class_type":"KSampler","_meta":{"title":"KSampler"}},"4":{"inputs":{"text":"1girl, long blonde hair, red sweater, facing camera, smiling, professionally, professionally color graded, half body shot, sharp focus, 8 k high definition, dslr, soft lighting, insanely detailed, intricate, elegant, matte skin","clip":["1",1]},"class_type":"CLIPTextEncode","_meta":{"title":"CLIP Text Encode (Prompt)"}},"5":{"inputs":{"text":"nsfw, sexy, breast, nude, 2 heads, duplicate, blurry, abstract, disfigured, deformed, framed, bad art, poorly drawn, extra limbs, b&w, weird colors, watermark, blur haze, long neck, elongated body, cropped image, out of frame, draft, deformed hands, twisted fingers, double image, malformed hands, multiple heads, ugly, poorly drawn hands, missing limb, cut-off, over satured, grain, lowres, bad anatomy, poorly drawn face, mutation, mutated, floating limbs, disconnected limbs, out of focus, long body, disgusting, extra fingers, missing arms, mutated hands, cloned face, missing legs,","clip":["1",1]},"class_type":"CLIPTextEncode","_meta":{"title":"CLIP Text Encode (Prompt)"}},"6":{"inputs":{"width":512,"height":512,"batch_size":1},"class_type":"EmptyLatentImage","_meta":{"title":"Empty Latent Image"}},"7":{"inputs":{"samples":["2",0],"vae":["8",0]},"class_type":"VAEDecode","_meta":{"title":"VAE Decode"}},"8":{"inputs":{"vae_name":"vaeFtMse840000EmaPruned_vae.safetensors"},"class_type":"VAELoader","_meta":{"title":"Load VAE"}},"9":{"inputs":{"images":["7",0]},"class_type":"PreviewImage","_meta":{"title":"Preview Image"}}}}' \
https://comfyui-api-server-111919368185.us-central1.run.app | jq .
```

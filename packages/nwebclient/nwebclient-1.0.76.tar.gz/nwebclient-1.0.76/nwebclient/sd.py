from nwebclient import sdb
from nwebclient import ticker
import json
import os
import requests
import time

from diffusers import PNDMScheduler, DDIMScheduler, LMSDiscreteScheduler, EulerDiscreteScheduler, DPMSolverMultistepScheduler
from diffusers import UniPCMultistepScheduler
import torch
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

def gen(pipe, prompt='photo', negative_prompt = None, prefix='sd',  guidance_scale = 7.5, num_inference_steps=30, height=800, width=640, num_images=1, dbfile='data.db'):
    # https://huggingface.co/docs/diffusers/v0.14.0/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline.__call__
    images = pipe(
      prompt,
      height = 800,
      width = 640,
      num_inference_steps = num_inference_steps,      # higher better quali default=45
      guidance_scale = guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
      num_images_per_prompt = num_images,
      negative_prompt = negative_prompt,
      ).images
    for i in range(len(images)):
        #  images[i].save(prefix+str(i)+".jpg")
        sdb.sdb_write_pil(images[i], prompt, negative_prompt, guidance_scale, prefix, dbfile)


"""
  from nwebclient import sd
  ig = sd.ImageGen()
  ig.prompt = "photo"
  ig.loop(5)
  
  ig.executeFromUrl('https://...')
"""
class ImageGen:
    generator = 'diffusers' # diffusers or automatic1111 dummy cn_pose_1111 diffcn
    # scheduler
    pipe = None
    prompt = "photo"
    negative_prompt = "text, cartoon, anime, drawing, meme, postcard, painting, ((fuzzy)), ((blurred)), ((low resolution)), ((b&w)), ((monochrome)), ambiguous, ((deformed)), oversaturated, ((out of shot)), ((incoherent)), (((glitched))), (((3d render))), cgi, ((incorrect anatomy)), bad hands, lowres, long body, ((blurry)), double, ((duplicate body parts)), (disfigured), (extra limbs), fused fingers, extra fingers, malformed hands, ((((mutated hands and fingers)))), conjoined, ((missing limbs)), logo, signature, mutated, jpeg artifacts, low quality, bad eyes, oversized, disproportionate, (((incorrect proportions))), exaggerated, (((aliasing)))"
    guidance_scale = 7.5
    num_inference_steps=25
    height=800
    width=640
    num_images=1
    prefix = 'sd'
    dbfile='data.db'
    # sdb jpg
    save_mode='sdb'
    loaded_model = None
    gen_count = 0
    api = None
    cn_image = None
    diff_cn = None
    def __init__(self, model_id="XpucT/Deliberate"):
        self.model_id = model_id
    def load(self):
        if self.loaded_model == self.model_id:
            return
        self.scheduler = DPMSolverMultistepScheduler.from_pretrained(self.model_id, subfolder="scheduler")
        device = "cuda"
        model_revision = None
        if self.scheduler is None:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, torch_dtype=torch.float16, revision=model_revision)
        else:
           self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, scheduler=self.scheduler,  torch_dtype=torch.float16, revision=model_revision) # custom_pipeline="lpw_stable_diffusion",
        self.pipe = self.pipe.to(device)
        if self.model_id=="XpucT/Deliberate" or self.model_id == "SG161222/Realistic_Vision_V1.4_Fantasy.ai":
            self.pipe.safety_checker = lambda images, clip_input: (images, False)
        self.load_model = self.model_id
    def initA1111(self):
        import webuiapi
        if self.api is None:
            self.api = webuiapi.WebUIApi()
    def initDiffCn(self):
        if self.diff_cn is None:
            self.controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-openpose")#, ) lllyasviel/sd-controlnet-canny
            self.diff_cn = StableDiffusionControlNetPipeline.from_pretrained(model_id, controlnet=controlnet) # , torch_dtype=torch.float16
            self.diff_cn.scheduler = UniPCMultistepScheduler.from_config(controlnet_pipe.scheduler.config)
            self.diff_cn.enable_model_cpu_offload()
            #controlnet_pipe.enable_xformers_memory_efficient_attention()
            self.diff_cn = self.diff_cn.to("cuda")
            if self.model_id=="XpucT/Deliberate" or self.model_id == "SG161222/Realistic_Vision_V1.4_Fantasy.ai":
                self.diff_cn.safety_checker = lambda images, clip_input: (images, False)
    def gen(self, loop_number=1):
        if self.generator == 'diffusers':
            self.genDiffusers(loop_number)
        elif self.generator == 'automatic1111':
            self.genA1111(loop_number)
        elif self.generator == 'cn_pose_1111':
            self.genA1111(loop_number)
        elif self.generator == 'diffcn':
            self.genDiffCn(loop_number)
        elif self.generator == 'dummy':
            time.sleep(1)
            print("Dummy Generation; " + str(loop_number))
            self.gen_count = self.gen_count + 1
    def genDiffCn(self, loop_number=1):
        self.initDiffCn()
        output= self.diff_cn(self.prompt, self.cn_image, negative_prompt=self.negative_prompt, num_inference_steps=25, num_images_per_prompt = 1, height = self.height, width = self.width)
        self.save_image(output[0][0], 0,loop_number)
        self.gen_count = self.gen_count + 1
    def genCnPose1111(self, loop_number=1):
        self.initA1111();
        result = self.api.txt2img(prompt=self.prompt,negative_prompt=self.negative_prompt, height=self.height, width=self.width, controlnet_units=[self.cn_image],cfg_scale=7)
        self.save_image(result.image, 0,loop_number)
        self.gen_count = self.gen_count + 1
    def genA1111(self, loop_number=1):  
        self.initA1111();
        result = self.api.txt2img(prompt=self.prompt,negative_prompt=self.negative_prompt, height=self.height, width=self.width, cfg_scale=7)
        self.save_image(result.image, 0,loop_number)
        self.gen_count = self.gen_count + 1
    def genDiffusers(self, loop_number=1):
        if self.pipe is None:
            self.load()
        images = self.pipe(self.prompt,
            height = self.height,
            width = self.width,
            num_inference_steps = self.num_inference_steps,      # higher better quali default=45
            guidance_scale = self.guidance_scale,                # Prioritize creativity  7.5  Prioritize prompt (higher)
            num_images_per_prompt = self.num_images,
            negative_prompt = self.negative_prompt,
        ).images
        self.gen_count = self.gen_count + 1
        for i in range(len(images)):
            #  images[i].save(prefix+str(i)+".jpg")
            self.save_image(images[i], i, loop_number)
    def save_image(self, image, i, loop_number):
        if self.save_mode == 'sdb':
            sdb.sdb_write_pil(image, self.prompt, self.negative_prompt, self.guidance_scale, self.prefix, self.dbfile)
        if self.save_mode == 'jpg':
            image.save(self.prefix+'_'+str(loop_number)+'_'+str(i)+'.jpg')
    def loop(self, count):
        for i in range(count):
            print("Loop "+str(i)+"/"+str(count))
            self.gen(loop_number=i)
    def execute(self, data):
        if "prompt" in data:
            self.prompt = data['prompt']
        if "negative_prompt" in data:
            self.negative_prompt = data['negative_prompt']
        if "prefix" in data:
            self.prefix = data['prefix']
        if "guidance_scale" in data:
            self.guidance_scale = float(data['guidance_scale'])
        if "height" in data:
            self.height = int(data['height'])
        if "width" in data:
            self.width = int(data['width'])
        if "model" in data:
            self.model_id = data['model']
            self.load()
        count = 10
        if "count" in data:
            count = int(data['count'])
        self.loop(count)
    def executeJsonFile(self, file, delete=True):
        data = json.load(open(file))
        self.execute(data)
        if delete:
            os.remove(file)
    def executeMany(self, data, count = 50):
        for key in data:
            self.prompt = data[key]
            self.prefix = key
            self.loop(count)
    def executeJobs(self, data):
        self.info("Start: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        jobs = data['jobs']
        i = 0
        for job in jobs:
            self.info("Job " + str(i) + "/" + str(len(jobs)) )
            self.execute(job)
            i=i+1
        result_url = data['result_url']
        if result_url.startswith('http'):
            files = {'upload_file': open('data.db', 'rb')}
            params = {'name': data['worker_name'], 'g': data['group_id']}
            res = requests.post(result_url, params=params, files=files)
            print(res.text)
        self.info("End: "+time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime()))
        return i
    def executeFromUrl(self, url):
        res = requests.get(url)
        data = json.loads(res.text)
        return self.executeJobs(data)
    def info(self, message):
        print("[INFO] " + message)
            
            
        
class ImageGenProcess(ticker.FileExtObserver):
    ext = ".sdjob"
    def __init__(self, generator):
        self.generator = generator
    def processFile(self, filename):
        self.generator.executeJsonFile(filename)

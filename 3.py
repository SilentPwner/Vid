# الخلية 3: توليد الصورة من النص
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    use_safetensors=True
)
pipe = pipe.to("cuda")
pipe.enable_xformers_memory_efficient_attention()

# بناء الـ prompt
prompt = f"{user_input}, digital art, clean background"
negative_prompt = "blurry, ugly, disfigured, multiple people"

# توليد الصورة
with torch.no_grad():
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=512,
        height=512,
        num_inference_steps=25
    ).images[0]

# حفظ الصورة
image_path = "generated_image.png"
image.save(image_path)
print("Image generated successfully!")
display.display(image)
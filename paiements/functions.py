from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO



def calc_cumul_int(*args):
    prod_sum = 0
    for i in list(args):
        try: 
            prod_sum = int(i) + prod_sum
        except: 
            continue
    return prod_sum



def resize_image(file, max_size):
    # Open the image file
    img = Image.open(file)
    
    # Calculate the aspect ratio
    aspect_ratio = img.width / img.height
    if aspect_ratio > 1:
        new_width = min(max_size, img.width)
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = min(max_size, img.height)
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save the resized image to a BytesIO object
    img_io = BytesIO()
    resized_img.save(img_io, format=img.format)
    img_io.seek(0)
    
    # Create a new InMemoryUploadedFile object
    resized_file = InMemoryUploadedFile(
        img_io, None, file.name, file.content_type, img_io.tell, None
    )
    
    return resized_file


def is_image_extension_valid(file) -> bool:
    allowed_extensions = ['jpg','jpeg','png']
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return False
    return True
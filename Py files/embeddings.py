import openai
import torch
import numpy as np
import pytesseract
import os
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel
from extraction import extract_data  # Import the extraction function


load_dotenv(dotenv_path=r'M:\OKCU\Project\Chatdoc\.env')
openai.api_key = os.getenv('OPENAI_API_KEY')  

# Initialize CLIP processor and model
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

def get_text_embedding(text):
    """Generate text embedding using OpenAI's API."""
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # You can adjust the model name based on your preference
        input=text
    )
    return np.array(response['data'][0]['embedding'])

def get_image_embedding(image):
    """Generate image embedding using CLIP."""
    inputs = processor(images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        image_embeddings = clip_model.get_image_features(**inputs)
    return image_embeddings.squeeze(0).cpu().numpy()

def get_text_from_image(image):
    """Extract text from an image using OCR."""
    return pytesseract.image_to_string(image).strip()

def generate_embeddings(file_path):
    """Generate embeddings for the extracted data from the document."""
    # Extract text and images from the document
    page_data = extract_data(file_path)
    
    result = []

    for page_info in page_data:
        page_embeddings = {}
        page_embeddings['page'] = page_info['page']
        
        # Get text embedding for the page text
        page_embeddings['text_embedding'] = get_text_embedding(page_info['text'])
        
        page_embeddings['images'] = []
        
        # Process images and their corresponding text
        for img_info in page_info['images']:
            img = img_info['image']
            
            # Get image embedding using CLIP
            image_embedding = get_image_embedding(img)
            
            # Extract text from the image and get its corresponding text embedding
            text_on_image = img_info['text_from_image']
            text_on_image_embedding = get_text_embedding(text_on_image)
            
            page_embeddings['images'].append({
                'image_embedding': image_embedding,
                'text_on_image_embedding': text_on_image_embedding
            })
        
        # Combine the embeddings (text, images, and text on images)
        combined_embedding = np.concatenate([
            page_embeddings['text_embedding'], 
            np.mean([item['image_embedding'] for item in page_embeddings['images']], axis=0),
            np.mean([item['text_on_image_embedding'] for item in page_embeddings['images']], axis=0)
        ])
        
        page_embeddings['combined_embedding'] = combined_embedding
        result.append(page_embeddings)
    
    return result


# Example usage
file_path = r"C:\\Users\\Vasanth\\Desktop\\which chart when.pdf"
embeddings_data = generate_embeddings(file_path)

# Print only the combined embeddings for each page (no text)
for page_info in embeddings_data:
    print(f"Page: {page_info['page']}")
    # print(f"Text:\n{page_info['text']}")  # Commented out text print
    # print(f"Number of Images: {len(page_info['images'])}")  # Commented out image count print
    # for img_info in page_info['images']:
    #     print(f"Image Text: {img_info['text_from_image']}")  # Commented out image text print
    print(f"Combined embedding:\n{page_info['combined_embedding']}")
    print("\n" + "-"*50 + "\n")

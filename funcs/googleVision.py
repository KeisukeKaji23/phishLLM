# Let's start by importing the necessary modules only once at the beginning of the script
from google.cloud import vision
import io


def pil_to_byte_array(image):
    """Converts a PIL image to a byte array."""
    byte_array = io.BytesIO()
    image.save(byte_array, format="PNG")
    byte_array = byte_array.getvalue()

    return byte_array


def detect_features(image, feature_type):
    """Detects features in the PIL image."""
    client = vision.ImageAnnotatorClient()

    # Convert the PIL image to bytes
    byte_array = pil_to_byte_array(image)

    # Create a vision.Image object
    vision_image = vision.Image(content=byte_array)

    if feature_type == "logos":
        response = client.logo_detection(image=vision_image)
        features = response.logo_annotations
    elif feature_type == "labels":
        response = client.label_detection(image=vision_image)
        features = response.label_annotations
    elif feature_type == "text":
        response = client.text_detection(image=vision_image)
        features = response.text_annotations
        if features:
            features = [features[0]]  # Only keep the first result
    else:
        raise ValueError(
            "Invalid feature type. Available types are: logos, labels, text."
        )

    # Convert the results to a dictionary and return it
    # Now we include position information instead of score
    return [feature.description for feature in features]


def detect_logos(image):
    """Detects logos in the PIL image."""
    return detect_features(image, "logos")


def detect_labels(image):
    """Detects labels in the PIL image."""
    return detect_features(image, "labels")


def detect_text(image):
    """Detects text in the PIL image."""
    return detect_features(image, "text")

import dlib
import cv2
import numpy as np
import os
from scipy.spatial import distance

MODELS_PATH = "/app/models/"
FACES_PATH = "/app/faces/"
TO_IDENTIFY_PATH = "/app/to-identify/"


def load_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(MODELS_PATH + "shape_predictor_5_face_landmarks.dat")
    facerec = dlib.face_recognition_model_v1(MODELS_PATH + "dlib_face_recognition_resnet_model_v1.dat")
    return detector, sp, facerec


def extract_embeddings(detector, sp, facerec, image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector(image, 1)
    if not faces:
        return None
    shape = sp(image, faces[0])
    return np.array(facerec.compute_face_descriptor(image, shape))


def load_known_embeddings(detector, sp, facerec):
    known_embeddings = {}
    for user_id in os.listdir(FACES_PATH):
        user_path = os.path.join(FACES_PATH, user_id)
        if os.path.isdir(user_path):
            embeddings = [extract_embeddings(detector, sp, facerec, os.path.join(user_path, f))
                          for f in os.listdir(user_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
            embeddings = [e for e in embeddings if e is not None]
            if embeddings:
                known_embeddings[user_id] = np.mean(embeddings, axis=0)
    return known_embeddings


def identify_face(new_embedding, known_embeddings, threshold=0.6):
    min_dist = float("inf")
    identity = None
    for user_id, known_embedding in known_embeddings.items():
        dist = distance.euclidean(new_embedding, known_embedding)
        if dist < min_dist and dist < threshold:
            min_dist = dist
            identity = user_id
    return identity


def process_images_to_identify(detector, sp, facerec, known_embeddings):
    for filename in os.listdir(TO_IDENTIFY_PATH):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(TO_IDENTIFY_PATH, filename)
            new_embedding = extract_embeddings(detector, sp, facerec, image_path)
            if new_embedding is not None:
                identity = identify_face(new_embedding, known_embeddings)
                if identity:
                    print(f'Imagem: {filename} identificada como: {identity}')
                else:
                    print(f'Imagem: {filename} não identificada.')
            else:
                print(f'Nenhuma face detectada em: {filename}.')


if __name__ == '__main__':
    local_detector, local_sp, local_facerec = load_models()
    local_known_embeddings = load_known_embeddings(detector=local_detector, sp=local_sp, facerec=local_facerec)
    process_images_to_identify(
        detector=local_detector,
        sp=local_sp,
        facerec=local_facerec,
        known_embeddings=local_known_embeddings)

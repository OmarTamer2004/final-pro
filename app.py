
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("garbage_classifier.keras")
    class_names = np.load("class_names.npy", allow_pickle=True)
    return model, class_names

model, class_names = load_model()

st.title("🗑️ Garbage Classification App")
st.markdown("Upload an image of garbage, and the model will classify it.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction)

    st.markdown(f"### 🧠 Prediction: `{predicted_class}`")
    st.markdown(f"### 🔍 Confidence: `{confidence * 100:.2f}%`")

from pathlib import Path

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parent

# model live here
MODEL_PATH = BASE_DIR / "best.pt"

# image size
IMG_SIZE = 640


# =========================================================
# CONFIDENCE
# =========================================================

# special class get special confidence
CLASS_CONF = {
    "wrinkle": 0.05,
}

# everything else use this
DEFAULT_CONF = 0.25

# YOLO get low number first
# then filter by class later
YOLO_CONF = 0.01


# =========================================================
# TITLE
# =========================================================

st.title("🧵 Fabric Defect Detection")

st.markdown(
    "YOLO11s fabric defect detection system"
)

st.markdown("---")


# =========================================================
# LOAD MODEL
# =========================================================

# check model
if not MODEL_PATH.exists():

    st.error(
        f"Model not found: {MODEL_PATH}"
    )

    st.stop()


# load model
model = YOLO(str(MODEL_PATH))


# =========================================================
# UPLOAD
# =========================================================

st.header("Upload Image")

uploaded_file = st.file_uploader(
    "Choose image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)


# no image = do nothing
if uploaded_file is None:

    st.info(
        "Please upload a image."
    )

    st.stop()


# =========================================================
# GET IMAGE
# =========================================================

image = Image.open(
    uploaded_file
).convert("RGB")

image_np = np.array(image)


# show uploaded image
st.subheader("Uploaded Image")

st.image(
    image,
    caption="Original image",
    use_container_width=True
)


# =========================================================
# BUTTON
# =========================================================

st.markdown("---")

scan = st.button(
    "🔍 Inspect Fabric"
)


# no click = stop
if not scan:

    st.info(
        "Click Inspect Fabric to start."
    )

    st.stop()


# =========================================================
# RUN YOLO
# =========================================================

with st.spinner("Inspecting fabric..."):

    # YOLO finds low confidence box first
    results = model.predict(
        image,
        imgsz=IMG_SIZE,
        conf=YOLO_CONF,
        verbose=False
    )


result = results[0]


# =========================================================
# GET ONLY GOOD DETECTIONS
# =========================================================

detections = []


if (
    result.boxes is not None
    and len(result.boxes) > 0
):

    for i in range(
        len(result.boxes)
    ):

        # get class number
        class_id = int(
            result.boxes.cls[i].item()
        )

        # get confidence
        confidence = float(
            result.boxes.conf[i].item()
        )

        # get class name
        class_name = result.names[
            class_id
        ]

        # get class confidence
        # special class = special threshold
        # everything else = default
        threshold = CLASS_CONF.get(
            class_name,
            DEFAULT_CONF
        )

        # too weak = throw away
        if confidence < threshold:
            continue

        # get box
        box = (
            result.boxes.xyxy[i]
            .cpu()
            .numpy()
            .astype(int)
        )

        detections.append(
            {
                "class": class_name,
                "confidence": confidence,
                "threshold": threshold,
                "box": box
            }
        )


# =========================================================
# BOX
# =========================================================

# copy image
output = cv2.cvtColor(
    image_np.copy(),
    cv2.COLOR_RGB2BGR
)


for detection in detections:

    # get box
    x1, y1, x2, y2 = detection["box"]

    # get name
    class_name = detection["class"]

    # get confidence
    confidence = detection["confidence"]

    # draw box
    cv2.rectangle(
        output,
        (x1, y1),
        (x2, y2),
        (42, 112, 210),
        3
    )

    # text on box
    label = (
        f"{class_name} "
        f"{confidence:.0%}"
    )

    font = cv2.FONT_HERSHEY_SIMPLEX

    # get text size
    (
        text_w,
        text_h
    ), _ = cv2.getTextSize(
        label,
        font,
        0.6,
        2
    )

    # don't let text go outside image
    label_y = max(
        y1,
        text_h + 10
    )

    # text background
    cv2.rectangle(
        output,
        (
            x1,
            label_y - text_h - 10
        ),
        (
            x1 + text_w + 10,
            label_y
        ),
        (42, 112, 210),
        -1
    )

    # write text
    cv2.putText(
        output,
        label,
        (
            x1 + 5,
            label_y - 5
        ),
        font,
        0.6,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )


# BGR back to RGB
output_rgb = cv2.cvtColor(
    output,
    cv2.COLOR_BGR2RGB
)


# =========================================================
# RESULT
# =========================================================

st.markdown("---")

st.header("Inspection Result")


# show result image
st.image(
    output_rgb,
    caption="Detection result",
    use_container_width=True
)


# =========================================================
# SUMMARY
# =========================================================

st.subheader("Detection Summary")

# count all boxes
total_defects = len(detections)

# count different classes
defect_types = len(
    set(
        d["class"]
        for d in detections
    )
)

# get highest confidence
if detections:

    highest_confidence = max(
        d["confidence"]
        for d in detections
    )

else:

    highest_confidence = 0


# print summary
st.text(
    f"Total defects detected: {total_defects}\n"
    f"Defect types detected: {defect_types}\n"
    f"Highest confidence: {highest_confidence:.1%}"
)


# =========================================================
# STATUS
# =========================================================

if detections:

    st.warning(
        f"{total_defects} fabric defect(s) detected."
    )

else:

    st.success(
        "No fabric defects detected."
    )


# =========================================================
# TEXT RESULT
# =========================================================

st.markdown("---")

st.subheader("Detection Result")


# make plain text result
if detections:

    result_text = ""

    for i, detection in enumerate(
        detections,
        1
    ):

        result_text += (
            f"{i}. "
            f"{detection['class']} | "
            f"Confidence: "
            f"{detection['confidence']:.1%} | "
            f"Threshold: "
            f"{detection['threshold']:.0%}\n"
        )

    st.text(result_text)

else:

    st.text(
        "No defects detected."
    )
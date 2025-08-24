# الخلية 4: استخراج الهيكل العظمي
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def extract_pose(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if not results.pose_landmarks:
        print("No pose detected. Using default motion.")
        return None
    
    # رسم الهيكل العظمي على الصورة
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
    )
    
    # حفظ الصورة المشروحة
    annotated_path = "annotated_pose.png"
    cv2.imwrite(annotated_path, annotated_image)
    
    print("Pose extracted and annotated image saved.")
    display.display(Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)))
    return results.pose_landmarks

landmarks = extract_pose(image_path)
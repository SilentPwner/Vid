# الخلية 6: تطبيق تأثير الحركة من فيديو مرجعي
def apply_motion_based_on_description(static_image_path, parsed_description, output_path="final_output.mp4"):
    """
    تختار الفيديو المرجعي المناسب بناءً على وصف المستخدم
    """
    # تحديد الفيديو المناسب بناءً على الإجراء
    action_to_video = {
        "eat": "eating_action.mp4",
        "walk": "walking_action.mp4", 
        "run": "running_action.mp4",
        "talk": "talking_action.mp4"
    }
    
    # تحديد خلفية الفيديو
    background_to_video = {
        "beach": "beach_background.mp4",
        "park": "park_background.mp4",
        "room": "room_background.mp4"
    }
    
    # اختيار فيديو الحركة المناسب
    action_video = None
    for action in parsed_description["actions"]:
        if action in action_to_video:
            action_video = action_to_video[action]
            break
    
    # إذا لم نجد فيديو حركة مناسب، نستخدم فيديو افتراضي
    if action_video is None:
        action_video = "walking_action.mp4"
    
    # اختيار فيديو الخلفية المناسب
    background_video = None
    for obj in parsed_description["objects"] + [parsed_description.get("background", "")]:
        if obj in background_to_video:
            background_video = background_to_video[obj]
            break
    
    # إذا لم نجد فيديو خلفية مناسب، نستخدم فيديو افتراضي
    if background_video is None:
        background_video = "room_background.mp4"
    
    # مسارات الفيديوهات
    action_video_path = f"assets/videos/reference/{action_video}"
    background_video_path = f"assets/videos/reference/{background_video}"
    
    print(f"Using action video: {action_video}")
    print(f"Using background video: {background_video}")
    
    # التأكد من وجود الفيديوهات
    if not os.path.exists(action_video_path):
        raise FileNotFoundError(f"Action video not found: {action_video_path}")
    if not os.path.exists(background_video_path):
        raise FileNotFoundError(f"Background video not found: {background_video_path}")
    
    # دمج الفيديوهين مع الصورة
    final_video = combine_videos_with_image(static_image_path, action_video_path, background_video_path, output_path)
    
    return final_video

def combine_videos_with_image(static_img_path, action_video_path, background_video_path, output_path):
    """
    تدمج الفيديوهين مع الصورة الثابتة
    """
    # تحميل الصورة الثابتة
    static_img = cv2.imread(static_img_path)
    if static_img is None:
        raise ValueError(f"Could not load image from: {static_img_path}")
    
    # فتح فيديو الحركة
    action_cap = cv2.VideoCapture(action_video_path)
    if not action_cap.isOpened():
        raise ValueError(f"Could not open action video: {action_video_path}")
    
    # فتح فيديو الخلفية
    bg_cap = cv2.VideoCapture(background_video_path)
    if not bg_cap.isOpened():
        raise ValueError(f"Could not open background video: {background_video_path}")
    
    # الحصول على خصائص فيديو الحركة
    width = int(action_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(action_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = action_cap.get(cv2.CAP_PROP_FPS)
    
    # إعداد كاتب الفيديو الناتج
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # ضبط حجم الصورة ليتناسب مع الفيديو
    static_img_resized = cv2.resize(static_img, (width, height))
    
    frame_count = 0
    while action_cap.isOpened():
        ret_action, action_frame = action_cap.read()
        ret_bg, bg_frame = bg_cap.read()
        
        if not ret_action:
            break
        
        # إذا انتهى فيديو الخلفية، نعيد تشغيله
        if not ret_bg:
            bg_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret_bg, bg_frame = bg_cap.read()
        
        # دمج الإطارات الثلاثة (الخلفية، الصورة، الحركة)
        combined_frame = bg_frame.copy()
        alpha = 0.7
        combined_frame = cv2.addWeighted(combined_frame, 1, static_img_resized, alpha, 0)
        beta = 0.3
        combined_frame = cv2.addWeighted(combined_frame, 1, action_frame, beta, 0)
        
        # إضافة معلومات عن الإطار
        cv2.putText(combined_frame, f"Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        out.write(combined_frame)
        frame_count += 1
        
        if frame_count % 30 == 0:
            print(f"Processing frame {frame_count}")
    
    action_cap.release()
    bg_cap.release()
    out.release()
    
    print(f"Video processing complete! Saved to: {output_path}")
    return output_path

# معالجة الفيديو بناءً على وصف المستخدم
final_video = apply_motion_based_on_description("generated_image.png", parsed)

# عرض الفيديو النهائي
print("Final video:")
display(Video(final_video, embed=True))
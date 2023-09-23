import cv2
import pyrealsense2 as rs
import numpy as np

# Create a pipeline
pipeline = rs.pipeline()

# Create a configuration object
config = rs.config()

# Enable color and depth streams with their resolutions
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start the pipeline
pipeline.start(config)

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

while True:
    # Wait for a coherent pair of frames: color and depth
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    # Convert the color and depth frames to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # Detect faces in the color image
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.3, 5)

    for x, y, w, h in faces:
        # Calculate the position of the recognition box relative to the center of the screen
        center_x = x + (w // 2)
        center_y = y + (h // 2)
        screen_center = (color_image.shape[1] // 2, color_image.shape[0] // 2)
        position_x = center_x - screen_center[0]
        position_y = center_y - screen_center[1]

        # Get the depth value at the center of the recognition box
        depth_value = depth_frame.get_distance(center_x, center_y)

        # Draw a rectangle around the face in the color image
        cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the depth value and position relative to the center
        cv2.putText(
            color_image,
            "Depth: {0:.2f} m".format(depth_value),
            (x, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            color_image,
            "Position: ({0}, {1})".format(position_x, position_y),
            (x, y - 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

    # Display the color image with face detection
    cv2.imshow("Face Detection", color_image)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Stop the pipeline and close OpenCV windows
pipeline.stop()
cv2.destroyAllWindows()

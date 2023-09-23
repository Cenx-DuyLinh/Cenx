import cv2
import pyrealsense2 as rs
import numpy as np

# Initialize RealSense pipeline and configuration
pipeline = rs.pipeline()
config = rs.config()

video_config = {
    "stream_type_color": rs.stream.color,
    "stream_type_depth": rs.stream.depth,
    "width": 640,
    "height": 480,
    "format_color": rs.format.bgr8,
    "format_depth": rs.format.z16,
    "framerate": 30,
}
config.enable_stream(
    video_config["stream_type_color"],
    video_config["width"],
    video_config["height"],
    video_config["format_color"],
    video_config["framerate"],
)
config.enable_stream(
    video_config["stream_type_depth"],
    video_config["width"],
    video_config["height"],
    video_config["format_depth"],
    video_config["framerate"],
)

# Start pipeline
pipeline.start(config)

# Retrieve sensor profile for each stream
profile = pipeline.get_active_profile()
color_sensor = profile.get_device().query_sensors()[
    0
]  # Assuming the color stream is the first sensor
depth_sensor = profile.get_device().query_sensors()[
    1
]  # Assuming the depth stream is the second sensor

color_min = np.uint8([255, 0, 0])  # Red
color_max = np.uint8([75, 0, 255])  # Dark Blue
while True:
    frames = pipeline.wait_for_frames()

    # Get color stream
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())

    # Get depth stream
    depth_frame = frames.get_depth_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    depth_colormap = cv2.applyColorMap(
        cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
    )
    mask = cv2.inRange(depth_image, 0, 1000)
    mask_colormap = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
    output_image = cv2.bitwise_or(depth_colormap, mask_colormap)

    # Show image
    combine_image = np.hstack((color_image, output_image))
    cv2.imshow("Stream", combine_image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

pipeline.stop()
cv2.destroyAllWindows()

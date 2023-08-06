from kfp.components import func_to_container_op


def haar_from_frames_func(
    cascade_file_path: str,
    frames_dir: str,
    output_dir: str,
):
    #######################################
    # Imports
    #######################################
    import os
    import logging
    import cv2
    import pandas as pd

    #######################################
    # Config
    #######################################
    #######################################
    # Functions
    #######################################
    # Load cascade file
    def load_cascades(cascade_file_path: str):
        haar_frames_dir = "/usr/local/share/opencv4/haarcascades/"
        cascades_df = pd.read_csv(cascade_file_path)
        cascades = []
        for index, row in cascades_df.iterrows():
            cascade = {
                "id": index,
                "name": row["name"],
                "haar": cv2.CascadeClassifier(f"{haar_frames_dir}/{row['file']}"),
            }
            cascades.append(cascade)
        print("Cascades:")
        print(cascades)
        return cascades

    # Parse frame with single haar cascade
    def haar_from_frame(frame_path, frame_number, output_dir, cascades):
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        if not os.getcwd() == output_dir:
            os.chdir(output_dir)
        try:
            # Read in the image
            img = cv2.imread(frame_path)
            # Convert the colour image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect things in the image
            for i in range(len(cascades)):
                cascade = cascades[i]
                matches = cascade["haar"].detectMultiScale(gray, 1.3, 5)
                num_found = len(matches)
                if num_found > 0:
                    print(
                        "Frame %s Cascade %s found: %s"
                        % (frame_number, cascade["name"], num_found)
                    )
                    for (x, y, w, h) in matches:
                        crop_img = img[y : (y + h), x : (x + w)]
                        # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
                        save_name = "f{0}c{1}x{2}y{3}w{4}h{5}.jpg".format(
                            frame_number, cascade["id"], x, y, w, h
                        )
                        # save_path = "{0}/".format(output_dir, )
                        cv2.imwrite(save_name, crop_img)
        except Exception as e:
            print("Uh oh error on frame {0}".format(frame_number))
            print(e)
            raise

    # Run haar_from_frame on directory of frames
    def haar_from_frames(frames_dir, output_dir, cascades):
        frames_unsorted = os.listdir(frames_dir)
        output_dir_contents = os.listdir(output_dir)
        logging.info(f"Number of files in frames_dir: {len(frames_unsorted)}")
        logging.info(f"Number of files in output_dir: {len(output_dir)}")
        if len(frames_unsorted) == len(output_dir_contents):
            logging.info(
                "Output dir already populated with correct number of files, skipping operation"
            )
        frames_order = [
            int(x.replace("f", "").replace(".jpg", "")) for x in frames_unsorted
        ]
        frame_list = [
            {"number": number, "path": "{0}/{1}".format(frames_dir, name)}
            for (number, name) in sorted(zip(frames_order, frames_unsorted))
        ]
        print("Number of frames in input_dir: {0}".format(frame_list))
        for frame in frame_list:
            haar_from_frame(
                frame_path=frame["path"],
                frame_number=frame["number"],
                output_dir=output_dir,
                cascades=cascades,
            )

    #######################################
    # Main Process
    #######################################
    cascades = load_cascades(cascade_file_path=cascade_file_path)
    haar_from_frames(frames_dir=frames_dir, output_dir=output_dir, cascades=cascades)


HaarFromFramesOp = func_to_container_op(
    haar_from_frames_func,
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/haar_from_frames",
    output_component_file="component.yaml",
)

from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/bytetrack_from_videos",
    output_component_file="component.yaml",
)
def bytetrack_from_videos(
    input_video_dir: Input[Artifact],
    input_weights: Input[Artifact],
    output_video_dir: Output[Artifact],
    output_text_file_dataset_dir: Output[Dataset],
    output_video_dir_path: str,
    output_text_file_dataset_dir_path: str,
    device: str = "gpu",  # Must be gpu or cpu
):
    """
    Run bytetrack on a directory of videos.

    Args:
        input_video_dir: Input directory of videos.
        input_weights: Input weights file.
        output_video_dir: Output directory of videos.
        output_text_file_dataset_dir: Output directory of text files.
        output_video_dir_path: Output directory of videos. Must start with /gcs.
        output_text_file_dataset_dir_path: Output directory of text files. Must start with /gcs.
        device: Device to use. Must be gpu or cpu.

    Returns:
        None
    """
    import os
    import time
    from datetime import timedelta
    import pandas as pd
    import shutil
    from loguru import logger
    from tools.demo_track import make_parser, main, get_exp

    start_time = time.time()

    ################################
    # Helper functions
    ################################

    ################################
    # Setup output paths
    ################################

    output_video_dir.path = output_video_dir_path
    output_text_file_dataset_dir.path = output_text_file_dataset_dir_path

    os.makedirs(output_video_dir.path, exist_ok=True)
    os.makedirs(output_text_file_dataset_dir.path, exist_ok=True)

    # List the videos in the input directory
    file_names = os.listdir(input_video_dir.path)
    file_paths = [
        os.path.join(input_video_dir.path, file_name) for file_name in file_names
    ]
    file_names_and_paths = list(zip(file_names, file_paths))
    file_names_and_paths.sort()
    logger.info(f"Number of files to process: {len(file_names)}")

    logger.info(
        f"output_video_dir.path: {output_video_dir.path}, output_video_dir.uri: {output_video_dir.uri}"
    )
    logger.info(
        f"output_text_file_dataset_dir.path: {output_text_file_dataset_dir.path}, output_text_file_dataset_dir.uri: {output_text_file_dataset_dir.uri}"
    )

    ################################
    # Run bytetrack
    ################################

    video_processing_times = []
    file_index = 0
    for file_name_and_path in file_names_and_paths:
        # Log start time
        start_time_this_video = time.time()
        logger.info(f"Processing {file_name_and_path[1]}")
        # Create arguments for bytetrack
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--path",
            file_name_and_path[1],
            "--fuse",
            "--save_result",
        ]
        if device == "gpu":
            arg_list += ["--fp16"]
        elif device == "cpu":
            arg_list += ["--device", "cpu"]
        # Run bytetrack
        args = make_parser().parse_args(arg_list)
        exp = get_exp(args.exp_file, args.name)
        main(exp=exp, args=args)
        # Copy outputs to GCS
        source_dir = "/ByteTrack/YOLOX_outputs/yolox_x_mix_det/track_vis"
        source_video = f"{source_dir}/output.mp4"
        source_results = f"{source_dir}/results.txt"
        output_video_path_local = os.path.join(
            output_video_dir.path, file_name_and_path[0]
        )
        logger.info(f"output_video_path_local: {output_video_path_local}")
        output_text_file_dataset_path_local = (
            os.path.join(output_text_file_dataset_dir.path, file_name_and_path[0])
            + ".csv"
        )
        logger.info(
            f"output_text_file_dataset_path_local: {output_text_file_dataset_path_local}"
        )
        shutil.copyfile(source_video, output_video_path_local)
        shutil.copyfile(source_results, output_text_file_dataset_path_local)
        # Add video number to results file
        df = pd.read_csv(output_text_file_dataset_path_local)
        df["video_number"] = file_index
        df.to_csv(output_text_file_dataset_path_local, index=None)
        # Log end time
        end_time_this_video = time.time()
        video_processing_time = timedelta(
            seconds=(end_time_this_video - start_time_this_video)
        )
        video_processing_time = video_processing_time - timedelta(
            microseconds=video_processing_time.microseconds
        )
        video_processing_times.append(str(video_processing_time))
        logger.info(f"Processing time: {str(video_processing_time)}")
        file_index += 1

    # Log all the video processing times
    logger.info(f"Video processing times: {video_processing_times}")

    # Log total time
    end_time = time.time()
    total_time = timedelta(seconds=(end_time - start_time))
    total_time = total_time - timedelta(microseconds=total_time.microseconds)
    logger.info(f"Total processing time: {str(total_time)}")

    # output_text_file_dataset_dir.path = os.path.join(
    #     output_text_file_dataset_dir.path, "data.csv"
    # )

    # # Combine all the results into a single csv file
    # file_paths = [
    #     os.path.join(output_text_file_dataset_dir.path, file_name)
    #     for file_name in os.listdir(output_text_file_dataset_dir.path)
    # ]
    # dfs = [pd.read_csv(file_path, header=None) for file_path in file_paths]
    # df_shapes = [df.shape for df in dfs]
    # logger.info(f"df_shapes: {df_shapes}")
    # df = pd.concat(dfs)
    # df.to_csv(output_text_file_dataset.path, index=False)

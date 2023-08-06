#!/usr/bin/env python
import json
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from textwrap import dedent

from Hive.utils.log_utils import (
    get_logger,
    add_verbosity_options_to_argparser,
    log_lvl_from_verbosity_args,
)

DESC = dedent(
    """
    Run nnUNet command to run inference and save the predictions for a set of volumes.
    """  # noqa: E501
)
EPILOG = dedent(
    """
    Example call:
    ::
        {filename} -i /INPUT_FOLDER -o /OUTPUT_FOLDER --config-file ../LungLobeSeg_3d_fullres_100_LungLobeSeg_3D_Single_Modality.json
        {filename} -i /INPUT_FOLDER -o /OUTPUT_FOLDER --config-file ../LungLobeSeg_3d_fullres_100_LungLobeSeg_3D_Single_Modality.json --save_npz
    """.format(  # noqa: E501
        filename=Path(__file__).name
    )
)


def get_arg_parser():
    pars = ArgumentParser(description=DESC, epilog=EPILOG, formatter_class=RawTextHelpFormatter)

    pars.add_argument(
        "-i",
        "--input-folder",
        type=str,
        required=True,
        help="Folder path containing the volumes to be predicted",
    )

    pars.add_argument(
        "-o",
        "--output-folder",
        type=str,
        required=True,
        help="Folder path where to save the predictions",
    )

    pars.add_argument(
        "--config-file",
        type=str,
        required=True,
        help="File path for the configuration dictionary, used to retrieve experiments variables (Task_ID)",
    )

    add_verbosity_options_to_argparser(pars)

    return pars


def main():
    parser = get_arg_parser()
    arguments, unknown_arguments = parser.parse_known_args()
    args = vars(arguments)

    logger = get_logger(  # NOQA: F841
        name=Path(__file__).name,
        level=log_lvl_from_verbosity_args(args),
    )

    config_file = args["config_file"]

    with open(config_file) as json_file:
        data = json.load(json_file)



        os.environ["nnUNet_raw_data_base"] = data["base_folder"]
        if data["base_folder"][0] != "/":
            os.environ["nnUNet_raw_data_base"] = str(Path(data["root_results_folder"]).joinpath(data["base_folder"]))
        os.environ["nnUNet_preprocessed"] = data["preprocessing_folder"]
        if data["preprocessing_folder"][0] != "/":
            os.environ["nnUNet_preprocessed"] = str(Path(data["root_results_folder"]).joinpath(data["preprocessing_folder"]))
        os.environ["RESULTS_FOLDER"] = data["results_folder"]
        if data["results_folder"][0] != "/":
            os.environ["RESULTS_FOLDER"] = str(
                Path(data["root_results_folder"]).joinpath(data["results_folder"]))
        if data["predictions_path"][0] != "/":
            data["predictions_path"] = str(
                Path(data["root_results_folder"]).joinpath(data["predictions_path"]))
        os.environ["nnUNet_def_n_proc"] = os.environ["N_THREADS"]
        os.environ["MKL_THREADING_LAYER"] = "GNU"
        os.environ["nnunet_use_progress_bar"] = "1"
        Path(args["output_folder"]).mkdir(parents=True, exist_ok=True)
        arguments_list = [
            "-i",
            args["input_folder"],
            "-o",
            args["output_folder"],
            "--model_folder",
            data["predictions_path"],
            "-t",
            "Task" + data["Task_ID"] + "_" + data["Task_Name"],
            "-tr",
            data["TRAINER_CLASS_NAME"],
        ]

        arguments_list.extend(["-m", data["TRAINING_CONFIGURATION"]])

        arguments_list.extend(unknown_arguments)
        os.system("nnUNet_predict " + " ".join(arguments_list))


if __name__ == "__main__":
    main()

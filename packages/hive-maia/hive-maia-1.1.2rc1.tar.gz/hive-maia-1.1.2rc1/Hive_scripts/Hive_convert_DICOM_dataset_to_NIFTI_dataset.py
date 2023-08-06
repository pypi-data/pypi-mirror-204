#!/usr/bin/env python

import datetime
import json
#import simple_orthanc
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from multiprocessing import Pool
from pathlib import Path
from textwrap import dedent

from tqdm import tqdm

from Hive.utils.file_utils import subfolders
from Hive.utils.log_utils import add_verbosity_options_to_argparser, get_logger, log_lvl_from_verbosity_args
from Hive.utils.volume_utils import convert_DICOM_folder_to_NIFTI_image, convert_DICOM_server_folder_to_NIFTI_image, resample_image

TIMESTAMP = "{:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

DESC = dedent(
    """
    Script to convert a ``DICOM`` dataset (structured as Patient-Study-Series) into a NIFTI format (with the `Patient ID` as the folder name).
    When multiple studies for the same patient are found, different **DICOM studies** are saved in different folders, appending the study index to the patient name.
    *DICOM series* for the same study are saved in the same patient folder.
    """  # noqa: E501
)
EPILOG = dedent(
    """
    Example call:
    ::
        {filename}  --data-folder /PATH/TO/DICOM_DATA --output-folder /PATH/TO/NIFTI_DATASET
    """.format(  # noqa: E501
        filename=Path(__file__).stem
    )
)

if "N_THREADS" not in os.environ:
    os.environ["N_THREADS"] = "1"


def get_arg_parser():
    pars = ArgumentParser(description=DESC, epilog=EPILOG, formatter_class=RawTextHelpFormatter)

    pars.add_argument(
        "--data-folder",
        type=str,
        required=True,
        help="DICOM Dataset folder.",
    )

    pars.add_argument(
        "--output-folder",
        type=str,
        required=True,
        help="Output folder where to save the converted NIFTI dataset.",
    )

    pars.add_argument(
        "--n-workers",
        type=int,
        required=False,
        default=os.environ["N_THREADS"],
        help="Number of worker threads to use. (Default: {})".format(os.environ["N_THREADS"]),
    )

    add_verbosity_options_to_argparser(pars)

    return pars


def main():
    parser = get_arg_parser()
    arguments = vars(parser.parse_args())

    logger = get_logger(  # NOQA: F841
        name=Path(__file__).name,
        level=log_lvl_from_verbosity_args(arguments),
    )
    subjects = subfolders(arguments["data_folder"], join=False)

    #orthanc = simple_orthanc.Orthanc(host='orthanc.lymph-detection.k8s-maia.com',
    #                                port=80,
    #                                username='simben',
    #                                 password='MarLU2318')

    selected_subjects = [
        'Breast_MRI_464',
        'Breast_MRI_370',
        'Breast_MRI_148',
        'Breast_MRI_329',
        'Breast_MRI_805',
        'Breast_MRI_334',
        'Breast_MRI_819',
        'Breast_MRI_726',
        'Breast_MRI_773',
        'Breast_MRI_246',
        'Breast_MRI_363',
        'Breast_MRI_338',
        'Breast_MRI_686',
        'Breast_MRI_762',
        'Breast_MRI_636',
        'Breast_MRI_781',
        'Breast_MRI_705',
        'Breast_MRI_229',
        'Breast_MRI_141',
        'Breast_MRI_802',
        'Breast_MRI_440',
        'Breast_MRI_832',
        'Breast_MRI_143',
        'Breast_MRI_354',
        'Breast_MRI_018',
        'Breast_MRI_238',
        'Breast_MRI_616',
        'Breast_MRI_528',
        'Breast_MRI_392',
        'Breast_MRI_562',
        'Breast_MRI_166',
        'Breast_MRI_575',
        'Breast_MRI_204',
        'Breast_MRI_230',
        'Breast_MRI_031',
        'Breast_MRI_876',
        'Breast_MRI_902',
        'Breast_MRI_530',
        'Breast_MRI_041',
        'Breast_MRI_279',
        'Breast_MRI_112',
        'Breast_MRI_489',
        'Breast_MRI_741',
        'Breast_MRI_002',
        'Breast_MRI_302',
        'Breast_MRI_561',
        'Breast_MRI_272',
        'Breast_MRI_339',
        'Breast_MRI_888',
        'Breast_MRI_054',
        'Breast_MRI_495',
        'Breast_MRI_383',
        'Breast_MRI_688',
        'Breast_MRI_286',
        'Breast_MRI_466',
        'Breast_MRI_618',
        'Breast_MRI_287',
        'Breast_MRI_529',
        'Breast_MRI_503',
        'Breast_MRI_827',
        'Breast_MRI_320',
        'Breast_MRI_640',
        'Breast_MRI_359',
        'Breast_MRI_492',
        'Breast_MRI_797',
        'Breast_MRI_087',
        'Breast_MRI_089',
        'Breast_MRI_025',
        'Breast_MRI_572',
        'Breast_MRI_435',
        'Breast_MRI_023',
        'Breast_MRI_497',
        'Breast_MRI_501',
        'Breast_MRI_076',
        'Breast_MRI_080',
        'Breast_MRI_723',
        'Breast_MRI_426',
        'Breast_MRI_587',
        'Breast_MRI_170',
        'Breast_MRI_369',
        'Breast_MRI_788',
        'Breast_MRI_693',
        'Breast_MRI_727',
        'Breast_MRI_602',
        'Breast_MRI_525',
        'Breast_MRI_681',
        'Breast_MRI_694',
        'Breast_MRI_670',
        'Breast_MRI_186',
        'Breast_MRI_652',
        'Breast_MRI_612',
        'Breast_MRI_124',
        'Breast_MRI_290',
        'Breast_MRI_006',
        'Breast_MRI_595',
        'Breast_MRI_105',
        'Breast_MRI_553',
        'Breast_MRI_280',
        'Breast_MRI_337',
        'Breast_MRI_021'
    ]
    #subjects = orthanc.PatientName

    pool = Pool(int(arguments["n_workers"]))
    Path(arguments["output_folder"]).mkdir(parents=True, exist_ok=True)
    DICOM_to_NIFTI_conversions = []
    for subject in subjects:

        if subject in selected_subjects:
        #subject_nifti_filename = arguments["output_folder"]
        #DICOM_to_NIFTI_conversions.append(
        #pool.starmap_async(
        #    convert_DICOM_server_folder_to_NIFTI_image,
        #    ((subject, subject_nifti_filename, orthanc),),
        #)
        #)
            subject_dicom_folder = str(Path(arguments["data_folder"]).joinpath(subject))
            subject_nifti_filename = arguments["output_folder"]
            DICOM_to_NIFTI_conversions.append(
                pool.starmap_async(
        #        resample_image,
        #        ((
        #            str(Path(subject_nifti_filename).joinpath(subject,subject+"_CT.nii.gz")),
        #            str(Path(subject_nifti_filename).joinpath(subject, subject + "_PET.nii.gz")),
        #             str(Path(subject_nifti_filename).joinpath(subject, subject + "_downsampled_CT.nii.gz"))
        #         ),),
                    convert_DICOM_folder_to_NIFTI_image,
                    ((subject_dicom_folder, subject_nifti_filename),),
                )
            )

    patients_map = {}
    for i in tqdm(DICOM_to_NIFTI_conversions):
        patient_study_map = i.get()
        patients_map[list(patient_study_map[0].keys())[0]] = patient_study_map[0][list(patient_study_map[0].keys())[0]]

    with open(Path(arguments["output_folder"]).parent.joinpath(Path(arguments["output_folder"]).name + ".json"),
              "w") as file:
        json.dump(patients_map, file)


if __name__ == "__main__":
    main()

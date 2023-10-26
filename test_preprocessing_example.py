# TODO move this to tutorial
import datetime
from tqdm import tqdm
from auxiliary.turbopath import turbopath

from auxiliary.normalization.percentile_normalizer import PercentileNormalizer


from brainles_preprocessing.core import (
    preprocess_modality_centric_to_atlas_space,
    Modality,
)

# from brainles_preprocessing.brats import preprocess_brats_style_t1_centric


def preprocess(inputDir):
    inputDir = turbopath(inputDir)
    try:
        print("*** start ***")

        # where are the raw mr files?
        btk_raw_dir = turbopath(inputDir)

        # is the exam already processed?
        brainles_dir = turbopath(inputDir) + "/" + inputDir.name + "_brainles"
        prep_dir = brainles_dir + "/preprocessed"

        # if not os.path.exists(prep_dir):
        # if os.path.exists(prep_dir):
        t1_file = btk_raw_dir.files("*t1.nii.gz")
        t1c_file = btk_raw_dir.files("*t1c.nii.gz")
        t2_file = btk_raw_dir.files("*t2.nii.gz")
        flair_file = btk_raw_dir.files("*fla.nii.gz")

        if len(t1_file) == len(t1c_file) == len(t2_file) == len(flair_file) == 1:
            print(t1_file)
            print(t1c_file)
            print(t2_file)
            print(flair_file)

            t1File = t1_file[0]
            t1cFile = t1c_file[0]
            t2File = t2_file[0]
            flaFile = flair_file[0]

            # normalizer
            percentile_normalizer = PercentileNormalizer(
                lower_percentile=0.5,
                upper_percentile=99.5,
                lower_limit=0,
                upper_limit=1,
            )

            # define modalities
            center = Modality(
                modality_name="t1c",
                input_path=t1cFile,
                output_path=prep_dir + "/" + inputDir.name + "_t1c.nii.gz",
                bet=False,
                normalizer=percentile_normalizer,
            )

            moving_modalities = [
                Modality(
                    modality_name="t1",
                    input_path=t1File,
                    output_path=prep_dir + "/" + inputDir.name + "_t1.nii.gz",
                    bet=False,
                    normalizer=percentile_normalizer,
                ),
                Modality(
                    modality_name="t2",
                    input_path=t2File,
                    output_path=prep_dir + "/" + inputDir.name + "_t2.nii.gz",
                    bet=False,
                    normalizer=percentile_normalizer,
                ),
                Modality(
                    modality_name="fla",
                    input_path=flaFile,
                    output_path=prep_dir + "/" + inputDir.name + "_fla.nii.gz",
                    bet=True,
                    normalizer=percentile_normalizer,
                ),
            ]
            # execute it
            preprocess_modality_centric_to_atlas_space(
                center_modality=center,
                moving_modalities=moving_modalities,
                bet_mode=None,
                temporary_directory="tempo/" + inputDir.name,
            )

    except Exception as e:
        print("error: " + str(e))
        print("conversion error for:", inputDir)

        time = str(datetime.datetime.now().time())

        print("** finished:", inputDir.name, "at:", time)


### *** GOGOGO *** ###
if __name__ == "__main__":
    EXAMPLE_DATA_DIR = turbopath("example_data")

    exams = EXAMPLE_DATA_DIR.dirs()

    for exam in tqdm(exams):
        print(exam)
        preprocess(exam)
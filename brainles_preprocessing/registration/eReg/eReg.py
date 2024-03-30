# TODO add typing and docs
from ereg.registration import RegistrationClass

from brainles_preprocessing.registration.registrator import Registrator


class eRegRegistrator(Registrator):
    def __init__(
        self,
        # TODO define default
        configuration_file: str | None = None,
    ):
        """
        # TODO
        """
        self.configuration_file = configuration_file

    def register(
        self,
        fixed_image_path: str,
        moving_image_path: str,
        transformed_image_path: str,
        matrix_path: str,
        log_file_path: str = None,
    ) -> None:
        """
        Register images using NiftyReg.

        Args:
            fixed_image_path (str): Path to the fixed image.
            moving_image_path (str): Path to the moving image.
            transformed_image_path (str): Path to the transformed image (output).
            matrix_path (str): Path to the transformation matrix (output).
            log_file_path (str): Path to the log file.
        """
        # TODO do we need to handle kwargs?
        registrator = RegistrationClass(
            configuration_file=self.configuration_file,
        )

        registrator.register(
            target_image=fixed_image_path,
            moving_image=moving_image_path,
            output_image=transformed_image_path,
            transform_file=matrix_path,
            log_file=log_file_path,
        )

    def transform(
        self,
        fixed_image_path: str,
        moving_image_path: str,
        transformed_image_path: str,
        matrix_path: str,
        log_file_path: str = None,
    ) -> None:
        """
        Apply a transformation using NiftyReg.

        Args:
            fixed_image_path (str): Path to the fixed image.
            moving_image_path (str): Path to the moving image.
            transformed_image_path (str): Path to the transformed image (output).
            matrix_path (str): Path to the transformation matrix.
            log_file_path (str): Path to the log file.
        """
        # TODO do we need to handle kwargs?
        registrator = RegistrationClass(
            configuration_file=self.configuration_file,
        )

        registrator.resample_image(
            target_image=fixed_image_path,
            moving_image=moving_image_path,
            output_image=transformed_image_path,
            transform_file=matrix_path,
            log_file=log_file_path,
        )

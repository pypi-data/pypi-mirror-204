"""
Fake science task
"""
import numpy as np
from astropy.io import fits
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_test.models.parameters import TestParameters


class GenerateCalibratedData(WorkflowTaskBase, FitsDataMixin, InputDatasetMixin):

    record_provenance = True

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = TestParameters(self.input_dataset_parameters)

    def run(self):
        rng = np.random.default_rng()
        count = 1  # keep a running count to increment the dsps repeat number
        with self.apm_task_step("Looping over inputs"):
            for path, hdu in self.fits_data_read_hdu(tags=Tag.input()):
                header = hdu.header
                with self.apm_processing_step("Doing some calculations"):
                    header["DSPSNUM"] = count
                    data = hdu.data

                    # Just do some weird crap. We don't use the loaded random array directly so that we
                    # don't have to care that the shapes are the same as the "real" data.
                    random_signal = rng.normal(*self.parameters.randomness, size=data.shape)
                    data = (
                        data + random_signal
                    )  # Needs to be like this because data will start as int-type
                    data += self.parameters.constant
                    output_hdu = fits.PrimaryHDU(data=data, header=header)

                with self.apm_writing_step("Writing data"):
                    output_hdul = fits.HDUList([output_hdu])
                    self.fits_data_write(
                        hdu_list=output_hdul,
                        tags=[
                            Tag.calibrated(),
                            Tag.frame(),
                            Tag.stokes("I"),
                            Tag.dsps_repeat(count),
                        ],
                    )
                count += 1

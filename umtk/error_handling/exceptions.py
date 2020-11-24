from .base_error_code import BaseErrorCode


# ===================================================================
# Dicom Reading Related Exceptions
# ===================================================================
class BaseError(Exception):
    def __init__(self, error_msg):
        super().__init__(self)
        self.error_msg = error_msg


class ReadDicomHeaderError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.READ_DICOM_HEADER_ERROR


class ReadDicomDataError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.READ_DICOM_DATA_ERROR


class MissingImagePositionTagError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.MISSING_IMAGE_POSITION_TAG_ERROR


class MissingPixelSpacingTagError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.MISSING_PIXEL_SPACING_TAG_ERROR


class MissingSeriesUidTagError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.MISSING_SERIES_UID_TAG_ERROR


class MissingInstanceNumberTagError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.MISSING_INSTANCE_NUMBER_TAG_ERROR


class MultipleInputSeriesError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.MULTIPLE_INPUT_SERIES_ERROR


class NotEnoughSlicesError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.NOT_ENOUGH_SLICES_ERROR


class InconsistentInstanceNumberError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.INCONSISTENT_INSTANCE_NUMBER_ERROR


class InconsistentZPixelSpacingError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.INCONSISTENT_ZPIXEL_SPACING_ERROR


class IncorrectZPixelSpacingError(BaseError):
    def __init__(self, error_msg):
        super().__init__(error_msg)
        self.error_code = BaseErrorCode.INCORRECT_ZPIXEL_SPACING_ERROR

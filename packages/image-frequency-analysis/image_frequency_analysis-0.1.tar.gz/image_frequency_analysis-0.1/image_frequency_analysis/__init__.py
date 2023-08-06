from .frequency_analysis import FrequencyAnalysis


def image_frequency_analysis(
    image_path, filter_radius=80, high_pass_filter=False, low_pass_filter=False
):

    """
    This definition invokes the Frequency Analysis class
    to apply the Transformation on the image based on the
    attributes passed to the class

    Attributes:

    image_path - This is the file path for the image on which the transformation needs to be applied

    filter_radius - This property defines to what extent the low or high frequency value needs to be allowed to
                    pass through in the filtering process. Defaul value = 80

    high_pass_filter - This is a boolean value which indicates to use the default high pass filter mask on the image.
                    Default value = False

    low_pass_filter - This is a boolean value which indicates to use the default low pass filter mask on the image.
                    Default value = False

    When both the high_pass_filter and low_pass_filter is False, by default high pass filter mask is applied on the image.

    Throws value error when both high_pass_filter and low_pass_filter value are set to be True.

    """
    if high_pass_filter == True and low_pass_filter == True:
        raise ValueError(
            "Both high_pass_filter and low_pass_filter flag cannot be True. Please choose only one type of filter"
        )

    output = FrequencyAnalysis(
        image_path=image_path,
        filter_radius=filter_radius,
        high_pass_filter=high_pass_filter,
        low_pass_filter=low_pass_filter,
    )

    return output

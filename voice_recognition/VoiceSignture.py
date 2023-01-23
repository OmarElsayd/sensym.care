def gender_detection(first_name, last_name):
    """
    This method will detect gender
    :param first_name:
    :param last_name:
    :return:
    """
    mysp=__import__("my-voice-analysis")

    p = f"{first_name}_{last_name}.wav"  # Audio File title
    c = r"."  # Path to the Audio_File directory (Python 3.7)
    mysp.myspgend(p, c)
    mysp.mysptotal(p,c)
    mysp.mysppron(p,c)
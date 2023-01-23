import os


def check_client_dir(first_name : str, last_name : str) -> bool:
    """
    This method will check if the user directory exists
    :param last_name:
    :param first_name:
    :return:  boolean
    """
    if os.path.isdir(f"{first_name}_{last_name}".lower()):
        return True
    else:
        return False


def create_client_dir(first_name : str, last_name : str) -> None:
    """
    This method will create the user directory
    :param last_name:
    :param first_name:
    :return:
    """
    cur_worrking_dir = os.getcwd()
    print(cur_worrking_dir)
    folder_name_formate = f"{first_name}_{last_name}".lower()
    os.mkdir(folder_name_formate)
    print("The user directory has been created")
    os.chdir(cur_worrking_dir)


def create_session_dir() -> None:
    """
    This method will create the session directory
    :return:
    """
    current_working_dir = os.getcwd()
    print(current_working_dir)
    session_number = len(os.listdir()) + 1
    session_folder = f"session{session_number}"
    os.mkdir(session_folder)
    os.chdir(session_folder)
    create_static_folder()
    os.chdir(current_working_dir)


def create_static_folder() -> None:
    """
    This method will create the static folder
    :return:    None
    """
    os.mkdir("static")


def get_session_name(last_name : str) -> str:
    """
    This method will get the session name
    :param last_name:
    :return:
    """
    current_working_dir = os.getcwd()
    if current_working_dir.endswith(last_name.lower()):
        session_name = f"session{len(os.listdir())}"
        print(session_name)
        os.chdir(current_working_dir)
        return session_name


def cd_client_dir(first_name : str, last_name : str) -> None:
    """
    This method will change the directory to the user directory
    :param last_name:
    :param first_name:
    :return:
    """
    folder_name_formate = f"{first_name}_{last_name}".lower()
    os.chdir(folder_name_formate)


def cd_session_dir(first_name,last_name):
    """
    This method will change the directory to the session directory
    :param first_name: first name of the user
    :param last_name:  last name of the user
    :return:        None
    """
    print(os.getcwd())
    session_number = len(os.listdir())
    session_folder = f"session{session_number}"
    os.chdir(session_folder)
    print(os.getcwd())

def cd_static_dir():
    """
    This method will change the directory to the static directory
    :return:        None
    """
    os.chdir("static")
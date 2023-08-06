# Simple use Date and text parsing from pdf rtf and images (with use of call back function)

This is a simple package provided by Marvsai healthcare LTD.

def find_dates(file_contents: str):
    """
      Find any dates in a large python string usually taken from a file or pdf

      Args:
          file_contents (str): The string in which to find any format of dates


      Returns:
          List[datetime.datetime]: A list of datetime objects the latest can be found using max()


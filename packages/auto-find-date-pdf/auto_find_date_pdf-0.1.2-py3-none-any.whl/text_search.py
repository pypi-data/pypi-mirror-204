import logging as log
import re
from datetime import datetime, timedelta
from re import Pattern
from pypdf import PdfReader
from typing import Callable


def supported_images(imgname:str)->bool:
    strings = ["JPEG", "JPG", "PNG","PNG8", "PNG24", "GIF", "GIF", "BMP", "WEBP",
               "TIFF"]

    endI = imgname.rfind('.')
    if endI<0:
        return False
    if imgname[endI+1:].upper() in strings:
        return True
    return False


def extract_rtf_pdf(name: str, get_ai_text:Callable=None)->str:
    text = ''
    if name[-3:].find('rt')>-1:
        from striprtf.striprtf import rtf_to_text
        with open(name, 'r') as doc:
            rtf_data = doc.read()
            text = rtf_to_text(rtf_data, errors='ignore')
    elif name[-3:].lower().find('pdf')>-1:
        log.info('This is an image')
        if get_ai_text:
            text = get_ai_text(name)
        if len(text) == 0:
            with open(name, 'rb') as f:

                # Create a PDF reader object
                pdf_reader = PdfReader(f)
                # Get the number of pages in the PDF document
                num_pages = pdf_reader.pages
                # Loop over each page in the PDF document
                for page_num in num_pages:
                    # Extract the text from the page
                    text += page_num.extract_text()
        elif supported_images(name):
            if get_ai_text:
                text = get_ai_text(name)

    return text


date_dash_pattern = re.compile(r'\d{1,2}-\w{3}-\d{4}')
date_pattern_gen = re.compile(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}')


def find_dates_alt(file_contents: str, dates: list = []):
    # Define a regular expression pattern to match dates

    # Find all matches of the pattern in the file contents
    matches = date_pattern_gen.findall(file_contents)

    # Convert the matches to datetime objects
    for match in matches:
        try:
            date = datetime.strptime(match, '%m/%d/%y')
        except ValueError:
            try:
                date = datetime.strptime(match, '%m/%d/%Y')
            except ValueError:
                try:
                    date = datetime.strptime(match, '%d/%m/%Y')
                except ValueError:
                    try:
                        date = datetime.strptime(match, '%m-%d-%Y')
                    except ValueError:
                        try:
                            date = datetime.strptime(match, '%d-%m-%Y')
                        except ValueError:
                            date = None
        if date is not None:
            dates.append(date)


def find_dates(file_contents: str):
    # Open the file asynchronously and read the contents
    # async with aiofiles.open(file_path, 'r') as file:
    #     file_contents = await file.read()

    # Define a regular expression pattern to match dates

    # Find all matches of the pattern in the file contents
    matches = date_dash_pattern.findall(file_contents)
    # Convert the matches to datetime objects
    dates = []
    if matches:
        try:
            for match in matches:
                date = datetime.strptime(match, '%d-%b-%Y')
                dates.append(date)
        except Exception as e:
            log.info('Count not convert date:')
    else:
        matches = find_dates_alt(file_contents, dates)

    if not dates:
        dates = [datetime.utcnow() - timedelta(days=1)]
    return dates

pattern = ''

def init_replace(replacements:dict):
    # Create a regular expression pattern that matches any of the keys in the replacements dictionary
    global pattern
    pattern = re.compile('|'.join(replacements.keys()))
    return pattern

def _replace_multiple_strings(input_string:str, pattern:Pattern, replacements_dict:dict )->str:
    """
    Replace multiple strings in the input string using a dictionary of replacement pairs and related precompiled
    Pattern

    Args:
        input_string (str): The string in which to replace the substrings.
        pattern (Pattern): Should normally be equal to re.compile('|'.join(replacements_dict.keys()))
        replacements_dict (dict): A dictionary of replacement pairs, where the keys are the
            substrings to be replaced and the values are the replacement strings.

    Returns:
        str: The input string with all instances of the substrings replaced with their
            corresponding replacement strings.
    """
    # Use re.sub() to replace the words
    output_string = pattern.sub(lambda x: replacements_dict[x.group(0)], input_string)
    return output_string

def cached_replace_multiple_strings(input_string:str, replacements_dict:dict )->str:
    """
    Replace multiple strings in the input string using a dictionary of replacement pairs.
    Before this is called init_replace should be called to prevent compilation of Pattern every time

    Args:
        input_string (str): The string in which to replace the substrings.
        replacements_dict (dict): A dictionary of replacement pairs, where the keys are the
            substrings to be replaced and the values are the replacement strings.

    Returns:
        str: The input string with all instances of the substrings replaced with their
            corresponding replacement strings.
    """
    global pattern
    if not pattern:
        pattern = re.compile('|'.join(replacements_dict.keys()))

    return _replace_multiple_strings(input_string, pattern, replacements_dict)

def replace_multiple_strings(input_string:str, replacements_dict:dict )->str:
    """
    Replace multiple strings in the input string using a dictionary of replacement pairs.

    Args:
        input_string (str): The string in which to replace the substrings.
        replacements_dict (dict): A dictionary of replacement pairs, where the keys are the
            substrings to be replaced and the values are the replacement strings.

    Returns:
        str: The input string with all instances of the substrings replaced with their
            corresponding replacement strings.
    """
    if not replacements_dict:
        return input_string
    pattern = re.compile('|'.join(replacements_dict.keys()))

    return _replace_multiple_strings(input_string, pattern, replacements_dict)
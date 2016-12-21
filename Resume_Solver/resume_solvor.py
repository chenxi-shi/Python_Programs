import re
import PyPDF2
import os
import csv
from collections import namedtuple
from functools import reduce
import warnings
import docx2txt

# TODO: solve doc


# print(app_name_set)

def page_to_str(*args):
    page = ""
    for i in args:
        if isinstance(i, str):
            page = "{} {}".format(page, i)
        elif isinstance(i, PyPDF2.pdf.PageObject):
            page = "{} {}".format(page, i.extractText())
        else:
            raise ValueError
    return " ".join(page.lower().split())


def pdf_to_str(_filename):

    with open(_filename, "rb") as f:
        pdfReader = PyPDF2.PdfFileReader(f)
        # print(type(pdfReader.getPage(0)))
        all_page_map = map(pdfReader.getPage, range(pdfReader.getNumPages()))
        all_str = reduce(page_to_str, all_page_map, "") # initial value "", in case iter length=0

    return all_str


abilities = namedtuple("abilities", ["bash", "python", "hadoop", "reduce",
                                     "matlab", "fortran", "java", "perl", "linux",
                                     "sql", "openstack", "putty", "computer", "science"])


def get_ability_info(_str):
    ability_sheet = []
    for _ability in abilities._fields:
        if _ability in _str:
            ability_sheet.append(1)
        else:
            ability_sheet.append(0)
    return abilities._make(ability_sheet)

def get_owner(app_lst, all_page_str, file_type, _filename):
    # get the owner of the CV
    for app_name in app_lst:
        if len(app_name) > 1:
            if app_name[0] in all_page_str and app_name[-1] in all_page_str:
                app_dict[app_name] = ability
                return os.path.join(directory, "-".join(app_name)) + "." + file_type
    return _filename


if __name__ == "__main__":
    # Warning was raised as an exception
    warnings.filterwarnings("error")

    mistake_files = set()
    file_person_pair = set()
    # get all applications" name
    app_dict = {}
    with open("application_names.csv", "r") as an:
        an_csv = csv.reader(an)
        headers = next(an_csv)
        for row in an_csv:
            app_dict[tuple(map(lambda s: s.lower(), row))] = None

    dir = os.path.dirname(__file__)
    directory = os.path.join(dir, "all_applications")
    print(directory)
    filenames_tuple = tuple(os.listdir(directory))
    for filename in filenames_tuple:
        filename = os.path.join(directory, filename)
        print(filename)
        if re.match(r".*\.[pP][dD][fF]", filename):

            # solve pdf to string
            try:
                all_page_str = pdf_to_str(filename)
            except:
                mistake_files.add(filename)
                ability = None
            else:
                # extract ability info from CV
                ability = get_ability_info(all_page_str)
                file_person_pair.add((get_owner(app_dict.keys(), all_page_str, "pdf", filename), filename))

        elif re.match(r".*\.[dD][oO][cC][xX]?", filename):
            all_page_str = docx2txt.process(filename)
            # extract ability info from CV
            ability = get_ability_info(all_page_str)
            file_person_pair.add((get_owner(app_dict.keys(), all_page_str, "docx",filename), filename))

        else:
            mistake_files.add(filename)
            ability = None





    # output result
    # On Windows, always open your files in binary mode ("rb" or "wb") before passing them to csv.reader or csv.writer.
    with open("output.csv", "w") as f:
        w = csv.writer(f)

        w.writerow(["name"] + list(abilities._fields))
        out = []
        for application, r in app_dict.items():
            person_info = [" ".join(application)]
            if r is None:
                out.append(tuple(person_info))
            else:
                print(person_info + list(r))
                out.append(tuple(person_info + list(r)))


        # out = [([" ".join(application)] + [None] if r is None else list(r)) for application, r in app_dict.items()]
        w.writerows(out)

    # rename file
    for tname, sname in file_person_pair:
        try:
            os.rename(sname, tname)
        except:
            mistake_files.add(sname)


    # output mistake_files
    with open("mistake_files.txt", "w") as f:
        for a in mistake_files:
            f.write("{}\n".format(a))
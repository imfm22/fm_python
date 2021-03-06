import sys
import os

from pdfrw import PdfReader, PdfWriter, IndirectPdfDict


def cat_pdf(dir_path, pdf_dict):
    pdf_names = os.listdir(dir_path)
    if not len(pdf_names):
        print("There is no file in dir: {}".format(dir_path))
        return

    out_name = "cat_" + pdf_names[0]
    writer = PdfWriter()

    for pdf_name in pdf_names:
        if not pdf_name.endswith(".pdf"):
            continue

        pdf_path = os.path.join(dir_path, pdf_name)
        writer.addpages(PdfReader(pdf_path).pages)

    writer.trailer.Info = pdf_dict
    writer.write(out_name)


if __name__ == '__main__':
    # Example
    dir_path = '/home/fm22/Documents/图书馆/Cheet-Sheet/dataquest'
    pdf_dict = IndirectPdfDict(
        Title='cheet sheet',
        Author='fm22',
        Subject='None',
        Creator='None',
    )
    cat_pdf(dir_path, pdf_dict)

# this py file will contain the file names of all pdf to be analyzed
# as well as the location in everywhere inside the PC
# best things is, it do all the messy pointing job and leave the main
# py file neat. It is encouraged to use this to access pdf-s at diff location
# without having to group all of them into same folder. When we wan to track back
# to the pdf file, we will just have to go from here

from pathlib import Path


def pdf_bank():
    # dir of the all pdf
    directory = 'C://Users//YH//Desktop//Master//Papers//Useful//ScDirect_Jan//'
    # ----------[filename of all pdf without .pdf]----------
    # 1-5
    pdf = ['A pressure-based method for monitoring leaks in a pipe distribution system Review']
    pdf += ['A-Graph-based-Analysis-of-Leak-Localization-in-Urban-W_2014_Procedia-Enginee']
    pdf += ['An efficient VRF system fault diagnosis strategy for refrigerant charge amount based on '
            'PCA and dual neural network model']
    pdf += ['A-New-Indicator-for-Real-time-Leak-Detection-in-Water-Distri_2014_Procedia-E']
    pdf += ['Burst detection in district metering areas using a data driven clustering algorithm']
    # 6-10
    pdf += ['Cloud based machine learning approaches for leakage assessment']
    pdf += ['Cloud-based-Event-Detection-Platform-for-Water-Distribution_2015_Procedia-En']
    pdf += ['Detection of gas leakage sound using modular']
    pdf += ['Fully automatic AI-based leak detection system']
    pdf += ['Integration of modern remote sensing technologies for faster utility']
    # 11- 15
    pdf += ['Leak-Localization-in-Water-Distribution-Networks-using-Pres_2015_IFAC-Papers']
    pdf += ['Methodology for leakage isolation using pressure sensitivity analysis']
    pdf += ['Real-time-Burst-Detection-in-Water-Distribution-Systems-Usi_2015_Procedia-En']
    pdf += ['Sampling Design for Leak Detection in Water Distribution Networks']
    pdf += ['WML--Wireless-Sensor-Network-based-Machine-Learning-for-_2015_Procedia-Compu']
    # concatenate the filename with the directory
    pdf_full_addr = [(directory + filename + '.pdf') for filename in pdf]

    # inspection of file existence before passing out the full address
    missing_logger = []
    for addr in pdf_full_addr:
        my_file = Path(addr)
        if not my_file.is_file():
            missing_logger.append(addr)
    # if list is empty, it will return False, will not raise error
    if missing_logger:
        print('MISSING FILE:')
        for addr in missing_logger:
            print(addr)
        raise FileNotFoundError('[YH] FILES ABOVE ARE MISSING')
    else:
        # return the full addr only if all files are valid one
        return pdf_full_addr



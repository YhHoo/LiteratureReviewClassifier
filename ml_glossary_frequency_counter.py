pdf = 'Today Jackson is attending the meeting at Traders hotel'

wanted = 'traders hotel'

if wanted in pdf.lower():
    print('FOUND !')
else:
    print('NOT FOUND =(')
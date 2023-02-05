import csv
states = {'AL': 0, 'AK': 0, 'AZ': 0, 'AR': 0, 'CA': 0, 'CO': 0, 'CT': 0, 'DE': 0, 'FL': 0, 'GA': 0, 'HI': 0, 'ID': 0, 'IL': 0, 'IN': 0, 'IA': 0, 'KS': 0, 'KY': 0, 'LA': 0, 'ME': 0, 'MD': 0, 'MA': 0, 'MI': 0, 'MN': 0, 'MS': 0, 'MO': 0, 'MT': 0, 'NE': 0, 'NV': 0, 'NH': 0, 'NJ': 0, 'NM': 0, 'NY': 0, 'NC': 0, 'ND': 0, 'OH': 0, 'OK': 0, 'OR': 0, 'PA': 0, 'RI': 0, 'SC': 0, 'SD': 0, 'TN': 0, 'TX': 0, 'UT': 0, 'VT': 0, 'VA': 0, 'WA': 0, 'WV': 0, 'WI': 0, 'WY': 0}

def parseCSV(file, addsub, weight):
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        linecount = 0
        for row in csv_reader:
            if linecount == 1:
                print(row)
                max = float(row[0])
            if linecount == 50:
                min = float(row[0])
            linecount+=1
        linecount = 0
        csv_file.seek(0)
        for row in csv_reader:
            if linecount == 0:
                pass
            else:
                states[row[1]] += addsub*(float(row[0])*weight-min)/(max-min)
            linecount += 1

parseCSV('Book1.csv', 1, 1.5)



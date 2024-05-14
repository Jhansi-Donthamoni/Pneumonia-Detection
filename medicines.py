import csv

class MedicineFilter:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def filter_medicines(self):
        filtered_medicines = []
        with open(self.csv_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                if row['use0'] in ["Treatment of Cough", "Treatment of Bacterial infections"]:
                    medicine = {'name': row['name'], 'substitute': row['substitute1']}
                    filtered_medicines.append(medicine)
                    count += 1
                    if count == 7:  # Limit to 7 medicines
                        break
        return filtered_medicines

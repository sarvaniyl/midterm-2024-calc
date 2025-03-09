import csv
import logging

class CSVHandler:
    """Handles CSV processing."""

    def read_csv(self, file_path):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    logging.info(f"Row: {row}")
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")

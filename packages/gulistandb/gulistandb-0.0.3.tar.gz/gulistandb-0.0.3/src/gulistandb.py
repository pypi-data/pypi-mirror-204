import os
import pandas as pd
import time
import csv


class Table:

    # current_directory = os.getcwd()
    def __init__(self, tableName, *column) -> None:
        self.TableName = tableName
        self.column = column
        self.folder_path = os.path.join(
            os.getcwd(), "Data")
        self.file_path = self.folder_path + '/' + self.TableName + '.csv'
        print("Table Created Successfully", self.file_path)

    def commit(self):
        self.folder_path = os.path.join(
            os.getcwd(), "Data")
        self.file_path = self.folder_path + '/' + self.TableName + '.csv'
        print("Table Created Successfully", self.file_path)
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(
                    self.folder_path)
            # filename = f'{self.file_path}/{self.TableName}.csv'
            with open(self.file_path, 'x', encoding='utf-8') as f:
                for i, key in enumerate(self.column):
                    f.write(key)
                    if i == len(self.column)-1:
                        break

                    else:
                        f.write(',')
        except (FileExistsError):
            print("This File Name Already Exists, Try Anything Else")

    def rename(self, newName):
        folder_path = os.path.join(
            os.getcwd(), "Data")
        post_file_path = folder_path + '/' + newName + '.csv'
        if os.path.exists(post_file_path):
            print("This FIlENAME ALREADY EXISTS")
            return -1
        self.drop()
        self.TableName = newName
        self.commit()

    def drop(self):
        if os.path.exists(self.file_path):
            try:
                os.unlink(self.file_path)
                # send2trash.send2trash(self.file_path)
                print(f"The file {self.file_path} has been deleted.")
            except PermissionError as e:
                print(f"Failed to delete {self.file_path}: {e}")
            except Exception as e:
                print(
                    f"An error occurred while deleting {self.file_path}: {e}")
        else:
            print(f"The file {self.file_path} does not exist.")

    def read(self, type='csv'):
        start = time.time()
        df = pd.read_csv(self.file_path, encoding='ISO-8859-1')
        if type == 'dict':
            data_dict = df.to_dict('records')
            print(data_dict)
        else:
            print(df)
        end = time.time()
        print(end - start)  # 0.2018742561340332

    def get(self):

        start = time.time()

        with open(self.file_path, 'r') as file:
            data = file.read()
            print(data)

        end = time.time()
        print(end - start)  # 11.899632692337036

    def insert(self, *datas):
        if len(datas) == len(self.column):
            with open(self.file_path, 'a') as f:
                f.write('\n')
                for i, data in enumerate(datas):
                    f.write(data)
                    if i == len(datas)-1:
                        break
                        # continue
                    else:
                        f.write(',')
        else:
            print(
                f"Please provide input data that is similar in quantity and order to the columns in your table.\nYour table has {len(self.column)} columns, but you provided {len(datas)} columns.")

    def update(self, _primary_id, content):
        # Read in the CSV file as a pandas DataFrame
        df = pd.read_csv(self.file_path)

        # Select rows based on ID
        id_to_check = _primary_id
        selected_rows = df[df['ID'] == id_to_check]
        # Print the selected rows
        with open(self.file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            # Write the updated rows to the file
            writer.writerow(['new data', 'new data', 'new data'])

    def delete(self, _primary_id):
        """ DELETE  """
        pass

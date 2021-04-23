import pandas as pd
from csv import writer

def updateTestCases(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
        

df = pd.read_csv('test_cases.csv')
input_lst = df['input']
output = df['output']

if len(input_lst)!=len(output):
  #print('Input doesnt match with output length!!')
  raise Exception('Input doesnt match with output length!!')

def retTestCase():
    return (input_lst,output)

if __name__ == '__main__':
    from bot import JethiyaAI

    babuchakEngine = JethiyaAI()
    count,wrongTag = babuchakEngine.test(input_lst,output)

    print("="*35)
    print("Final score : ",count, "/",len(output),"\nwrongTags : ",set(wrongTag))
    print("="*35)

from faker import Faker 
from pprint import pprint
import pandas as pd
import csv
from tqdm import tqdm
import logging

fake = Faker(locale='fr_FR')
""" Génération de data aléatoirement"""


logging.basicConfig(level=logging.INFO, 
                    filemode= 'a',
                    filename=  'file.log',
                    format= "%(asctime)s : %(levelname)s :  %(message)s"
                    )

def generate_data( n: int)-> list :
    """Generation de données

    Args:
        n (int): Nombre de ligne à générer

    Returns:
        list[dict]: Liste de dictionnaire 
    """    
    data : list = []
    for _ in range(n):
        dict_data : dict = {}
        dict_data['Country_code'] =  fake.current_country_code()
        dict_data['Department'] =  fake.department() 
        dict_data['Postcode'] =  fake.postcode()
        dict_data['administrative_unit'] =   fake.administrative_unit()
        dict_data['Fist_name'] =  fake.first_name()
        dict_data['Last_name'] = fake.last_name()
        dict_data['Age'] = fake.random_int(20, 65)
        dict_data['Email'] = fake.ascii_free_email()
        dict_data['Job'] =  fake.job()
        dict_data['Salary'] = fake.random_int(2000, 12000, 150)
        dict_data['Phone'] = fake.phone_number()
        dict_data['City'] = fake.city()  
        dict_data['Citation'] = fake.catch_phrase()
        data.append(dict_data)
    logging.info(f"Generation de {n} lignes.")
    return data
    
data = generate_data(n =10000)
#pprint(data)
with open('data_generared.csv', 'w', encoding ='utf-8') as f_write:
    for dic in tqdm(data) :
        w = csv.DictWriter(f_write, fieldnames= dic.keys(), delimiter= ';') # ideal pour manipuler les fichier csv
        if f_write.tell() == 0:
            w.writeheader()  

        w.writerow(dic)
    logging.info(f"Ecriture de {10000} lignes et {13} colonnes sur un fichier csv.")

with open('data_generared.csv', 'r', encoding ='utf-8') as f_read:
    df = pd.read_csv(f_read, sep = ';')
    print(df.head(10))

import pubchempy
import pandas as pd

xlsx = "CAS_file.xlsx"


def generate_from_cas(xlsx_name, output_name=None):
    csv = pd.read_excel(xlsx_name)
    names = []
    MF = []
    synonyms = []
    assert "CAS No." in list(csv.columns), "file must contain CAS No. column"
    cas_list = list(csv.loc[:, "CAS No."])
    for cas in cas_list:
        if type(cas) is str:
            result = pubchempy.get_compounds(cas, "name")
            print(result)
            if len(result) == 0:
                MF.append("NA")
                names.append("NA")
                synonyms.append("NA")
            else:
                MF.append(result[0].molecular_formula)
                names.append(result[0].iupac_name)
                synonyms_ = result[0].synonyms
                if synonyms_[0] == cas:
                    s = synonyms_[1]
                else:
                    s = synonyms_[0]
                synonyms.append(s)
                print(result[0].molecular_formula)
                print(result[0].iupac_name)
                print(s)
        else:
            MF.append("NA")
            names.append("NA")
            synonyms.append("NA")
    df = pd.DataFrame()
    df["CAS_No."] = cas_list
    df['Synonyms'] = synonyms
    df["Molecular_formula"] = MF
    df["IUPAC_name"] = names
    if output_name is None:
        output_name = xlsx[0:-5] + "processed"
    df.to_csv(output_name + ".csv", index=False)


generate_from_cas(xlsx)

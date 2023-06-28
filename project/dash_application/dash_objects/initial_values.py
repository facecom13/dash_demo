import datetime

start_date = datetime.datetime(2023, 1, 1)
finish_date = datetime.datetime(2029, 1, 1)

colors_dict = {0: "#32935F",
                   1:"#FFC000",
                   2:"#E8E8E8",
                   3:"#b3e5ca",
                   4:"#909090",
                   5:"#a0745b",
                   6:'#b27aa1',

                   7:'#E1EEDD',
                   8:'#F0A04B',
                   9:'#183A1D',
                   10:'#698269',
                   11: '#B99B6B',
                   12: '#AA5656',
                   13: '#678983',
                   14: '#FFB100',
                   15: '#658864',
                   16: '#B7B78A',
                   17: '#815B5B',
                   18: '#5D3891',
                   19: '#5D3891',
                   20: '#86E5FF',
                   21: '#A555EC',
                   22: '#0F6292',
                   23: '#FFED00',
                    24: "#8aa2c8",
                    25:'#17bdd5',
                    26:"#ea6755",
                    27:"#b7e781",
                    28:"#fe7f0e",
                    29:'#FEFBE9',
                    30:"#5d68b7"
                   }

credit_excel_rename_dict = {
            'credit_agreement_total_volume': 'ОбщаяСуммаДоговора',
            'credit_volume': 'СуммаТраншаКредита',
            'credit_tranch_date': 'ДатаТраншаКредита',
            'agreement_code': 'ВидПлатежа',
            'creditor': 'Кредитор',
            'credit_contract': 'Договор',
            'contract_title': 'ВидДоговора',
            'date': 'Дата',
            'amount': 'ЗначениеПлатежа',
            'credit_annual_rate': 'Ставка',
            'credit_line_type': 'ТипКредитнойЛинии',
            'freelimitremainings': 'СвободныйОстатокЛимита',
            'limitdeadline': 'СрокДействияЛимита',
            'ral_credit_transh_getting_deadline':'РАЛ_СрокПолученияТраншей',

        }
from database.connection import connectionAlchemy
import pandas as pd

class prodData(connectionAlchemy):

    def queryFailCauses(self, startDate, endDate, PASelected):
        """
            Retorna um dataframe com os seguintes dados:
            --------------
            PA      
                número de produto acabado
                
            NS      
                número de serie
                
            STEP
                descrição da step de teste do produto
                
            TIPO
                indica a etapa
                    1 -> primeira etapa
                    
                    2 -> segunda etapa
                
            STATUS  
                retorna se o produto foi aprovado naquela especifica step
                    A -> aprovado
                    
                    R -> reprovado
                    
            RECNO    
                ID da inserção no banco de dados
                
            HORA
                hora que o produto foi testado
        """

        sql = """
                SELECT z2.Z2_PRODUTO as PA, z9.ZZ9_SERIAL as NS, z9.ZZ9_STEP as STEP,
                z9.ZZ9_TIPO as TIPO, z9.ZZ9_STATUS as STATUS,TRY_CONVERT(date,(z9.ZZ9_DATE)) as DATA,
                z9.R_E_C_N_O_ as RECNO
                FROM SZ2990 AS z2 
                INNER JOIN ZZ9990 AS z9 ON z2.Z2_SERIE=z9.ZZ9_SERIAL
                WHERE z2.Z2_PRODUTO = %(PA)s AND z9.ZZ9_DATE BETWEEN %(start_date)s AND %(end_date)s ORDER BY RECNO
            """

        df = pd.read_sql(sql, self.engine, params={"PA":PASelected, "start_date":startDate, "end_date":endDate})
        #remove espaços da string
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    
    def queryFpyByDate(self, startDate, endDate):
        """
            Retorna um dataframe com os seguintes dados:
            --------------
            PA      
                número de produto acabado
                
            NS      
                número de serie
                
            NOME
                descrição do nome do produto
                
            TIPO
                indica a etapa
                    1 -> primeira etapa
                    
                    2 -> segunda etapa
                    
            NS_JIGA
                número de série da jiga utilizada
                
            STATUS  
                retorna se o produto foi aprovado
                    A -> aprovado
                    
                    R -> reprovado
                    
            DATA    
                data que o produto foi testado
                
            HORA
                hora que o produto foi testado
        """

        sql = """ SELECT z2.Z2_PRODUTO as PA, z8.ZZ8_NUMEQ as NS, b1.B1_DESC as NOME,
                z8.ZZ8_TIPO as TIPO, z8.ZZ8_NUMBER as NS_JIGA, z8.ZZ8_STATUS as STATUS,
                z8.ZZ8_OPNUM as OP, TRY_CONVERT(date,(z8.ZZ8_DATE)) as DATA, z8.ZZ8_HOUR as HORA, z8.R_E_C_N_O_ as RECNO
                FROM SZ2990 AS z2 
                INNER JOIN ZZ8990 AS z8 ON z2.Z2_SERIE=z8.ZZ8_NUMEQ
                INNER JOIN SB1990 AS b1 ON z2.Z2_PRODUTO=b1.B1_COD
                WHERE z8.ZZ8_OPNUM!='' AND z8.ZZ8_DATE BETWEEN %(start_date)s AND %(end_date)s ORDER BY RECNO"""
        df = pd.read_sql_query(sql, self.engine, params={"start_date":startDate, "end_date":endDate})
        #remove espaços da string
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    
    def queryFpyByDateAndPA(self, startDate, endDate, PASelected):
        """
            Retorna um dataframe com os seguintes dados:
            --------------
            PA      
                número de produto acabado
                
            NS      
                número de serie
                
            NOME
                descrição do nome do produto
                
            TIPO
                indica a etapa
                    1 -> primeira etapa
                    
                    2 -> segunda etapa
                    
            NS_JIGA
                número de série da jiga utilizada
                
            STATUS  
                retorna se o produto foi aprovado
                    A -> aprovado
                    
                    R -> reprovado
                    
            DATA    
                data que o produto foi testado
                
            HORA
                hora que o produto foi testado
        """

        sql = """
                SELECT z2.Z2_PRODUTO as PA, z8.ZZ8_NUMEQ as NS, b1.B1_DESC as NOME,
                z8.ZZ8_TIPO as TIPO, z8.ZZ8_NUMBER as NS_JIGA, z8.ZZ8_STATUS as STATUS,
                TRY_CONVERT(date,(z8.ZZ8_DATE)) as DATA, z8.ZZ8_HOUR as HORA, z8.R_E_C_N_O_ as RECNO
                FROM SZ2990 AS z2 
                INNER JOIN ZZ8990 AS z8 ON z2.Z2_SERIE=z8.ZZ8_NUMEQ
                INNER JOIN SB1990 AS b1 ON z2.Z2_PRODUTO=b1.B1_COD
                WHERE z2.Z2_PRODUTO = %(PA)s AND z8.ZZ8_DATE BETWEEN %(start_date)s AND %(end_date)s ORDER BY RECNO
            """

        df = pd.read_sql_query(sql, self.engine, params={"PA":PASelected, "start_date":startDate, "end_date":endDate})
        #remove espaços da string
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        return df
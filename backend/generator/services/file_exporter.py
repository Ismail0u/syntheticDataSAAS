import json
import csv
import pandas as pd
from io import StringIO, BytesIO
import xml.etree.ElementTree as ET
from xml.dom import minidom

class FileExporter:
    """
    A utility class containing static methods to convert a list of dictionaries 
    (the generated dataset) into various file formats (JSON, CSV, XLSX, SQL, XML).
    """
    
    @staticmethod
    def to_json(data):
        """Exporte en JSON"""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_csv(data):
        """Exporte en CSV"""
        if not data:
            return ""
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()
    
    @staticmethod
    def to_excel(data):
        """Exporte en Excel (XLSX)"""
        if not data:
            return None
        
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def to_sql(data, table_name='synthetic_data'):
        """Exporte en SQL INSERT statements"""
        if not data:
            return ""
        
        columns = ', '.join(data[0].keys())
        sql_statements = []
        
        for row in data:
            values = ', '.join([f"'{str(v).replace('\'', '\'\'')}'" for v in row.values()])
            sql_statements.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
        
        return '\n'.join(sql_statements)
    
    @staticmethod
    def to_xml(data, root_name='dataset', item_name='item'):
        """Exporte en XML"""
        if not data:
            return ""
        
        root = ET.Element(root_name)
        
        for row in data:
            item = ET.SubElement(root, item_name)
            for key, value in row.items():
                field = ET.SubElement(item, key)
                field.text = str(value)
        
        # Pretty print
        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
        return xml_str
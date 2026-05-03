# # import requests
# # from database.database_manager import DatabaseManager 

# # def get_data_grouped_by_date():
# #     """Groups database results by date: { '14-04-2026': [user1, user2], ... }"""
# #     query = "SELECT * FROM assessment_tests WHERE membership_number='' and pass_fail='PASS'"
    
# #     grouped_data = []
# #     with DatabaseManager('data/ahv_data.db') as db:
# #         data = db.connection.execute(query).fetchall()
        
# #         for i in data:
# #             entry = {
# #                'name': i[1],
# #                'surname': i[2],
# #             }
# #             grouped_data.append(entry)
# #     print(len(grouped_data))
# #     return grouped_data

# # print(get_data_grouped_by_date())

# from fpdf import FPDF
# from datetime import datetime
# from database.database_manager import DatabaseManager 

# class PDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, 'TSKH Assessment Pass List', 0, 1, 'C')
#         self.ln(5)

#     def footer(self):
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# def generate_pdf_from_list(data_list):
#     pdf = PDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=10)
    
#     # Table Header
#     pdf.set_fill_color(200, 220, 255)
#     pdf.cell(10, 10, '#', 1, 0, 'C', 1)
#     pdf.cell(90, 10, 'Name', 1, 0, 'C', 1)
#     pdf.cell(90, 10, 'Surname', 1, 1, 'C', 1)
#     pdf.cell(90, 10, 'cellphone', 1, 1, 'C', 1)

#     # Table Rows
#     for index, entry in enumerate(data_list, start=1):
#         pdf.cell(10, 10, str(index), 1, 0, 'C')
#         pdf.cell(90, 10, str(entry['name']), 1, 0, 'L')
#         pdf.cell(90, 10, str(entry['surname']), 1, 1, 'L')
#         pdf.cell(90, 10, str(entry['cellphone']), 1, 1, 'L')

#     filename = f"passed_assessments_{datetime.now().strftime('%Y-%m-%d')}.pdf"
#     pdf.output(filename)
#     print(f"✅ PDF List created: {filename}")

# def get_data_grouped_by_date():
#     """Groups database results by date: { '14-04-2026': [user1, user2], ... }"""
#     query = "SELECT * FROM assessment_tests WHERE membership_number='' and pass_fail='PASS'"
#     query2 = 'SELECT cell_number FROM trsh_membership_numbers WHERE name=? and surname=?'
    
#     grouped_data = []
#     with DatabaseManager('data/ahv_data.db') as db:
#         data = db.connection.execute(query).fetchall()
        
#         for i in data:
#             cellnumber = db.connection.execute(query2, (i[1], i[2])).fetchone()
#             entry = {
#                'name': i[1],
#                'surname': i[2],
#                'cellphone': cellnumber,
#             }
#             grouped_data.append(entry)
    
#     # If there is data, generate the PDF
#     if grouped_data:
#         generate_pdf_from_list(grouped_data)
#     else:
#         print("No records found to export.")
        
#     return grouped_data

# # Execute
# data = get_data_grouped_by_date()

from fpdf import FPDF
from datetime import datetime
from database.database_manager import DatabaseManager 

class PDF(FPDF):
    def header(self):
        # Add a logo here if needed: self.image('logo.png', 10, 8, 33)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'TSKH Assessment Pass List', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_from_list(data_list):
    pdf = PDF()
    pdf.add_page()
    
    # Column Widths (Total = 190mm to fit A4 with margins)
    w_idx = 10
    w_name = 60
    w_sur = 60
    w_cell = 60

    # Table Header
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(w_idx, 10, '#', 1, 0, 'C', 1)
    pdf.cell(w_name, 10, 'Name', 1, 0, 'C', 1)
    pdf.cell(w_sur, 10, 'Surname', 1, 0, 'C', 1)
    pdf.cell(w_cell, 10, 'Cellphone', 1, 1, 'C', 1) # ln=1 moves to next line

    # Table Rows
    pdf.set_font("Arial", size=10)
    for index, entry in enumerate(data_list, start=1):
        # Check for page break
        if pdf.get_y() > 260:
            pdf.add_page()
            
        pdf.cell(w_idx, 9, str(index), 1, 0, 'C')
        pdf.cell(w_name, 9, str(entry['name']), 1, 0, 'L')
        pdf.cell(w_sur, 9, str(entry['surname']), 1, 0, 'L')
        
        # Display "N/A" if cellphone is missing
        cell_text = str(entry['cellphone']) if entry['cellphone'] else "N/A"
        pdf.cell(w_cell, 9, cell_text, 1, 1, 'L')

    filename = f"passed_assessments_{datetime.now().strftime('%Y-%m-%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"✅ PDF List created: {filename}")

def get_data_grouped_by_date():
    query = "SELECT * FROM assessment_tests WHERE membership_number='' and pass_fail='PASS'"
    query2 = 'SELECT cell_number FROM trsh_membership_numbers WHERE name=? and surname=? LIMIT 1'
    
    grouped_data = []
    with DatabaseManager('data/ahv_data.db') as db:
        data = db.connection.execute(query).fetchall()
        
        for i in data:
            # i[1] = name, i[2] = surname (Assumed based on your previous code)
            res = db.connection.execute(query2, (i[1], i[2])).fetchone()
            
            # extract value from tuple: ('082...', ) -> '082...'
            cellnumber = res[0] if res else None
            
            entry = {
               'name': i[1],
               'surname': i[2],
               'cellphone': cellnumber,
            }
            grouped_data.append(entry)
    
    print(f"Records found: {len(grouped_data)}")
    
    if grouped_data:
        generate_pdf_from_list(grouped_data)
        
    return grouped_data

if __name__ == "__main__":
    get_data_grouped_by_date()
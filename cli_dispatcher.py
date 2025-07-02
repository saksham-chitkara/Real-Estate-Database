from db_connection import DBconnection
import queries
from tabulate import tabulate
import error_handling as error
from colorama import Fore, Style, init
init(autoreset=True)
LIGHTBLUE = Fore.CYAN + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT

def pretty_print(results):
    if results:
        print(tabulate(results, headers='keys', tablefmt='grid'))
        print(SUCCESS + str(len(results)) + " result" + ("" if len(results) == 1 else "s"))
    else:
        print(Fore.YELLOW + 'No data')
    print()  # Add blank line after output

def select(cmd_list, dbms, cmd_num=0):
    query_types = ['all_investors', 'all_tenants', 'properties_for_sale', 'property_dealers']
    if cmd_num > 0:
        if cmd_num <= len(query_types):
            query = queries.SELECT(query_types[cmd_num-1])
            results = dbms.execute_query(query, fetch=True)
            pretty_print(results)
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'select'):
            return
        query = queries.SELECT(cmd_list[1], *cmd_list[2:])
        results = dbms.execute_query(query, fetch=True)
        pretty_print(results)

def project(cmd_list, dbms, cmd_num=0):
    query_types = ['investors_multicity', 'ongoing_projects', 'top_expensive_properties']
    if cmd_num > 0:
        adjusted_num = cmd_num - 5
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            if query_types[adjusted_num] == 'ongoing_projects':
                firm_id = input(LIGHTBLUE + "Enter firm ID: " + Style.RESET_ALL)
                query = queries.PROJECT(query_types[adjusted_num], firm_id)
            else:
                query = queries.PROJECT(query_types[adjusted_num])
            results = dbms.execute_query(query, fetch=True)
            pretty_print(results)
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'project'):
            return
        query = queries.PROJECT(cmd_list[1], *cmd_list[2:])
        results = dbms.execute_query(query, fetch=True)
        pretty_print(results)

def aggregate(cmd_list, dbms, cmd_num=0):
    query_types = [
        'avg_revenue_high_reputation', 
        'investment_stats_last_year', 
        'project_roi_by_contractor_type',
        'total_properties',
        'avg_credit_score_tenants'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 8
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            query = queries.AGGREGATE(query_types[adjusted_num])
            results = dbms.execute_query(query, fetch=True)
            pretty_print(results)
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'aggregate'):
            return
        query = queries.AGGREGATE(cmd_list[1], *cmd_list[2:])
        results = dbms.execute_query(query, fetch=True)
        pretty_print(results)

def search(cmd_list, dbms, cmd_num=0):
    query_types = [
        'properties_by_keyword',
        'properties_by_amenities_and_price',
        'marketing_firms_by_specialization'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 13
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            if query_types[adjusted_num] == 'properties_by_keyword':
                keyword = input(LIGHTBLUE + "Enter keyword to search: " + Style.RESET_ALL)
                query = queries.SEARCH(query_types[adjusted_num], keyword)
            elif query_types[adjusted_num] == 'properties_by_amenities_and_price':
                min_price = input(LIGHTBLUE + "Enter minimum price: " + Style.RESET_ALL)
                max_price = input(LIGHTBLUE + "Enter maximum price: " + Style.RESET_ALL)
                amenities = input(LIGHTBLUE + "Enter amenities (comma separated): " + Style.RESET_ALL).split(',')
                query = queries.SEARCH(query_types[adjusted_num], min_price, max_price, amenities)
            elif query_types[adjusted_num] == 'marketing_firms_by_specialization':
                specialization = input(LIGHTBLUE + "Enter specialization: " + Style.RESET_ALL)
                query = queries.SEARCH(query_types[adjusted_num], specialization)
            results = dbms.execute_query(query, fetch=True)
            pretty_print(results)
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'search'):
            return
        query = queries.SEARCH(cmd_list[1], *cmd_list[2:])
        results = dbms.execute_query(query, fetch=True)
        pretty_print(results)

def analysis(cmd_list, dbms, cmd_num=0):
    query_types = [
        'investment_roi_trends',
        'property_value_by_amenities',
        'investment_success_by_firm_rating',
        'marketing_impact_analysis',
        'investor_property_type_preference',
        'city_investment_analysis'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 16
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            query = queries.ANALYSIS(query_types[adjusted_num])
            results = dbms.execute_query(query, fetch=True)
            pretty_print(results)
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'analysis'):
            return
        query = queries.ANALYSIS(cmd_list[1], *cmd_list[2:])
        results = dbms.execute_query(query, fetch=True)
        pretty_print(results)

def insert(cmd_list, dbms, cmd_num=0):
    query_types = [
        'project_investment',
        'new_tenant',
        'lessee_details'
    ]
    # Foreign key info for user prompts
    fk_info = {
        'project_investment': {
            2: 'ProjectConcerned (must be an existing ProjectID in Project table)'
        },
        'lessee_details': {
            6: 'GuarantorContact (must be unique, 10-digit integer)'
        },
        'new_tenant': {
            2: 'DependsOn (must be an existing TenantID in Tenant table, or blank for none)'
        }
    }
    
    def validate_input(value, data_type, field_name):
        try:
            if data_type == 'int':
                return int(value)
            elif data_type == 'float':
                return float(value)
            elif data_type == 'date':
                from datetime import datetime
                return datetime.strptime(value, '%Y-%m-%d').date()
            else:
                return value
        except ValueError:
            print(Fore.RED + f"Invalid {data_type} format for {field_name}. Please try again.")
            return None
    
    def collect_project_investment_data():
        print(LIGHTBLUE + "Enter project investment details:")
        print(Fore.YELLOW + "InvestmentID is a primary key and must be unique.")
        investment_id = None
        while investment_id is None:
            investment_id = validate_input(input(LIGHTBLUE + "InvestmentID (integer): " + Style.RESET_ALL), 'int', 'InvestmentID')
        invested_amount = None
        while invested_amount is None:
            invested_amount = validate_input(input(LIGHTBLUE + "InvestedAmount (decimal): " + Style.RESET_ALL), 'float', 'InvestedAmount')
        print(Fore.YELLOW + "ProjectConcerned is a foreign key. The value must be an existing ProjectID in the Project table.")
        project_concerned = None
        while project_concerned is None:
            project_concerned = validate_input(input(LIGHTBLUE + "ProjectConcerned (integer): " + Style.RESET_ALL), 'int', 'ProjectConcerned')
        investment_date = None
        while investment_date is None:
            investment_date = validate_input(input(LIGHTBLUE + "InvestmentDate (YYYY-MM-DD): " + Style.RESET_ALL), 'date', 'InvestmentDate')
        profit_margin = None
        while profit_margin is None:
            profit_margin = validate_input(input(LIGHTBLUE + "ProfitMargin (decimal): " + Style.RESET_ALL), 'float', 'ProfitMargin')
        projected_roi = None
        while projected_roi is None:
            projected_roi = validate_input(input(LIGHTBLUE + "ProjectedROI (decimal): " + Style.RESET_ALL), 'float', 'ProjectedROI')
        risk_level = None
        while risk_level is None:
            risk_level = validate_input(input(LIGHTBLUE + "RiskLevel (0-10): " + Style.RESET_ALL), 'int', 'RiskLevel')
            if risk_level is not None and (risk_level < 0 or risk_level > 10):
                print(Fore.RED + "RiskLevel must be between 0 and 10")
                risk_level = None
        return (investment_id, invested_amount, project_concerned, investment_date, profit_margin, projected_roi, risk_level)
    
    def collect_tenant_data():
        print(LIGHTBLUE + "Enter tenant details:")
        print(Fore.YELLOW + "TenantID is a primary key and must be unique.")
        tenant_id = None
        while tenant_id is None:
            tenant_id = validate_input(input(LIGHTBLUE + "TenantID (integer): " + Style.RESET_ALL), 'int', 'TenantID')
        name = input(LIGHTBLUE + "Name: " + Style.RESET_ALL)
        print(Fore.YELLOW + "DependsOn is a foreign key. The value must be an existing TenantID in the Tenant table, or blank for none.")
        depends_on = input(LIGHTBLUE + "DependsOn (TenantID, leave blank if none): " + Style.RESET_ALL)
        depends_on = validate_input(depends_on, 'int', 'DependsOn') if depends_on.strip() else None
        return (tenant_id, name, depends_on)

    def collect_lessee_details_data():
        print(LIGHTBLUE + "Enter lessee details:")
        print(Fore.YELLOW + "LesseID is a primary key and must be unique.")
        lesse_id = None
        while lesse_id is None:
            lesse_id = validate_input(input(LIGHTBLUE + "LesseID (integer): " + Style.RESET_ALL), 'int', 'LesseID')
        name = input(LIGHTBLUE + "Name: " + Style.RESET_ALL)
        occupation = input(LIGHTBLUE + "Occupation: " + Style.RESET_ALL)
        annual_income = None
        while annual_income is None:
            annual_income = validate_input(input(LIGHTBLUE + "AnnualIncome (decimal): " + Style.RESET_ALL), 'float', 'AnnualIncome')
        print(Fore.YELLOW + "LeasePurpose options: RESIDENTIAL, COMMERCIAL")
        lease_purpose = input(LIGHTBLUE + "LeasePurpose: " + Style.RESET_ALL)
        credit_score = None
        while credit_score is None:
            credit_score = validate_input(input(LIGHTBLUE + "CreditScore (decimal): " + Style.RESET_ALL), 'float', 'CreditScore')
        guarantor_contact = None
        while guarantor_contact is None:
            raw = input(LIGHTBLUE + "GuarantorContact (10-digit integer): " + Style.RESET_ALL)
            if raw.isdigit() and len(raw) == 10:
                guarantor_contact = int(raw)
            else:
                print(Fore.RED + "GuarantorContact must be a 10-digit number.")
        return (lesse_id, name, occupation, annual_income, lease_purpose, credit_score, guarantor_contact)

    if cmd_num > 0:
        adjusted_num = cmd_num - 22
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            query_type = query_types[adjusted_num]
            if query_type == 'project_investment':
                args = collect_project_investment_data()
            elif query_type == 'new_tenant':
                args = collect_tenant_data()
            elif query_type == 'lessee_details':
                args = collect_lessee_details_data()
            query = queries.INSERT(query_type, *args)
            try:
                dbms.execute_query(query)
                print(SUCCESS + f"Successfully inserted {query_type}")
            except Exception as e:
                error.db_error(str(e))
            print()  # Add blank line after output
        else:
            print(Fore.RED + f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'insert'):
            return
        query_type = cmd_list[1]
        if query_type == 'project_investment':
            args = collect_project_investment_data()
        elif query_type == 'new_tenant':
            args = collect_tenant_data()
        elif query_type == 'lessee_details':
            args = collect_lessee_details_data()
        else:
            print(Fore.RED + f"Invalid insert type: {query_type}")
            return
        query = queries.INSERT(query_type, *args)
        try:
            dbms.execute_query(query)
            print(SUCCESS + f"Successfully inserted {query_type}")
        except Exception as e:
            error.db_error(str(e))
        print()  # Add blank line after output

def update(cmd_list, dbms, cmd_num=0):
    query_types = [
        'projected_roi',
        'marketing_firm_reputation',
        'specific_marketing_firm_reputation'
    ]
    
    def validate_input(value, data_type, field_name):
        try:
            if data_type == 'int':
                return int(value)
            elif data_type == 'float':
                return float(value)
            elif data_type == 'date':
                from datetime import datetime
                return datetime.strptime(value, '%Y-%m-%d').date()
            else:
                return value
        except ValueError:
            print(Fore.RED + f"Invalid {data_type} format for {field_name}. Please try again.")
            return None
    
    def collect_specific_firm_reputation_data():
        print(LIGHTBLUE + "Update specific marketing firm reputation:")
        rating = None
        while rating is None:
            rating = validate_input(input(LIGHTBLUE + "Enter new reputation rating (0-10): " + Style.RESET_ALL), 'int', 'ReputationRating')
            if rating is not None and (rating < 0 or rating > 10):
                print(Fore.RED + "Reputation rating must be between 0 and 10")
                rating = None
        print(Fore.YELLOW + "MarketFirmID is a foreign key. The value must be an existing MarketFirmID in the MarketingFirm table.")
        firm_id = None
        while firm_id is None:
            firm_id = validate_input(input(LIGHTBLUE + "Enter marketing firm ID: " + Style.RESET_ALL), 'int', 'MarketFirmID')
        return (rating, firm_id)
    
    def confirm_bulk_update(update_type):
        """Confirm bulk update operations"""
        descriptions = {
            'projected_roi': 'increase projected ROI by 5% for all ongoing projects',
            'marketing_firm_reputation': 'increase reputation rating by 1 for marketing firms with >100 clients founded after 2023'
        }
        
        description = descriptions.get(update_type, update_type)
        confirmation = input(f"Are you sure you want to {description}? (yes/no): ")
        return confirmation.lower() == 'yes'
    
    if cmd_num > 0:
        adjusted_num = cmd_num - 25
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            query_type = query_types[adjusted_num]
            
            if query_type == 'specific_marketing_firm_reputation':
                args = collect_specific_firm_reputation_data()
                query = queries.UPDATE(query_type, *args)
            else:
                if confirm_bulk_update(query_type):
                    query = queries.UPDATE(query_type)
                else:
                    print("Update operation cancelled")
                    return
            
            try:
                dbms.execute_query(query)
                print(SUCCESS + f"Successfully updated {query_type}")
            except Exception as e:
                error.db_error(str(e))
            print()  # Add blank line after output
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'update'):
            return
        
        query_type = cmd_list[1]
        
        if query_type == 'specific_marketing_firm_reputation':
            args = collect_specific_firm_reputation_data()
            query = queries.UPDATE(query_type, *args)
        elif query_type in ['projected_roi', 'marketing_firm_reputation']:
            if confirm_bulk_update(query_type):
                query = queries.UPDATE(query_type)
            else:
                print("Update operation cancelled")
                return
        else:
            print(f"Invalid update type: {query_type}")
            return
        
        try:
            dbms.execute_query(query)
            print(SUCCESS + f"Successfully updated {query_type}")
        except Exception as e:
            error.db_error(str(e))
        print()  # Add blank line after output

def delete(cmd_list, dbms, cmd_num=0):
    query_types = [
        'tenants_with_poor_payment_history',
        'properties_for_demolition',
        'high_risk_investments'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 28
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            confirmation = input(f"Are you sure you want to delete {query_types[adjusted_num]}? (yes/no): ")
            if confirmation.lower() == 'yes':
                query = queries.DELETE(query_types[adjusted_num])
                dbms.execute_query(query)
                print(SUCCESS + f"Successfully deleted {query_types[adjusted_num]}")
            else:
                print("Delete operation cancelled")
            print()  # Add blank line after output
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'delete'):
            return
        confirmation = input(f"Are you sure you want to delete {cmd_list[1]}? (yes/no): ")
        if confirmation.lower() == 'yes':
            query = queries.DELETE(cmd_list[1], *cmd_list[2:])
            dbms.execute_query(query)
            print(SUCCESS + f"Successfully deleted {cmd_list[1]}")
        else:
            print("Delete operation cancelled")
        print()  # Add blank line after output

def main():
    dbms = DBconnection()
    
    while True:
        user_input = input(MAGENTA + "Your choice: " + Style.RESET_ALL)
        
        if user_input.lower() == 'q':
            print("Thank you for using the Real Estate Database System. Goodbye!")
            break
        elif user_input.lower() == 'h':
            with open('help.txt', 'r') as f:
                print(f.read())
        else:
            # Check if it's a numeric command
            if user_input.isdigit():
                cmd_num = int(user_input)
                if 1 <= cmd_num <= 4:
                    select([], dbms, cmd_num)
                elif 5 <= cmd_num <= 7:
                    project([], dbms, cmd_num)
                elif 8 <= cmd_num <= 12:
                    aggregate([], dbms, cmd_num)
                elif 13 <= cmd_num <= 15:
                    search([], dbms, cmd_num)
                elif 16 <= cmd_num <= 21:
                    analysis([], dbms, cmd_num)
                elif 22 <= cmd_num <= 24:
                    insert([], dbms, cmd_num)
                elif 25 <= cmd_num <= 27:
                    update([], dbms, cmd_num)
                elif 28 <= cmd_num <= 30:
                    delete([], dbms, cmd_num)
                else:
                    print(Fore.RED + "Invalid query number. Type 'h' for help.")
            else:
                # Handle text commands
                parts = user_input.split()
                cmd = parts[0]
                cmd_list = parts
                
                if cmd == 'select':
                    select(cmd_list, dbms)
                elif cmd == 'project':
                    project(cmd_list, dbms)
                elif cmd == 'aggregate':
                    aggregate(cmd_list, dbms)
                elif cmd == 'search':
                    search(cmd_list, dbms)
                elif cmd == 'analysis':
                    analysis(cmd_list, dbms)
                elif cmd == 'insert':
                    insert(cmd_list, dbms)
                elif cmd == 'update':
                    update(cmd_list, dbms)
                elif cmd == 'delete':
                    delete(cmd_list, dbms)
                else:
                    print(Fore.RED + "Invalid command. Type 'h' for help.")

if __name__ == "__main__":
    main()

import DBconnection
import queries
from tabulate import tabulate
import error

def pretty_print(results):
    if results:
        print(tabulate(results, headers='keys', tablefmt='grid'))
        print(len(results), "result" if len(results) == 1 else "results")
    else:
        print('No data')

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
                firm_id = input("Enter firm ID: ")
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
                keyword = input("Enter keyword to search: ")
                query = queries.SEARCH(query_types[adjusted_num], keyword)
            elif query_types[adjusted_num] == 'properties_by_amenities_and_price':
                min_price = input("Enter minimum price: ")
                max_price = input("Enter maximum price: ")
                amenities = input("Enter amenities (comma separated): ").split(',')
                query = queries.SEARCH(query_types[adjusted_num], min_price, max_price, amenities)
            elif query_types[adjusted_num] == 'marketing_firms_by_specialization':
                specialization = input("Enter specialization: ")
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
        'property'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 22
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            print(f"To insert {query_types[adjusted_num]}, please use the command: insert {query_types[adjusted_num]} [args]")
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'insert'):
            return
        query = queries.INSERT(cmd_list[1], *cmd_list[2:])
        dbms.execute_query(query)
        print(f"Successfully inserted {cmd_list[1]}")

def update(cmd_list, dbms, cmd_num=0):
    query_types = [
        'projected_roi',
        'marketing_firm_reputation',
        'specific_marketing_firm_reputation'
    ]
    if cmd_num > 0:
        adjusted_num = cmd_num - 25
        if adjusted_num >= 0 and adjusted_num < len(query_types):
            if query_types[adjusted_num] == 'specific_marketing_firm_reputation':
                rating = input("Enter new reputation rating: ")
                firm_id = input("Enter marketing firm ID: ")
                query = queries.UPDATE(query_types[adjusted_num], rating, firm_id)
            else:
                query = queries.UPDATE(query_types[adjusted_num])
            dbms.execute_query(query)
            print(f"Successfully updated with {query_types[adjusted_num]}")
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'update'):
            return
        query = queries.UPDATE(cmd_list[1], *cmd_list[2:])
        dbms.execute_query(query)
        print(f"Successfully updated with {cmd_list[1]}")

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
                print(f"Successfully deleted {query_types[adjusted_num]}")
            else:
                print("Delete operation cancelled")
        else:
            print(f"Invalid selection number: {cmd_num}")
    else:
        if error.compare_list(len(cmd_list), 2, 'delete'):
            return
        confirmation = input(f"Are you sure you want to delete {cmd_list[1]}? (yes/no): ")
        if confirmation.lower() == 'yes':
            query = queries.DELETE(cmd_list[1], *cmd_list[2:])
            dbms.execute_query(query)
            print(f"Successfully deleted {cmd_list[1]}")
        else:
            print("Delete operation cancelled")

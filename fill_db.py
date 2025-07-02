import random
import pymysql
from faker import Faker
from datetime import datetime, timedelta
from itertools import cycle

# Database configuration
DB_CONFIG = {
    'host': '',      # Fill your host (e.g., localhost)
    'user': '',      # Fill your MySQL username
    'password': '',  # Fill your MySQL password
    'database': ''   # Fill your database name (e.g., REAL_ESTATE)
}

# Ensure database exists before connecting
DB_NAME = DB_CONFIG['database']
DB_CONFIG_BASE = {
    'host': DB_CONFIG['host'],
    'user': DB_CONFIG['user'],
    'password': DB_CONFIG['password'],
}
try:
    temp_conn = pymysql.connect(**DB_CONFIG_BASE)
    with temp_conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    temp_conn.close()
except Exception as e:
    print(f"Error creating database {DB_NAME}: {e}")

class ComprehensiveRealEstatePopulator:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.fake = Faker()
        self.used_ids = set()
        self.used_contacts = set()
        self.used_locations = set()

    def generate_unique_id(self, max_range=1000000):
        while True:
            new_id = random.randint(1, max_range)
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id

    def generate_unique_contact(self):
        while True:
            contact = random.randint(1000000000, 9999999999)
            if contact not in self.used_contacts:
                self.used_contacts.add(contact)
                return contact

    def generate_marketing_firms(self, num_firms=5):
        """Generate marketing firms with unique Location and ContactInfo"""
        specializations = [
            "Digital Marketing",
            "Search Engine Optimization (SEO)",
            "Search Engine Marketing (SEM)",
            "Social Media Marketing (SMM)",
            "Content Marketing",
            "Email Marketing",
            "Influencer Marketing",
            "E-commerce Marketing",
            "Print Advertising",
            "Television Advertising",
            "Radio Advertising",
            "Outdoor Advertising",
            "Brand Strategy Development",
            "Graphic Design",
            "Web Development",
            "Public Relations (PR)",
            "Event Marketing",
            "Market Research",
            "Video Production",
            "Product Marketing",
            "Affiliate Marketing",
            "Conversion Rate Optimization (CRO)",
            "Analytics and Reporting",
            "Mobile Marketing",
            "Experiential Marketing"
        ]

        firms = []
        for _ in range(num_firms):
            firm = (
                self.generate_unique_id(),
                self.fake.company(),
                self.generate_unique_location(),
                self.fake.random_int(min=1990, max=2024),
                self.generate_unique_contact(),
                random.choice(specializations),
                random.randint(0, 10),
                random.randint(10, 1000),
                round(self.fake.pydecimal(left_digits=10, right_digits=2, positive=True), 2)
            )
            firms.append(firm)
        
        insert_query = """
        INSERT IGNORE INTO MarketingFirm 
        (MarketFirmID, Name, Location, FoundedYear, ContactInfo, 
        Specialization, ReputationRating, NumberOfClients, AnnualRevenue) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, firms)
        return firms

    def generate_unique_location(self):
        """Helper method to generate unique locations"""
        while True:
            location = self.fake.city()
            if location not in self.used_locations:
                self.used_locations.add(location)
                return location

    def generate_services_of_marketing_firm(self, firms):
        """Generate services for marketing firms"""
        services = []
        services_list = [
            'Property Valuation', 'Market Analysis', 
            'Investment Consulting', 'Property Photography', 
            'Digital Marketing', 'Legal Consultation'
        ]
        
        for firm in firms:
            num_services = random.randint(2, len(services_list))
            selected_services = random.sample(services_list, num_services)
            for service in selected_services:
                services.append((firm[0], service))
        
        insert_query = """
        INSERT IGNORE INTO ServicesOfMarketingFirm 
        (MarketFirmID, ServicesOffered) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, services)
        return services
    
    def generate_unique_contact(self):
        """Helper method to generate unique contact numbers"""
        while True:
            contact = random.randint(1000000000, 9999999999)
            if contact not in self.used_contacts:
                self.used_contacts.add(contact)
                return contact

    def generate_unique_guarantor_contact(self):
        """Helper method to generate unique guarantor contact numbers"""
        while True:
            contact = random.randint(1000000000, 9999999999)
            if contact not in self.used_guarantor_contacts:
                self.used_guarantor_contacts.add(contact)
                return contact

    def generate_purchaser(self, num_purchasers=10):
        """Generate purchaser records according to schema"""
        purchasers = []
        
        for _ in range(num_purchasers):
            purchaser = (
                self.generate_unique_id(),
                self.fake.name(),
                self.generate_unique_contact(),  # Unique contact
                self.fake.date_between(start_date='-2y', end_date='today'),
                random.choice(['Cash', 'Bank Transfer', 'Mortgage', 'Installment']),
                round(self.fake.pydecimal(left_digits=16, right_digits=2, positive=True), 2),
                self.fake.text(max_nb_chars=100),
                round(random.uniform(0.01, 0.99), 2),  # Equity between 0 and 1
                self.fake.date_between(start_date='-1y', end_date='+1y'),
                self.fake.building_number(),
                self.fake.street_name(),
                random.randint(1, 1000),
                self.fake.city(),
                random.randint(10000, 99999)
            )
            purchasers.append(purchaser)
        
        insert_query = """
        INSERT IGNORE INTO Purchaser 
        (PurchaserID, Name, ContactInfo, DateOfPurchase, PaymentMethod, 
        AmountPayed, Purpose, Equity, DateOfSell, Address_StreetNo, 
        Address_StreetName, Address_BuildingNo, Address_City, Address_Zipcode) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, purchasers)
        return purchasers
    
    def generate_real_property(self, marketing_firms, num_properties=10):
        """Generate real property records matching schema constraints"""
        if not marketing_firms:
            raise ValueError("Marketing firms list cannot be empty")
            
        properties = []
        for _ in range(num_properties):
            property_item = (
                self.generate_unique_id(),
                self.fake.company() + " Property",
                self.fake.text(max_nb_chars=100),
                round(self.fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2),
                random.choice(['Available', 'Sold', 'Rented', 'Marked for Demolition']),
                random.choice(['Residential', 'Commercial', 'Intellectual']),
                self.fake.text(max_nb_chars=200),  # MaintenanceHistory
                random.choice(marketing_firms)[0],  # MarketFirmID (foreign key)
                self.fake.building_number(),
                self.fake.street_name(),
                random.randint(1, 1000),
                self.fake.city(),
                random.randint(10000, 99999)
            )
            properties.append(property_item)
        
        insert_query = """
        INSERT IGNORE INTO RealProperty 
        (PropertyID, Name, Description, Price, Status, PropertyType, 
        MaintenanceHistory, MarketFirmID, Address_StreetNo, Address_StreetName, 
        Address_BuildingNo, Address_City, Address_Zipcode) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, properties)
        return properties
    
    def generate_projects(self, construction_firms, properties, num_projects=10):
        """Generate project records according to schema"""
        if not construction_firms:
            raise ValueError("Construction firms list cannot be empty")
            
        projects = []
        # First generate parent projects
        num_parent_projects = num_projects // 10  # Some projects will be parent projects
        
        # Generate parent projects first
        parent_projects = []
        for _ in range(num_parent_projects):
            project = (
                self.generate_unique_id(),
                self.fake.catch_phrase() + " Project",
                random.choice(['Completed', 'Ongoing']),  # Match ENUM
                round(self.fake.pydecimal(left_digits=10, right_digits=2, positive=True), 2),
                None,  # No parent for these
                random.choice(construction_firms)[0],  # FirmID foreign key
                random.choice(properties)[0]
            )
            parent_projects.append(project)
            projects.append(project)
        
        # Generate child projects
        for _ in range(num_projects - num_parent_projects):
            project = (
                self.generate_unique_id(),
                self.fake.catch_phrase() + " Project",
                random.choice(['Completed', 'Ongoing']),  # Match ENUM
                round(self.fake.pydecimal(left_digits=10, right_digits=2, positive=True), 2),
                random.choice(parent_projects)[0] if parent_projects else None,  # ParentProject foreign key
                random.choice(construction_firms)[0],  # FirmID foreign key
                random.choice(properties)[0]
            )
            projects.append(project)
        
        insert_query = """
        INSERT IGNORE INTO Project 
        (ProjectID, ProjectName, Status, EstimatedCost, ParentProject, FirmID, PropertyID) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, projects)
        return projects
    
    def generate_property_dealers(self, num_dealers=5):
        """Generate property dealer records according to schema"""
        dealers = []
        
        for _ in range(num_dealers):
            dealer = (
                self.generate_unique_id(),
                self.fake.name(),
                self.generate_unique_contact(),  # Unique contact number
                random.randint(1, 30),  # ExperienceYears
                round(random.uniform(1.0, 10.0), 2),  # Rating between 1-10
                self.fake.text(max_nb_chars=100)  # License
            )
            dealers.append(dealer)
        
        insert_query = """
        INSERT IGNORE INTO PropertyDealer 
        (DealerID, Name, ContactInfo, ExperienceYears, Rating, License) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, dealers)
        return dealers

    def generate_real_estate(self, properties, num_estates=10):
        """Generate real estate records according to schema"""
        estates = []
        selected_properties = random.sample(properties, min(num_estates, len(properties)))
        
        for property_item in selected_properties:
            estate = (
                self.generate_unique_id(),
                round(self.fake.pydecimal(left_digits=10, right_digits=2, positive=True), 2),  # CurrentValue
                self.fake.text(max_nb_chars=100),  # PastValueTrends
                property_item[0]  # RelatedProperty foreign key
            )
            estates.append(estate)
        
        insert_query = """
        INSERT IGNORE INTO RealEstate 
        (RealEstateID, CurrentValue, PastValueTrends, RelatedProperty) 
        VALUES (%s, %s, %s, %s)
        """
        self.execute_many(insert_query, estates)
        return estates

    def generate_investors(self, num_investors=10):
        """Generate investor records according to schema"""
        investors = []
        
        for _ in range(num_investors):
            investor = (
                self.generate_unique_id(),
                self.fake.name(),
                random.randint(0, 10),  # RiskAssessment between 0-10
                random.choice(['Contractor', 'RealEstateInvestor', 'Both'])  # Match ENUM
            )
            investors.append(investor)
        
        insert_query = """
        INSERT IGNORE INTO Investor 
        (InvestorID, Name, RiskAssessment, InvestorType) 
        VALUES (%s, %s, %s, %s)
        """
        self.execute_many(insert_query, investors)
        return investors

    def generate_project_investments(self, projects, investors):
        """Generate project investment records according to schema"""
        if not projects or not investors:
            raise ValueError("Projects and investors lists cannot be empty")
            
        investments = []
        for project in projects:
            num_investors = random.randint(1, min(3, len(investors)))
            # selected_investors = random.sample(investors, num_investors)
            
            for _ in range(num_investors):
                investment = (
                    self.generate_unique_id(),
                    project[0],  # ProjectConcerned foreign key
                    round(self.fake.pydecimal(left_digits=9, right_digits=2, positive=True), 2),
                    self.fake.date_between(start_date='-2y', end_date='today'),
                    round(random.uniform(0.01, 99.99), 2),  # ProfitMargin
                    round(self.fake.pydecimal(left_digits=9, right_digits=2, positive=True), 2),
                    random.randint(0, 10)  # RiskLevel between 0-10
                )
                investments.append(investment)
        
        insert_query = """
        INSERT IGNORE INTO ProjectInvestments 
        (InvestmentID, ProjectConcerned, InvestedAmount, InvestmentDate, 
        ProfitMargin, ProjectedROI, RiskLevel) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, investments)
        return investments

    def generate_investments_in_project(self, project_investments, investors):
        """Generate many-to-many relationship between investments and investors"""
        investment_relations = []
        
        for investment in project_investments:
            # num_investors = random.randint(1, min(3, len(investors)))
            selected_investor = random.choice(investors)
            investment_relations.append((
                investment[0],  # InvestmentID
                selected_investor[0]     # InvestorID
            ))
        
        insert_query = """
        INSERT IGNORE INTO InvestmentsInProject 
        (InvestmentID, InvestorID) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, investment_relations)
        return investment_relations
    
    def generate_mentors(self, investors):
        """Generate mentor relationships between investors"""
        mentor_relationships = []
        
        for investor in investors:
            # Some investors will be mentors
            if random.random() < 0.3:  # 30% chance of being a mentor
                possible_mentees = [i for i in investors if i[0] != investor[0]]
                num_mentees = random.randint(1, max(25, len(possible_mentees)))
                
                for mentee in random.sample(possible_mentees, num_mentees):
                    mentor_relationships.append((
                        investor[0],  # InvestorID
                        mentee[0]     # MentorID
                    ))
        
        insert_query = """
        INSERT IGNORE INTO Mentors 
        (InvestorID, MentorID) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, mentor_relationships)
        return mentor_relationships

    def generate_property_amenities(self, properties):
        """Generate amenities for properties"""
        amenities = []
        amenity_types = [
            "Swimming Pool", "Gym", "Parking", "Security System",
            "Garden", "Elevator", "Smart Home Features", "Solar Panels",
            "Storage Space", "Playground"
        ]
        
        for property_item in properties:
            num_amenities = random.randint(2, 6)
            selected_amenities = random.sample(amenity_types, num_amenities)
            
            for amenity in selected_amenities:
                amenities.append((
                    property_item[0],  # PropertyID
                    amenity
                ))
        
        insert_query = """
        INSERT IGNORE INTO PropertyAmenities 
        (PropertyID, Amenity) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, amenities)
        return amenities

    def generate_reviews_of_firms(self, construction_firms):
        """Generate reviews for construction firms"""
        reviews = []
        
        for firm in construction_firms:
            num_reviews = random.randint(2, 5)
            for _ in range(num_reviews):
                review = (
                    firm[0],  # FirmID
                    self.fake.text(max_nb_chars=100)  # Reviews
                )
                reviews.append(review)
        
        insert_query = """
        INSERT IGNORE INTO ReviewsOfFirms 
        (FirmID, Reviews) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, reviews)
        return reviews
    
    def generate_payments_of_tenants(self, tenants):
        """Generate payment records for tenants"""
        payments = []
        
        for tenant in tenants:
            num_payments = random.randint(3, 12)
            for _ in range(num_payments):
                payment = (
                    tenant[0],  # TenantID
                    self.fake.date_between(start_date='-1y', end_date='today'),
                    f"Rent payment for {self.fake.month_name()}"
                )
                payments.append(payment)
        
        insert_query = """
        INSERT IGNORE INTO PaymentsOfTenants 
        (TenantID, PaymentDate, PaymentDescription) 
        VALUES (%s, %s, %s)
        """
        self.execute_many(insert_query, payments)
        return payments

    def generate_rental_relationship(self, tenants, properties):
        """Generate rental relationships between tenants and properties"""
        relationships = []
        available_properties = [p for p in properties if p[4] in ['Available', 'Rented']]
        
        for tenant in tenants:
            if available_properties:
                property_items = random.sample(available_properties, random.randint(1, min(20, len(properties))))

                for property_item in property_items:
                    relationships.append((
                        property_item[0],  # PropertyID
                        tenant[0]          # TenantID
                    ))
        
        insert_query = """
        INSERT IGNORE INTO RentalRelationship 
        (PropertyID, TenantID) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, relationships)
        return relationships
    
    def generate_preferences_of_investors(self, investors):
        """Generate preferences for investors"""
        preferences = []
        preference_types = [
            'High-Yield Properties', 'Commercial Real Estate',
            'Residential Development', 'Industrial Properties',
            'Mixed-Use Projects', 'Green Buildings',
            'Urban Development', 'Suburban Properties'
        ]
        
        for investor in investors:
            num_preferences = random.randint(2, 4)
            selected_preferences = random.sample(preference_types, num_preferences)
            for preference in selected_preferences:
                preferences.append((
                    investor[0],  # InvestorID
                    preference
                ))
        
        insert_query = """
        INSERT IGNORE INTO PreferencesOfInvestors 
        (InvestorID, Preferences) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, preferences)
        return preferences

    def generate_real_estate_investment(self, investors, projects):
        """Generate real estate investments"""
        investments = []
        
        for investor in investors:
            num_investments = random.randint(1, min(25, len(projects)))
            selected_projects = random.sample(projects, num_investments)
            
            for project in selected_projects:
                investment = (
                    self.generate_unique_id(),
                    investor[0],  # InvestorID
                    round(self.fake.pydecimal(left_digits=10, right_digits=2, positive=True), 2),
                    self.fake.date_between(start_date='-2y', end_date='today'),
                    round(random.uniform(0.01, 0.99), 2),  # Equity
                    project[0],  # ProjectConcerned
                    round(self.fake.pydecimal(left_digits=16, right_digits=2, positive=True), 2),
                    random.randint(0, 10)  # RiskLevel between 0-10
                )
                investments.append(investment)
        
        insert_query = """
        INSERT IGNORE INTO RealEstateInvestment 
        (InvestmentID, InvestorID, InvestedAmount, InvestmentDate, 
        Equity, ProjectConcerned, ProjectedROI, RiskLevel) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, investments)
        return investments
    
    def execute_many(self, query, data):
        """Execute multiple insert statements with error handling"""
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, data)
                self.connection.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise

    def generate_construction_firms(self, num_firms=5):
        """Generate construction firm records according to schema"""
        firms = []
        for _ in range(num_firms):
            firm = (
                self.generate_unique_id(),
                self.fake.company(),        # FirmName VARCHAR(255)
                self.fake.text(max_nb_chars=100),  # Portfolio TEXT
                round(random.uniform(1.0, 10.0), 2),  # Ratings DECIMAL(5,2)
                self.fake.text(max_nb_chars=100)  # License TEXT
            )
            firms.append(firm)
        
        insert_query = """
        INSERT IGNORE INTO ConstructionFirm 
        (FirmID, FirmName, Portfolio, Ratings, License) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, firms)
        return firms

    def generate_reviews_of_firms(self, construction_firms):
        """Generate reviews for construction firms"""
        reviews = []
        for firm in construction_firms:
            num_reviews = random.randint(2, 5)
            for _ in range(num_reviews):
                review = (
                    firm[0],  # FirmID
                    self.fake.text(max_nb_chars=200)  # Reviews TEXT
                )
                reviews.append(review)
        
        insert_query = """
        INSERT IGNORE INTO ReviewsOfFirms 
        (FirmID, Reviews) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, reviews)
        return reviews
    def generate_deals(self, properties, dealers, purchasers, construction_firms):
        """Generate deals between properties, dealers, purchasers and construction firms"""
        if not all([properties, dealers, purchasers, construction_firms]):
            raise ValueError("All entity lists must not be empty")
            
        deals = []
        for property_item in properties:
            random_purchasers = random.sample(purchasers, random.randint(1, min(25, len(purchasers))))
            for purchaser in random_purchasers :
                deal = (
                    property_item[0],  # PropertyID
                    random.choice(dealers)[0],  # DealerID
                    purchaser[0],  # PurchaserID
                    random.choice(construction_firms)[0]  # FirmID
                )
                deals.append(deal)
        
        insert_query = """
        INSERT IGNORE INTO DealtBy 
        (PropertyID, DealerID, PurchaserID, FirmID) 
        VALUES (%s, %s, %s, %s)
        """
        self.execute_many(insert_query, deals)
        return deals
    def generate_tenants(self, num_tenants=10):
        """Generate tenant records according to schema constraints"""
        tenants = []
        for _ in range(num_tenants):
            tenant = (
                self.generate_unique_id(),  # TenantID INT PRIMARY KEY
                self.fake.name(),          # Name VARCHAR(255)
                None                       # DependsOn INT (will be updated later)
            )
            tenants.append(tenant)
        
        # First insert all tenants
        insert_query = """
        INSERT IGNORE INTO Tenant 
        (TenantID, Name, DependsOn) 
        VALUES (%s, %s, %s)
        """
        self.execute_many(insert_query, tenants)
        
        # Update dependencies for some tenants
        dependent_tenants = random.sample(tenants, random.randint(1, len(tenants) // 4))
        updated_tenants = []
        for tenant in dependent_tenants:
            # Ensure we don't create circular dependencies
            possible_mentors = [t for t in tenants if t[0] != tenant[0]]
            if possible_mentors:
                depends_on = random.choice(possible_mentors)
                updated_tenants.append((depends_on[0], tenant[0]))
        
        if updated_tenants:
            update_query = """
            UPDATE Tenant 
            SET DependsOn = %s 
            WHERE TenantID = %s
            """
            self.execute_many(update_query, updated_tenants)
        
        return tenants
    def generate_tenantspreferences(self, tenants):
        """Generate preferences for tenants according to schema"""
        preferences = []
        preference_types = [
            "Pet-Friendly",
            "Close to Public Transport",
            "Quiet Neighborhood",
            "Modern Amenities",
            "Spacious",
            "Affordable",
            "Garden Access",
            "Security System"
        ]
        
        for tenant in tenants:
            num_preferences = random.randint(1, 5)
            selected_preferences = random.sample(preference_types, num_preferences)
            for pref in selected_preferences:
                preferences.append((
                    tenant[0],  # TenantID
                    pref       # Preference VARCHAR(255)
                ))
        
        insert_query = """
        INSERT IGNORE INTO TenantsPreferences 
        (TenantID, Preference) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, preferences)
        return preferences
    def generate_lesse_details(self, num_lesses=10):
        """Generate lesse details according to schema constraints"""
        lesses = []
        used_guarantor_contacts = set()
        
        for _ in range(num_lesses):
            # Generate unique guarantor contact
            while True:
                guarantor_contact = random.randint(1000000000, 9999999999)
                if guarantor_contact not in used_guarantor_contacts:
                    used_guarantor_contacts.add(guarantor_contact)
                    break
            
            lesse = (
                self.generate_unique_id(),  # LesseID INT PRIMARY KEY
                self.fake.name(),          # Name VARCHAR(255)
                self.fake.job(),           # Occupation VARCHAR(255)
                round(self.fake.pydecimal(left_digits=7, right_digits=2, positive=True), 2),  # AnnualIncome DECIMAL(18,2)
                random.choice(['RESIDENTIAL', 'COMMERCIAL']),  # LeasePurpose ENUM
                round(random.uniform(300, 850), 2),  # CreditScore DECIMAL(5,2)
                guarantor_contact          # GuarantorContact BIGINT UNIQUE
            )
            lesses.append(lesse)
        
        insert_query = """
        INSERT IGNORE INTO LesseDetails 
        (LesseID, Name, Occupation, AnnualIncome, LeasePurpose, 
        CreditScore, GuarantorContact) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, lesses)
        return lesses
    
    def generate_guarantors(self, lesses):
        """Generate guarantor records according to schema"""
        guarantors = []
        
        for lesse in lesses:
            guarantor = (
                lesse[6],        # GuarantorContact from lesse (PRIMARY KEY)
                self.fake.name() # GuarantorName VARCHAR(255)
            )
            guarantors.append(guarantor)
        
        insert_query = """
        INSERT IGNORE INTO Guarantors 
        (GuarantorContact, GuarantorName) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, guarantors)
        return guarantors
    
    def generate_lease(self, lesses, properties):
        """Generate lease records according to schema"""
        if not lesses or not properties:
            raise ValueError("Lesses and properties lists cannot be empty")
            
        leases = []
        for lesse in lesses:
            property_items = random.sample(properties,  random.randint(1, min(20, len(properties))))

            for property_item in property_items:
                lease_start = self.fake.date_between(start_date='-2y', end_date='today')
                lease_end = self.fake.date_between(start_date=lease_start, end_date='+2y')
                
                lease = (
                    self.generate_unique_id(),  # LeaseID INT PRIMARY KEY
                    lease_start,               # LeaseStartDate DATE
                    lease_end,                 # LeaseEndDate DATE
                    lesse[0],                  # LesseID INT FOREIGN KEY
                    property_item[0]           # PropertyID INT FOREIGN KEY
                )
                leases.append(lease)
        
        insert_query = """
        INSERT IGNORE INTO Lease 
        (LeaseID, LeaseStartDate, LeaseEndDate, LesseID, PropertyID) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.execute_many(insert_query, leases)
        return leases
    
    def generate_lease_terms(self, leases):
        """Generate lease terms according to schema"""
        lease_terms = []
        terms = [
            "Monthly Payment Required",
            "Security Deposit Required",
            "Pet Policy",
            "Maintenance Terms",
            "Utilities Included",
            "Parking Included",
            "Insurance Required",
            "Subletting Policy"
        ]
        
        for lease in leases:
            num_terms = random.randint(2, 5)
            selected_terms = random.sample(terms, num_terms)
            for term in selected_terms:
                lease_terms.append((
                    lease[0],  # LeaseID INT
                    term      # LeaseTerms VARCHAR(255)
                ))
        
        insert_query = """
        INSERT IGNORE INTO LeaseTerms 
        (LeaseID, LeaseTerms) 
        VALUES (%s, %s)
        """
        self.execute_many(insert_query, lease_terms)
        return lease_terms

    def populate_database(self):
        """Main method to orchestrate database population"""
        try:
            print("Starting database population...")
            # Data volume constants
            ENTRY_COUNT = 60  # Use 60 entries per table (adjust as needed)

            print("Generating marketing firms...")
            marketing_firms = self.generate_marketing_firms(ENTRY_COUNT)
            self.generate_services_of_marketing_firm(marketing_firms)

            print("Generating properties...")
            properties = self.generate_real_property(marketing_firms, ENTRY_COUNT)
            self.generate_property_amenities(properties)

            print("Generating construction firms...")
            construction_firms = self.generate_construction_firms(ENTRY_COUNT)
            self.generate_reviews_of_firms(construction_firms)

            print("Generating dealers and purchasers...")
            property_dealers = self.generate_property_dealers(ENTRY_COUNT)
            purchasers = self.generate_purchaser(ENTRY_COUNT)

            print("Generating lesse details...")
            lesses = self.generate_lesse_details(ENTRY_COUNT)

            print("Generating real estate...")
            self.generate_real_estate(properties, ENTRY_COUNT)

            print("Generating investors...")
            investors = self.generate_investors(ENTRY_COUNT)
            self.generate_mentors(investors)
            self.generate_preferences_of_investors(investors)

            print("Generating projects...")
            projects = self.generate_projects(construction_firms, properties, ENTRY_COUNT)
            project_investments = self.generate_project_investments(projects, investors)
            self.generate_investments_in_project(project_investments, investors)
            self.generate_real_estate_investment(investors, projects)

            print("Generating deals...")
            deals = self.generate_deals(properties, property_dealers, purchasers, construction_firms)

            print("Generating tenants...")
            tenants = self.generate_tenants(ENTRY_COUNT)
            self.generate_tenantspreferences(tenants)
            self.generate_payments_of_tenants(tenants)
            self.generate_rental_relationship(tenants, properties)

            print("Generating leases...")
            leases = self.generate_lease(lesses, properties)
            self.generate_lease_terms(leases)
            self.generate_guarantors(lesses)

            print("Database successfully populated!")
        except Exception as e:
            print(f"An error occurred during database population: {e}")
            raise

    def get_existing_ids(self, table_name, id_column):
        """Get existing IDs from a table"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT {id_column} FROM {table_name}")
                results = cursor.fetchall()
                return [row[id_column] for row in results]
        except Exception as e:
            print(f"Error getting existing IDs from {table_name}: {e}")
            return []

    def bulk_insert(self, table_name, data_list, columns):
        """Bulk insert data into a table"""
        if not data_list:
            return
        
        try:
            with self.connection.cursor() as cursor:
                # Create placeholders for the query
                placeholders = ', '.join(['%s'] * len(columns))
                column_names = ', '.join(columns)
                query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
                
                # Prepare data for bulk insert
                values = []
                for item in data_list:
                    row_values = []
                    for col in columns:
                        # Convert column name to match data keys (handle case differences)
                        key = col.lower().replace('_', '')
                        for data_key in item.keys():
                            if data_key.lower().replace('_', '') == key:
                                row_values.append(item[data_key])
                                break
                        else:
                            row_values.append(None)
                    values.append(tuple(row_values))
                
                cursor.executemany(query, values)
                self.connection.commit()
                print(f"Successfully inserted {len(data_list)} records into {table_name}")
        except Exception as e:
            print(f"Error bulk inserting into {table_name}: {e}")
            self.connection.rollback()

    def generate_users(self, num_users=20):
        """Generate users for authentication"""
        users_data = []
        user_types = ['admin', 'dealer', 'user']
        
        # Create at least one admin
        admin_data = {
            'email': 'admin@realestate.com',
            'password': 'admin123',  # In real app, this should be hashed
            'user_type': 'admin',
            'name': 'System Administrator',
            'contact_info': self.generate_unique_contact()
        }
        users_data.append(admin_data)
        
        for i in range(num_users - 1):
            user_data = {
                'email': self.fake.email(),
                'password': 'password123',  # In real app, this should be hashed
                'user_type': random.choice(user_types),
                'name': self.fake.name(),
                'contact_info': self.generate_unique_contact()
            }
            users_data.append(user_data)
        
        self.bulk_insert('Users', users_data, 
                        ['Email', 'Password', 'UserType', 'Name', 'ContactInfo'])
        return len(users_data)

    def generate_transactions(self, num_transactions=50):
        """Generate transaction records"""
        property_ids = self.get_existing_ids('RealProperty', 'PropertyID')
        user_ids = self.get_existing_ids('Users', 'UserID')
        
        if not property_ids or not user_ids:
            print("No properties or users found for transactions")
            return 0
        
        transactions_data = []
        transaction_types = ['purchase', 'sale', 'lease_payment', 'investment']
        statuses = ['pending', 'completed', 'failed']
        
        for i in range(num_transactions):
            transaction_data = {
                'property_id': random.choice(property_ids),
                'user_id': random.choice(user_ids),
                'transaction_type': random.choice(transaction_types),
                'amount': round(random.uniform(1000, 100000), 2),
                'description': self.fake.text(max_nb_chars=200),
                'status': random.choice(statuses)
            }
            transactions_data.append(transaction_data)
        
        self.bulk_insert('Transactions', transactions_data,
                        ['PropertyID', 'UserID', 'TransactionType', 'Amount', 'Description', 'Status'])
        return len(transactions_data)

    def generate_tenant_applications(self, num_applications=30):
        """Generate tenant applications"""
        user_ids = self.get_existing_ids('Users', 'UserID')
        property_ids = self.get_existing_ids('RealProperty', 'PropertyID')
        
        if not user_ids or not property_ids:
            print("No users or properties found for tenant applications")
            return 0
        
        applications_data = []
        statuses = ['pending', 'approved', 'rejected']
        lease_purposes = ['RESIDENTIAL', 'COMMERCIAL']
        
        for i in range(num_applications):
            application_data = {
                'user_id': random.choice(user_ids),
                'property_id': random.choice(property_ids),
                'status': random.choice(statuses),
                'credit_score': round(random.uniform(300, 850), 2),
                'annual_income': round(random.uniform(30000, 200000), 2),
                'lease_purpose': random.choice(lease_purposes),
                'message': self.fake.text(max_nb_chars=500)
            }
            applications_data.append(application_data)
        
        self.bulk_insert('TenantApplications', applications_data,
                        ['UserID', 'PropertyID', 'Status', 'CreditScore', 'AnnualIncome', 'LeasePurpose', 'Message'])
        return len(applications_data)

    def generate_investor_applications(self, num_applications=25):
        """Generate investor applications"""
        user_ids = self.get_existing_ids('Users', 'UserID')
        project_ids = self.get_existing_ids('Project', 'ProjectID')
        
        if not user_ids or not project_ids:
            print("No users or projects found for investor applications")
            return 0
        
        applications_data = []
        statuses = ['pending', 'approved', 'rejected']
        investor_types = ['Contractor', 'RealEstateInvestor', 'Both']
        
        for i in range(num_applications):
            application_data = {
                'user_id': random.choice(user_ids),
                'project_id': random.choice(project_ids),
                'status': random.choice(statuses),
                'proposed_amount': round(random.uniform(10000, 1000000), 2),
                'risk_assessment': random.randint(1, 10),
                'investor_type': random.choice(investor_types),
                'message': self.fake.text(max_nb_chars=500)
            }
            applications_data.append(application_data)
        
        self.bulk_insert('InvestorApplications', applications_data,
                        ['UserID', 'ProjectID', 'Status', 'ProposedAmount', 'RiskAssessment', 'InvestorType', 'Message'])
        return len(applications_data)

    def generate_payment_history(self, num_payments=40):
        """Generate payment history records"""
        tenant_ids = self.get_existing_ids('Tenant', 'TenantID')
        property_ids = self.get_existing_ids('RealProperty', 'PropertyID')
        
        if not tenant_ids or not property_ids:
            print("No tenants or properties found for payment history")
            return 0
        
        payments_data = []
        payment_types = ['rent', 'security_deposit', 'maintenance', 'other']
        statuses = ['paid', 'pending', 'overdue']
        
        for i in range(num_payments):
            payment_data = {
                'tenant_id': random.choice(tenant_ids),
                'property_id': random.choice(property_ids),
                'amount': round(random.uniform(500, 5000), 2),
                'payment_date': self.fake.date_between(start_date='-1y', end_date='today'),
                'payment_type': random.choice(payment_types),
                'status': random.choice(statuses),
                'description': self.fake.text(max_nb_chars=200)
            }
            payments_data.append(payment_data)
        
        self.bulk_insert('PaymentHistory', payments_data,
                        ['TenantID', 'PropertyID', 'Amount', 'PaymentDate', 'PaymentType', 'Status', 'Description'])
        return len(payments_data)

    def close_connection(self):
        """Close database connection"""
        try:
            self.connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

    
if __name__ == "__main__":
    try:
        # Initialize database populator
        populator = ComprehensiveRealEstatePopulator(**DB_CONFIG)
        # Populate database
        populator.populate_database()
        print("Database population completed successfully!")
    except Exception as e:
        print(f"Error during database population: {e}")
    finally:
        # Ensure connection is closed
        if 'populator' in locals():
            populator.close_connection()


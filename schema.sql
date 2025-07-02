-- 1. MarketingFirm
CREATE TABLE MarketingFirm (
    MarketFirmID INT PRIMARY KEY,
    Name VARCHAR(255),
    Location VARCHAR(255) UNIQUE,
    FoundedYear YEAR,
    ContactInfo BIGINT UNIQUE,
    Specialization VARCHAR(255),
    ReputationRating INT CHECK (ReputationRating BETWEEN 0 AND 10),
    NumberOfClients INT,
    AnnualRevenue DECIMAL(18, 2)
);

-- 2. RealProperty
-- marketed by one marketing firm only.
CREATE TABLE RealProperty (
    PropertyID INT PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT,
    Price DECIMAL(18, 2),
    Status ENUM('Available', 'Sold', 'Rented', 'Marked for Demolition'),
    PropertyType ENUM('Residential', 'Commercial', 'Intellectual'),
    MaintenanceHistory TEXT,
    MarketFirmID INT,
    Address_StreetNo VARCHAR(255),
    Address_StreetName VARCHAR(255),
    Address_BuildingNo INT,
    Address_City VARCHAR(255),
    Address_Zipcode INT,
    FOREIGN KEY (MarketFirmID) REFERENCES MarketingFirm(MarketFirmID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 3. Tenant
CREATE TABLE Tenant (
    TenantID INT PRIMARY KEY,
    Name VARCHAR(255),
    DependsOn INT,
    FOREIGN KEY (DependsOn) REFERENCES Tenant(TenantID) ON DELETE SET NULL ON UPDATE CASCADE
);

-- 4. LesseDetails
CREATE TABLE LesseDetails (
    LesseID INT PRIMARY KEY,
    Name VARCHAR(255),
    Occupation VARCHAR(255),
    AnnualIncome DECIMAL(18, 2),
    LeasePurpose ENUM('RESIDENTIAL', 'COMMERCIAL'),
    CreditScore DECIMAL(5, 2),
    GuarantorContact BIGINT UNIQUE
);

-- 5. Purchaser
CREATE TABLE Purchaser (
    PurchaserID INT PRIMARY KEY,
    Name VARCHAR(255),
    ContactInfo BIGINT UNIQUE,
    DateOfPurchase DATE,
    PaymentMethod VARCHAR(255),
    AmountPayed DECIMAL(18, 2),
    Purpose VARCHAR(255),
    Equity DECIMAL(3, 2),
    DateOfSell DATE,
    Address_StreetNo VARCHAR(255),
    Address_StreetName VARCHAR(255),
    Address_BuildingNo INT,
    Address_City VARCHAR(255),
    Address_Zipcode INT
);

-- 6. PropertyDealer
CREATE TABLE PropertyDealer (
    DealerID INT PRIMARY KEY,
    Name VARCHAR(255),
    ContactInfo BIGINT UNIQUE,
    ExperienceYears INT,
    Rating DECIMAL(5, 2),
    License TEXT
);

-- 7. ConstructionFirm
CREATE TABLE ConstructionFirm (
    FirmID INT PRIMARY KEY,
    FirmName VARCHAR(255),
    Portfolio TEXT,
    Ratings DECIMAL(5, 2),
    License TEXT
);

-- 8. Project
CREATE TABLE Project (
    ProjectID INT PRIMARY KEY,
    ProjectName VARCHAR(255),
    Status ENUM('Completed', 'Ongoing'),
    EstimatedCost DECIMAL(18, 2),
    ParentProject INT,
    FirmID INT,
    PropertyID INT,
    FOREIGN KEY (ParentProject) REFERENCES Project(ProjectID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FirmID) REFERENCES ConstructionFirm(FirmID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 9. RealEstate...
CREATE TABLE RealEstate (
    RealEstateID INT PRIMARY KEY,
    CurrentValue DECIMAL(18, 2),
    PastValueTrends TEXT,
    RelatedProperty INT,
    FOREIGN KEY (RelatedProperty) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 10. Investor..
CREATE TABLE Investor (
    InvestorID INT PRIMARY KEY,
    Name VARCHAR(255),
    RiskAssessment INT CHECK (RiskAssessment BETWEEN 0 AND 10),
    InvestorType ENUM('Contractor', 'RealEstateInvestor', 'Both')
);

-- 11. ProjectInvestments,,,
CREATE TABLE ProjectInvestments (
    InvestmentID INT PRIMARY KEY,
    ProjectConcerned INT,
    InvestedAmount DECIMAL(18, 2),
    InvestmentDate DATE,
    ProfitMargin DECIMAL(5, 2),
    ProjectedROI DECIMAL(18, 2),
    RiskLevel INT CHECK (RiskLevel BETWEEN 0 AND 10),
    FOREIGN KEY (ProjectConcerned) REFERENCES Project(ProjectID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 12. Lease .. 
CREATE TABLE Lease (
    LeaseID INT PRIMARY KEY,
    LeaseStartDate DATE,
    LeaseEndDate DATE,
    LesseID INT,
    PropertyID INT,
    FOREIGN KEY (LesseID) REFERENCES LesseDetails(LesseID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 13. Guarantors ... (one guarantor per lesse)
CREATE TABLE Guarantors (
    GuarantorContact BIGINT PRIMARY KEY,
    GuarantorName VARCHAR(255),
    FOREIGN KEY (GuarantorContact) REFERENCES LesseDetails(GuarantorContact) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 14. ServicesOfMarketingFirm ...
CREATE TABLE ServicesOfMarketingFirm (
    MarketFirmID INT,
    ServicesOffered VARCHAR(255),
    PRIMARY KEY (MarketFirmID, ServicesOffered),
    FOREIGN KEY (MarketFirmID) REFERENCES MarketingFirm(MarketFirmID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 15. RentalRelationship...
CREATE TABLE RentalRelationship (
    PropertyID INT,
    TenantID INT,
    PRIMARY KEY (PropertyID, TenantID),
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TenantID) REFERENCES Tenant(TenantID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 16. PaymentsOfTenants..
CREATE TABLE PaymentsOfTenants (
    TenantID INT,
    PaymentDate DATE,
    PaymentDescription VARCHAR(255),
    PRIMARY KEY (TenantID, PaymentDate),
    FOREIGN KEY (TenantID) REFERENCES Tenant(TenantID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 17. TenantsPreferences..
CREATE TABLE TenantsPreferences (
    TenantID INT,
    Preference VARCHAR(255),
    PRIMARY KEY (TenantID, Preference),
    FOREIGN KEY (TenantID) REFERENCES Tenant(TenantID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 18. LeaseTerms,...
CREATE TABLE LeaseTerms (
    LeaseID INT,
    LeaseTerms VARCHAR(255),
    PRIMARY KEY (LeaseID, LeaseTerms),
    FOREIGN KEY (LeaseID) REFERENCES Lease(LeaseID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 19. PropertyAmenities....
CREATE TABLE PropertyAmenities (
    PropertyID INT,
    Amenity VARCHAR(255),
    PRIMARY KEY (PropertyID, Amenity),
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 20. DealtBy
CREATE TABLE DealtBy (
    PropertyID INT,
    DealerID INT,
    PurchaserID INT,
    FirmID INT,
    PRIMARY KEY (PropertyID, DealerID, PurchaserID, FirmID),
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (FirmID) REFERENCES ConstructionFirm(FirmID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DealerID) REFERENCES PropertyDealer(DealerID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (PurchaserID) REFERENCES Purchaser(PurchaserID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 21. ReviewsOfFirms..
CREATE TABLE ReviewsOfFirms (
    FirmID INT,
    Reviews TEXT,
    PRIMARY KEY (FirmID, Reviews(255)),
    FOREIGN KEY (FirmID) REFERENCES ConstructionFirm(FirmID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 22. PreferencesOfInvestors..
CREATE TABLE PreferencesOfInvestors (
    InvestorID INT,
    Preferences VARCHAR(255),
    PRIMARY KEY (InvestorID, Preferences),
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 23. Mentors...
CREATE TABLE Mentors (
    InvestorID INT,
    MentorID INT,
    PRIMARY KEY (InvestorID, MentorID),
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MentorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 24. RealEstateInvestment...
CREATE TABLE RealEstateInvestment (
    InvestmentID INT PRIMARY KEY,
    InvestorID INT,
    InvestedAmount DECIMAL(18, 2),
    InvestmentDate DATE,
    Equity DECIMAL(5, 2),
    ProjectConcerned INT,
    ProjectedROI DECIMAL(18, 2),
    RiskLevel INT CHECK (RiskLevel BETWEEN 0 AND 10),
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (ProjectConcerned) REFERENCES Project(ProjectID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 25. InvestmentsInProject ....
CREATE TABLE InvestmentsInProject ( 
    InvestmentID INT,
    InvestorID INT,
    PRIMARY KEY (InvestmentID, InvestorID),
    FOREIGN KEY (InvestmentID) REFERENCES ProjectInvestments(InvestmentID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 26. Users table for authentication
CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    UserType ENUM('admin', 'dealer', 'user') NOT NULL,
    Name VARCHAR(255),
    ContactInfo BIGINT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IsActive BOOLEAN DEFAULT TRUE
);

-- 27. UserSessions for session management
CREATE TABLE UserSessions (
    SessionID VARCHAR(255) PRIMARY KEY,
    UserID INT NOT NULL,
    ExpiresAt TIMESTAMP NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- 28. UserProfiles for additional user information
CREATE TABLE UserProfiles (
    ProfileID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT UNIQUE NOT NULL,
    DealerID INT NULL,
    PurchaserID INT NULL,
    InvestorID INT NULL,
    TenantID INT NULL,
    Mode ENUM('purchaser', 'investor') DEFAULT 'purchaser',
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (DealerID) REFERENCES PropertyDealer(DealerID) ON DELETE SET NULL,
    FOREIGN KEY (PurchaserID) REFERENCES Purchaser(PurchaserID) ON DELETE SET NULL,
    FOREIGN KEY (InvestorID) REFERENCES Investor(InvestorID) ON DELETE SET NULL,
    FOREIGN KEY (TenantID) REFERENCES Tenant(TenantID) ON DELETE SET NULL
);

-- 29. Transactions table for tracking all financial transactions
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    PropertyID INT,
    UserID INT,
    TransactionType ENUM('purchase', 'sale', 'lease_payment', 'investment') NOT NULL,
    Amount DECIMAL(18, 2) NOT NULL,
    TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Description TEXT,
    Status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE SET NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE SET NULL
);

-- 30. TenantApplications for tenant application process
CREATE TABLE TenantApplications (
    ApplicationID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    PropertyID INT NOT NULL,
    ApplicationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    CreditScore DECIMAL(5, 2),
    AnnualIncome DECIMAL(18, 2),
    LeasePurpose ENUM('RESIDENTIAL', 'COMMERCIAL'),
    Message TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE
);

-- 31. InvestorApplications for investor application process
CREATE TABLE InvestorApplications (
    ApplicationID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT NOT NULL,
    ProjectID INT NOT NULL,
    ApplicationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    ProposedAmount DECIMAL(18, 2) NOT NULL,
    RiskAssessment INT CHECK (RiskAssessment BETWEEN 0 AND 10),
    InvestorType ENUM('Contractor', 'RealEstateInvestor', 'Both'),
    Message TEXT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID) ON DELETE CASCADE
);

-- 32. PaymentHistory for tracking payment records
CREATE TABLE PaymentHistory (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    TenantID INT,
    PropertyID INT,
    Amount DECIMAL(18, 2) NOT NULL,
    PaymentDate DATE NOT NULL,
    PaymentType ENUM('rent', 'security_deposit', 'maintenance', 'other') NOT NULL,
    Status ENUM('paid', 'pending', 'overdue') DEFAULT 'pending',
    Description TEXT,
    FOREIGN KEY (TenantID) REFERENCES Tenant(TenantID) ON DELETE CASCADE,
    FOREIGN KEY (PropertyID) REFERENCES RealProperty(PropertyID) ON DELETE CASCADE
);

# queries.py - Modular query functions for RealEstateDB CLI

def SELECT(query_type, *args):
    if query_type == 'all_investors':
        return ("SELECT InvestorID, Name, InvestorType, RiskAssessment FROM Investor;", None)
    elif query_type == 'all_tenants':
        return ("SELECT TenantID, Name, Preferences FROM Tenant;", None)
    elif query_type == 'properties_for_sale':
        return ("SELECT PropertyID, Name, Status FROM RealProperty WHERE Status = 'Available';", None)
    elif query_type == 'property_dealers':
        return ("SELECT DealerID, Name, ContactInfo FROM PropertyDealer;", None)
    return (None, None)

def PROJECT(query_type, *args):
    if query_type == 'investors_multicity':
        return ("""
        SELECT Investor.InvestorID, Investor.Name, SUM(ProjectInvestments.InvestedAmount) AS TotalInvestment, GROUP_CONCAT(DISTINCT RealProperty.Address_City) AS CitiesInvolved
        FROM Investor JOIN InvestmentsInProject ON Investor.InvestorID = InvestmentsInProject.InvestorID
        JOIN ProjectInvestments ON InvestmentsInProject.InvestmentID = ProjectInvestments.InvestmentID
        JOIN Project ON ProjectInvestments.ProjectConcerned = Project.ProjectID
        JOIN RealProperty ON Project.PropertyID = RealProperty.PropertyID
        GROUP BY Investor.InvestorID, Investor.Name
        HAVING COUNT(DISTINCT RealProperty.Address_City) > 1;
        """, None)
    elif query_type == 'ongoing_projects':
        return ("SELECT ProjectName, EstimatedCost FROM Project WHERE Status = 'Ongoing' AND FirmID = %s;", (args[0],))
    elif query_type == 'top_expensive_properties':
        return ("SELECT PropertyID, Name, Price FROM RealProperty ORDER BY Price DESC LIMIT 5;", None)
    return (None, None)

def AGGREGATE(query_type, *args):
    if query_type == 'avg_revenue_high_reputation':
        return ("SELECT AVG(AnnualRevenue) AS AvgRevenue FROM MarketingFirm WHERE ReputationRating >= 8;", None)
    elif query_type == 'investment_stats_last_year':
        return ("""
        SELECT I.InvestorID, SUM(PI.InvestedAmount) AS TotalInvestment, AVG(PI.ProjectedROI) AS AvgROI
        FROM Investor I JOIN InvestmentsInProject IP ON I.InvestorID = IP.InvestorID JOIN ProjectInvestments PI ON IP.InvestmentID = PI.InvestmentID
        WHERE I.InvestorType = 'RealEstateInvestor' AND PI.InvestmentDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY I.InvestorID, I.Name;
        """, None)
    elif query_type == 'project_roi_by_contractor_type':
        return ("""
        SELECT Project.ProjectName, Investor.InvestorType, AVG(ProjectInvestments.RiskLevel) AS AvgRiskLevel, AVG(ProjectInvestments.ProjectedROI) AS AvgProjectedROI
        FROM Project JOIN ProjectInvestments ON Project.ProjectID = ProjectInvestments.ProjectConcerned
        JOIN InvestmentsInProject IP ON ProjectInvestments.InvestmentID = IP.InvestmentID JOIN Investor ON Investor.InvestorID = IP.InvestorID
        GROUP BY Project.ProjectName, Investor.InvestorType LIMIT 1000;
        """, None)
    elif query_type == 'total_properties':
        return ("SELECT COUNT(*) AS TotalProperties FROM RealProperty;", None)
    elif query_type == 'avg_credit_score_tenants':
        return ("SELECT AVG(CreditScore) AS AvgCreditScore FROM LesseDetails;", None)
    return (None, None)

def SEARCH(query_type, *args):
    if query_type == 'properties_by_keyword':
        return ("SELECT PropertyID, Name FROM RealProperty WHERE Name LIKE %s LIMIT 1000;", ('%' + args[0] + '%',))
    elif query_type == 'properties_by_amenities_and_price':
        return ("""
        SELECT DISTINCT RealProperty.PropertyID, RealProperty.Name, RealProperty.Address_City, GROUP_CONCAT(DISTINCT PA.Amenity) AS Amenities
        FROM RealProperty JOIN PropertyAmenities PA ON PA.PropertyID = RealProperty.PropertyID
        WHERE (Price BETWEEN %s AND %s) AND (PA.Amenity IN %s)
        GROUP BY RealProperty.PropertyID;
        """, (args[0], args[1], args[2]))
    elif query_type == 'marketing_firms_by_specialization':
        return ("SELECT * FROM MarketingFirm WHERE Specialization IN (%s);", (args[0],))
    return (None, None)

def ANALYSIS(query_type, *args):
    if query_type == 'high_roi_investors_in_top_firms':
        return ("""
        SELECT ConstructionFirm.FirmID, COUNT(DISTINCT Investor.InvestorID) AS NumHighROIInvestors
        FROM Investor JOIN InvestmentsInProject IP ON Investor.InvestorID = IP.InvestorID
        JOIN ProjectInvestments PI ON PI.InvestmentID = IP.InvestmentID 
        JOIN Project ON PI.ProjectConcerned = Project.ProjectID
        JOIN ConstructionFirm ON Project.FirmID = ConstructionFirm.FirmID
        WHERE ProjectedROI > 10 AND ConstructionFirm.Ratings >= 9
        GROUP BY ConstructionFirm.FirmID;
        """, None)
    elif query_type == 'most_active_investor':
        return ("SELECT InvestorID, Name FROM Investor ORDER BY RiskAssessment DESC LIMIT 1;", None)
    elif query_type == 'city_with_most_properties':
        return ("SELECT Address_City, COUNT(*) AS NumProperties FROM RealProperty GROUP BY Address_City ORDER BY NumProperties DESC LIMIT 1;", None)
    elif query_type == 'firm_with_most_projects':
        return ("SELECT FirmID, COUNT(*) AS NumProjects FROM Project GROUP BY FirmID ORDER BY NumProjects DESC LIMIT 1;", None)
    elif query_type == 'most_expensive_property':
        return ("SELECT PropertyID, Name, Price FROM RealProperty ORDER BY Price DESC LIMIT 1;", None)
    elif query_type == 'tenant_with_highest_credit':
        return ("SELECT TenantID, Name, CreditScore FROM LesseDetails ORDER BY CreditScore DESC LIMIT 1;", None)
    elif query_type == 'investment_roi_trends':
        return ("""
        SELECT YEAR(PI.InvestmentDate) AS Year, 
               AVG(PI.ProjectedROI) AS AvgROI, 
               SUM(PI.InvestedAmount) AS TotalInvestment
        FROM ProjectInvestments PI
        GROUP BY YEAR(PI.InvestmentDate)
        ORDER BY Year;
        """, None)
    elif query_type == 'property_value_by_amenities':
        return ("""
        SELECT PA.Amenity, 
               AVG(RP.Price) AS AvgPropertyValue, 
               COUNT(DISTINCT RP.PropertyID) AS PropertyCount
        FROM PropertyAmenities PA
        JOIN RealProperty RP ON PA.PropertyID = RP.PropertyID
        GROUP BY PA.Amenity
        ORDER BY AvgPropertyValue DESC;
        """, None)
    elif query_type == 'investment_success_by_firm_rating':
        return ("""
        SELECT CF.Ratings AS FirmRating,
               AVG(PI.ProjectedROI) AS AvgROI,
               COUNT(DISTINCT P.ProjectID) AS NumProjects,
               SUM(PI.InvestedAmount) AS TotalInvestment
        FROM ConstructionFirm CF
        JOIN Project P ON CF.FirmID = P.FirmID
        JOIN ProjectInvestments PI ON P.ProjectID = PI.ProjectConcerned
        GROUP BY CF.Ratings
        ORDER BY CF.Ratings DESC;
        """, None)
    elif query_type == 'marketing_impact_analysis':
        return ("""
        SELECT MF.Specialization,
               AVG(MF.ReputationRating) AS AvgReputation,
               AVG(RP.Price) AS AvgPropertyPrice,
               AVG(DATEDIFF(L.EndDate, L.StartDate))/30 AS AvgLeaseMonths
        FROM MarketingFirm MF
        JOIN RealProperty RP ON MF.MarketFirmID = RP.MarketingFirmID
        LEFT JOIN Lease L ON RP.PropertyID = L.PropertyID
        GROUP BY MF.Specialization
        ORDER BY AvgPropertyPrice DESC;
        """, None)
    elif query_type == 'investor_property_type_preference':
        return ("""
        SELECT I.InvestorType,
               RP.PropertyType,
               COUNT(DISTINCT P.ProjectID) AS ProjectCount,
               SUM(PI.InvestedAmount) AS TotalInvestment,
               AVG(PI.ProjectedROI) AS AvgROI
        FROM Investor I
        JOIN InvestmentsInProject IIP ON I.InvestorID = IIP.InvestorID
        JOIN ProjectInvestments PI ON IIP.InvestmentID = PI.InvestmentID
        JOIN Project P ON PI.ProjectConcerned = P.ProjectID
        JOIN RealProperty RP ON P.PropertyID = RP.PropertyID
        GROUP BY I.InvestorType, RP.PropertyType
        ORDER BY TotalInvestment DESC;
        """, None)
    elif query_type == 'city_investment_analysis':
        return ("""
        SELECT RP.Address_City AS City,
               COUNT(DISTINCT RP.PropertyID) AS PropertyCount,
               AVG(RP.Price) AS AvgPropertyValue,
               SUM(PI.InvestedAmount) AS TotalInvestment,
               SUM(PI.InvestedAmount)/COUNT(DISTINCT RP.PropertyID) AS InvestmentPerProperty
        FROM RealProperty RP
        JOIN Project P ON RP.PropertyID = P.PropertyID
        JOIN ProjectInvestments PI ON P.ProjectID = PI.ProjectConcerned
        GROUP BY RP.Address_City
        ORDER BY TotalInvestment DESC;
        """, None)
    return (None, None)

def INSERT(query_type, *args):
    if query_type == 'project_investment':
        return ("""
        INSERT INTO ProjectInvestments (InvestmentID, InvestedAmount, ProjectConcerned, InvestmentDate, ProfitMargin, ProjectedROI, RiskLevel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, args)
    elif query_type == 'new_tenant':
        return ("INSERT INTO Tenant (TenantID, Name, Preferences, PaymentHistory) VALUES (%s, %s, %s, %s);", args)
    elif query_type == 'property':
        return ("INSERT INTO RealProperty (PropertyID, Name, Description, Price, Status, PropertyType, Amenities, DeveloperFirmID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", args)
    return (None, None)

def UPDATE(query_type, *args):
    if query_type == 'projected_roi':
        return ("UPDATE ProjectInvestments SET ProjectedROI = ProjectedROI * 1.05 WHERE ProjectConcerned IN (SELECT ProjectID FROM Project WHERE Status = 'Ongoing');", None)
    elif query_type == 'marketing_firm_reputation':
        return ("UPDATE MarketingFirm SET ReputationRating = ReputationRating + 1 WHERE NumberOfClients > 100 AND FoundedYear >= '2023-01-01';", None)
    elif query_type == 'specific_marketing_firm_reputation':
        return ("UPDATE MarketingFirm SET ReputationRating = %s WHERE MarketFirmID = %s;", (args[0], args[1]))
    return (None, None)

def DELETE(query_type, *args):
    if query_type == 'tenants_with_poor_payment_history':
        return ("""
        DELETE FROM Tenant WHERE TenantID IN (SELECT TenantID FROM PaymentHistory GROUP BY TenantID HAVING COUNT(*) < 5);
        """, None)
    elif query_type == 'properties_for_demolition':
        return ("DELETE FROM RealProperty WHERE Status = 'Marked for Demolition';", None)
    elif query_type == 'high_risk_investments':
        return ("DELETE FROM ProjectInvestments WHERE RiskLevel > 9;", None)
    return (None, None)

# CLI command to query mapping
def get_query(category, query_type, *args):
    if category == 'select':
        return SELECT(query_type, *args)
    elif category == 'project':
        return PROJECT(query_type, *args)
    elif category == 'aggregate':
        return AGGREGATE(query_type, *args)
    elif category == 'search':
        return SEARCH(query_type, *args)
    elif category == 'analysis':
        return ANALYSIS(query_type, *args)
    elif category == 'insert':
        return INSERT(query_type, *args)
    elif category == 'update':
        return UPDATE(query_type, *args)
    elif category == 'delete':
        return DELETE(query_type, *args)
    else:
        return (None, None)

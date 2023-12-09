import mysql.connector as connector
import pandas as pd

global con, cur
con = connector.connect(host='localhost', port='3306', user='root', password='root', database='hoteldatabase')
cur = con.cursor()


def createTables():
    queries = [
     """CREATE TABLE mps_users (
            user_id  DOUBLE NOT NULL COMMENT 'Users ID Number',
            username VARCHAR(30) NOT NULL COMMENT 'Username of the Customer',
            password VARCHAR(30) NOT NULL COMMENT 'Password of the Customers'
        )""",
        
        """ALTER TABLE mps_users ADD CONSTRAINT mps_users_pk PRIMARY KEY ( user_id )""",
        """ALTER TABLE MPS_USERS MODIFY COLUMN USER_ID DOUBLE NOT NULL UNIQUE AUTO_INCREMENT FIRST""",
        
        """CREATE TABLE mps_customer (
            cust_id           INT NOT NULL COMMENT 'Customer ID Number',
            cust_addr_street  VARCHAR(30) NOT NULL COMMENT 'Street Address of the Customer',
            cust_addr_city    VARCHAR(30) NOT NULL COMMENT 'City Address of the Customer',
            cust_addr_state   VARCHAR(30) NOT NULL COMMENT 'State Address of the Customer',
            cust_addr_country VARCHAR(30) NOT NULL COMMENT 'Customer''s Country Address',
            cust_addr_zipcode VARCHAR(10) NOT NULL COMMENT 'Zipcode of the Customer',
            cust_email        VARCHAR(75) NOT NULL COMMENT 'Email Address of the Customer',
            cust_phone_no     VARCHAR(14) NOT NULL COMMENT 'Phone Numbe rof the Customer',
            cust_type         VARCHAR(1) NOT NULL COMMENT 'Type of the Customer i.e., Individual or Corporate',
            user_id           DOUBLE NOT NULL
        )"""
        
        """ALTER TABLE mps_customer ADD CONSTRAINT ch_inh_mps_customer CHECK ( cust_type IN ( 'C', 'I' ) )""",
        """CREATE UNIQUE INDEX mps_customer__idx ON mps_customer (user_id ASC )""",
        """ALTER TABLE mps_customer ADD CONSTRAINT mps_customer_pk PRIMARY KEY ( cust_id )""",
        """ALTER TABLE MPS_CUSTOMER MODIFY COLUMN CUST_ID INT NOT NULL UNIQUE AUTO_INCREMENT FIRST""",
        """ALTER TABLE mps_customer ADD CONSTRAINT mps_customer_mps_users_fk FOREIGN KEY ( user_id )""",
        """REFERENCES mps_users ( user_id )""",
        
        """CREATE TABLE mps_corp_disc (
            discount_id            INT NOT NULL COMMENT 'Discount ID Number',
            discount_fixed_percent DECIMAL(7, 2) NOT NULL COMMENT 'Fixed Corprate Discount for Corporate Companies',
            affl_company           VARCHAR(30) NOT NULL COMMENT 'Discounts for Affliliated Companies'
        )""",
        
        """ALTER TABLE mps_corp_disc ADD CONSTRAINT mps_corp_disc_pk PRIMARY KEY ( discount_id )""",
        
        """CREATE TABLE mps_cust_corp (
            cust_id         INT NOT NULL COMMENT 'Customer ID Number',
            emp_id          INT NOT NULL COMMENT 'Corporate Customer Employee ID Number',
            company_name    VARCHAR(30) NOT NULL COMMENT 'Corporate Customer''s Company Name',
            company_regn_no VARCHAR(10) NOT NULL COMMENT 'Corporate Customer Company''s Registeration Number'
        )""",
        
        """ALTER TABLE mps_cust_corp ADD CONSTRAINT mps_cust_corp_pk PRIMARY KEY ( cust_id )""",
        """ALTER TABLE mps_cust_corp ADD CONSTRAINT mps_cust_corp_pkv1 UNIQUE ( emp_id )""",
        
        """CREATE TABLE mps_cust_indiv (
            cust_id             INT NOT NULL COMMENT 'Customer ID Number',
            drivers_licence_no  VARCHAR(13) NOT NULL COMMENT 'Individual Customer''s Driver License Number',
            fname               VARCHAR(30) NOT NULL COMMENT 'First Name of the Individual Customer',
            lname               VARCHAR(30) NOT NULL COMMENT 'Last Name of the Individual Customer',
            insurance_cmp_name  VARCHAR(30) NOT NULL COMMENT 'Name of the Insurance Company used by the Individual Customer',
            insurance_policy_no VARCHAR(13) NOT NULL COMMENT 'Individual Customer''s Insurance Policy Number'
        )""",
        """ALTER TABLE mps_cust_indiv ADD CONSTRAINT mps_cust_indiv_pk PRIMARY KEY ( cust_id )""",
        """ALTER TABLE mps_cust_indiv ADD CONSTRAINT mps_cust_indiv_pkv1 UNIQUE ( drivers_licence_no )""",
        """CREATE TABLE mps_disc (
            discount_id   INT NOT NULL COMMENT 'Discount ID Number',
            discount_type VARCHAR(1) NOT NULL COMMENT 'Type of the Discount'
        )""",

        """ALTER TABLE mps_disc ADD CONSTRAINT ch_inh_mps_disc CHECK ( discount_type IN ( 'C', 'I' ) )""",
        

       ]
    try:
        for query in queries:
            cur.execute(query)
            con.commit()
            print("OK ", query)
            
            
        print('Tables created successfully')
    except connector.Error as err:
        print('Error',err)

















#corporate add
#need changes
def addMpsCorporation(corp_name,reg_no):
    query = f"insert into mps_corporation values({corp_name},'{reg_no}')"
    cur.execute(query)
    con.commit()
    

def addMpsCustCorporate(emp_id,corp_id):
    query = 'select customer_id from mps_cust_corporate order by customer_id desc limit 1'
    cur.execute(query)
    for row in cur:
        cid = int(row[0])
    cid += 10
    query = f"insert into mps_cust_corporate values({cid},{emp_id},'{corp_id}')"
    cur.execute(query)
    con.commit()
    return cid






#individual


def addMPSCustomerIndividual(dl_no,insurance_company,insurance_policy_no):
    query = 'select customer_id from mps_cust_individual order by customer_id desc limit 1'
    cur.execute(query)
    for row in cur:
        customer_id = int(row[0])
    customer_id+=10
    query = f"insert into mps_cust_individual values({customer_id},{dl_no},'{insurance_company},{insurance_policy_no}')"
    cur.execute(query)
    con.commit()
    return customer_id
  


def addMPSCustomer(customer_type,first_name,last_name,email,phone,address_street,address_city,address_state,address_zipcode):


    query = f"insert into mps_customer values({customer_type},'{first_name},{last_name},{email},{phone},{address_street},{address_city},{address_state},{address_zipcode}')"
    cur.execute(query)
    con.commit()

    



#vehicle

    
def addMPSVehicle(location_id,class_id, make,model,make_year,vin_no,liscense_plate_no):
   
    
    query = f"insert into mps_vehicle values({location_id},{class_id},'{make},{model},{make_year},{vin_no},{liscense_plate_no}')"
    cur.execute(query)
    con.commit()
    
    
    
    
    
    
def addMPSVehicleClass(Vclass,rent_charge,extra_charge):
    query = f"insert into mps_cust_individual values({Vclass},{rent_charge},'{extra_charge}')"
    cur.execute(query)
    con.commit()

def addMPSOfficeLocation(address_street,address_city,address_state,address_zipcode,phone):
    query = f"insert into mps_cust_individual values({address_street},{address_city},'{address_state},{address_zipcode},{phone}')"
    cur.execute(query)
    con.commit()
    

def addMPSRentalService(pickup_date, dropoff_date, start_odo, end_odo, daily_limit, service_status, pickup_location_id, dropoff_location_id, customer_id, vehicle_id, coupon_id):
    
    query = f"insert into mps_rental_service values({pickup_date},{dropoff_date},'{start_odo},{end_odo},{daily_limit},{service_status},{pickup_location_id},{dropoff_location_id},{customer_id},{vehicle_id},{coupon_id}')"
    cur.execute(query)
    con.commit()

def addMPSPayment(pay_method,card_no,pay_date,customer_id):
    query = f"insert into mps_payment values({pay_method},{card_no},'{pay_date},{customer_id}')"
    cur.execute(query)
    con.commit()

    
def addMpsCoupon(coupon_type,discount):
    query = f"insert into mps_coupon values({coupon_type},{discount}')"
    cur.execute(query)
    con.commit()
    
def addMPSCouponCorp(coupon_id,corp_id):
    query = f"insert into mps_coupon_corp values({coupon_id},{corp_id}')"
    cur.execute(query)
    con.commit()
    




def getMPSCouponCorp():
    query = pd.read_sql_query('select * from mps_coupon_corp', con)
    df = pd.DataFrame(query, columns=['coupon_id', 'corp_id'])
    return df


def getMpsCoupon():
    query = pd.read_sql_query('select * from mps_coupon', con)
    df = pd.DataFrame(query, columns=['coupon_id', 'coupon_type', 'discount'])
    return df


def getMPSPayment():
    query = pd.read_sql_query('select * from mps_payment', con)
    df = pd.DataFrame(query, columns=['payment_id', 'customer_id', 'card_no', 'pay_date'])
    return df


def getMPSRentalService():
    query = pd.read_sql_query('select * from mps_rental_service', con)
    df = pd.DataFrame(query, columns=['pickup_date', 'dropoff_date', 'start_odo', 'end_odo', 'daily_limit', 'service_status', 'pickup_location_id', 'dropoff_location_id', 'customer_id', 'vehicle_id', 'coupon_id'])
    return df


def getMPSOfficeLocation():
    query = pd.read_sql_query('select * from mps_cust_individual', con)
    df = pd.DataFrame(query, columns=['customer_id', 'dl_no', 'insurance_company', 'insurance_policy_no'])
    return df









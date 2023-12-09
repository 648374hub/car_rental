-- SQLINES DEMO *** le SQL Developer Data Modeler 23.1.0.087.0806
-- SQLINES DEMO *** -12-08 16:58:30 EST
-- SQLINES DEMO *** le Database 21c 
-- SQLINES DEMO *** le Database 21c



-- SQLINES DEMO *** no DDL - MDSYS.SDO_GEOMETRY

-- SQLINES DEMO *** no DDL - XMLTYPE
	
----------------------------
CREATE TABLE mps_users (
    user_id  DOUBLE NOT NULL COMMENT 'Users ID Number',
    username VARCHAR(30) NOT NULL COMMENT 'Username of the Customer',
    password VARCHAR(30) NOT NULL COMMENT 'Password of the Customers'
);

ALTER TABLE mps_users ADD CONSTRAINT mps_users_pk PRIMARY KEY ( user_id );
ALTER TABLE MPS_USERS MODIFY COLUMN USER_ID DOUBLE NOT NULL UNIQUE AUTO_INCREMENT FIRST;

CREATE TABLE mps_customer (
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
);

ALTER TABLE mps_customer ADD CONSTRAINT ch_inh_mps_customer CHECK ( cust_type IN ( 'C', 'I' ) );
CREATE UNIQUE INDEX mps_customer__idx ON  mps_customer (user_id ASC );
ALTER TABLE mps_customer ADD CONSTRAINT mps_customer_pk PRIMARY KEY ( cust_id );
ALTER TABLE MPS_CUSTOMER MODIFY COLUMN CUST_ID INT NOT NULL UNIQUE AUTO_INCREMENT FIRST;
ALTER TABLE mps_customer ADD CONSTRAINT mps_customer_mps_users_fk FOREIGN KEY ( user_id ) 
REFERENCES mps_users ( user_id ); 
------------------------------------

CREATE TABLE mps_corp_disc (
    discount_id            INT NOT NULL COMMENT 'Discount ID Number',
    discount_fixed_percent DECIMAL(7, 2) NOT NULL COMMENT 'Fixed Corprate Discount for Corporate Companies',
    affl_company           VARCHAR(30) NOT NULL COMMENT 'Discounts for Affliliated Companies'
);

ALTER TABLE mps_corp_disc ADD CONSTRAINT mps_corp_disc_pk PRIMARY KEY ( discount_id );

CREATE TABLE mps_cust_corp (
    cust_id         INT NOT NULL COMMENT 'Customer ID Number',
    emp_id          INT NOT NULL COMMENT 'Corporate Customer Employee ID Number',
    company_name    VARCHAR(30) NOT NULL COMMENT 'Corporate Customer''s Company Name',
    company_regn_no VARCHAR(10) NOT NULL COMMENT 'Corporate Customer Company''s Registeration Number'
);

ALTER TABLE mps_cust_corp ADD CONSTRAINT mps_cust_corp_pk PRIMARY KEY ( cust_id );
ALTER TABLE mps_cust_corp ADD CONSTRAINT mps_cust_corp_pkv1 UNIQUE ( emp_id );

CREATE TABLE mps_cust_indiv (
    cust_id             INT NOT NULL COMMENT 'Customer ID Number',
    drivers_licence_no  VARCHAR(13) NOT NULL COMMENT 'Individual Customer''s Driver License Number',
    fname               VARCHAR(30) NOT NULL COMMENT 'First Name of the Individual Customer',
    lname               VARCHAR(30) NOT NULL COMMENT 'Last Name of the Individual Customer',
    insurance_cmp_name  VARCHAR(30) NOT NULL COMMENT 'Name of the Insurance Company used by the Individual Customer',
    insurance_policy_no VARCHAR(13) NOT NULL COMMENT 'Individual Customer''s Insurance Policy Number'
);

ALTER TABLE mps_cust_indiv ADD CONSTRAINT mps_cust_indiv_pk PRIMARY KEY ( cust_id );
ALTER TABLE mps_cust_indiv ADD CONSTRAINT mps_cust_indiv_pkv1 UNIQUE ( drivers_licence_no );


CREATE TABLE mps_disc (
    discount_id   INT NOT NULL COMMENT 'Discount ID Number',
    discount_type VARCHAR(1) NOT NULL COMMENT 'Type of the Discount'
);

ALTER TABLE mps_disc ADD CONSTRAINT ch_inh_mps_disc CHECK ( discount_type IN ( 'C', 'I' ) );

ALTER TABLE mps_disc ADD CONSTRAINT mps_disc_pk PRIMARY KEY ( discount_id );

CREATE TABLE mps_indiv_disc (
    discount_id         INT NOT NULL COMMENT 'Discount ID Number',
    discount_percent    DECIMAL(7, 2) NOT NULL COMMENT 'Discount Percentage for the Individual Customers',
    discount_valid_from DATETIME NOT NULL COMMENT 'Validity start date of the Discount',
    discount_valid_to   DATETIME NOT NULL COMMENT 'Validity end date of the Discount'
);

ALTER TABLE mps_indiv_disc ADD CONSTRAINT mps_indiv_disc_pk PRIMARY KEY ( discount_id );

SET SQL_MODE = NO_AUTO_VALUE_ON_ZERO;
CREATE TABLE mps_invoice (
    inv_id              INT NOT NULL COMMENT 'Invoice ID Number',
    inv_date            DATETIME NOT NULL COMMENT 'Date Generated in the Invoice',
    inv_amount          DECIMAL(7, 2) NOT NULL COMMENT 'Amount generated in the Invoice',
    invoice_paid_status VARCHAR(10) NOT NULL COMMENT 'Status updated if the Invoice Amount is paid in full',
    rent_serv_id        INT NOT NULL
);

ALTER TABLE mps_invoice ADD CONSTRAINT mps_invoice_pk PRIMARY KEY ( inv_id );
ALTER TABLE MPS_INVOICE MODIFY COLUMN INV_ID INT(11) NOT NULL UNIQUE AUTO_INCREMENT FIRST;
ALTER TABLE MPS_INVOICE AUTO_INCREMENT=21;


CREATE TABLE mps_loc (
    loc_id           INT NOT NULL COMMENT 'Location ID Number',
    loc_addr_street  VARCHAR(30) NOT NULL COMMENT 'Street Address of the Location',
    loc_addr_city    VARCHAR(30) NOT NULL COMMENT 'City of the Location',
    loc_addr_state   VARCHAR(30) NOT NULL COMMENT 'State of the Location',
    loc_addr_country VARCHAR(30) NOT NULL COMMENT ' Location Country',
    loc_addr_zipcode VARCHAR(10) NOT NULL COMMENT 'Location Zipcode',
    loc_phone_no     VARCHAR(14) NOT NULL COMMENT 'Location Phone Number'
);



ALTER TABLE mps_loc ADD CONSTRAINT mps_loc_pk PRIMARY KEY ( loc_id );


CREATE TABLE mps_payment (
    payment_id          INT NOT NULL COMMENT 'Payment ID Number',
    payment_date        DATETIME NOT NULL COMMENT 'Date of the Payment',
    payment_card_no     BIGINT NOT NULL COMMENT 'Card Number used for Payment',
    payment_amount      DECIMAL(7, 2) NOT NULL COMMENT 'Amount that need to be paid off',
    payment_method_type VARCHAR(30) NOT NULL COMMENT 'Type of Payment Methods like Credit card, Debit Card or Gift Card',
    inv_id              INT NOT NULL
);



ALTER TABLE mps_payment ADD CONSTRAINT mps_payment_pk PRIMARY KEY ( payment_id );


CREATE TABLE mps_rent_serv (
    rent_serv_id            INT NOT NULL COMMENT 'Rental Service ID Number',
    pickup_date             DATETIME NOT NULL COMMENT 'Pickup Date of the Vehicle Rental',
    planned_dropoff_date    DATETIME NOT NULL COMMENT 'Dropoff Date of the Vehicle Rental which was planned originally',
    actual_dropoff_date     DATETIME NOT NULL COMMENT 'Actual Dropoff Date of the Vehicle Class',
    start_odometer          INT NOT NULL COMMENT 'Start Odometer of the Vehicle Rental',
    end_odometer            INT NOT NULL COMMENT 'End Odometer of the Vehicle Rental',
    daily_odometer_limit    DECIMAL(7, 2) NOT NULL COMMENT 'Daily Limit of the Odometer',
    daily_odometer_lim_flag VARCHAR(1) NOT NULL COMMENT 'Flag for Daily Odometer Limit',
    discount_id             INT NOT NULL,
    cust_id                 INT NOT NULL,
    pickup_loc              INT NOT NULL,
    dropoff_loc             INT NOT NULL
);




ALTER TABLE mps_rent_serv ADD CONSTRAINT mps_rent_serv_pk PRIMARY KEY ( rent_serv_id );


CREATE TABLE mps_roles (
    role_id VARCHAR(30) NOT NULL COMMENT 'ROLE ID i.e. Admin or Customer'
);


ALTER TABLE mps_roles ADD CONSTRAINT mps_roles_pk PRIMARY KEY ( role_id );


CREATE TABLE mps_user_roles (
    user_id DOUBLE NOT NULL,
    role_id VARCHAR(30) NOT NULL
);

ALTER TABLE mps_user_roles ADD CONSTRAINT mps_user_roles_pk PRIMARY KEY ( user_id,
                                                                          role_id );

CREATE TABLE mps_veh_class (
    veh_class_id               INT NOT NULL COMMENT 'Vehicle Class ID Number',
    veh_class_type             VARCHAR(30) NOT NULL COMMENT 'Type of the Vehicle Class',
    veh_rental_rate            DECIMAL(7, 2) NOT NULL COMMENT 'Rental Rate of the Vehicle Class',
    veh_over_mileage_fees      DECIMAL(7, 2) NOT NULL COMMENT 'Over Mileage Fees of the Vehicle Class',
    mps_rent_serv_rent_serv_id INT NOT NULL
);



ALTER TABLE mps_veh_class ADD CONSTRAINT mps_veh_class_pk PRIMARY KEY ( veh_class_id );


CREATE TABLE mps_vehicle (
    veh_vin              BIGINT NOT NULL COMMENT 'Vehicle Identification Number',
    veh_make             VARCHAR(30) NOT NULL COMMENT 'Make of the Vehicle',
    veh_model            VARCHAR(30) NOT NULL COMMENT 'Model of the Vehicle',
    veh_year             SMALLINT NOT NULL COMMENT 'Year in which the Vehicle was made',
    veh_license_plate_no VARCHAR(8) NOT NULL COMMENT 'Licens ePlate Number of the Vehicle',
    loc_id               INT NOT NULL,
    veh_class_id         INT NOT NULL
);



ALTER TABLE mps_vehicle ADD CONSTRAINT mps_vehicle_pk PRIMARY KEY ( veh_vin );

ALTER TABLE mps_corp_disc
    ADD CONSTRAINT mps_corp_disc_mps_disc_fk FOREIGN KEY ( discount_id )
        REFERENCES mps_disc ( discount_id );

ALTER TABLE mps_cust_corp
    ADD CONSTRAINT mps_cust_corp_mps_customer_fk FOREIGN KEY ( cust_id )
        REFERENCES mps_customer ( cust_id );

ALTER TABLE mps_cust_indiv
    ADD CONSTRAINT mps_cust_indiv_mps_customer_fk FOREIGN KEY ( cust_id )
        REFERENCES mps_customer ( cust_id );



ALTER TABLE mps_indiv_disc
    ADD CONSTRAINT mps_indiv_disc_mps_disc_fk FOREIGN KEY ( discount_id )
        REFERENCES mps_disc ( discount_id );

ALTER TABLE mps_invoice
    ADD CONSTRAINT mps_invoice_mps_rent_serv_fk FOREIGN KEY ( rent_serv_id )
        REFERENCES mps_rent_serv ( rent_serv_id );

ALTER TABLE mps_payment
    ADD CONSTRAINT mps_payment_mps_invoice_fk FOREIGN KEY ( inv_id )
        REFERENCES mps_invoice ( inv_id );

ALTER TABLE mps_rent_serv
    ADD CONSTRAINT mps_rent_serv_mps_customer_fk FOREIGN KEY ( cust_id )
        REFERENCES mps_customer ( cust_id );

ALTER TABLE mps_rent_serv
    ADD CONSTRAINT mps_rent_serv_mps_disc_fk FOREIGN KEY ( discount_id )
        REFERENCES mps_disc ( discount_id );

ALTER TABLE mps_rent_serv
    ADD CONSTRAINT mps_rent_serv_mps_loc_fk FOREIGN KEY ( pickup_loc )
        REFERENCES mps_loc ( loc_id );

ALTER TABLE mps_rent_serv
    ADD CONSTRAINT mps_rent_serv_mps_loc_fkv2 FOREIGN KEY ( dropoff_loc )
        REFERENCES mps_loc ( loc_id );

ALTER TABLE mps_user_roles
    ADD CONSTRAINT mps_user_roles_mps_roles_fk FOREIGN KEY ( role_id )
        REFERENCES mps_roles ( role_id );

ALTER TABLE mps_user_roles
    ADD CONSTRAINT mps_user_roles_mps_users_fk FOREIGN KEY ( user_id )
        REFERENCES mps_users ( user_id );

ALTER TABLE mps_veh_class
    ADD CONSTRAINT mps_veh_class_mps_rent_serv_fk FOREIGN KEY ( mps_rent_serv_rent_serv_id )
        REFERENCES mps_rent_serv ( rent_serv_id );

ALTER TABLE mps_vehicle
    ADD CONSTRAINT mps_vehicle_mps_loc_fk FOREIGN KEY ( loc_id )
        REFERENCES mps_loc ( loc_id );

ALTER TABLE mps_vehicle
    ADD CONSTRAINT mps_vehicle_mps_veh_class_fk FOREIGN KEY ( veh_class_id )
        REFERENCES mps_veh_class ( veh_class_id );


DELIMITER ;
DROP TRIGGER IF EXISTS arc_fkarc_3_mps_cust_corp;

DELIMITER //
CREATE TRIGGER arc_fkarc_3_mps_cust_corp BEFORE
    INSERT ON MPS_CUST_CORP
    FOR EACH ROW
BEGIN
	DECLARE d VARCHAR(1);
	DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        RESIGNAL;
    END ;
    DECLARE EXIT HANDLER FOR NOT FOUND  BEGIN    END;
    SELECT
        a.cust_type
    INTO d
    FROM
        mps_customer a
    WHERE
        a.cust_id = NEW.cust_id;
        
    IF (( d IS NULL) OR (d <> 'C' )) THEN
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CUST_CORP_MPS_CUSTOMER_FK in Table MPS_CUST_CORP violates Arc constraint on Table MPS_CUSTOMER, discriminator column CUST_TYPE doesnt have value C';
    END IF;

END; //

DELIMITER ;

DROP TRIGGER IF EXISTS arc_fkarc_3_mps_cust_corp_update;

DELIMITER //
CREATE TRIGGER arc_fkarc_3_mps_cust_corp_update BEFORE
    UPDATE ON MPS_CUST_CORP
    FOR EACH ROW
BEGIN
	DECLARE d VARCHAR(1);
	DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        RESIGNAL;
    END ;
    DECLARE EXIT HANDLER FOR NOT FOUND  BEGIN    END;
    SELECT
        a.cust_type
    INTO d
    FROM
        mps_customer a
    WHERE
        a.cust_id = NEW.cust_id;
        
    IF (( d IS NULL) OR (d <> 'C' )) THEN
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CUST_CORP_MPS_CUSTOMER_FK in Table MPS_CUST_CORP violates Arc constraint on Table MPS_CUSTOMER, discriminator column CUST_TYPE doesnt have value C';
    END IF;

END; //


DELIMITER ;
DROP TRIGGER IF EXISTS arc_fkarc_3_mps_cust_indiv;

DELIMITER //

CREATE TRIGGER arc_fkarc_3_mps_cust_indiv BEFORE
    INSERT ON mps_cust_indiv
    FOR EACH ROW
  
BEGIN
  DECLARE d VARCHAR(1);
  DECLARE EXIT HANDLER FOR not found BEGIN   
    END;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.cust_type
    INTO d
    FROM
        mps_customer a
    WHERE
        a.cust_id = new.cust_id;

    IF ( d IS NULL OR d <> 'I' ) THEN
    SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CUST_INDIV_MPS_CUSTOMER_FK in Table MPS_CUST_INDIV violates Arc constraint on Table MPS_CUSTOMER - discriminator column CUST_TYPE doesnt have value I';        
		
    END IF;

    
END;
//

DELIMITER  ;
DROP TRIGGER IF EXISTS arc_fkarc_3_mps_cust_indiv_update;

DELIMITER //

CREATE TRIGGER arc_fkarc_3_mps_cust_indiv_update BEFORE
    UPDATE ON mps_cust_indiv
    FOR EACH ROW
  
BEGIN
  DECLARE d VARCHAR(1);
  DECLARE EXIT HANDLER FOR not found BEGIN   
    END;
  DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.cust_type
    INTO d
    FROM
        mps_customer a
    WHERE
        a.cust_id = new.cust_id;

    IF ( d IS NULL OR d <> 'I' ) THEN
    SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CUST_INDIV_MPS_CUSTOMER_FK in Table MPS_CUST_INDIV violates Arc constraint on Table MPS_CUSTOMER - discriminator column CUST_TYPE doesnt have value I';        
		
    END IF;

    
END;
//

DELIMITER  ;
DROP TRIGGER IF EXISTS arc_fkarc_4_mps_indiv_disc;

DELIMITER //

CREATE TRIGGER arc_fkarc_4_mps_indiv_disc BEFORE
    INSERT ON mps_indiv_disc
    FOR EACH ROW
    
BEGIN
	DECLARE d VARCHAR(1);
    DECLARE EXIT HANDLER FOR not found BEGIN
    END;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.discount_type
    INTO d
    FROM
        mps_disc a
    WHERE
        a.discount_id = new.discount_id;

    IF ( d IS NULL OR d <> 'I' ) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_INDIV_DISC_MPS_DISC_FK in Table MPS_INDIV_DISC violates Arc constraint on Table MPS_DISC - discriminator column DISCOUNT_TYPE doesnt have value I';
    END IF;

    
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS arc_fkarc_4_mps_indiv_disc_update;

DELIMITER //

CREATE TRIGGER arc_fkarc_4_mps_indiv_disc_update BEFORE
    UPDATE ON mps_indiv_disc
    FOR EACH ROW
    
BEGIN
	DECLARE d VARCHAR(1);
    DECLARE EXIT HANDLER FOR not found BEGIN
    END;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.discount_type
    INTO d
    FROM
        mps_disc a
    WHERE
        a.discount_id = new.discount_id;

    IF ( d IS NULL OR d <> 'I' ) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_INDIV_DISC_MPS_DISC_FK in Table MPS_INDIV_DISC violates Arc constraint on Table MPS_DISC - discriminator column DISCOUNT_TYPE doesnt have value I';
    END IF;

    
END;
//

DELIMITER ;

DROP TRIGGER IF EXISTS arc_fkarc_4_mps_corp_disc;

DELIMITER //

CREATE TRIGGER arc_fkarc_4_mps_corp_disc BEFORE
    INSERT ON mps_corp_disc
    FOR EACH ROW
    
BEGIN
	DECLARE d VARCHAR(1);
    DECLARE EXIT HANDLER FOR not found BEGIN
    END;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.discount_type
    INTO d
    FROM
        mps_disc a
    WHERE
        a.discount_id = new.discount_id;

    IF ( d IS NULL OR d <> 'C' ) THEN
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CORP_DISC_MPS_DISC_FK in Table MPS_CORP_DISC violates Arc constraint on Table MPS_DISC - discriminator column DISCOUNT_TYPE doesnt have value C';
    END IF;

    
END;
//
DELIMITER ;

DROP TRIGGER IF EXISTS arc_fkarc_4_mps_corp_disc_update;

DELIMITER //

CREATE TRIGGER arc_fkarc_4_mps_corp_disc_update BEFORE
    UPDATE ON mps_corp_disc
    FOR EACH ROW
    
BEGIN
	DECLARE d VARCHAR(1);
    DECLARE EXIT HANDLER FOR not found BEGIN
    END;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN
        RESIGNAL;
    END;
    SELECT
        a.discount_type
    INTO d
    FROM
        mps_disc a
    WHERE
        a.discount_id = new.discount_id;

    IF ( d IS NULL OR d <> 'C' ) THEN
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'FK MPS_CORP_DISC_MPS_DISC_FK in Table MPS_CORP_DISC violates Arc constraint on Table MPS_DISC - discriminator column DISCOUNT_TYPE doesnt have value C';
    END IF;

    
END;
//

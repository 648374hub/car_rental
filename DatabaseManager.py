import mysql.connector
import hashlib
import pandas as pd


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


class DatabaseManager:
    def __init__(self, db_user, db_password, host, database) -> None:
        self.conn = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=host,
            database=database,
        )

        self.cursor = self.conn.cursor(dictionary=True)

    def update_userdata(self, username, password):
        self.cursor.execute(
            "INSERT INTO MPS_USERS(username,password) VALUES (?,?)",
            (username, password),
        )
        self.conn.commit()

    def login_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM MPS_USERS WHERE username =? AND password = ?",
            (username, password),
        )
        data = self.cursor.fetchall()
        return data

    def login_admin(self, username, password):  # TODO: Complete this
        self.cursor.execute(
            """
            SELECT role.role_id
            FROM MPS_USERS user
            LEFT JOIN MPS_USER_ROLES role ON user.user_id = role.user_id
            WHERE username =? AND password = ?
        """,
            (username, password),
        )
        data = self.cursor.fetchall()["role_id"]
        return data

    ######Srujana part starts

    #### Customer profile

    def get_customer_details(self, username):
        self.cursor.execute(
            """
            SELECT
                u.user_id,
                CASE
                    WHEN c.cust_type = 'I' THEN CONCAT(ci.fname, ' ', ci.lname)
                    WHEN c.cust_type = 'C' THEN cc.company_name
                END AS customer_name,
                CASE
                    WHEN c.cust_type = 'I' THEN 'Individual'
                    WHEN c.cust_type = 'C' THEN 'Corporate'
                END AS customer_type,
                CASE
                    WHEN c.cust_type = 'I' THEN ci.drivers_licence_no
                    WHEN c.cust_type = 'C' THEN cc.company_regn_no
                END AS identification_number,
                CASE
                    WHEN c.cust_type = 'I' THEN ci.insurance_cmp_name
                    WHEN c.cust_type = 'C' THEN NULL
                END AS insurance_company
            FROM
                mps_users u
            INNER JOIN
                mps_customer c ON u.user_id = c.user_id
            LEFT JOIN
                mps_cust_indiv ci ON c.cust_id = ci.cust_id
            LEFT JOIN
                mps_cust_corp cc ON c.cust_id = cc.cust_id
            WHERE
                u.username = ?
        """,
            (username),
        )
        data = self.cursor.fetchall()
        return data

    def get_customer_bookings(self, username):
        query = (
            """
        SELECT
            rs.rent_serv_id,
            rs.pickup_date,
            rs.planned_dropoff_date,
            rs.actual_dropoff_date,
            vc.veh_class_type,
            v.veh_make,
            v.veh_model,
            l.loc_addr_street,
            l.loc_addr_city,
            l.loc_addr_state,
            l.loc_addr_country,
            l.loc_addr_zipcode
        FROM
            mps_users u
        JOIN
            mps_customer c ON u.user_id = c.user_id
        JOIN
            mps_rent_serv rs ON c.cust_id = rs.cust_id
        JOIN
            mps_veh_class vc ON rs.rent_serv_id = vc.mps_rent_serv_rent_serv_id
        JOIN
            mps_vehicle v ON v.veh_class_id = vc.veh_class_id
        JOIN
            mps_loc l ON v.loc_id = l.loc_id
        WHERE
            u.username = ?;
         """,
            (username),
        )
        data = pd.read_sql(query, self.conn)
        return data

    ##List available car details
    def list_avail_cars(self, limit):
        self.cursor.execute(
            """
		SELECT vc.veh_class_id, vc.veh_class_type, vc.veh_rental_rate,
        vc.veh_over_mileage_fees, v.veh_vin, v.veh_make, v.veh_model,
        v.veh_year, v.veh_license_plate_no
        FROM mps_vehicle v
        INNER JOIN mps_veh_class vc ON v.veh_class_id = vc.veh_class_id
        LIMIT ?; """,
            (limit),
        )

        row_headers = [
            x[0] for x in self.cursor.description
        ]  # this will extract row headers
        data = self.cursor.fetchall()
        json_data = []
        for result in data:
            json_data.append(dict(zip(row_headers, result)))
        return json_data

    ###Book a Car page

    def get_rent_details(self, veh_class):
        self.cursor.execute(
            """
		SELECT
        veh_class_id,
        veh_class_type,
        veh_rental_rate,
        veh_over_mileage_fees
        FROM mps_veh_class 
        WHERE veh_class_type = ?;
        """,
            (veh_class),
        )
        data = self.cursor.fetchall()
        return data

    def get_customer_type(self, username):
        self.cursor.execute(
            """
            SELECT c.cust_type
            FROM mps_users u
            JOIN mps_customer c ON u.user_id = c.user_id
            WHERE u.username = ?
        """,
            (username),
        )
        custType = self.cursor.fetchall()
        return custType["cust_type"]

    def isDiscountValid(self, username, discountID):
        custType = self.get_customer_type(username)
        self.cursor.execute(
            """
            SELECT 
                CASE ?
                    WHEN 'C' THEN cd.discount_fixed_percent
                    WHEN 'I' THEN id.discount_percent
                END AS discount_percent
            FROM mps_disc d
            LEFT JOIN mps_corp_disc cd ON d.discount_id = cd.discount_id
            LEFT JOIN mps_indiv_disc id ON d.discount_id = id.discount_id
            WHERE (cd.discount_id = ? AND discType = 'C') OR (id.discount_id = ? AND discType = 'I')
            LIMIT 1
            """,
            (custType, discountID, custType),
        )
        discPercent = self.cursor.fetchall()
        return discPercent["discount_percent"]

    ###Book a car page second part

    def get_indiv_cust_dets(self, username):
        self.cursor.execute(
            "select user_id from mps_users where username = ?", (username)
        )
        user_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            """SELECT c.cust_id, ci.drivers_licence_no, ci.fname, ci.lname, 
                 ci.insurance_cmp_name, ci.insurance_policy_no, 
                 c.cust_addr_street, c.cust_addr_city, c.cust_addr_state, 
                 c.cust_addr_country, c.cust_addr_zipcode, c.cust_email, c.cust_phone_no 
                 FROM mps_customer c 
                 INNER JOIN mps_cust_indiv ci ON c.cust_id = ci.cust_id 
                 WHERE c.user_id = ?""",
            (user_id),
        )
        data = self.cursor.fetchall()
        return data

    def get_corp_cust_dets(self, username):
        self.cursor.execute(
            "select user_id from mps_users where username = ?", (username)
        )
        user_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            """SELECT c.cust_id, cc.emp_id, cc.company_name, cc.company_regn_no,
            c.cust_addr_street, c.cust_addr_city, c.cust_addr_state,
            c.cust_addr_country, c.cust_addr_zipcode, c.cust_email, c.cust_phone_no
            FROM mps_customer c
            INNER JOIN mps_cust_corp cc ON c.cust_id = cc.cust_id
            WHERE c.user_id = ?""",
            (user_id),
        )
        data = self.cursor.fetchall()
        return data

    ##########admin functionalities

    def update_rent(self, veh_class, rent):
        self.cursor.execute(
            """
        UPDATE mps_veh_class v
        SET v.veh_rental_rate = ? 
        WHERE v.veh_class_type = ?;
        """,
            (rent, veh_class),
        )
        self.conn.commit()

    def update_over_mil(self, veh_class, omf):
        self.cursor.execute(
            """
        UPDATE mps_veh_class v
        SET  v.VEH_OVER_MILEAGE_FEES =?
        WHERE v.veh_class_type = ?;
        """,
            (omf, veh_class),
        )
        self.conn.commit()

    ##veh updates only after rent serv is updated
    def register_car(self, vehicle_details):
        address = vehicle_details["vehicle_address"]
        vehicle_details.pop("vehicle_address")

        self.cursor.execute("SELECT MAX(veh_vin) FROM mps_vehicle")
        data = self.cursor.fetchone()[0]
        if data is None:
            data = 0
        vehicle_details["VEH_VIN"] = data + 1

        self.cursor.execute(
            "SELECT veh_class_id FROM MPS_VEH_CLASS WHERE veh_class_type = ?",
            (vehicle_details["veh_class_type"]),
        )
        vehicle_details["VEH_CLASS_ID"] = self.cursor.fetchone()[0]
        vehicle_details.pop("veh_class_type")

        self.cursor.execute("SELECT MAX(loc_id) FROM mps_loc")
        data = self.cursor.fetchone()[0]
        if data is None:
            data = 0
        vehicle_details["LOC_ID"] = data + 1
        address["LOC_ID"] = data + 1

        self.cursor.execute(
            """
            INSERT INTO MPS_VEHICLE (VEH_VIN, VEH_MAKE, VEH_MODEL, VEH_YEAR, VEH_LICENSE_PLATE_NO, LOC_ID, VEH_CLASS_ID)
            VALUES(%(VEH_VIN)s, %(VEH_MAKE)s, %(VEH_MODEL)s, %(VEH_YEAR)s, %(VEH_LICENSE_PLATE_NO)s, %(LOC_ID)s, %(VEH_CLASS_ID)s)
            """,
            vehicle_details,
        )

        self.cursor.execute(
            """
            INSERT INTO MPS_LOC (LOC_ID, LOC_ADDR_STREET, LOC_ADDR_CITY, LOC_ADDR_STATE, LOC_ADDR_COUNTRY, LOC_ADDR_ZIPCODE)
            VALUES(%(LOC_ID)s, %(LOC_ADDR_STREET)s, %(LOC_ADDR_CITY)s, %(LOC_ADDR_STATE)s, %(LOC_ADDR_COUNTRY)s, %(LOC_ADDR_ZIPCODE)s)
            """,
            address,
        )
        self.conn.commit()

    def add_discount_corp(self, coupon, fix_percent, aff_comp):
        self.cursor.execute(
            "INSERT INTO MPS_DISC (discount_id, discount_type) VALUES(?,'C')", (coupon)
        )
        # self.cursor.commit()
        self.cursor.execute(
            "INSERT INTO MPS_CORP_DISC (discount_id, discount_fixed_percent, affl_company) VALUES (?,?,?)",
            (coupon, fix_percent, aff_comp),
        )
        self.cursor.commit()

    def add_discount_ind(self, coupon, disc_perc, from_date, to_date):
        self.cursor.execute(
            "INSERT INTO MPS_DISC (discount_id, discount_type) VALUES(?,'I')", (coupon)
        )
        self.cursor.execute(
            "INSERT INTO MPS_INDIV_DISC (discount_id, discount_percent, discount_valid_from, discount_valid_to) VALUES (?,?,?,?)",
            (coupon, disc_perc, from_date, to_date),
        )
        self.cursor.commit()

    def update_drop_off(
        self, invoice_id, end_odometer, actual_dropoff, odometer_flag, total
    ):
        self.cursor.execute(
            """
                UPDATE mps_rent_serv 
                SET actual_dropoff_date = ?, end_odometer = ?, daily_odometer_limit_flag = ? 
                WHERE rent_serv_id = (
                    SELECT rs.rent_serv_id 
                    FROM mps_rent_serv rs 
                    INNER JOIN mps_invoice inv ON rs.rent_serv_id = inv.rent_serv_id 
                    WHERE inv.inv_id = ?
            """,
            (actual_dropoff, end_odometer, odometer_flag, invoice_id),
        )
        self.cursor.execute(
            """
                UPDATE mps_invoice 
                SET inv_amount = ? 
                WHERE inv.inv_id = ?
            """,
            (total, invoice_id),
        )
        self.cursor.commit()

    def get_booking_details(self, invoice_id):
        self.cursor.execute(
            f"""
            SELECT *
            FROM MPS_INVOICE inv 
            LEFT JOIN MPS_RENT_SERV rs ON inv.rent_serv_id = rs.rent_serve_id
            LEFT JOIN MPS_VEH_CLASS vc ON rs.rent_serve_id = vc.mps_rent_serve_rent_serve_id
            WHERE inv.inv_id = {invoice_id}
        """
        )
        data = self.cursor.fetchall()
        return data

    # def update

-- CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
CREATE USER IF NOT EXISTS gatechUser@localhost IDENTIFIED BY 'GatechUser33!';

DROP DATABASE IF EXISTS cs6400_su20_team33; 
SET default_storage_engine=InnoDB;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE DATABASE IF NOT EXISTS cs6400_su20_team33 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE cs6400_su20_team33;

GRANT SELECT, INSERT, UPDATE, DELETE, FILE ON *.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON gatechuser.* TO 'gatechUser'@'localhost';
GRANT ALL PRIVILEGES ON cs6400_su20_team33.* TO 'gatechUser'@'localhost';
FLUSH PRIVILEGES;

-- Tables 

CREATE TABLE RegularVolunteer (
  regularVolunteerID INT unsigned NOT NULL AUTO_INCREMENT,
  volunteer_email VARCHAR(64) NOT NULL,
  password VARCHAR(50) NOT NULL,
  volunteer_first_name VARCHAR(30) NOT NULL,
  volunteer_last_name VARCHAR(30) NOT NULL,
  cell_phone BIGINT NOT NULL,
  date_started_volunteering DATE NOT NULL,
  CONSTRAINT RegularVolunteer_pkey PRIMARY KEY (regularVolunteerID),
  UNIQUE KEY volunteer_email (volunteer_email)
);

CREATE TABLE AdminVolunteer (
  adminVolunteerID INT UNSIGNED NOT NULL AUTO_INCREMENT,
  volunteer_email VARCHAR(64) NOT NULL,
  CONSTRAINT AdminVolunteer_pkey PRIMARY KEY (adminVolunteerID),
  UNIQUE KEY volunteer_email (volunteer_email)
);

CREATE TABLE Expense (
  dog_id INT UNSIGNED NOT NULL,
  date_of_expense DATE NOT NULL,
  expense_amount FLOAT NULL,
  optional_description VARCHAR(250) NULL,
  vendor_name VARCHAR(60) NOT NULL,
  CONSTRAINT Expense_pkey PRIMARY KEY (dog_id , date_of_expense, vendor_name)
);

CREATE TABLE Vendor (
  vendor_name VARCHAR(60) NOT NULL,
  CONSTRAINT Vendor_pkey PRIMARY KEY (vendor_name)
);

CREATE TABLE Applicant
(
    applicant_email VARCHAR(64) NOT NULL,
    applicant_first_name VARCHAR(30) NOT NULL,
    applicant_last_name VARCHAR(30) NOT NULL,
    phone_number BIGINT NOT NULL,
    zip_code VARCHAR(5) NOT NULL,
    street VARCHAR(25) NOT NULL,
    city VARCHAR(64) NOT NULL,
    state VARCHAR(2) NOT NULL,
    CONSTRAINT Applicant_pkey PRIMARY KEY (applicant_email)
);

CREATE TABLE AdoptionApplication
(
    application_number INT UNSIGNED Not Null AUTO_INCREMENT,
    applicant_email VARCHAR(64) NOT NULL,
    co_applicant_first_name VARCHAR(30),
    co_applicant_last_name VARCHAR(30),
    application_date Date NOT NULL,
    CONSTRAINT AdoptionApplication_pkey PRIMARY KEY (application_number)
);

CREATE TABLE ApprovedApplication
(
     approvedApplicationID INT UNSIGNED NOT NULL AUTO_INCREMENT,
     application_number INT UNSIGNED NOT Null,
     applicant_email VARCHAR(64) NOT NULL,
     adoption_date DATE NULL,
     CONSTRAINT ApprovedApplication_pkey PRIMARY KEY (approvedApplicationID),
     UNIQUE KEY application_number(application_number)
);

CREATE TABLE RejectedApplication
(
    rejectedApplicationID INT unsigned NOT NULL AUTO_INCREMENT,
    application_number INT UNSIGNED NOT Null,
    applicant_email VARCHAR(64) NOT NULL,
    CONSTRAINT RejectedApplication_pkey PRIMARY KEY (RejectedApplicationID),
    UNIQUE KEY application_number(application_number)
);


CREATE TABLE Dog
(
     dog_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
     dog_name VARCHAR(30) NOT NULL,
     sex ENUM("Male", "Female", "Unknown") NOT NULL,
     description VARCHAR(250) NOT NULL,
     alteration_status BOOLEAN NOT NULL, 
     dob DATE NOT NULL,
     surrender_date DATE NOT NULL,
     surrender_reason VARCHAR(250) NOT NULL,
     surrendered_by_animal_control BOOLEAN NOT NULL,
     application_number INT UNSIGNED Null,
     volunteer_email VARCHAR(50) NOT NULL,
     CONSTRAINT Dog_pkey PRIMARY KEY (dog_id)
);


CREATE TABLE Breed
(
    breed_name VARCHAR(100) NOT NULL,
    CONSTRAINT Breed_pkey PRIMARY KEY (breed_name)
);

CREATE TABLE AssignedTo
(
    dog_id  INT UNSIGNED NOT Null,
    breed_name VARCHAR(100) NOT NULL,
    UNIQUE KEY (dog_id ,breed_name)
);

CREATE TABLE MicrochipId (
    value VARCHAR (50),
    dog_id INT UNSIGNED NOT NULL,
    CONSTRAINT MicrochipId_pkey PRIMARY KEY(value)
);



-- Constraints   Foreign Keys: FK_ChildTable_childColumn_ParentTable_parentColumn

ALTER TABLE AdminVolunteer
  ADD CONSTRAINT fk_AdminVolunteer_volunteeremail_RegularVolunteer_volunteeremail FOREIGN KEY (volunteer_email) REFERENCES RegularVolunteer (volunteer_email);

ALTER TABLE Expense
  ADD CONSTRAINT fk_Expense_dogid_Dog_dogid  FOREIGN KEY (dog_id ) REFERENCES Dog (dog_id ),
  ADD CONSTRAINT fk_Expense_vendorname_Vendor_vendorname FOREIGN KEY (vendor_name) REFERENCES Vendor (vendor_name);

ALTER TABLE AdoptionApplication
  ADD CONSTRAINT fk_AdoptionApplication_applicantemail_Applicant_applicantemail     
  FOREIGN KEY (applicant_email) REFERENCES Applicant(applicant_email);

ALTER TABLE ApprovedApplication
  ADD CONSTRAINT fk_ApprovedApplication_appnum_AdoptionApplication_appnum 
  FOREIGN KEY (application_number) REFERENCES AdoptionApplication(application_number),
  ADD CONSTRAINT fk_ApprovedApplication_applicantemail_Applicant_applicantemail
  FOREIGN KEY (applicant_email) REFERENCES Applicant(applicant_email);

ALTER TABLE RejectedApplication
  ADD CONSTRAINT fk_Rejected_appnum_AdoptionApplication_appnum 
  FOREIGN KEY (application_number) REFERENCES AdoptionApplication(application_number),
  ADD CONSTRAINT fk_RejectedApplication_applicantemail_Applicant_applicantemail
  FOREIGN KEY (applicant_email) REFERENCES Applicant(applicant_email);

ALTER TABLE Dog
  ADD CONSTRAINT fk_Dog_applicationnumber_ApprovedApplication_applicationnumber
  FOREIGN KEY (application_number) REFERENCES ApprovedApplication(application_number),
  ADD CONSTRAINT fk_Dog_volunteeremail_RegularVolunteer_volunteeremail 
  FOREIGN KEY (volunteer_email) REFERENCES RegularVolunteer(volunteer_email);

ALTER TABLE AssignedTo
  ADD CONSTRAINT fk_AssignedTo_dogid_Dog_dogid 
  FOREIGN KEY (dog_id ) REFERENCES Dog(dog_id ),
  ADD CONSTRAINT fk_AssignedTo_breedname_Breed_breedname 
  FOREIGN KEY (breed_name) REFERENCES Breed(breed_name);

ALTER TABLE MicrochipId
  ADD CONSTRAINT fk_MicrochipId_dogid_Dog_dogid 
  FOREIGN KEY (dog_id) REFERENCES Dog (dog_id);
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	5.7.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `HD_app_agreement2`
--

DROP TABLE IF EXISTS `HD_app_agreement2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_agreement2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `pakiet_id` int(11) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_agreement2_status_id_dedb9268_fk_HD_app_ag` (`status_id`),
  KEY `HD_app_agreement2_company_id_961e59ad_fk_HD_app_company_id` (`company_id`),
  KEY `HD_app_agreement2_pakiet_id_680d3cf8` (`pakiet_id`),
  CONSTRAINT `HD_app_agreement2_company_id_961e59ad_fk_HD_app_company_id` FOREIGN KEY (`company_id`) REFERENCES `HD_app_company` (`id`),
  CONSTRAINT `HD_app_agreement2_pakiet_id_680d3cf8_fk_HD_app_pakiet_id` FOREIGN KEY (`pakiet_id`) REFERENCES `HD_app_pakiet` (`id`),
  CONSTRAINT `HD_app_agreement2_status_id_dedb9268_fk_HD_app_ag` FOREIGN KEY (`status_id`) REFERENCES `HD_app_agreementstatus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_agreement2`
--

LOCK TABLES `HD_app_agreement2` WRITE;
/*!40000 ALTER TABLE `HD_app_agreement2` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_agreement2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_agreementstatus`
--

DROP TABLE IF EXISTS `HD_app_agreementstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_agreementstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_agreementstatus`
--

LOCK TABLES `HD_app_agreementstatus` WRITE;
/*!40000 ALTER TABLE `HD_app_agreementstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_agreementstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_company`
--

DROP TABLE IF EXISTS `HD_app_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `thumb` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `adres` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_accepted` tinyint(1) NOT NULL,
  `care_id` int(11) DEFAULT NULL,
  `care_substitute_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_company_care_id_d772336f_fk_auth_user_id` (`care_id`),
  KEY `HD_app_company_care_substitute_id_21d66c9b_fk_auth_user_id` (`care_substitute_id`),
  CONSTRAINT `HD_app_company_care_id_d772336f_fk_auth_user_id` FOREIGN KEY (`care_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `HD_app_company_care_substitute_id_21d66c9b_fk_auth_user_id` FOREIGN KEY (`care_substitute_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_company`
--

LOCK TABLES `HD_app_company` WRITE;
/*!40000 ALTER TABLE `HD_app_company` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_customer2`
--

DROP TABLE IF EXISTS `HD_app_customer2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_customer2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `postal_code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nip` varchar(13) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cellphone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_customer2`
--

LOCK TABLES `HD_app_customer2` WRITE;
/*!40000 ALTER TABLE `HD_app_customer2` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_customer2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_hardware`
--

DROP TABLE IF EXISTS `HD_app_hardware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_hardware` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform_system` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform_version` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform_hostname` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cpu` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cpu_max` double NOT NULL,
  `cpu_physical_cores` decimal(2,0) NOT NULL,
  `cpu_total_cores` decimal(5,0) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `service_order_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_hardware_order_id_b0b1742b_fk_HD_app_order_id` (`order_id`),
  KEY `HD_app_hardware_service_order_id_ff47c778_fk_HD_app_se` (`service_order_id`),
  KEY `HD_app_hardware_user_id_65c026a2_fk_auth_user_id` (`user_id`),
  CONSTRAINT `HD_app_hardware_order_id_b0b1742b_fk_HD_app_order_id` FOREIGN KEY (`order_id`) REFERENCES `HD_app_order` (`id`),
  CONSTRAINT `HD_app_hardware_service_order_id_ff47c778_fk_HD_app_se` FOREIGN KEY (`service_order_id`) REFERENCES `HD_app_serviceorder` (`id`),
  CONSTRAINT `HD_app_hardware_user_id_65c026a2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_hardware`
--

LOCK TABLES `HD_app_hardware` WRITE;
/*!40000 ALTER TABLE `HD_app_hardware` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_hardware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_implementationtype`
--

DROP TABLE IF EXISTS `HD_app_implementationtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_implementationtype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_implementationtype`
--

LOCK TABLES `HD_app_implementationtype` WRITE;
/*!40000 ALTER TABLE `HD_app_implementationtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_implementationtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_message`
--

DROP TABLE IF EXISTS `HD_app_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `attachment` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `receipt_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_message_receipt_id_443d8930_fk_auth_user_id` (`receipt_id`),
  KEY `HD_app_message_sender_id_90a268ec_fk_auth_user_id` (`sender_id`),
  CONSTRAINT `HD_app_message_receipt_id_443d8930_fk_auth_user_id` FOREIGN KEY (`receipt_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `HD_app_message_sender_id_90a268ec_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_message`
--

LOCK TABLES `HD_app_message` WRITE;
/*!40000 ALTER TABLE `HD_app_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_netinterface`
--

DROP TABLE IF EXISTS `HD_app_netinterface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_netinterface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mac` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hardware_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_netinterface_hardware_id_40e168c2_fk_HD_app_hardware_id` (`hardware_id`),
  CONSTRAINT `HD_app_netinterface_hardware_id_40e168c2_fk_HD_app_hardware_id` FOREIGN KEY (`hardware_id`) REFERENCES `HD_app_hardware` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_netinterface`
--

LOCK TABLES `HD_app_netinterface` WRITE;
/*!40000 ALTER TABLE `HD_app_netinterface` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_netinterface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_news`
--

DROP TABLE IF EXISTS `HD_app_news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `thumb` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_news_user_id_ea2e85ae_fk_auth_user_id` (`user_id`),
  CONSTRAINT `HD_app_news_user_id_ea2e85ae_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_news`
--

LOCK TABLES `HD_app_news` WRITE;
/*!40000 ALTER TABLE `HD_app_news` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_ord`
--

DROP TABLE IF EXISTS `HD_app_ord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_ord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start` datetime(6) NOT NULL,
  `stop` datetime(6) NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `agreement_id` int(11) NOT NULL,
  `order_type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_ord_agreement_id_4a4b4bb4_fk_HD_app_agreement2_id` (`agreement_id`),
  KEY `HD_app_ord_order_type_id_d04d2252_fk_HD_app_ordertype_id` (`order_type_id`),
  KEY `HD_app_ord_user_id_e1c2f59a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `HD_app_ord_agreement_id_4a4b4bb4_fk_HD_app_agreement2_id` FOREIGN KEY (`agreement_id`) REFERENCES `HD_app_agreement2` (`id`),
  CONSTRAINT `HD_app_ord_order_type_id_d04d2252_fk_HD_app_ordertype_id` FOREIGN KEY (`order_type_id`) REFERENCES `HD_app_ordertype` (`id`),
  CONSTRAINT `HD_app_ord_user_id_e1c2f59a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_ord`
--

LOCK TABLES `HD_app_ord` WRITE;
/*!40000 ALTER TABLE `HD_app_ord` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_ord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_order`
--

DROP TABLE IF EXISTS `HD_app_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_datetime` datetime(6) DEFAULT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `updated_date` datetime(6) DEFAULT NULL,
  `attachment` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `agreement_id` int(11) NOT NULL,
  `care_id` int(11) DEFAULT NULL,
  `implementation_type_id` int(11) DEFAULT NULL,
  `order_status_id` int(11) DEFAULT NULL,
  `order_type_id` int(11) DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_order_care_id_c652f793_fk_auth_user_id` (`care_id`),
  KEY `HD_app_order_implementation_type__08a721aa_fk_HD_app_im` (`implementation_type_id`),
  KEY `HD_app_order_order_status_id_4fca7628_fk_HD_app_orderstatus_id` (`order_status_id`),
  KEY `HD_app_order_order_type_id_c5a54e36_fk_HD_app_ordertype_id` (`order_type_id`),
  KEY `HD_app_order_agreement_id_f08b76c9_fk_HD_app_agreement2_id` (`agreement_id`),
  CONSTRAINT `HD_app_order_agreement_id_f08b76c9_fk_HD_app_agreement2_id` FOREIGN KEY (`agreement_id`) REFERENCES `HD_app_agreement2` (`id`),
  CONSTRAINT `HD_app_order_care_id_c652f793_fk_auth_user_id` FOREIGN KEY (`care_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `HD_app_order_implementation_type__08a721aa_fk_HD_app_im` FOREIGN KEY (`implementation_type_id`) REFERENCES `HD_app_implementationtype` (`id`),
  CONSTRAINT `HD_app_order_order_status_id_4fca7628_fk_HD_app_orderstatus_id` FOREIGN KEY (`order_status_id`) REFERENCES `HD_app_orderstatus` (`id`),
  CONSTRAINT `HD_app_order_order_type_id_c5a54e36_fk_HD_app_ordertype_id` FOREIGN KEY (`order_type_id`) REFERENCES `HD_app_ordertype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_order`
--

LOCK TABLES `HD_app_order` WRITE;
/*!40000 ALTER TABLE `HD_app_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_ordercategory`
--

DROP TABLE IF EXISTS `HD_app_ordercategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_ordercategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_ordercategory`
--

LOCK TABLES `HD_app_ordercategory` WRITE;
/*!40000 ALTER TABLE `HD_app_ordercategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_ordercategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_orderstatus`
--

DROP TABLE IF EXISTS `HD_app_orderstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_orderstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_orderstatus`
--

LOCK TABLES `HD_app_orderstatus` WRITE;
/*!40000 ALTER TABLE `HD_app_orderstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_orderstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_ordertype`
--

DROP TABLE IF EXISTS `HD_app_ordertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_ordertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_ordertype`
--

LOCK TABLES `HD_app_ordertype` WRITE;
/*!40000 ALTER TABLE `HD_app_ordertype` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_ordertype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_pakiet`
--

DROP TABLE IF EXISTS `HD_app_pakiet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_pakiet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ratestack_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_pakiet_ratestack_id_8cf3fef8_fk_HD_app_ratestack_id` (`ratestack_id`),
  CONSTRAINT `HD_app_pakiet_ratestack_id_8cf3fef8_fk_HD_app_ratestack_id` FOREIGN KEY (`ratestack_id`) REFERENCES `HD_app_ratestack` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_pakiet`
--

LOCK TABLES `HD_app_pakiet` WRITE;
/*!40000 ALTER TABLE `HD_app_pakiet` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_pakiet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_partition`
--

DROP TABLE IF EXISTS `HD_app_partition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_partition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_size` double NOT NULL,
  `used_size` double NOT NULL,
  `free_size` double NOT NULL,
  `used_percentage` double NOT NULL,
  `hardware_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_partition_hardware_id_7d07d82e_fk_HD_app_hardware_id` (`hardware_id`),
  CONSTRAINT `HD_app_partition_hardware_id_7d07d82e_fk_HD_app_hardware_id` FOREIGN KEY (`hardware_id`) REFERENCES `HD_app_hardware` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_partition`
--

LOCK TABLES `HD_app_partition` WRITE;
/*!40000 ALTER TABLE `HD_app_partition` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_partition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_profile`
--

DROP TABLE IF EXISTS `HD_app_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cellphone` decimal(12,0) DEFAULT NULL,
  `thumb` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `idf` decimal(10,0) DEFAULT NULL,
  `tablef` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `typ_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `HD_app_profile_company_id_b60e1757_fk_HD_app_company_id` (`company_id`),
  KEY `HD_app_profile_typ_id_d277390e_fk_HD_app_profiletype_id` (`typ_id`),
  CONSTRAINT `HD_app_profile_company_id_b60e1757_fk_HD_app_company_id` FOREIGN KEY (`company_id`) REFERENCES `HD_app_company` (`id`),
  CONSTRAINT `HD_app_profile_typ_id_d277390e_fk_HD_app_profiletype_id` FOREIGN KEY (`typ_id`) REFERENCES `HD_app_profiletype` (`id`),
  CONSTRAINT `HD_app_profile_user_id_f52b932d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_profile`
--

LOCK TABLES `HD_app_profile` WRITE;
/*!40000 ALTER TABLE `HD_app_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_profiletype`
--

DROP TABLE IF EXISTS `HD_app_profiletype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_profiletype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_profiletype`
--

LOCK TABLES `HD_app_profiletype` WRITE;
/*!40000 ALTER TABLE `HD_app_profiletype` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_profiletype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_rate`
--

DROP TABLE IF EXISTS `HD_app_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start` time(6) NOT NULL,
  `stop` time(6) NOT NULL,
  `price` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_rate`
--

LOCK TABLES `HD_app_rate` WRITE;
/*!40000 ALTER TABLE `HD_app_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_ratestack`
--

DROP TABLE IF EXISTS `HD_app_ratestack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_ratestack` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_ratestack`
--

LOCK TABLES `HD_app_ratestack` WRITE;
/*!40000 ALTER TABLE `HD_app_ratestack` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_ratestack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_ratestack_rate`
--

DROP TABLE IF EXISTS `HD_app_ratestack_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_ratestack_rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ratestack_id` int(11) NOT NULL,
  `rate_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HD_app_ratestack_rate_ratestack_id_rate_id_996e9e42_uniq` (`ratestack_id`,`rate_id`),
  KEY `HD_app_ratestack_rate_rate_id_daa38c39_fk_HD_app_rate_id` (`rate_id`),
  CONSTRAINT `HD_app_ratestack_rat_ratestack_id_d464d183_fk_HD_app_ra` FOREIGN KEY (`ratestack_id`) REFERENCES `HD_app_ratestack` (`id`),
  CONSTRAINT `HD_app_ratestack_rate_rate_id_daa38c39_fk_HD_app_rate_id` FOREIGN KEY (`rate_id`) REFERENCES `HD_app_rate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_ratestack_rate`
--

LOCK TABLES `HD_app_ratestack_rate` WRITE;
/*!40000 ALTER TABLE `HD_app_ratestack_rate` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_ratestack_rate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_serviceorder`
--

DROP TABLE IF EXISTS `HD_app_serviceorder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_serviceorder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `no` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_datetime` datetime(6) DEFAULT NULL,
  `end_datetime` datetime(6) DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_date` datetime(6) DEFAULT NULL,
  `care_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `order_type_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `HD_app_serviceorder_care_id_b4d097ff_fk_auth_user_id` (`care_id`),
  KEY `HD_app_serviceorder_category_id_3f58823a_fk_HD_app_or` (`category_id`),
  KEY `HD_app_serviceorder_company_id_6b64a4da_fk_HD_app_company_id` (`company_id`),
  KEY `HD_app_serviceorder_order_type_id_4f1cdbe7_fk_HD_app_or` (`order_type_id`),
  KEY `HD_app_serviceorder_status_id_8618b8df_fk_HD_app_orderstatus_id` (`status_id`),
  KEY `HD_app_serviceorder_user_id_fc936828_fk_auth_user_id` (`user_id`),
  CONSTRAINT `HD_app_serviceorder_care_id_b4d097ff_fk_auth_user_id` FOREIGN KEY (`care_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `HD_app_serviceorder_category_id_3f58823a_fk_HD_app_or` FOREIGN KEY (`category_id`) REFERENCES `HD_app_ordercategory` (`id`),
  CONSTRAINT `HD_app_serviceorder_company_id_6b64a4da_fk_HD_app_company_id` FOREIGN KEY (`company_id`) REFERENCES `HD_app_company` (`id`),
  CONSTRAINT `HD_app_serviceorder_order_type_id_4f1cdbe7_fk_HD_app_or` FOREIGN KEY (`order_type_id`) REFERENCES `HD_app_ordertype` (`id`),
  CONSTRAINT `HD_app_serviceorder_status_id_8618b8df_fk_HD_app_orderstatus_id` FOREIGN KEY (`status_id`) REFERENCES `HD_app_orderstatus` (`id`),
  CONSTRAINT `HD_app_serviceorder_user_id_fc936828_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_serviceorder`
--

LOCK TABLES `HD_app_serviceorder` WRITE;
/*!40000 ALTER TABLE `HD_app_serviceorder` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_serviceorder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HD_app_usersettings`
--

DROP TABLE IF EXISTS `HD_app_usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HD_app_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email_notifications` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `HD_app_usersettings_user_id_853d8276_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HD_app_usersettings`
--

LOCK TABLES `HD_app_usersettings` WRITE;
/*!40000 ALTER TABLE `HD_app_usersettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `HD_app_usersettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Umowa',7,'add_agreement2'),(26,'Can change Umowa',7,'change_agreement2'),(27,'Can delete Umowa',7,'delete_agreement2'),(28,'Can view Umowa',7,'view_agreement2'),(29,'Can add Status umowy',8,'add_agreementstatus'),(30,'Can change Status umowy',8,'change_agreementstatus'),(31,'Can delete Status umowy',8,'delete_agreementstatus'),(32,'Can view Status umowy',8,'view_agreementstatus'),(33,'Can add Firma',9,'add_company'),(34,'Can change Firma',9,'change_company'),(35,'Can delete Firma',9,'delete_company'),(36,'Can view Firma',9,'view_company'),(37,'Can add Klient',10,'add_customer2'),(38,'Can change Klient',10,'change_customer2'),(39,'Can delete Klient',10,'delete_customer2'),(40,'Can view Klient',10,'view_customer2'),(41,'Can add Sprzęt PC',11,'add_hardware'),(42,'Can change Sprzęt PC',11,'change_hardware'),(43,'Can delete Sprzęt PC',11,'delete_hardware'),(44,'Can view Sprzęt PC',11,'view_hardware'),(45,'Can add Typ realizacji',12,'add_implementationtype'),(46,'Can change Typ realizacji',12,'change_implementationtype'),(47,'Can delete Typ realizacji',12,'delete_implementationtype'),(48,'Can view Typ realizacji',12,'view_implementationtype'),(49,'Can add Kategoria zlecenia',13,'add_ordercategory'),(50,'Can change Kategoria zlecenia',13,'change_ordercategory'),(51,'Can delete Kategoria zlecenia',13,'delete_ordercategory'),(52,'Can view Kategoria zlecenia',13,'view_ordercategory'),(53,'Can add Stan zlecenia',14,'add_orderstatus'),(54,'Can change Stan zlecenia',14,'change_orderstatus'),(55,'Can delete Stan zlecenia',14,'delete_orderstatus'),(56,'Can view Stan zlecenia',14,'view_orderstatus'),(57,'Can add Typ zlecenia',15,'add_ordertype'),(58,'Can change Typ zlecenia',15,'change_ordertype'),(59,'Can delete Typ zlecenia',15,'delete_ordertype'),(60,'Can view Typ zlecenia',15,'view_ordertype'),(61,'Can add Typ użytkownika',16,'add_profiletype'),(62,'Can change Typ użytkownika',16,'change_profiletype'),(63,'Can delete Typ użytkownika',16,'delete_profiletype'),(64,'Can view Typ użytkownika',16,'view_profiletype'),(65,'Can add Ustawienia użytkownika',17,'add_usersettings'),(66,'Can change Ustawienia użytkownika',17,'change_usersettings'),(67,'Can delete Ustawienia użytkownika',17,'delete_usersettings'),(68,'Can view Ustawienia użytkownika',17,'view_usersettings'),(69,'Can add Zlecenie serwisowe',18,'add_serviceorder'),(70,'Can change Zlecenie serwisowe',18,'change_serviceorder'),(71,'Can delete Zlecenie serwisowe',18,'delete_serviceorder'),(72,'Can view Zlecenie serwisowe',18,'view_serviceorder'),(73,'Can add Profil użytkownika',19,'add_profile'),(74,'Can change Profil użytkownika',19,'change_profile'),(75,'Can delete Profil użytkownika',19,'delete_profile'),(76,'Can view Profil użytkownika',19,'view_profile'),(77,'Can add Partycja',20,'add_partition'),(78,'Can change Partycja',20,'change_partition'),(79,'Can delete Partycja',20,'delete_partition'),(80,'Can view Partycja',20,'view_partition'),(81,'Can add Zlecenie',21,'add_order'),(82,'Can change Zlecenie',21,'change_order'),(83,'Can delete Zlecenie',21,'delete_order'),(84,'Can view Zlecenie',21,'view_order'),(85,'Can add News',22,'add_news'),(86,'Can change News',22,'change_news'),(87,'Can delete News',22,'delete_news'),(88,'Can view News',22,'view_news'),(89,'Can add net interface',23,'add_netinterface'),(90,'Can change net interface',23,'change_netinterface'),(91,'Can delete net interface',23,'delete_netinterface'),(92,'Can view net interface',23,'view_netinterface'),(93,'Can add Message',24,'add_message'),(94,'Can change Message',24,'change_message'),(95,'Can delete Message',24,'delete_message'),(96,'Can view Message',24,'view_message'),(97,'Can add Ord',25,'add_ord'),(98,'Can change Ord',25,'change_ord'),(99,'Can delete Ord',25,'delete_ord'),(100,'Can view Ord',25,'view_ord'),(101,'Can add Rate',26,'add_rate'),(102,'Can change Rate',26,'change_rate'),(103,'Can delete Rate',26,'delete_rate'),(104,'Can view Rate',26,'view_rate'),(105,'Can add Pakiet',27,'add_pakiet'),(106,'Can change Pakiet',27,'change_pakiet'),(107,'Can delete Pakiet',27,'delete_pakiet'),(108,'Can view Pakiet',27,'view_pakiet'),(109,'Can add RateStack',28,'add_ratestack'),(110,'Can change RateStack',28,'change_ratestack'),(111,'Can delete RateStack',28,'delete_ratestack'),(112,'Can view RateStack',28,'view_ratestack'),(113,'Can add Token',29,'add_token'),(114,'Can change Token',29,'change_token'),(115,'Can delete Token',29,'delete_token'),(116,'Can view Token',29,'view_token');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(29,'authtoken','token'),(5,'contenttypes','contenttype'),(7,'HD_app','agreement2'),(8,'HD_app','agreementstatus'),(9,'HD_app','company'),(10,'HD_app','customer2'),(11,'HD_app','hardware'),(12,'HD_app','implementationtype'),(24,'HD_app','message'),(23,'HD_app','netinterface'),(22,'HD_app','news'),(25,'HD_app','ord'),(21,'HD_app','order'),(13,'HD_app','ordercategory'),(14,'HD_app','orderstatus'),(15,'HD_app','ordertype'),(27,'HD_app','pakiet'),(20,'HD_app','partition'),(19,'HD_app','profile'),(16,'HD_app','profiletype'),(26,'HD_app','rate'),(28,'HD_app','ratestack'),(18,'HD_app','serviceorder'),(17,'HD_app','usersettings'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-08-24 15:43:18.650305'),(2,'auth','0001_initial','2020-08-24 15:43:18.784323'),(3,'HD_app','0001_initial','2020-08-24 15:43:20.039747'),(4,'HD_app','0002_ord','2020-08-24 15:43:21.134471'),(5,'HD_app','0003_auto_20200624_1542','2020-08-24 15:43:21.283440'),(6,'HD_app','0004_auto_20200624_1544','2020-08-24 15:43:21.338382'),(7,'HD_app','0005_auto_20200624_1551','2020-08-24 15:43:21.419403'),(8,'HD_app','0006_auto_20200624_1606','2020-08-24 15:43:21.613875'),(9,'HD_app','0007_auto_20200819_1311','2020-08-24 15:43:21.704416'),(10,'HD_app','0008_auto_20200819_1454','2020-08-24 15:43:21.981622'),(11,'HD_app','0009_remove_agreement2_rate','2020-08-24 15:43:22.075221'),(12,'HD_app','0010_auto_20200819_1505','2020-08-24 15:43:22.151996'),(13,'HD_app','0011_auto_20200819_1510','2020-08-24 15:43:22.262149'),(14,'HD_app','0012_auto_20200819_1515','2020-08-24 15:43:22.346250'),(15,'HD_app','0013_pakiet_ratestack','2020-08-24 15:43:22.413945'),(16,'HD_app','0014_auto_20200819_1525','2020-08-24 15:43:22.514948'),(17,'HD_app','0015_auto_20200819_1537','2020-08-24 15:43:22.697810'),(18,'HD_app','0016_auto_20200820_1841','2020-08-24 15:43:23.022804'),(19,'HD_app','0017_auto_20200820_1847','2020-08-24 15:43:23.146140'),(20,'HD_app','0018_auto_20200821_0837','2020-08-24 15:43:23.413761'),(21,'admin','0001_initial','2020-08-24 15:43:23.495517'),(22,'admin','0002_logentry_remove_auto_add','2020-08-24 15:43:23.595223'),(23,'admin','0003_logentry_add_action_flag_choices','2020-08-24 15:43:23.622389'),(24,'contenttypes','0002_remove_content_type_name','2020-08-24 15:43:23.717285'),(25,'auth','0002_alter_permission_name_max_length','2020-08-24 15:43:23.778961'),(26,'auth','0003_alter_user_email_max_length','2020-08-24 15:43:23.814028'),(27,'auth','0004_alter_user_username_opts','2020-08-24 15:43:23.839044'),(28,'auth','0005_alter_user_last_login_null','2020-08-24 15:43:23.891711'),(29,'auth','0006_require_contenttypes_0002','2020-08-24 15:43:23.895953'),(30,'auth','0007_alter_validators_add_error_messages','2020-08-24 15:43:23.917169'),(31,'auth','0008_alter_user_username_max_length','2020-08-24 15:43:23.970573'),(32,'auth','0009_alter_user_last_name_max_length','2020-08-24 15:43:24.029642'),(33,'auth','0010_alter_group_name_max_length','2020-08-24 15:43:24.068959'),(34,'auth','0011_update_proxy_permissions','2020-08-24 15:43:24.095078'),(35,'auth','0012_alter_user_first_name_max_length','2020-08-24 15:43:24.149994'),(36,'authtoken','0001_initial','2020-08-24 15:43:24.197842'),(37,'authtoken','0002_auto_20160226_1747','2020-08-24 15:43:24.374069'),(38,'sessions','0001_initial','2020-08-24 15:43:24.400313');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-24 13:43:37

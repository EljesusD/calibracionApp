-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: laboratorio_calibracion
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '852ce651-b6da-11f0-b117-401a5819e91f:1-1231';

--
-- Table structure for table `certificado`
--

DROP TABLE IF EXISTS `certificado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificado` (
  `id_certificado` int NOT NULL AUTO_INCREMENT,
  `id_detalle` int NOT NULL,
  `numero_certificado` varchar(100) NOT NULL,
  `fecha_emision` date DEFAULT NULL,
  `observaciones` text,
  PRIMARY KEY (`id_certificado`),
  KEY `id_detalle` (`id_detalle`),
  CONSTRAINT `certificado_ibfk_1` FOREIGN KEY (`id_detalle`) REFERENCES `detalleorden` (`id_detalle`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificado`
--

LOCK TABLES `certificado` WRITE;
/*!40000 ALTER TABLE `certificado` DISABLE KEYS */;
INSERT INTO `certificado` VALUES (1,1,'CERT-2025-0001','2025-10-03','Instrumento verificado con resultados dentro de tolerancia.'),(2,2,'CERT-2025-0002','2025-10-03','Termómetro calibrado conforme a procedimiento interno PROC-TERM-01.'),(3,3,'CERT-2025-0003','2025-10-07','Calibración satisfactoria con mínima desviación.'),(4,4,'CERT-2025-0004','2025-10-09','Instrumento requiere mantenimiento adicional antes de recalibrar.');
/*!40000 ALTER TABLE `certificado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(150) NOT NULL,
  `contacto` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Industrias Nova S.A. de C.V.','María Sánchez','351-234-5678','contacto@nova.com','Av. Tecnológico 100, Jacona'),(2,'Laboratorios Alfa','Carlos Rivas','351-111-2233','c.rivas@alfa.com','Calle 10 #45, Jacona'),(3,'Mecánica del Norte','Rosa Aguilar','351-222-3344','r.aguilar@mecanorte.com','Blvd. Universidad 200, Zamora'),(4,'SIMAC LABORATORIO DE CALIBRACION','Martha Coyazo','3511234567','Martha.simac@simac.mx','Av. Universidad #123'),(5,'Agrana','Gonzalo Oregel','3511630437','Gonzalo@agrana.com','Jacona '),(6,'COFRUSA','Azucena Vargas','35135164684','','jacon');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleorden`
--

DROP TABLE IF EXISTS `detalleorden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleorden` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_orden` int NOT NULL,
  `id_equipo` int NOT NULL,
  `id_servicio` int NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `resultado` varchar(1000) NOT NULL,
  PRIMARY KEY (`id_detalle`),
  KEY `id_orden` (`id_orden`),
  KEY `id_equipo` (`id_equipo`),
  KEY `id_servicio` (`id_servicio`),
  CONSTRAINT `detalleorden_ibfk_1` FOREIGN KEY (`id_orden`) REFERENCES `ordenservicio` (`id_orden`),
  CONSTRAINT `detalleorden_ibfk_2` FOREIGN KEY (`id_equipo`) REFERENCES `equipo` (`id_equipo`),
  CONSTRAINT `detalleorden_ibfk_3` FOREIGN KEY (`id_servicio`) REFERENCES `serviciocalibracion` (`id_servicio`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleorden`
--

LOCK TABLES `detalleorden` WRITE;
/*!40000 ALTER TABLE `detalleorden` DISABLE KEYS */;
INSERT INTO `detalleorden` VALUES (1,1,1,1,'2025-10-02','2025-10-03','Aprobado'),(2,1,2,2,'2025-10-02','2025-10-02','Aprobado'),(3,2,3,3,'2025-10-04','2025-10-06','Aprobado con observaciones'),(4,3,4,4,'2025-10-06','2025-10-08','No Aprobado'),(5,7,5,4,'2026-02-26','2026-02-27','con material listo'),(6,8,9,6,'2026-02-27','2026-02-27','se realizo verificacion, resultando una desviacion de 3.5 kg, se realiza ajuste con 800 kg y nos da como resultado 800.5 con una desviacion de 0.5 kg'),(7,9,10,6,'2026-02-27','2026-03-01','En proceso de preparacion'),(8,10,6,4,'2026-03-13','2026-03-13','En proceso de preparacion'),(9,11,44,4,'2026-05-13','2026-05-13','');
/*!40000 ALTER TABLE `detalleorden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `id_empleado` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `correo` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `escolaridad` varchar(100) DEFAULT NULL,
  `id_rol` int DEFAULT NULL,
  PRIMARY KEY (`id_empleado`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
INSERT INTO `empleado` VALUES (1,'Jesús','Delgado Navarro','jesus@simac.mx','3511234567','Av. Universidad #123','Ing. en Electronica',1),(2,'Ivonne','Ibarra','Ivone@simax.mx','3519876543','Calle Hidalgo #45','Lic. en Metrología',1),(3,'Eduardo','Martinez Heredia','Eduardo@simac.mx','3516549872','Morelos #77','Téc. en Instrumentación',3),(4,'Gustavo','Martinez Ramirez','Gustavo@simac.mx','3516549872','Morelos #77','Téc. en Instrumentación',3),(5,'Martha','Coyazo','Martha@simac.mx','3516549872','Morelos #77','Ing. Metrologia',1),(6,'Miguel','Calderilla',' miguel@simac.mx','3513216548','Juárez #10','Bachillerato',4),(7,'Manuel','Calero','af@gmai.com','351235431','zamora','Ing. Metrologia',6);
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipo`
--

DROP TABLE IF EXISTS `equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipo` (
  `id_equipo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `marca` varchar(100) DEFAULT NULL,
  `modelo` varchar(100) DEFAULT NULL,
  `numero_serie` varchar(100) DEFAULT NULL,
  `rango_medicion` varchar(100) DEFAULT NULL,
  `resolucion` varchar(100) DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  PRIMARY KEY (`id_equipo`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `equipo_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipo`
--

LOCK TABLES `equipo` WRITE;
/*!40000 ALTER TABLE `equipo` DISABLE KEYS */;
INSERT INTO `equipo` VALUES (1,'Multímetro Digital','Fluke','87V','SN-86458','0-1000 V','0.01 V',1),(2,'Termómetro Digital','Omega','HH-25TC','TH-2256','-50 a 250 °C','0.1 °C',1),(3,'Balanza Analítica','Mettler Toledo','ML204','BL-9023','0 a 200 g','0.0001 g',2),(4,'Calibrador de Presión','Additel','ADT760','PR-4533','0-1000 psi','0.01 psi',3),(5,'Báscula','Torrey','L-EQ','G24-32146','0 a 5 kg','0.001',4),(6,'Báscula','Torrey','L-EQ','D06-46348','0 a 5 kg','0.001',4),(9,'Báscula bajo perfil','Dibatec','Platino','PLA-2022-221','0 a 1500 kg','0.5 kg',4),(10,'Báscula bajo perfil','Torrey','EQB','D25-564318','0 a 1500 kg','0.5 kg',6),(11,'Balanza Analitica','Ohaus','AX224','SN12345',NULL,NULL,1),(12,'Multimetro Digital','Fluke','87V','SN56789',NULL,NULL,1),(13,'Termometro Digital','Testo','110','SN99887',NULL,NULL,1),(14,'Manometro Digital','Fluke','700G','SN44556',NULL,NULL,2),(15,'Calibrador Vernier','Mitutoyo','500-196','SN77441',NULL,NULL,2),(16,'Micrometro Exterior','Mitutoyo','293-340','SN88122',NULL,NULL,2),(17,'Balanza Industrial','Mettler Toledo','ICS425','SN66554',NULL,NULL,3),(18,'Termohigrometro','Extech','445715','SN33422',NULL,NULL,3),(19,'Tacometro Digital','Lutron','DT-2234C','SN11993',NULL,NULL,3),(20,'Medidor de Presion','Wika','CPG1500','SN66778',NULL,NULL,1),(21,'Báscula bajo perfil','Torrey','EQB','A13-254354','0 a 1000 kg','0.5 kg',3),(22,'Báscula bajo perfil','Torrey','EQB','A13-254354','0 a 1000 kg','0.5 kg',5),(23,'Balanza Analitica','Ohaus','AX224','SN12345',NULL,NULL,1),(24,'Multimetro Digital','Fluke','87V','SN56789',NULL,NULL,1),(25,'Termometro Digital','Testo','110','SN99887',NULL,NULL,1),(26,'Manometro Digital','Fluke','700G','SN44556',NULL,NULL,2),(27,'Calibrador Vernier','Mitutoyo','500-196','SN77441',NULL,NULL,2),(28,'Micrometro Exterior','Mitutoyo','293-340','SN88122',NULL,NULL,2),(29,'Balanza Industrial','Mettler Toledo','ICS425','SN66554',NULL,NULL,3),(30,'Termohigrometro','Extech','445715','SN33422',NULL,NULL,3),(31,'Tacometro Digital','Lutron','DT-2234C','SN11993',NULL,NULL,3),(32,'Medidor de Presion','Wika','CPG1500','SN66778',NULL,NULL,1),(33,'Balanza Analitica','Ohaus','AX224','SN12345',NULL,NULL,1),(34,'Multimetro Digital','Fluke','87V','SN56789',NULL,NULL,1),(35,'Termometro Digital','Testo','110','SN99887',NULL,NULL,1),(36,'Manometro Digital','Fluke','700G','SN44556',NULL,NULL,2),(37,'Calibrador Vernier','Mitutoyo','500-196','SN77441',NULL,NULL,2),(38,'Micrometro Exterior','Mitutoyo','293-340','SN88122',NULL,NULL,2),(39,'Balanza Industrial','Mettler Toledo','ICS425','SN66554',NULL,NULL,3),(43,'Multímetro Digital','Fluke','87V','SN-86458','0-1000 V','0.01 V',1),(44,'Báscula','Torrey','L-EQ','A25-4545665','0 a 5 kg','0.001',2);
/*!40000 ALTER TABLE `equipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturas_temperatura`
--

DROP TABLE IF EXISTS `lecturas_temperatura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturas_temperatura` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `valor` decimal(5,2) NOT NULL,
  `dispositivo` varchar(50) DEFAULT 'sensor1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturas_temperatura`
--

LOCK TABLES `lecturas_temperatura` WRITE;
/*!40000 ALTER TABLE `lecturas_temperatura` DISABLE KEYS */;
INSERT INTO `lecturas_temperatura` VALUES (1,'2026-03-13 08:00:00',23.45,'ESP32'),(2,'2026-03-13 08:05:00',23.60,'ESP32'),(3,'2026-03-13 08:10:00',23.80,'ESP32'),(4,'2026-03-13 08:15:00',24.10,'ESP32'),(5,'2026-03-13 08:20:00',24.25,'ESP32'),(6,'2026-03-13 08:25:00',24.40,'ESP32'),(7,'2026-03-13 08:30:00',24.55,'ESP32'),(8,'2026-03-13 08:35:00',24.70,'ESP32'),(9,'2026-03-13 08:40:00',24.85,'ESP32'),(10,'2026-03-13 08:45:00',25.00,'ESP32');
/*!40000 ALTER TABLE `lecturas_temperatura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenservicio`
--

DROP TABLE IF EXISTS `ordenservicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenservicio` (
  `id_orden` int NOT NULL AUTO_INCREMENT,
  `fecha_solicitud` date NOT NULL,
  `estado` varchar(50) DEFAULT 'Pendiente',
  `id_cliente` int NOT NULL,
  `id_empleado` int DEFAULT NULL,
  PRIMARY KEY (`id_orden`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_empleado` (`id_empleado`),
  CONSTRAINT `ordenservicio_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `ordenservicio_ibfk_2` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenservicio`
--

LOCK TABLES `ordenservicio` WRITE;
/*!40000 ALTER TABLE `ordenservicio` DISABLE KEYS */;
INSERT INTO `ordenservicio` VALUES (1,'2025-10-01','Aprobado',1,2),(2,'2025-10-03','En proceso',2,1),(3,'2025-10-05','En Proceso',3,2),(4,'2026-02-26','En Proceso',4,2),(7,'2026-02-25','En Proceso',4,4),(8,'2026-02-26','En Proceso',4,1),(9,'2026-02-27','En Proceso',6,4),(10,'2026-03-13','En Proceso',3,7),(11,'2026-05-12','aprobado',6,1);
/*!40000 ALTER TABLE `ordenservicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Administrador','Tiene acceso total al sistema, puede gestionar usuarios y servicios.'),(2,'Supervisor','Supervisa el trabajo técnico y valida la emisión de certificados.'),(3,'Técnico','Realiza calibraciones y registra resultados de mediciones.'),(4,'Recepcionista','Atiende a los clientes y registra órdenes de servicio.'),(6,'Asesor ','Solo Revisa Orden');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serviciocalibracion`
--

DROP TABLE IF EXISTS `serviciocalibracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `serviciocalibracion` (
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `nombre_servicio` varchar(150) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  `tiempo_estimado` int DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  PRIMARY KEY (`id_servicio`),
  KEY `fk_servicio_cliente` (`id_cliente`),
  CONSTRAINT `fk_servicio_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serviciocalibracion`
--

LOCK TABLES `serviciocalibracion` WRITE;
/*!40000 ALTER TABLE `serviciocalibracion` DISABLE KEYS */;
INSERT INTO `serviciocalibracion` VALUES (1,'Calibración de Multímetros','Verificación y ajuste de precisión de multímetros digitales.',800.00,2,1),(2,'Calibración de Termómetros','Calibración de termómetros de líquido y digitales según norma ISO 17025.',600.00,1,NULL),(3,'Calibración de Balanzas','Servicio de calibración de balanzas analíticas e industriales.',1200.00,3,3),(4,'calibracion de báscula','calibracion con intervalos',1500.00,2,NULL),(6,'Reparacion de plataforma','Báscula bajo perfil de  0 a 1500 kg',800.00,1,4),(8,'Reparacion de plataforma','correctivo',800.00,1,6),(9,'Calibracion Bascula','Calibración de Báscula',1200.00,1,4);
/*!40000 ALTER TABLE `serviciocalibracion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicioequipo`
--

DROP TABLE IF EXISTS `servicioequipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicioequipo` (
  `id_servicio_equipo` int NOT NULL AUTO_INCREMENT,
  `id_servicio` int NOT NULL,
  `id_equipo` int NOT NULL,
  PRIMARY KEY (`id_servicio_equipo`),
  KEY `id_servicio` (`id_servicio`),
  KEY `id_equipo` (`id_equipo`),
  CONSTRAINT `servicioequipo_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `serviciocalibracion` (`id_servicio`),
  CONSTRAINT `servicioequipo_ibfk_2` FOREIGN KEY (`id_equipo`) REFERENCES `equipo` (`id_equipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicioequipo`
--

LOCK TABLES `servicioequipo` WRITE;
/*!40000 ALTER TABLE `servicioequipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `servicioequipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `id_empleado` int NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `username` (`username`),
  KEY `id_empleado` (`id_empleado`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_empleado`) REFERENCES `empleado` (`id_empleado`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'admin_lab','scrypt:32768:8:1$SdrzNnpV3LoSul40$84853b3da3e29fe848f29a64199946e0be6c3dc07fbd9cbc641d112749066be31fcc8ef59427001d039390c68470eb188450e564c6ec7c1096f464a006c81c7b',1,1),(2,'tecnico_lab','scrypt:32768:8:1$un8JpBCZ1u6SNWfM$733404d0670e00dd7040229bc5dac47ad4037f68210fe2758f23fb81b8c15e2d00923f8c3b66d50607ba3b68bd7e76c61cd219ba07627ac78df1c230d5af4093',1,3),(4,'admin_lab2','scrypt:32768:8:1$qV8o89pMEKtvkVAA$770f52f384565b4e9b84ba46906f7930dea8e9cef513263ac1e24b5d060e499c77f2486d5df83d5bb5f482417099a67e37bf2743e72fb8aaca3d8c930747c31b',1,2);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-21 19:21:36

-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 22, 2025 at 10:54 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbpcn`
--

-- --------------------------------------------------------

--
-- Table structure for table `alert_logs`
--

CREATE TABLE `alert_logs` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `value` varchar(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alert_logs`
--

INSERT INTO `alert_logs` (`id`, `sensorId`, `topic`, `value`, `status`, `timestamp`) VALUES
(35, 'tower-001', 'temperature', '34.80', 'Warning', '2025-07-19 09:24:09'),
(36, 'device-002', 'ph', '4.05', 'ph⚠️ : ph Limbah melebihi batas ambang!', '2025-07-19 10:07:15'),

-- --------------------------------------------------------

--
-- Table structure for table `data_cod`
--

CREATE TABLE `data_cod` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) NOT NULL,
  `cod` varchar(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_cod`
--

INSERT INTO `data_cod` (`id`, `sensorId`, `cod`, `timestamp`) VALUES
(1, 'device-001', '13.08', '2025-07-20 15:31:08'),
(2, 'device-002', '18.45', '2025-07-20 15:31:08'),

-- --------------------------------------------------------

--
-- Table structure for table `data_ph`
--

CREATE TABLE `data_ph` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `ph` varchar(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_ph`
--

INSERT INTO `data_ph` (`id`, `sensorId`, `ph`, `timestamp`) VALUES
(1, 'device-001', '10.89', '2025-07-21 10:10:26'),
(2, 'device-002', '7.3', '2025-07-21 10:10:26');

-- --------------------------------------------------------

--
-- Table structure for table `data_temperature`
--

CREATE TABLE `data_temperature` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `temperature` varchar(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_temperature`
--

INSERT INTO `data_temperature` (`id`, `sensorId`, `temperature`, `timestamp`) VALUES
(1, 'device-001', '58.96', '2025-07-21 10:10:26'),
(2, 'device-002', '35.17', '2025-07-21 10:10:26');

-- --------------------------------------------------------

--
-- Table structure for table `data_volume`
--

CREATE TABLE `data_volume` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `volume` varchar(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_volume`
--

INSERT INTO `data_volume` (`id`, `sensorId`, `volume`, `timestamp`) VALUES
(1, 'device-001', '833.71', '2025-07-21 10:10:11'),
(2, 'device-002', '1035.01', '2025-07-21 10:10:11'),
(3, 'device-001', '849.45', '2025-07-21 10:10:26'),
(4, 'device-002', '933.08', '2025-07-21 10:10:26');

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `deviceId` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `type_device` varchar(100) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`id`, `deviceId`, `name`, `latitude`, `longitude`, `location`, `type_device`, `last_seen`) VALUES
(1, 'device-001', 'well-1A', 1.469700, 101.556100, 'duri', 'Arduino R4', NULL),
(2, 'device-002', 'well-2A', 0.486000, 101.447100, 'rumbai', 'ESP32', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `dht22_temperature_data`
--

CREATE TABLE `dht22_temperature_data` (
  `id` int(11) NOT NULL,
  `SensorID` varchar(50) DEFAULT NULL,
  `Date_n_Time` varchar(50) DEFAULT NULL,
  `Temperature` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mqtt_acl`
--

CREATE TABLE `mqtt_acl` (
  `id` int(11) UNSIGNED NOT NULL,
  `ipaddress` varchar(60) NOT NULL DEFAULT '',
  `username` varchar(255) NOT NULL DEFAULT '',
  `clientid` varchar(255) NOT NULL DEFAULT '',
  `action` enum('publish','subscribe','all') NOT NULL,
  `permission` enum('allow','deny') NOT NULL,
  `topic` varchar(255) NOT NULL DEFAULT '',
  `qos` tinyint(1) DEFAULT NULL,
  `retain` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mqtt_acl`
--

INSERT INTO `mqtt_acl` (`id`, `ipaddress`, `username`, `clientid`, `action`, `permission`, `topic`, `qos`, `retain`) VALUES
(1, '127.0.0.1', 'PCNUsermqtt', 'esp32-client-forPCNTest00:4B:12:EE:43:9C', 'publish', 'deny', 'sensorpcn/temperature', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `mqtt_user`
--

CREATE TABLE `mqtt_user` (
  `id` int(11) UNSIGNED NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `password_hash` varchar(100) DEFAULT NULL,
  `salt` varchar(35) DEFAULT NULL,
  `is_superuser` tinyint(1) DEFAULT 0,
  `created` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mqtt_user`
--

INSERT INTO `mqtt_user` (`id`, `username`, `password_hash`, `salt`, `is_superuser`, `created`) VALUES
(1, 'emqx_u', '44edc2d57cde8d79c98145003e105b90a14f1460b79186ea9cfe83942fc5abb5', 'slat_foo123', 1, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alert_logs`
--
ALTER TABLE `alert_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_cod`
--
ALTER TABLE `data_cod`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);

--
-- Indexes for table `data_ph`
--
ALTER TABLE `data_ph`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);

--
-- Indexes for table `data_temperature`
--
ALTER TABLE `data_temperature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);

--
-- Indexes for table `data_volume`
--
ALTER TABLE `data_volume`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `device_code` (`deviceId`);

--
-- Indexes for table `dht22_humidity_data`
--
ALTER TABLE `dht22_humidity_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dht22_temperature_data`
--
ALTER TABLE `dht22_temperature_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mqtt_acl`
--
ALTER TABLE `mqtt_acl`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mqtt_user`
--
ALTER TABLE `mqtt_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mqtt_username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alert_logs`
--
ALTER TABLE `alert_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=857;

--
-- AUTO_INCREMENT for table `data_cod`
--
ALTER TABLE `data_cod`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=257;

--
-- AUTO_INCREMENT for table `data_ph`
--
ALTER TABLE `data_ph`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=689;

--
-- AUTO_INCREMENT for table `data_temperature`
--
ALTER TABLE `data_temperature`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=696;

--
-- AUTO_INCREMENT for table `data_volume`
--
ALTER TABLE `data_volume`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=682;

--
-- AUTO_INCREMENT for table `devices`
--
ALTER TABLE `devices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `mqtt_acl`
--
ALTER TABLE `mqtt_acl`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `mqtt_user`
--
ALTER TABLE `mqtt_user`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

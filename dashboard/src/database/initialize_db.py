import mysql.connector

# Koneksi ke MySQL
conn = mysql.connector.connect(
    host="localhost",      # ganti dengan host MySQL kamu
    user="root",           # ganti dengan user MySQL kamu
    password="",   # ganti dengan password MySQL kamu
    database="dbpcn"      # ganti dengan nama database kamu
)
curs = conn.cursor()

# Membuat tabel (jika belum ada)
curs.execute("""
CREATE TABLE `alert_logs` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `topic` varchar(100) DEFAULT NULL,
  `value` varchar(11) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `status` ENUM  ['read', 'unread'] NOT NULL
)
""")

curs.execute("""
CREATE TABLE `data_cod` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) NOT NULL,
  `cod` varchar(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
)
""")
curs.execute("""
CREATE TABLE `data_ph` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `ph` varchar(11) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT current_timestamp()
)
""")
curs.execute("""
CREATE TABLE `data_temperature` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `temperature` varchar(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
)
""")
curs.execute("""
CREATE TABLE `data_volume` (
  `id` int(11) NOT NULL,
  `sensorId` varchar(100) DEFAULT NULL,
  `volume` varchar(11) NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
)
""")
curs.execute("""
CREATE TABLE `devices` (
  `id` int(11) NOT NULL,
  `deviceId` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `type_device` varchar(100) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
)
""")
curs.execute("""
ALTER TABLE `alert_logs`
  ADD PRIMARY KEY (`id`);
ALTER TABLE `data_cod`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);
ALTER TABLE `data_ph`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);
ALTER TABLE `data_temperature`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);
ALTER TABLE `data_volume`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sensorId` (`sensorId`),
  ADD KEY `timestamp` (`timestamp`);
ALTER TABLE `devices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `device_code` (`deviceId`);
""")

conn.commit()
curs.close()
conn.close()
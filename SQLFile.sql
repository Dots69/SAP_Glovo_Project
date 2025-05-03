-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.7.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for glovo_app
CREATE DATABASE IF NOT EXISTS `glovo_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `glovo_app`;

-- Dumping structure for table glovo_app.menu_items
CREATE TABLE IF NOT EXISTS `menu_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table glovo_app.menu_items: ~4 rows (approximately)
INSERT INTO `menu_items` (`id`, `name`, `price`, `restaurant_id`) VALUES
	(1, 'Pizza Margherita', 8.99, 1),
	(2, 'Pasta Carbonara', 10.99, 1),
	(3, 'Тест Храна', 25, 2),
	(4, 'bigmac', 12, 3);

-- Dumping structure for table glovo_app.orders
CREATE TABLE IF NOT EXISTS `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) DEFAULT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  `courier_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `status` enum('pending','in_progress','done') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  KEY `restaurant_id` (`restaurant_id`),
  KEY `courier_id` (`courier_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`),
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`courier_id`) REFERENCES `users` (`id`),
  CONSTRAINT `orders_ibfk_4` FOREIGN KEY (`item_id`) REFERENCES `menu_items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table glovo_app.orders: ~4 rows (approximately)
INSERT INTO `orders` (`id`, `customer_id`, `restaurant_id`, `courier_id`, `item_id`, `quantity`, `status`) VALUES
	(1, 2, 1, NULL, 1, 2, 'pending'),
	(2, 1, 1, NULL, 1, 2, 'pending'),
	(3, 2, 1, 6, 2, 5, 'done'),
	(4, 2, 1, 6, 1, 10, 'done');

-- Dumping structure for table glovo_app.restaurants
CREATE TABLE IF NOT EXISTS `restaurants` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `restaurants_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table glovo_app.restaurants: ~3 rows (approximately)
INSERT INTO `restaurants` (`id`, `name`, `created_by`) VALUES
	(1, 'Pizza Place', 1),
	(2, 'Тест Ресторант', 1),
	(3, 'mcdonalds', 1);

-- Dumping structure for table glovo_app.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('customer','courier','admin') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table glovo_app.users: ~6 rows (approximately)
INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
	(1, 'admin', 'admin_password', 'admin'),
	(2, 'customer1', 'customer_password', 'customer'),
	(3, 'courier1', 'courier_password', 'courier'),
	(4, 'customer2', 'customer2', 'customer'),
	(5, 'test_user', '1234', 'customer'),
	(6, 'asd123', 'asd123', 'courier');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;

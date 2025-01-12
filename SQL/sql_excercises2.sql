USE Computer_Firm;

-- 1) select unique manufacturers of printers --
SELECT DISTINCT(manufacturer) as printer_manufacturer FROM Product
WHERE type = "Printer";

-- 2) model number, speed, hd capaciy for pcs with price < 500 -- 
SELECT model, speed, hd FROM PC
WHERE price < 500;

-- 3) find the model number, RAM and screen size of laptops with prices over 1000 --
SELECT model, ram, screen FROM Laptop
WHERE price > 1000;

-- 4) all color printer models -- 
SELECT model FROM Printer
WHERE color = 'n';

-- 5) find most expensive printer, its model and price --
SELECT price, model FROM Printer
WHERE price = (SELECT MAX(price) FROM Printer);

-- 6) laptops models with speed lower than slowest pc --
SELECT model FROM Laptop WHERE
speed < (SELECT MIN(speed) FROM PC);

-- 7) all info about laptops with models that start with 17 --
SELECT * FROM Laptop
WHERE model LIKE '17%';

-- 8) model, speed, ram, hd capacity, price for all avaliable PC and laptops in one set -- 
SELECT model, speed, ram, hd, 'PC' AS 'type' FROM PC
UNION
SELECT model, speed, ram, hd, 'Laptop' AS 'type' FROM Laptop;

-- 9) manufacturers and speed for all laptops having HDD capacity >= 10 GB --
SELECT manufacturer, speed FROM Laptop lp
JOIN Product USING (model)
WHERE lp.hd >= 10;

-- 10) models and prices, for all products by manufacturer B --
SELECT pr.model, 
       COALESCE(lp.price, pc.price, prt.price) AS price
FROM Product pr
LEFT JOIN Laptop lp ON pr.model = lp.model
LEFT JOIN PC pc ON pr.model = pc.model
LEFT JOIN Printer prt ON pr.model = prt.model
WHERE pr.manufacturer = 'B';


-- 11) highest-priced pcs for each manufacturer --
WITH pc_full_table as (
SELECT * FROM Product
JOIN PC
USING (model)
)
SELECT pc_full_table.* FROM pc_full_table
JOIN 
(
SELECT MAX(price) as max_price, manufacturer FROM pc_full_table
GROUP BY manufacturer
) as max_prices
ON pc_full_table.manufacturer = max_prices.manufacturer AND pc_full_table.price = max_prices.max_price;

-- 12) update the prices of all PCs from model 1232 to be 100 higher than current prices -- 
SELECT * from PC;

SET SQL_SAFE_UPDATES = 0;
UPDATE PC
SET price = price + 100
WHERE model = 1232;
SET SQL_SAFE_UPDATES = 1;

SELECT * from PC;






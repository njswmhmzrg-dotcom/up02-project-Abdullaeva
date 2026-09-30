SELECT название, цена FROM Товар ORDER BY цена DESC LIMIT 1;

SELECT название, цена FROM Товар ORDER BY цена ASC LIMIT 1;

SELECT название, цена FROM Товар WHERE категория = 'Спорт';

SELECT * FROM Товар WHERE название LIKE '%о%';

SELECT id, дата, клиент, товар_id, количество FROM Заказ;

SELECT * FROM Заказ WHERE клиент = 'Иванов Иван Иванович';

SELECT Заказ.дата, Заказ.клиент, Товар.название, Заказ.количество 
FROM Заказ 
JOIN Товар ON Заказ.товар_id = Товар.id;

SELECT SUM(Товар.цена * Заказ.количество) 
FROM Заказ 
JOIN Товар ON Заказ.товар_id = Товар.id;

SELECT клиент, COUNT(*) as Количество_заказов 
FROM Заказ 
GROUP BY клиент;

SELECT название, цена, количество FROM Товар WHERE цена < 5000 AND количество > 0;
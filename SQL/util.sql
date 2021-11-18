SET @MyUserId='y1f9eyo93idrx8smca5pgntcha';

SELECT COUNT(*)
FROM Course
;


SELECT *
FROM Trail
WHERE Title LIKE 'Aprenda a Investir'
;


SELECT * 
FROM Course C
WHERE C.Title LIKE '%Turma 2%'
;

SELECT CT.CourseTrailOrder, C.*
FROM Trail T
		INNER JOIN CourseTrail CT ON CT.TrailId=T.Id
		INNER JOIN Course C ON CT.CourseId=C.Id
WHERE T.Title LIKE '%Aprenda a Investir%'
#WHERE C.Title LIKE 'Mercado financeiro%'
ORDER BY CT.CourseTrailOrder ASC
;


SELECT M.*
FROM Module AS M 
		INNER JOIN Course AS C ON M.CourseId=C.id
WHERE 	C.Title LIKE '%Turma 2%'
		#AND M.Title LIKE 'Modelo de Lucro Residual'
ORDER BY M.Order
;

SELECT L.*
FROM Lecture AS L 
		INNER JOIN Module AS M ON M.Id=L.ModuleId 
		INNER JOIN Course AS C ON M.CourseId=C.id
WHERE   C.Title LIKE '%Gestores%'
		#AND M.Title LIKE 'Modelo de Lucro Residual'
		#AND L.Tittle LIKE 'Comece a investir agora!'
ORDER BY M.Order,L.Order;


SELECT *
FROM Resource R
WHERE LectureId='4xrr8racgtq7page6i73j6585'
;

SELECT L.Tittle,R.*
FROM Resource AS R
		INNER JOIN Lecture AS L ON R.LectureId=L.Id
		INNER JOIN Module AS M ON M.Id=L.ModuleId 
        INNER JOIN Course AS C ON M.CourseId=C.id
WHERE C.Title LIKE 'Análise e Avaliação de Bancos'
		AND R.LectureId='5ebea2ffb08496007c4aa257'
ORDER BY M.Order,L.Order, R.Order
;

SELECT PS.*
FROM Product AS P 
		INNER JOIN ProductSubscription AS PS ON P.Id=PS.ProductId
		INNER JOIN Subscription AS S ON PS.SubscriptionId=S.Id
WHERE P.Title LIKE '%2be trader%'
	  AND S.UserId=@MyUserId
;


SELECT S.Id, L.Id
FROM Lecture AS L 
		INNER JOIN Module M ON M.Id=L.ModuleId 
		INNER JOIN Course C ON M.CourseId=C.Id
        INNER JOIN Subscription S ON S.CourseId=C.Id
WHERE   S.Id='g5idoanttidj5czhb1cscuuijg' AND
		C.id='5f2051b9d1e5870092f2de6j'
ORDER BY M.Order,L.Order;

SELECT A.*
FROM Annotation A
		INNER JOIN Subscription S ON A.SubscriptionId=S.Id
WHERE S.UserId=@MyUserId
;

SELECT * FROM INFORMATION_SCHEMA.TABLES
#WHERE TABLE_ROWS = 0
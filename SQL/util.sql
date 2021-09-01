SET @MyUserId='y1f9eyo93idrx8smca5pgntcha';

SELECT *
FROM Trail
WHERE Title LIKE 'Educação Financeira e Finanças Pessoais'
;


SELECT * 
FROM Course C
WHERE C.Id ='4g4upg35xtspnezs9adznxmnr'
;

SELECT C.*
FROM Trail T
		INNER JOIN CourseTrail CT ON CT.TrailId=T.Id
		INNER JOIN Course C ON CT.CourseId=C.Id
WHERE T.Title LIKE '%Educação Financeira e Finanças Pessoais%'
#WHERE C.Title LIKE 'Mercado financeiro%'
ORDER BY CT.CourseTrailOrder ASC
;


SELECT M.*
FROM Module AS M 
		INNER JOIN Course AS C ON M.CourseId=C.id
WHERE C.Title LIKE '%Minicurso Gestores%'
ORDER BY M.Order
;

SELECT L.*
FROM Lecture AS L 
		INNER JOIN Module AS M ON M.Id=L.ModuleId 
        INNER JOIN Course AS C ON M.CourseId=C.id
WHERE C.Title LIKE '%Minicurso Gestores%' #AND L.Tittle LIKE '%alternativas%'
ORDER BY M.Order,L.Order
;


SELECT R.*
FROM Resource AS R
		INNER JOIN Lecture AS L ON R.LectureId=L.Id
		INNER JOIN Module AS M ON M.Id=L.ModuleId 
        INNER JOIN Course AS C ON M.CourseId=C.id
WHERE C.Title LIKE '%Start%'
ORDER BY M.Order,L.Order, R.Order
;



SELECT PS.*
FROM Product AS P 
		INNER JOIN ProductSubscription AS PS ON P.Id=PS.ProductId
		INNER JOIN Subscription AS S ON PS.SubscriptionId=S.Id
WHERE P.Title LIKE '%2be trader%'
	  AND S.UserId='y1f9eyo93idrx8smca5pgntcha'
;



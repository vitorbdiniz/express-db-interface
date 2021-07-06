UPDATE Module
SET 
    Title = 'Aulas com Gestores'
WHERE
    Id ='5f3d942c66a051004ada3b58'
;

UPDATE Lecture
SET
    ModuleId='5f3d940966a0510024da3caf',
    UpdatedAt=1623673051342,
    `Order`=7
WHERE
    Id ='5f2da6d79809aa00224a7b6b'
;

UPDATE Module
SET
    Title='Lives e Workshops'
WHERE
    Id ='5f3d940966a0510024da3caf'
;

DELETE FROM Module
WHERE Id='5f3d942c66a051004ada3b59';

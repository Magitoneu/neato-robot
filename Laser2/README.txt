
Hi ha els diferents programes que poden ser executats:

	- Goto x y: el robot anirà al punt que es troba a la distància x i y desde la posició actual. (x, y en mm) 
	- GotoObstacles x y: igual que l'anterior però si entre mig hi ha obstacles els evitarà.
	- Avoid: simplement evitarà xocar, movent-se sense cap direcció en concret.
	- FollowWall : el robot buscarà una paret en la direcció frontal, quan la trobi la seguirà. 
	- ExitMaze x y: intentarà sortir d'un laberint anant cap el punt en la distància x i y. Usant followWall.
	- Predator: intentarà atrapar a l'objecte més proper.
	- Prey: s'escaparà de l'objecte més proper.

Execució:

python laser_test.py Programa

Programa ha de ser un dels mencionats anteriorment
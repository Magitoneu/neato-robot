
Hi ha els diferents programes que poden ser executats:

	- Goto x y: el robot anir� al punt que es troba a la dist�ncia x i y desde la posici� actual. (x, y en mm) 
	- GotoObstacles x y: igual que l'anterior per� si entre mig hi ha obstacles els evitar�.
	- Avoid: simplement evitar� xocar, movent-se sense cap direcci� en concret.
	- FollowWall : el robot buscar� una paret en la direcci� frontal, quan la trobi la seguir�. 
	- ExitMaze x y: intentar� sortir d'un laberint anant cap el punt en la dist�ncia x i y. Usant followWall.
	- Predator: intentar� atrapar a l'objecte m�s proper.
	- Prey: s'escapar� de l'objecte m�s proper.

Execuci�:

python laser_test.py Programa

Programa ha de ser un dels mencionats anteriorment
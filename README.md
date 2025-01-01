Purpose:

Freeze micropatch files so game would select Data ones



Usage:
Create a folder with following components for you game client:
components = {
    'Steam': ['steam_api.dll', 'wotblitz.exe'],
    'WGC': ['wgc_api.dll', 'wgc_api.exe', 'wotblitz.exe'],
    'LGC': ['tanksblitz.exe']

Inside that folder or in Data create another folder with Bfile.ini and unmod.ini

Bfile example:

C:\Games\World_of_Tanks_Blitz\Data\Gfx\UI\BattleLoadingScreen\amigosville\BackgroundLoading.packed.webp.dvpljmp3
C:\Games\World_of_Tanks_Blitz\Data\Gfx\UI\BattleLoadingScreen\amigosville_02\BackgroundLoading.packed.webp.dvpljmp3
C:\Games\World_of_Tanks_Blitz\Data\Gfx\UI\BattleLoadingScreen\amigosville_03\BackgroundLoading.packed.webp.dvpljmp3
C:\Games\World_of_Tanks_Blitz\Data\Gfx\UI\BattleLoadingScreen\canal\BackgroundLoading.packed.webp.dvpljmp3


[pathgm]
1=C:\Games\World_of_Tanks_Blitz\Data
2=(WG) DorTeBB 3.1
3=1.0.0.20


Make your own Bfile and then use sDLC manager

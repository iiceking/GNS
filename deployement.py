import os
import shutil

# Emplacement des fichiers de configuration générés
config_directory = '/path/to/generated/configs/'

# Répertoires cibles dans GNS3 pour chaque routeur
gns3_router_directories = {
    'R1': '/user/gns3_project/R1_config',
    'R2': '/user/gns3_project/R2_config',
    'R3': '/user/gns3_project/R3_config',
    'R4': '/user/gns3_project/R4_config', 
    'R5': '/user/gns3_project/R5_config', 
    'R6': '/user/gns3_project/R6_config',
}

def deploy_configs():
    for router, directory in gns3_router_directories.items():
        config_file = os.path.join(config_directory, f'{router}_config.txt')
        target_file = os.path.join(directory, f'{router}_config.txt')

        if os.path.exists(config_file):
            shutil.copy(config_file, target_file)
            print(f'Configuration de {router} déployée avec succès.')
        else:
            print(f'Fichier de configuration pour {router} introuvable.')

deploy_configs()


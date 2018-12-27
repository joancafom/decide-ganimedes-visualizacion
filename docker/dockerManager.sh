#!/bin/bash

respuesta=99

while  [ $respuesta -ne 0 ];
do
	clear
	echo "+----------------------------------------------------------------------+"
	echo "|              Panel de Administración - Decide-Ganimedes              |"
	echo "+----------------------------------------------------------------------+"
	echo "| 1) Listar imágenes, contenedores, volúmenes y redes                  |"
	echo "| 2) Encender contenedores con docker-compose                          |"
	echo "| 3) Apagar contenedores con docker-compose                            |"
	echo "| 4) Apagar contenedores y eliminar componentes sin uso                |"
	echo "| 5) Crear un usuario de administración para web                       |"
	echo "| 6) Eliminar componentes innecesarios sin uso (Purgar docker)         |"
	echo "| 7) Eliminar todas las imágenes sin uso                               |"
	echo "| 8) Purgar Docker (mantiene los volúmenes)                            |"
	echo "| 9) Eliminar volúmenes                                                |"
	echo "|                                                                      |"
	echo "| 0) Salir                                                             |"
	echo "+----------------------------------------------------------------------+"
	read -n 1 -p "Seleccione una opción: " respuesta
	# Falta controlar algunos caracteres especiales como Intro, Tabulador y Espacio

	case "$respuesta" in
		''|*[0-9]*)
			case "$respuesta" in
				1)      echo -e "\nEjecutando - Listar imágenes y contenedores\n"
					echo -e "\n----------- Listado de imágenes -----------\n"		
					sudo docker images
					echo -e "\n-------- Listado de contenedores ----------\n"
					sudo docker container list
					echo -e "\n---------- Listado de volúmenes -----------\n"
					sudo docker volume list
					echo -e "\n------------- Listado de redes ------------\n"
					sudo docker network list
					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;

				2)	echo -e "\nEjecutando - Encender contenedores con docker-compose\n"
					sudo docker-compose up -d
					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;

				3)	echo -e "\nEjecutando - Apagar contenedores con docker-compose\n"
				        sudo docker-compose down
					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;

				4) 	echo -e "\nEjecutando - Apagar contenedores y eliminar componentes sin uso \n"
					sudo docker ps -aq > temp.txt 
					temporal=$(tr -d '\n' < temp.txt)
				        rm temp.txt

					if [ -z $temporal ];
					then
						echo -e "\nTodos los contenedores están apagados\n\n"	
					else
						sudo docker stop $(sudo docker ps -aq)
						sudo docker system prune -f
					fi
					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;


				5)	echo -e "\nEjecutando - Crear un usuario de administración para web\n"               
                                        sudo docker exec -ti decide_web ./manage.py createsuperuser
                                        read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
                                        ;;	

				6)      echo -e "\nEjecutando - Eliminar componentes sin uso (Purgar docker)\n"
					sudo docker system prune -f
                                        read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
                                        ;;

				7)      echo -e "\nEjecutando - Eliminar todas las imágenes sin uso\n"
				
					read -rp $'Importante: sólo se borrarán aquellas imágenes que no se estén ejecutándo contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;

					if [ $opc = "Y" ] || [ $opc = "y" ];
					then				
						sudo docker image prune -af
					fi

					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;
				
				8)	echo -e "\nEjecutando - Resetear Docker\n"

					read -rp $'\nImportante: se borrará todas las imágenes y contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;

                                        if [ $opc = "Y" ] || [ $opc = "y" ];
                                        then
                                                sudo docker stop $(sudo docker ps -aq)
                                                sudo docker system prune -af
						sudo docker volume prune -f
					       	sudo docker rmi $(sudo docker images -q) --> sudo docker system prune -a
                                        fi

 					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;
			
				9)	echo -e "\nEjecutando - Eliminar volúmenes \n"
					read -rp $'Importante: los volúmenes guardan datos persistentes importantes para los contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;
					if [ $opc = "Y" ] || [ $opc = "y" ];
					then
						sudo docker volume prune -f
					fi
					read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
					;;

				0)      echo -e "\n\n"
					echo " ______________________________________  "
					echo "/ Script desarrollado por el equipo de \\"
                                        echo "| Decide-Ganimedes-Censo. Para más     | "
					echo "\ información... mira en la wiki xDDD  / "
                                        echo " --------------------------------------  "
                                        echo "  \                                      "
                                        echo "   \                                     "
 					echo "       .--.                              "
       					echo "      |o_o |                             "
       					echo "      |:_/ |                             "
      					echo "     //   \ \                            "
     					echo "    (|     | )                           "
    					echo "   /'\_   _/\`\                           "
    					echo "   \___)=(___/                           "
					echo -e "\n\n"
					;;	
			esac
			;;
		*)	respuesta=99
			read -n 1 -p $'\n\nEsta opción no existe. Presione una tecla para volver al menú...\n'
			;;	
	esac
done

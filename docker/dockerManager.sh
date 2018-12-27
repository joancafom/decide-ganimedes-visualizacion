#!/bin/bash
#title:         dockerManager.sh
#description:   Panel de Administración para docker
#author:        Juan Carlos Utrilla
#created:       Dic 25 2018
#version:       1.0
#usage:         ./dockerManager.sh
#==============================================================================

function salir {
 	echo -e "\n\n"
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
	echo "   /'\_   _/\`\                          "
	echo "   \___)=(___/                           "
	echo -e "\n\n"
}

function menuEstadoDocker () {
	estadoDocker=$(sudo systemctl is-active docker)
	
	if [[ $estadoDocker == "inactive" ]];
        then
                echo -e "| \e[4mEstado del demonio de docker\e[0m: \e[33m\e[5m\e[1mINACTIVO\e[0m                               |"
	elif [[ $estadoDocker == "failed" ]];
	then
		echo -e "| \e[4mEstado del demonio de docker\e[0m: \e[31m\e[5m\e[1mFALLIDO\e[0m                                |"
	elif [[ $estadoDocker == "active" ]];
	then
		echo -e "| \e[4mEstado del demonio de docker\e[0m: \e[32m\e[1mACTIVO\e[0m                                 |"
	fi
}


function menu {
	estadoDocker=$(sudo systemctl is-active docker)
        echo -e "\e[1m+----------------------------------------------------------------------+\e[0m"
	echo -e "\e[1m|              Panel de Administración - Decide-Ganimedes              |\e[0m"
	echo -e "\e[1m+----------------------------------------------------------------------+\e[0m"
                                                                                       
        if [[ $estadoDocker == "active" ]];
	then
		echo -e "\e[1m| 1)\e[0m Listar imágenes, contenedores, volúmenes y redes                  \e[1m|\e[0m"
		echo -e "\e[1m| 2)\e[0m Encender contenedores con docker-compose                          \e[1m|\e[0m"
        	echo -e "\e[1m| 3)\e[0m Apagar contenedores con docker-compose                            \e[1m|\e[0m"
        	echo -e "\e[1m| 4)\e[0m Apagar contenedores y eliminar componentes sin uso                \e[1m|\e[0m"
        	echo -e "\e[1m| 5)\e[0m Crear un usuario de administración para web                       \e[1m|\e[0m"
        	echo -e "\e[1m| 6)\e[0m Eliminar todas las imágenes sin uso                               \e[1m|\e[0m"
        	echo -e "\e[1m| 7)\e[0m Resetear Docker (mantiene los volúmenes)                          \e[1m|\e[0m"
        	echo -e "\e[1m| 8)\e[0m Eliminar volúmenes                                                \e[1m|\e[0m"
		echo -e "\e[1m|\e[0m                                                                      \e[1m|\e[0m"
		echo -e "\e[1m| 9)\e[0m Desactivar demonio de docker                                      \e[1m|\e[0m"
	else
		echo -e "\e[1m| 1)\e[0m Activar demonio de docker                                         \e[1m|\e[0m"

		if [[ $estadoDocker == "failed" ]];
		then
			echo "|                                                                      |"
			echo -e "| \e[31mSi la activación del demonio de docker ha fallado puede ser debido a \e[0m|"
			echo -e "| \e[31mque el servicio se ha activado y apagado demasiadas veces de forma  \e[0m |"
	        	echo -e "| \e[31mmuy rápida. Espere 1 minuto para volver a intentarlo. \e[0m               |"	
		fi
	fi
        echo -e "|                                                                      |"
	menuEstadoDocker
	echo -e "\e[1m|                                                                      |\e[0m"
        echo -e "\e[1m| 0)\e[0m  Salir                                                            \e[1m|\e[0m"
        echo -e "\e[1m|                                                                      |\e[0m"
	echo -e "\e[1m+----------------------------------------------------------------------+\e[0m"
}

respuesta=99

while  [ $respuesta -ne 0 ];
do
clear
	menu
	read -n 1 -p "Seleccione una opción: " respuesta
	# Falta controlar algunos caracteres especiales como Intro, Tabulador y Espacio

	estadoDocker=$(sudo systemctl is-active docker)

        if [[ $estadoDocker == "active" ]];
        then
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

					6)      echo -e "\nEjecutando - Eliminar todas las imágenes sin uso\n"
					
						read -rp $'Importante: sólo se borrarán aquellas imágenes que no se estén ejecutándo contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;

						if [ $opc = "Y" ] || [ $opc = "y" ];
						then				
							sudo docker image prune -af
						fi

						read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
						;;
					
					7)	echo -e "\nEjecutando - Resetear Docker\n"
		
						read -rp $'\nImportante: se borrará todas las imágenes y contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;

						if [ $opc = "Y" ] || [ $opc = "y" ];
		               	                then
		                       	                sudo docker stop $(sudo docker ps -aq)
		                               	        sudo docker system prune -af
							sudo docker volume prune -f
						       	# sudo docker rmi $(sudo docker images -q) --> sudo docker system prune -a
						fi

						read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
						;;
				
					8)	echo -e "\nEjecutando - Eliminar volúmenes \n"
						read -rp $'Importante: los volúmenes guardan datos persistentes importantes para los contenedores. ¿Estás seguro de querer continuar? (Y/n): ' opc;
						if [ $opc = "Y" ] || [ $opc = "y" ];
						then
							sudo docker volume prune -f
						fi
						read -n 1 -p $'\nPresiona una tecla para volver al menú...\n'
						;;
		
					9)	echo -e "\nEjecutando - Desactivar demonio de Docker...\n"
						sudo systemctl stop docker
						;;

					0)      salir
						;;
				esac
				;;
			*)	respuesta=99
				read -n 1 -p $'\n\nEsta opción no existe. Presione una tecla para volver al menú...\n'
				;;	
		esac
	else
		case "$respuesta" in
			''|*[0-1]*)
			case "$respuesta" in
				1) 	echo -e "\nEjecutando - Activar demonio de docker... \n"
					sudo systemctl start docker
					;;

				0)	salir
					;;
			esac
			;;

		*) 	respuesta=99
			read -n 1 -p $'\n\nEsta opción no existe. Presione una tecla para volver al menú...\n'
                        ;;
		esac
	fi
done

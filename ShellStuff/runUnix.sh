#!/bin/bash


# idiomatic parameter and option handling in sh
comm="python3 "
host=""
param="Main_Parent.py"
reset=""
root=""
while test $# -gt 0
do
    case "$1" in
        "local") host="local"
            ;;
        "parent") param="Main_Parent.py"
             ;;
        "child") param="Main_Child.py"
            ;;
        "pytest") comm="pytest " param=${*:2}
            ;;
        "db") comm="python3 " param="../database/database.py"
            ;;    
        "init") comm="python3 " param="../database/init.py"
            ;;    
        "y") reset=" y "
            ;;    
        "root") root=" root "
            ;;    
        "backend") comm="python3 " param="../backEnd/backEnd.py"
            ;;                
        "bash") comm="/bin/bash " param=""
            ;;                
        "macro") comm="python3 " param="testMain.py"
            ;;               
        "sel") comm="python3 " param="OnTop.py"
            ;;         
        # --*) echo "bad option $1"
            # ;;
         #*) echo "argument $1"
            # ;;
    esac
    shift
done

command=$1

if [[ $host == "local" || $root != "" ]]
then
    #Change cnf to mysql host
    if [ ! -f /.cnf_copy ]; then 

        echo "CDing to littlelearners/database"
        cd ../database/

        echo "Making copy of .cnf"
        cp .cnf .cnf_copy

        echo "Executing changeCNFUNix.py"
        python3 ../ShellStuff/changeCNFUnix.py $root

        echo "cnf contents: "
        cat ../database/.cnf

    fi
fi

echo "CDing back to working diretory littlelearners/desktopApp"
cd ../desktopApp

if [ -e ../display ]
then
    disp=`cat ../display`
    #echo $disp
    $disp
    #echo $DISPLAY
fi
echo $comm $param $reset
$comm $param $reset

if [[ $host == "local" || $root != "" ]]
then
    #Change cnf back
    echo "CDing back to littlelearners/database"
    cd ../database

    echo "Removing .cnf"
    rm .cnf

    echo "renaming .cnf_copy to .cnf"
    mv .cnf_copy .cnf
fi
    
# #No parameters passed, run main.py connects to VM database
# if [ -z "$1" ]
# then
    # python3 Main.py
# else

    # #Change cnf to mysql host
    # if [ ! -f /.cnf_copy ]; then 

        # echo "CDing to littlelearners/database"
        # cd ../database/

        # echo "Making copy of .cnf"
        # cp .cnf .cnf_copy

        # echo "Executing changeCNFUNix.py"
        # python3 ../ShellStuff/changeCNFUnix.py

    # fi

    # echo "CDing back to working diretory littlelearners/desktopApp"
    # cd ../desktopApp

    # echo "Executing parameter list: $*"

    # #Run pytest
    # if [[ $command == "pytest" ]]
    # then
        # tests=${*:2}
        # if [[ -z "${tests}" ]]
        # then 
            # pytest ../
        # else
            # pytest $tests
        # fi
    # #Run main.py connecting to local database
    # elif [[ $command == "local" ]]
    # then
        # python3 Main.py
    # #Run database.py
    # elif [[ $command == "db" ]]
    # then
        # python3 ../database/database.py
    # fi

    # #Change cnf back
    # echo "CDing back to littlelearners/database"
    # cd ../database

    # echo "Removing .cnf"
    # rm .cnf

    # echo "renaming .cnf_copy to .cnf"
    # mv .cnf_copy .cnf


# fi
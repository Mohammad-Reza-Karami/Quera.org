declare -A Commands=([add]=1 [check]=1 [free]=1 [exit]=1)
declare -A Hours=()

while [ 1 ]
do
    read Input
    Input=($Input)
    Command=${Input[0]}

    if [[ -n "${Commands[$Command]}" ]]
    then
        # add command:
        if [ "$Command" == "add" ]
        then
            declare -i Start=${Input[1]}
            declare -i Stop=${Input[2]}
            for Hour in $(seq $Start $((Stop - 1)))
            do
                Hours[$Hour]="Busy"
            done
            echo A meeting from $Start to $Stop added to your day!
        # check command:
        elif [ "$Command" == "check" ]
        then
            declare -i Start=${Input[1]}
            declare -i Stop=${Input[2]}
            declare -i Counter=0
            for Hour in $(seq $Start $Stop)
            do
                if [ "${Hours[$Hour]}" == "Busy" ]
                then
                Counter+=1
                fi
            done
            if [ $Counter == 0 ]
            then
            echo You can add a meeting from $Start to $Stop!
            else
            echo You can\'t have a meeting from $Start to $Stop!
            fi
        # free command:
        elif [ "$Command" == "free" ]
        then
            declare -i Start=${Input[1]}
            declare -i Stop=${Input[2]}
            for Hour in $(seq $Start $Stop)
            do
                Hours[$Hour]="Free"
            done
            echo You\'re now free from $Start to $Stop!
        # exit command:
        else
        echo Bye Bye!
        break
        fi
    else
        echo Command not found.
    fi
done
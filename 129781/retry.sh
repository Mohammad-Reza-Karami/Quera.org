Server=$1
Status=`curl $Server`
echo ret is: $Status

while [ "$Status" != "[200]" ]
do
    Status=`curl $Server`
    echo ret is: $Status
done
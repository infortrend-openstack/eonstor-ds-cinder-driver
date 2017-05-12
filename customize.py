#!/bin/bash
echo "Please enter custom name: "
read CUSTOMER

sed -i "s#infortrend#$CUSTOMER#g" infortrend/infortrend_fc_cli.py
sed -i "s#Infortrend#$CUSTOMER#g" infortrend/infortrend_fc_cli.py

sed -i "s#infortrend#$CUSTOMER#g" infortrend/infortrend_iscsi_cli.py
sed -i "s#Infortrend#$CUSTOMER#g" infortrend/infortrend_iscsi_cli.py

sed -i "s#infortrend#$CUSTOMER#g" infortrend/eonstor_ds_cli/*
sed -i "s#Infortrend#$CUSTOMER#g" infortrend/eonstor_ds_cli/*

mv ./infortrend/infortrend_fc_cli.py ./infortrend/${CUSTOMER}_fc_cli.py
mv ./infortrend/infortrend_iscsi_cli.py ./infortrend/${CUSTOMER}_iscsi_cli.py
mv ./infortrend ./${CUSTOMER}

DRIVER_FOLDER=$(find / -name infortrend | grep cinder/volume/drivers | sed 's#infortrend##g')
echo "Putting $CUSTOMER driver to directory: $DRIVER_FOLDER"
mv ./${CUSTOMER} $DRIVER_FOLDER

CINDER_FOLDER=$(echo -e ${DRIVER_FOLDER} | sed 's#/volume/drivers/##g')
cat <<EOF >>$CINDER_FOLDER/exception.py
class ${CUSTOMER}CliException(CinderException):
    message = _("$CUSTOMER CLI exception: %(err)s Param: %(param)s "
                    "(Return Code: %(rc)s) (Output: %(out)s)")
EOF

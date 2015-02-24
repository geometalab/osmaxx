#!/bin/bash


sudo cp /vagrant/osmaxx.vhost /etc/apache2/sites-available/osmaxx.conf
sudo ln -s /etc/apache2/sites-available/osmaxx.conf /etc/apache2/sites-enabled/osmaxx.conf
sudo a2ensite osmaxx
service apache2 restart
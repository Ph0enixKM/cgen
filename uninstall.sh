echo -e "\e[2m-- Requesting sudo privileges --\e[0m"
sudo echo

sudo rm -rf ${HOME}/.cgen
sudo rm /bin/cgen

echo -e '\n\033[42m\033[30m DONE \e[0m'
echo -e '\e[32mCGen has been successfully uninstalled 🎉'
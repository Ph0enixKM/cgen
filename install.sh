#!/bin/bash

echo -e "\e[38;5;3m-- Make sure you have installed: wget tar --\e[0m"
echo -e "\e[38;5;3m\e[2mPress [Enter] if you do...\e[0m"
read

echo -e "\e[2m-- Requesting sudo privileges --\e[0m"
sudo echo

handle() {
    $@
    if [[ $? != '0' ]]; then
        echo -e "\n\033[41m\033[30m ERROR \e[0m"
        echo -e "\033[31mCouldn't install CGen. Aborting... \e[0m"
        exit 1
    fi
}

handle wget https://github.com/Ph0enixKM/cgen/releases/latest/download/cgen_linux_x86_64.tar.gz
handle tar -xvzf cgen_linux_x86_64.tar.gz
handle mv dist ${HOME}/.cgen -f
handle rm cgen_linux_x86_64.tar.gz
handle sudo ln -s ${HOME}/.cgen/cgen /bin/cgen -f

echo -e '\n\033[42m\033[30m DONE \e[0m'
echo -e '\e[32mCGen has been successfully installed 🎉'
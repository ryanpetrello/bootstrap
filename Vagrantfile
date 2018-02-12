# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "EarlAbides/archlinux64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
  config.ssh.forward_x11 = true
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provision.yml"
  end
end

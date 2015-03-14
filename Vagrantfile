# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.synced_folder ".", "/home/vagrant/app"
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :forwarded_port, guest: 8000, host: 8000

  config.vm.provision "ansible" do |ansible|
  ansible.playbook = "../devops/ansible/site.yml"
  ansible.sudo = true
  ansible.host_key_checking = false
  # ansible.verbose = 'vvvv'
  ansible.tags = ["vagrant"]
  ansible.skip_tags = ["security", "ntp", "swap"]
  ansible.groups = {
        "web" => ["machine1"],
  }
  ansible.extra_vars = {
      vagrantvm: true,
      ansible_ssh_user: 'vagrant'}
  end
end


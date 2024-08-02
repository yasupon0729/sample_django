#!/bin/bash
docker compose up -d
docker compose exec back bash -c "
  mkdir -p /home/appuser/.ssh && chmod 700 /home/appuser/.ssh
  if [ ! -f /home/appuser/.ssh/id_rsa ]; then
    ssh-keygen -t rsa -b 4096 -N '' -f /home/appuser/.ssh/id_rsa
  fi
  eval \$(ssh-agent -s)
  ssh-add /home/appuser/.ssh/id_rsa
"
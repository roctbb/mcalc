npm install
sudo pip3 install -r requirements.txt
sudo cp mcalc.conf /etc/supervisor/conf.d/
sudo cp mcalc_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d backend.calc.ai.medsenger.ru -d calc.ai.medsenger.ru
touch config.py

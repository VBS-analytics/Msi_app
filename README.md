# For importing .sql file in mysql

mysql -u username -p password database_name < /path/to/your/file.sql
mysql>source /path/to/your/file.sql

sudo fuser -n tcp -k 8000


### docker to mysql host
GRANT ALL PRIVILEGES ON vscrmnew.* TO 'harish'@'%' identified by 'Admin@123!!';
flush privileges;

### docker to mysql host
CREATE USER 'vbs-ubsr0089'@'172.21.12.19' IDENTIFIED BY 'Admin@123';


## make sure the bind-address = 0.0.0.0
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
bind-address = 0.0.0.0
sudo systemctl restart mysql.service

### For gettings the docker IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 9cfa26373293
`9cfa26373293` is the container id '172.22.0.3'
172.23.0.3
import geoip2.database
import os


class IpDatabase():
    def __init__(self,path='dashboard/'):

        self.ip_dict={}

        self.country_path=os.path.join(path,'Country.mmdb')
        self.asn_path=os.path.join(path,'Asn.mmdb')
        self.city_path=os.path.join(path,'City.mmdb')


    def get_country(self,path,ip):
        with geoip2.database.Reader(path) as reader:
            res=reader.country(ip)
            return res.country.name

    def get_city(self,path,ip):
        with geoip2.database.Reader(path) as reader:
            res=reader.city(ip)
            return res

    def get_asn(self,path,ip):
        with geoip2.database.Reader(path) as reader:
            res=reader.asn(ip)
            return res

    def update_data(self,ip):

        pass

x=IpDatabase()
y=x.get_country(x.country_path,'10.132.254.12')
print(y)


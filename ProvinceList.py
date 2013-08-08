__author__ = 'ron.liu'
#encoding=utf-8
import urllib,urllib2,bs4,cookielib,re,sqlite3,logging,sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
sqlite_conn = sqlite3.connect(r'hospital.db')
sqlite_cursor = sqlite_conn.cursor()

sql_desc = '''
create table hospital (
    [tkid]            integer PRIMARY KEY autoincrement,
    [province]        varchar (50),
    [city]         int default 0,
    [url]          varchar (255),
    [createdate]      datetime default (datetime('now', 'localtime'))
);
'''
sqlite_cursor.execute(sql_desc)

sql_desc = '''
create table  hospital_message (
    [tkid]            integer PRIMARY KEY autoincrement,
    [province]        varchar (255),
    [city]        varchar (255),
    [hospital]        varchar (255),
    [address]        varchar (255),
    [telphone]        varchar (255),
    [level]        varchar (255),
    [key_departments]        varchar (255),
    [jingyinfangshi]        varchar (255),
    [fax]        varchar (255),
    [emailaddress]        varchar (255),
    [website]        varchar (255),
    [provinceurl]     varchar (255),
    [createdate]      datetime default (datetime('now', 'localtime'))
);
'''
sqlite_cursor.execute(sql_desc)


def get_province():
    # sqlite_conn = sqlite3.connect('hospital.db')
    # sqlite_cursor = sqlite_conn.cursor()
    provinceurl=r'http://www.a-hospital.com/w/%E5%85%A8%E5%9B%BD%E5%8C%BB%E9%99%A2%E5%88%97%E8%A1%A8'
    result=urllib2.urlopen(provinceurl,timeout=200).read()
    soup=bs4.BeautifulSoup(result)
    m=soup.findAll({'span' : True, 'a' : True},title=re.compile(u'.医院列表'))
    HospitalList=m[10:493]
    HosProv=[]
    for i in range(483):
        if HospitalList[i].string[-4:]==u'医院列表':
            province=HospitalList[i].string[0:-4]
        else:
            HosProv.append(province+' '+HospitalList[i].string+' '+'http://www.a-hospital.com'+HospitalList[i]['href'])
            province_str=province
            city_str=HospitalList[i].string
            url_str='http://www.a-hospital.com'+HospitalList[i]['href']
            sql_hospital = "INSERT INTO hospital(province,city,url) values ('"+"%s','%s','%s"%(province_str,city_str,url_str)+"') ;"
            print sql_hospital
            sqlite_cursor.execute(sql_hospital)
            sqlite_conn.commit()
            hospital_message(province_str,city_str,url_str)

def hospital_message(province,city,provinceurl):
    provinceurl=provinceurl
    province=province
    city=city
    try:
        result=urllib2.urlopen(provinceurl,timeout=200).read()
        soup=bs4.BeautifulSoup(result)
        com=re.compile(r'点击医院名称进入相关条目可以阅读更多关于此医院的信息。.*?<h2>',re.S)
        fix_html=re.findall(com,str(soup))[0][85:-4]
        # fix_html=file('fix_html.html','r').read()    #测试用
        soup2=bs4.BeautifulSoup(str(fix_html))
        s=soup2.contents[1].contents
        for item in s: #去掉\n
            if item!='\n':
                item_soup=bs4.BeautifulSoup(str(item))
                try:
                    hospital=item_soup.li.b.a.string
                except:
                    hospital=item_soup.li.b.string
                other=item_soup.li.ul.findAll('li')
                address=''
                telphone=''
                level=''
                key_departments=''
                jingyinfangshi=''
                fax=''
                emailaddress=''
                website=''
                for message in other:
                    message_soup=bs4.BeautifulSoup(str(message))
                    if message_soup.li.b.string==u'医院地址':
                        address=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'联系电话':
                        telphone=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'医院等级':
                        level=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'重点科室':
                        key_departments=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'经营方式':
                        jingyinfangshi=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'传真号码':
                        fax=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'电子邮箱':
                        emailaddress=message_soup.li.contents[1][1:]
                    elif message_soup.li.b.string==u'医院网站':
                        website=message_soup.li.contents[1][1:]
                hospital_message = "INSERT INTO hospital_message(province,city,hospital,address,telphone,level,key_departments,jingyinfangshi,fax,emailaddress,website,provinceurl) values ('"+"%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s"%(province,city,hospital,address,telphone,level,key_departments,jingyinfangshi,fax,emailaddress,website,provinceurl)+"') ;"
                print hospital_message
                sqlite_cursor.execute(hospital_message)
                sqlite_conn.commit()
    except:
        hospital=''
        address=''
        telphone=''
        level=''
        key_departments=''
        jingyinfangshi=''
        fax=''
        emailaddress=''
        website=''
        hospital_message = "INSERT INTO hospital_message(province,city,hospital,address,telphone,level,key_departments,jingyinfangshi,fax,emailaddress,website,provinceurl) values ('"+"%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s"%(province,city,hospital,address,telphone,level,key_departments,jingyinfangshi,fax,emailaddress,website,provinceurl)+"') ;"
        print hospital_message
        sqlite_cursor.execute(hospital_message)
        sqlite_conn.commit()
        #print hospital,address,telphone,level,key_departments,jingyinfangshi,fax,emailaddress,website

get_province()




# print hospial,other,len(other),'\n'
#         a.append(item)
# print len(a)
#m=soup.findAll({'li' : True, 'b' : True},)
#print m[1]

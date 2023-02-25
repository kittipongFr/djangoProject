from __future__ import unicode_literals
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('CarRental', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL("INSERT INTO carrental_geographies (id,name) VALUES " \
                          "(1,'ภาคเหนือ')," \
                          "(2,'ภาคกลาง')," \
                          "(3,'ภาคตะวันออกเฉียงเหนือ')," \
                          "(4,'ภาคตะวันตก')," \
                          "(5,'ภาคตะวันออก')," \
                          "(6,'ภาคใต้');" \
                          ),

        migrations.RunSQL("INSERT INTO carrental_provinces (id, code, name_th, name_en, geography_id_id) VALUES"\
            "(1, '10', 'กรุงเทพมหานคร', 'Bangkok', 2),"\
            "(2, '11', 'สมุทรปราการ', 'Samut Prakan', 2),"\
            "(3, '12', 'นนทบุรี', 'Nonthaburi', 2),"\
            "(4, '13', 'ปทุมธานี', 'Pathum Thani', 2),"\
            "(5, '14', 'พระนครศรีอยุธยา', 'Phra Nakhon Si Ayutthaya', 2),"\
            "(6, '15', 'อ่างทอง', 'Ang Thong', 2),"\
            "(7, '16', 'ลพบุรี', 'Loburi', 2),"\
            "(8, '17', 'สิงห์บุรี', 'Sing Buri', 2),"\
            "(9, '18', 'ชัยนาท', 'Chai Nat', 2),"\
            "(10, '19', 'สระบุรี', 'Saraburi', 2),"\
            "(11, '20', 'ชลบุรี', 'Chon Buri', 5),"\
            "(12, '21', 'ระยอง', 'Rayong', 5),"\
            "(13, '22', 'จันทบุรี', 'Chanthaburi', 5),"\
            "(14, '23', 'ตราด', 'Trat', 5),"\
            "(15, '24', 'ฉะเชิงเทรา', 'Chachoengsao', 5),"\
            "(16, '25', 'ปราจีนบุรี', 'Prachin Buri', 5),"\
            "(17, '26', 'นครนายก', 'Nakhon Nayok', 2),"\
            "(18, '27', 'สระแก้ว', 'Sa Kaeo', 5),"\
            "(19, '30', 'นครราชสีมา', 'Nakhon Ratchasima', 3),"\
            "(20, '31', 'บุรีรัมย์', 'Buri Ram', 3),"\
            "(21, '32', 'สุรินทร์', 'Surin', 3),"\
            "(22, '33', 'ศรีสะเกษ', 'Si Sa Ket', 3),"\
            "(23, '34', 'อุบลราชธานี', 'Ubon Ratchathani', 3),"\
            "(24, '35', 'ยโสธร', 'Yasothon', 3),"\
            "(25, '36', 'ชัยภูมิ', 'Chaiyaphum', 3),"\
            "(26, '37', 'อำนาจเจริญ', 'Amnat Charoen', 3),"\
            "(27, '39', 'หนองบัวลำภู', 'Nong Bua Lam Phu', 3),"\
            "(28, '40', 'ขอนแก่น', 'Khon Kaen', 3),"\
            "(29, '41', 'อุดรธานี', 'Udon Thani', 3),"\
            "(30, '42', 'เลย', 'Loei', 3),"\
            "(31, '43', 'หนองคาย', 'Nong Khai', 3),"\
            "(32, '44', 'มหาสารคาม', 'Maha Sarakham', 3),"\
            "(33, '45', 'ร้อยเอ็ด', 'Roi Et', 3),"\
            "(34, '46', 'กาฬสินธุ์', 'Kalasin', 3),"\
            "(35, '47', 'สกลนคร', 'Sakon Nakhon', 3),"\
            "(36, '48', 'นครพนม', 'Nakhon Phanom', 3),"\
            "(37, '49', 'มุกดาหาร', 'Mukdahan', 3),"\
            "(38, '50', 'เชียงใหม่', 'Chiang Mai', 1),"\
            "(39, '51', 'ลำพูน', 'Lamphun', 1),"\
            "(40, '52', 'ลำปาง', 'Lampang', 1),"\
            "(41, '53', 'อุตรดิตถ์', 'Uttaradit', 1),"\
            "(42, '54', 'แพร่', 'Phrae', 1),"\
            "(43, '55', 'น่าน', 'Nan', 1),"\
            "(44, '56', 'พะเยา', 'Phayao', 1),"\
            "(45, '57', 'เชียงราย', 'Chiang Rai', 1),"\
            "(46, '58', 'แม่ฮ่องสอน', 'Mae Hong Son', 1),"\
            "(47, '60', 'นครสวรรค์', 'Nakhon Sawan', 2),"\
            "(48, '61', 'อุทัยธานี', 'Uthai Thani', 2),"\
            "(49, '62', 'กำแพงเพชร', 'Kamphaeng Phet', 2),"\
            "(50, '63', 'ตาก', 'Tak', 4),"\
            "(51, '64', 'สุโขทัย', 'Sukhothai', 2),"\
            "(52, '65', 'พิษณุโลก', 'Phitsanulok', 2),"\
            "(53, '66', 'พิจิตร', 'Phichit', 2),"\
            "(54, '67', 'เพชรบูรณ์', 'Phetchabun', 2),"\
            "(55, '70', 'ราชบุรี', 'Ratchaburi', 4),"\
            "(56, '71', 'กาญจนบุรี', 'Kanchanaburi', 4),"\
            "(57, '72', 'สุพรรณบุรี', 'Suphan Buri', 2),"\
            "(58, '73', 'นครปฐม', 'Nakhon Pathom', 2),"\
            "(59, '74', 'สมุทรสาคร', 'Samut Sakhon', 2),"\
            "(60, '75', 'สมุทรสงคราม', 'Samut Songkhram', 2),"\
            "(61, '76', 'เพชรบุรี', 'Phetchaburi', 4),"\
            "(62, '77', 'ประจวบคีรีขันธ์', 'Prachuap Khiri Khan', 4),"\
            "(63, '80', 'นครศรีธรรมราช', 'Nakhon Si Thammarat', 6),"\
            "(64, '81', 'กระบี่', 'Krabi', 6),"\
            "(65, '82', 'พังงา', 'Phangnga', 6),"\
            "(66, '83', 'ภูเก็ต', 'Phuket', 6),"\
            "(67, '84', 'สุราษฎร์ธานี', 'Surat Thani', 6),"\
            "(68, '85', 'ระนอง', 'Ranong', 6),"\
            "(69, '86', 'ชุมพร', 'Chumphon', 6),"\
            "(70, '90', 'สงขลา', 'Songkhla', 6),"\
            "(71, '91', 'สตูล', 'Satun', 6),"\
            "(72, '92', 'ตรัง', 'Trang', 6),"\
            "(73, '93', 'พัทลุง', 'Phatthalung', 6),"\
            "(74, '94', 'ปัตตานี', 'Pattani', 6),"\
            "(75, '95', 'ยะลา', 'Yala', 6),"\
            "(76, '96', 'นราธิวาส', 'Narathiwat', 6),"\
            "(77, '97', 'บึงกาฬ', 'buogkan', 3);"
    ),

        migrations.RunSQL("INSERT INTO carrental_owner(`own_id`, `name`, `address`, `email`, `tel`, `password`, `birthdate`, `img`,`provinces_id`, `linkLocation`) VALUES "\
        "('e001', 'kittipong', 'home', 'hjog717@gmail.com', '0963944908', '12345678', '2023-02-14', '', 19,'https://goo.gl/maps/aU6HxTs2gxECHJH96'),"\
        "('e00120', 'kittipong8', 'home', 'hjog717@gmail.com', '22', '22', '2023-02-09', '', 19, ''),"\
        "('frankgg', '0000', 'rrr', 'hjog@gmail.com', '0963944908', '081244fr', '2023-02-16', '', 64, ''),"\
       "('o001', 'frank', 'บ้าน', 'hjog717@gmail.com', '0963944908', '081244fr', '2023-02-25', '', 1, ''),"\
        "('ttt', 'kittipong8', '4444', 'hjog7170@gmail.com', '0963944908', '12345678', '2023-02-18', '', 19, '');"
    ),

        migrations.RunSQL("INSERT INTO carrental_member(`mem_id`, `name`, `email`, `tel`, `img`, `provinces_id`)VALUES"\
    "('frank007', 'kittipong8', 'kittipong@gmail.com', '0963944908', '', 28),"\
        "('m001', 'kittipong8', 'hjog7170@gmail.com', '0963944908', '', 19),"\
        "('m005', 'kittipong', 'hjog717@gmail.com', '000', 'static/image/Member/ford-ranger.png', 28),"\
        "('m006', 'kittipong@gmail.com', 'kittipong@gmail.com', '0963944908', '', 28),"\
        "('m009', 'kittipong@gmail.com', 'kittipong@gmail.com', '0963944908', '', 28);"
                          ),

        migrations.RunSQL("INSERT INTO carrental_bank (`id`, `bank_name`, `img`) VALUES "\
        "(1, 'กสิกร', 'static/image/Bank/a03cf5e37b4b1d0b376ad04a6b39e0b3.png'),"
        "(2, 'กรุงไทย', 'static/image/Bank/logo-krungthai-bank-public-ktb-150-145_2x.png');"\
    ),
        migrations.RunSQL("INSERT INTO carrental_ownbank (`id`, `bank_num`, `name`, `branch`, `bank_id_id`, `own_id_id`) VALUES"\
        "(2, '15426666', '5', 'ขอนแก่น', 2, 'frankgg'),"
        "(3, '1545155', 'กิตติพงษ์ พาบุดดา', 'ขอนแก่น', 2, 'e001'),"\
        "(4, '15355666', 'กิตติพงษ์ พาบุดดา', 'บัวใหญ่', 1, 'e001');"\

    ),
        migrations.RunSQL("INSERT INTO carrental_adress (`id`,`location`,`own_id_id`,`province_id`,`name`) VALUES "\
        "(1,'https://goo.gl/maps/nArN4vZ4H9JfhvrL7','e001',28,'สนามบินขอนแก่น'),"\
        "(2,'https://goo.gl/maps/nArN4vZ4H9JfhvrL7','e001',28,'สนามกีฬากลางขอนแก่น');"\

        ),
        migrations.RunSQL("INSERT INTO carrental_cartype (`type_id`,`type_name`,`picture`) VALUES "\
        "('10','EV car','static/image/types/10_2023-02-22.jpg'),"\
				"('2','Hatch Back','static/image/types/2_2023-02-13.jpg'),"\
				"('23','Sedan','static/image/types/23_2023-02-22.jpg'),"\
				"('3','Crossover','static/image/types/3_2023-02-22.png'),"\
				 "('33','Van','static/image/types/33_2023-02-22.png'),"\
				"('4','SUV','static/image/types/4_2023-02-13.jpg'),"\
				"('5','Pick up','static/image/types/5_2023-02-13.jpg'),"\
				 "('6','Sports car','static/image/types/6_2023-02-22.jpg');"\
        ),
        migrations.RunSQL("INSERT INTO carrental_car (`car_id`,`brand`,`car_model`,`img`,`price`,`status`,`own_id_id`,`provinces_id`,`type_id_id`,`gearType`,`seat`,`desc`,`address_id`) VALUES"\
"('222','Isuzu','D-Max','static/image/cars/222_2023-02-13.jpg',800,0,'e001',28,'5','เกียร์ธรรมดา','4','',1),"\
"('55','Toyota','cicic','static/image/cars/55_2023-02-13.jpg',500,1,'e001',28,'23','เกียร์ออร์โต้','4','',1),"\
 "('m001','Nisan','15','static/image/cars/m001_2023-02-26.png',500,0,'e001',28,'3','เกียร์ออร์โต้','4','555',1),"\
"('กพ5645','Nisan','Gtr','static/image/cars/กพ5645_2023-02-17.jpg',1500,0,'e001',28,'6','เกียร์ออร์โต้','2','',1),"\
 "('กฟ5236','Ford','Ranger','static/image/cars/กฟ5236_2023-02-21.png',1000,0,'e001',28,'5','เกียร์ธรรมดา','4','',1),"\
"('สด5625','Toyota','alphard','static/image/cars/สด5625_2023-02-23.png',1500,0,'e001',28,'33','เกียร์ออร์โต้','4','',1),"\
 "('สว1245','Toyota','Vios','static/image/cars/สว1245_2023-02-24.png',1200,0,'e001',28,'23','เกียร์ออร์โต้','4','โตโยต้า บริษัทรถยนต์ผู้นำตลาดเมืองไทย นำเสนอ 2019 โตโยต้า วิออส (Toyota Vios) จำนวน 3 รุ่นย่อย ได้แก่รุ่น Entry ราคา 6.09 แสนบาท รุ่น Mid ราคา 6.99 แสนบาท และรุ่น High ราคา 7.89 แสนบาท มา5555',1),"\
 "('หส5462','Tesla','Model3','static/image/cars/หส5462_2023-02-19.jpg',1200,1,'e001',28,'10','เกียร์ออร์โต้','4','',1);"

        ),

        migrations.RunSQL("INSERT INTO carrental_rent (`rent_id`, `rent_date`, `return_date`, `status`, `mem_id_id`, `own_id_id`, `car_id`, `price`, `amount`)VALUES" \
            "('r012', '2022-12-17', '2022-02-19', '7', 'm001', 'e001', '222', 1000, 2)," \
            "('r013', '2023-01-18', '2023-01-20', '7', 'm001', 'e001', 'สด5625', 1000, 3)," \
            "('r014', '2023-02-18', '2023-02-22', '5', 'm001', 'e001', '55', 1500, 2)," \
            "('r015', '2023-02-21', '2023-02-20', '5', 'm001', 'e001', '222', 2500, 1)," \
            "('r016', '2023-02-20', '2023-02-20', '5', 'm001', 'e001', 'กพ5645', 1500, 2)," \
            "('r017', '2023-02-28', '2023-03-01', '5', 'm001', 'e001', 'หส5462', 1500, 2)," \
            "('RN-2302000002', '2023-02-24', '2023-02-26', '7', 'm005', 'e001', '55', 500, 1)," \
            "('RN-2302000003', '2023-02-27', '2023-02-28', '7', 'm005', 'e001', 'กพ5645', 1500, 1)," \
            "('RN-2302000004', '2023-02-25', '2023-02-27', '6', 'm005', 'e001', 'กฟ5236', 1000, 2)," \
            "('RN-2302000005', '2023-02-25', '2023-02-26', '6', 'm005', 'e001', 'หส5462', 1200, 1)," \
            "('RN-2302000006', '2023-02-27', '2023-02-28', '6', 'm005', 'e001', '222', 800, 2)," \
            "('RN-2302000007', '2023-02-25', '2023-02-26', '4', 'm005', 'e001', 'หส5462', 1200, 2)," \
            "('RN-2302000008', '2023-02-25', '2023-02-27', '1', 'm005', 'e001', '55', 500, 3);" \

            ),


        migrations.RunSQL("INSERT INTO carrental_payment (`id`,`pay_id`,`pay_total`,`pay_date`,`slip_img`,`bank_id`,`rent_id_id`) VALUES "\
            "(1,'5551244',555,'2023-02-25','static/image/Slip/a03cf5e37b4b1d0b376ad04a6b39e0b3_LlyB1xp.png',4,'RN-2302000007'),"\
            "(2,'5622222',1845,'2023-02-25','static/image/Slip/5622222_2023-02-24.jpg',4,'RN-2302000007');"\

        ),
        migrations.RunSQL("INSERT INTO carrental_accepts (`id`, `a_date`, `comment`, `own_id`, `rent_id`)VALUES"\
        "(1, '2023-02-24 08:45:34.604828', '', 'e001', 'RN-2302000007'),"\
        "(2, '2023-02-24 08:51:09.062424', '', 'e001', 'RN-2302000007');"\
    ),
        migrations.RunSQL("INSERT INTO carrental_reject (`id`,`rdate`,`comment`,`own_id`,`rent_id`) VALUES "\
    
        "(1,'2023-02-21 12:02:00.721964','รถพัง','e001','r013'),"\
        "(2,'2023-02-24 04:44:42.914562','555','e001','RN-2302000003'),"\
        "(3,'2023-02-24 04:49:51.663334','22222','e001','RN-2302000002');"\



        ),
        migrations.RunSQL("INSERT INTO carrental_cancel (`id`, `cdate`, `comment`, `rent_id`, `mem_id`)VALUES"\
        "(1, '2023-02-24 05:04:13.179900', '55550222', 'RN-2302000004', 'm005'),"\
    "(2, '2023-02-24 05:06:34.751104', '55550222', 'RN-2302000004', 'm005'),"\
    "(3, '2023-02-24 05:35:32.512880', '5445', 'RN-2302000005', 'm005'),"\
    "(4, '2023-02-24 05:39:54.028115', '5555', 'RN-2302000006', 'm005');"\
        ),
        migrations.RunSQL("INSERT INTO carrental_confirms (`id`,`c_date`,`comment`,`own_id`,`rent_id_id`) VALUES "\

            "(1,'2023-02-24 05:55:39.100317','','e001','RN-2302000007'),"\
            "(2,'2023-02-24 06:01:12.101838','','e001','RN-2302000007');")


    ]

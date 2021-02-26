from PyQt5.QtWidgets import QTableWidgetItem, QMainWindow, QApplication
from ekle_python import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIntValidator         # Kod içinde gereken ütüphanelerimi import ettim.
import sqlite3

baglanti = sqlite3.connect("mydb.db")    # Db Sqlite3 te açtığım sw me baglandım.
curs = baglanti.cursor()                 #Bağlantıyı cursor ettim yani imleç ile datada dolaştıracagız.


class sotomasyonum(QMainWindow):        #Ana sınıfımı tanımladım ve eğitimini aldığım PyQt5 ve Qt designer ile olusturdugum Ana pencereyi girdim.

    def __init__(self):
        super().__init__()       #Programın ilk olarak çağırılmadan çalıştırmasını istediğim komutlarımı gireceğim initializer yanı ilk olarak baslatılac-
        self.ui = Ui_MainWindow()   #cak komutlarımı gireceğim fonksiyonu olusuturdum.
        self.ui.setupUi(self)        # Qt designerda tasarladıgım arayüz elemanlarına ulasıp komut eklemek için ui çağrısı yaptım.

        if baglanti:
            self.ui.label.setText("Veri Tabanı Bağlantısı Başarılı. ")        #Eğer veri tabanına baglandıysam bana dönüş yapmasını istedim.
        else:
            self.ui.label.setText("Bağlantı basarısız.")

        self.setWindowTitle("Şirket Otomasyon")         #Penceremin ismini değiştirdim. MainWindow yazısından kurtuldum.

        self.ui.eklebuton.clicked.connect(self.ekle)
        self.ui.listele_buton.clicked.connect(self.listele)
        self.ui.silbuton.clicked.connect(self.sil)                            #Burada ise eklediğim arayüz elemanlarını (buton/ line edit vs.) aşağıdaki
        self.ui.cikis.clicked.connect(self.cikis)                             # fonksiyonlar ile birleştirdim.
        self.ui.txtsicil.setValidator(QIntValidator(0,2147483647,self))
        self.ui.txtyasi.setValidator(QIntValidator(0, 2147483647, self))       # PyQt5 in yeni öğrendiğim bir özelliğini kullandım ve çok faydalı.
                                                                               # Sayı girilmesi gerekn yere harf girdirmiyor.
    def ekle(self):           # Calısan eklenmesi için fonksiyon açtım.Ekle butonuna basınca buraya gelecek ve islemleri yapacak.
        Sicill = self.ui.txtsicil.text()
        Adii = self.ui.txtadi.text()
        Soyadii = self.ui.txtsoyadi.text()        #kullanıcının gireceği lineeditleri değişen ismi verdim daha kolay ulasmak için.
        Yasii = self.ui.txtyasi.text()
        Cinss = self.ui.txtcins.text()

        if Sicill == "" or Adii == "" or Soyadii == "" or Yasii == "" or Cinss == "":     #Eğer değişkenlere girdi girlmez ise hata mesajı döndürdüm.
            QMessageBox.about(self, "UYARI !", "Lütfen tüm alanları doldurunuz ve sayısal değer gereken yere sayısal deger giriniz.")
                                                                          #aksi halde program kapanıyordu kendiliğinden.
        else:
            curs.execute("INSERT INTO Kayit values(?,?,?,?,?)", (Sicill, Adii, Soyadii, Yasii, Cinss,))
            baglanti.commit()


            #Burada ise veri tabanım içindeki kayıtları insert ettim.


        self.ui.txtsicil.clear()
        self.ui.txtadi.clear()
        self.ui.txtsoyadi.clear()
        self.ui.txtyasi.clear()        # Ve bulabildiğime çok sevindiğim bir özellik oldu line editlere girlen girdi eklenince temizlenmesi.
        self.ui.txtcins.clear()


    def sil(self):                   #Eleman silmek için gerekli fonk.
        con = "SELECT * FROM Kayit"       #Tabiki önce veri tabanına ulasmam lazımdı elemanlara.
        res = curs.execute(con)           #Ve baglantıya imleç atayıp üzerinden işlem yapmalıydım.
        for row in enumerate(res):        # Bu kısım açıkçası beni epeyce zorladı.Birsürü kaynak taradım en son arapça kaynakta row ve columnlar ile -
            if row[0] == self.ui.tableWidget.currentRow():    #işlem yapmam gerektiğini gördüm
                data = row[1]
                Sicill = data[0]
                Adi = data[1]          #Aslında veriler Rowda yani satırlarda tutuluyordu ve protatip için ilk satıra ulaşıp devamında diğerlerine ulaşacak-
                Soyadi = data[2]       #olan komutları girdim. Yani cursor ile imleci tum dataları seçtiğinde sildireceğim şekilde ayarladım.
                Yasi = data[3]         #işin iyi tarafı tek bir girdiiyi seçincede silebiliyor olması oldu beklemiyordum.
                Cins = data[4]
                curs.execute("DELETE FROM Kayit WHERE Sicil=? AND Adi=? AND Soyadi=? AND Yas=? AND Cinsiyet=?",
                             (Sicill, Adi, Soyadi, Yasi, Cins,))     #Burada ise klasik sqlite3 komutu ile kayıtlara ulasıp sildirdim.
                baglanti.commit()
                self.listele()   #Ardından listele komutuna baglandım çünkü ilme işlemi ardından güncellemek için
        return

    def listele(self):

        while self.ui.tableWidget.rowCount() > 0:  # Listelemk başlı başına bir çıkmaza soktu beni işler iyice karıştı çokça türkçe ve ing kaynak-
            self.ui.tableWidget.removeRow(
                0)  # kullandım okudum anladım iyice ve aslında data_Structures dersinde matrix kullanımını öğrenmem
        baglanti = 'SELECT * FROM Kayit'  # burada çok işime yaradı ve satırlar ile sütünlar arasında gezinip işlem yaptım.
        res = curs.execute(baglanti)
        for row_index, row_data in enumerate(res):
            self.ui.tableWidget.insertRow(row_index)  # Qt designer elemanı olan tabble Widgeti kullandım .
            for colm_index, colm_data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_index, colm_index, QTableWidgetItem(str(colm_data)))
        return


    def cikis(self):
        QMessageBox.about(self, "BİLGİLENDİRME !","Çıkış Yapıldı.")    #Programın süsü çıkış butonuuuu

        uygulama.exit()


uygulama = QApplication([])
pencere = sotomasyonum()          #Ve tabiki birisi uygulamayı çağırmalıydı :D
pencere.show()
uygulama.exec_()

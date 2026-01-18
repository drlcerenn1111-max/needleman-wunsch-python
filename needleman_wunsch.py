"""Bu yazılım Needleman-Wunsch algoritmasını kullanarak iki dizinin benzerliğini hesaplar."""
class NeedlemanWunsch:
    def __init__(self, seq1, seq2, match=5, mismatch=-1, gap_vertical=-2, gap_horizontal=-3):
        """
        Parametreler:
        seq1: ilk DNA dizisi
        seq2: ikinci DNA dizisi
        match: Eşleşme puanı
        mismatch: Eşleşmeme puanı
        gap_vertical: Dikey boşluk puanı (dikey gap)
        gap_horizontal: Yatay boşluk puanı (yatay gap)
        """
        
        self.seq1 = seq1.upper()
        self.seq2 = seq2.upper()
        
        # Uzun diziyi dikey (seq2) ve yatay (seq1) olarak hizala
        if len(seq1) > len(seq2):
            self.seq1 = seq2  # yatay (kısa)
            self.seq2 = seq1  # dikey (uzun)
            self.swapped = True

            # DÜZELTME: Diziler swap edildiğinde gap puanları da swap edilmeli
            # Ama gap_seq1 ve gap_seq2 olarak saklanmalı (hangi dizide gap olduğunu belirtir)
            self.gap_seq1 = gap_vertical   # seq1 (artık yatay olan) için gap puanı
            self.gap_seq2 = gap_horizontal  # seq2 (artık dikey olan) için gap puanı

        else:
            self.seq1 = seq1  # Yatay
            self.seq2 = seq2  # Dikey
            self.swapped = False

            self.gap_seq1 = gap_horizontal  # seq1 için gap puanı
            self.gap_seq2 = gap_vertical    # seq2 için gap puanı


        self.match_score = match
        self.mismatch_score = mismatch
        

        # Matris boyutları 
        self.rows = len(self.seq2) + 1  # uzun dizi (dikey)
        self.cols = len(self.seq1) + 1  # kısa dizi (yatay)

        # Puanlama ve yön matrisleri
        self.score_matrix = [[0] * self.cols for _ in range(self.rows)]
        self.direction_matrix = [[""] * self.cols for _ in range(self.rows)]

    def dizileri_goster(self):
        """Dizilerin bilgilerini ekrana yazdır"""
        print("=" * 60)
        print("DİZİLER")
        print("=" * 60)
        print(f"seq1 (YATAY): {self.seq1} (uzunluk: {len(self.seq1)})")
        print(f"seq2 (DİKEY): {self.seq2} (uzunluk: {len(self.seq2)})")
        print(f"Matris boyutu: {self.rows} satır × {self.cols} sütun")
        print()
    
    def matris_olustur(self):
        """İlk satır ve sütunu doldur, sonra tüm matrisi doldur"""
        # İlk satırı doldur (yatay gap'ler - seq1'de gap)
        for j in range(1, self.cols):
            """
            j sütun indeksimiz ve 0. satırdayız, sağa doğru ilerlemek istiyoruz.
            aradığımız kutu (0, j) koordinatındaki kutu.
            bir önceki kutudaki (0, j-1) kutu ile gap puanımıza atadığımız puanı topluyoruz
            """
            self.score_matrix[0][j] = self.score_matrix[0][j-1] + self.gap_seq1
            self.direction_matrix[0][j] = "←"  # sonradan geri dönüş için yön önemli

        # İlk sütunu doldur (dikey gap'ler - seq2'de gap)
        for i in range(1, self.rows):
            """
            i satır indeksimiz ve 0. sütundayız, aşağı doğru ilerlemek istiyoruz.
            aradığımız kutu (i, 0) koordinatındaki kutu.
            bir önceki kutudaki (i-1, 0) kutu ile gap puanımıza atadığımız puanı topluyoruz
            """
            self.score_matrix[i][0] = self.score_matrix[i-1][0] + self.gap_seq2
            self.direction_matrix[i][0] = "↑"  # sonradan geri dönüş için yön önemli

        # Şuana kadar boş bir matris oluşturduk ve ilk satır ve sütun için puanlama yaptık
        # Şimdi matrisin geri kalanını dolduruyoruz
        
        for i in range(1, self.rows):
            for j in range(1, self.cols):
                # Eşleşme veya uyuşmazlık kontrolü
                if self.seq2[i-1] == self.seq1[j-1]:
                    diagonal_score = self.score_matrix[i-1][j-1] + self.match_score
                    """
                    score_matrix[i][j] (şu anki hücre) bahsedilen diagonal_score için şu anki
                    hücrenin çapraz hücresi score_matrix[i-1][j-1] (çapraz / sol-üst)
                    """
                else:
                    diagonal_score = self.score_matrix[i-1][j-1] + self.mismatch_score

                vertical_score = self.score_matrix[i-1][j] + self.gap_seq2  # yukarıdan gelme (seq2'de gap)
                horizontal_score = self.score_matrix[i][j-1] + self.gap_seq1  # soldan gelme (seq1'de gap)

                # En yüksek puanı seç
                max_score = max(diagonal_score, vertical_score, horizontal_score)
                self.score_matrix[i][j] = max_score

                # Yönü kaydet (en yüksek puan için)
                if max_score == diagonal_score:
                    self.direction_matrix[i][j] = '↖'
                elif max_score == vertical_score:
                    self.direction_matrix[i][j] = '↑'
                else:
                    self.direction_matrix[i][j] = '←'

    def matrisi_goster(self):
        """Puanlama matrisini ekrana yazdır"""
        print("=" * 60)
        print("PUANLAMA MATRİSİ")
        print("=" * 60)

        # Matrisi oluşturan dizi satırlarını aralıklı yazdır
        dizi_satiri = "      " + "".join(f"{base:>5}" for base in self.seq1)
        print(dizi_satiri)  # yatay sıra seq1 yani column

        for i in range(self.rows):
            if i == 0:
                row_label = "  "  # matrisin tüm satırlarını gezerken yani column 0. satır boş bırakılır
            else:
                row_label = self.seq2[i-1] + " "  # i = 1 için 0. satır i = 2 için 1. satır

            row = row_label + "".join(f"{self.score_matrix[i][j]:>5}" for j in range(self.cols))
            print(row)
        print()

    def backtrace(self):
        """Geri iz sürme yöntemi için optimal hizalamayı bulmak"""
        # Geri izleme sırasında eşleşmeyi takip edebileceğimiz listeyi oluştururuz
        aligned_seq1 = []
        aligned_seq2 = []
        alignment = []
        
        print("=" * 60)
        print("BACKTRACE (GERİ İZ SÜRME)")
        print("=" * 60)

        # Global alignment için sağ alt köşeden başla
        i = self.rows - 1  # en alt satır
        j = self.cols - 1  # en sağ sütun
        max_score = self.score_matrix[i][j]
        
        print(f"Başlangıç pozisyonu: ({i}, {j}), Puan: {max_score}")
        print()

        # Geri iz sürme - matrisin başına kadar git
        while i > 0 or j > 0:
            direction = self.direction_matrix[i][j]
            
            if direction == '↖':  # Diagonal - eşleşme/uyumsuzluk
                aligned_seq1.append(self.seq1[j-1])
                aligned_seq2.append(self.seq2[i-1])
                
                if self.seq1[j-1] == self.seq2[i-1]:
                    alignment.append('|')  # Eşleşme
                else:
                    alignment.append('×')  # Uyumsuzluk
                
                i -= 1
                j -= 1
                
            elif direction == '↑':  # Yukarı - seq1'de gap (dikey hareket, seq2'den harf al)
                aligned_seq1.append('-')
                aligned_seq2.append(self.seq2[i-1])
                alignment.append(' ')
                i -= 1
                
            elif direction == '←':  # Sol - seq2'de gap (yatay hareket, seq1'den harf al)
                aligned_seq1.append(self.seq1[j-1])
                aligned_seq2.append('-')
                alignment.append(' ')
                j -= 1
        
        # Ters çevir (sondan başa gittik)
        aligned_seq1.reverse()
        aligned_seq2.reverse()
        alignment.reverse()
        
        return ''.join(aligned_seq1), ''.join(aligned_seq2), ''.join(alignment)

    def hizalamayi_goster(self, aligned_seq1, aligned_seq2, alignment):
        """Hizalamayı güzel bir formatta göster"""
        print("=" * 60)
        print("HIZALAMA SONUCU")
        print("=" * 60)
        
        # Eşleşme istatistiklerini hesapla
        match_count = alignment.count('|')
        mismatch_count = alignment.count('×')
        gap_count = alignment.count(' ')
        total_length = len(alignment)
        
        print(f"seq1: {aligned_seq1}")
        print(f"      {alignment}")
        print(f"seq2: {aligned_seq2}")
        print()
        print(f"Toplam uzunluk: {total_length}")
        print(f"Eşleşme: {match_count}")
        print(f"Uyuşmazlık: {mismatch_count}")
        print(f"Gap: {gap_count}")
        print(f"Benzerlik oranı: {match_count/total_length*100:.2f}%")
        print()

    


    def calistir(self):
        """Tüm adımları sırayla çalıştır"""
        self.dizileri_goster()
        self.matris_olustur()
        self.matrisi_goster()
        aligned_seq1, aligned_seq2, alignment = self.backtrace()
        self.hizalamayi_goster(aligned_seq1, aligned_seq2, alignment)
        
        return aligned_seq1, aligned_seq2, alignment


# MAIN BLOK
if __name__ == "__main__":
    # Örnek DNA dizileri
    seq1 = "GATTACAG"  # Bu değişecek (üstteki tablo)
    seq2 = "GATTCGAG"  # Bu değişecek (alttaki tablo)
    
    print("NEEDLEMAN-WUNSCH ALGORİTMASI")
    print("=" * 60)
    print()
    
    # NeedlemanWunsch objesi oluştur
    nw = NeedlemanWunsch(seq1, seq2, match=5, mismatch=-1, gap_vertical=-2, gap_horizontal=-3)
    
    # Algoritmayı çalıştır
    nw.calistir()
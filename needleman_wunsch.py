
" Bu yazılım Needleman-Wunsch algoritmasını kullanarak iki dizinin benzerliğini hesaplar."
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
        #uzun diziyi dikey (seq2) ve yatay (seq1) olarak hizala
        if len(seq1) >= len(seq2):
            self.seq1 =seq2 # yatay (kısa)
            self.seq2 =seq1 # dikey (uzun)
            self.swapped = True 
        else:
            self.seq1 = seq1  # Yatay
            self.seq2 = seq2  # Dikey
            self.swapped = False

        self.match_score = match
        self.mismatch_score = mismatch
        self.gap_vertical = gap_vertical
        self.gap_horizontal = gap_horizontal

        # matris boyutları 
        self.rows = len(self.seq2) +1 # uzun dizi (dikey)
        self.cols = len(self.seq1) +1 # kısa dizi (yatay)

        # puanlama matrisi
        self.score_matrix =[[0]* self.cols for _ in range(self.rows)]

    def dizileri_goster(self):
        print("Diziler")
        print(f"seq1 (YATAY): {self.seq1} (uzunluk: {len(self.seq1)})")
        print(f"seq2 (DİKEY): {self.seq2} (uzunluk: {len(self.seq2)})")
        print(f"Matris boyutu: {self.rows} satır × {self.cols} sütun")
    
    def matris_olusturma(self):
        for j in range(1, self.cols):
            """
            j sütun indeksimiz ve 0. satırdayız, sağa doğru ilerlemek istiyoruz.
            aradığımız kutu (0, j) koordinatındaki kutu.
            bir önceki kutudaki (0, j-1) kutu ile gap puanımıza atadığımız puanı topluyoruz
            """
            self.score_matrix[0][j] = self.score_matrix[0][j-1] + self.gap_horizontal
            # ilk satır (gap horizontal) için puanlama
            self.direction_matrix[0][j] = "sol" # !sonradan geri dönüş için yön önemli

        for i in range(1, self.rows):
            """
            i satır indeksimiz ve 0. sütundayız, aşağı doğru ilerlemek istiyoruz.
            aradığımız kutu (i, 0) koordinatındaki kutu.
            bir önceki kutudaki (i-1, 0) kutu ile gap puanımıza atadığımız puanı topluyoruz
            """
            self.score_matrix[i][0] = self.score_matrix[i-1][0] + self.gap_vertical
            # ilk sütun (gap vertical) için puanlama
            self.direction_matrix[i][0] = "üst" # !sonradan geri dönüş için yön önemli

# şuana kadar yaptığımız işlemde boş bir matris oluşturduk ve ilk satır ve sütun için puanlama yaptık.

        def matrisi_doldur(self):
            for i in range(1, self.rows):
                for j in range(1, self.cols):

                    if self.seq2[i-1]== self.seq1[j-1]:
                        diagonal_score = self.score_matrix[i-1][j-1] + self.match_score
                    """
                    score_matrix[i][j] (şu anki hücre) bahsedilen diagonal_score için şu anki
                    hücrenin çapraz hücresi score_matrix[i-1][j-1] (çapraz / sol-üst)
                    """
                else:
                    diagonal_score = self.score_matrix[i-1][j-1] + self.mismatch_score

                vertical_score = self.score_matrix[i-1][j] + self.gap_vertical # yukarıdan gelme
                horizontal_score = self.score_matrix[i][j-1] + self.gap_horizontal # soldan gelme

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
            print("=" * 60)
        print("PUANLAMA MATRİSİ")
        print("=" * 60)

        # matrisi oluşturan dizi satırlarını aralıklı yazdır
        dizi_satırı = "      " + "".join(f"{base:>5}" for base in self.seq1)
        print(dizi_satırı) # yatay sıra seq1 yani column

        for i in range(self.rows):
            if i == 0:
                row_label = "  " # matrisin tüm satırlarını gezerken yani column 0. satır boş bırakılır
            else:
                row_label = self.seq2[i-1] + " "  # i = 1 için 0. satır i = 2 için 1. satır

            row = row_label + "".join(f"{self.score_matrix[i][j]:>5}" for j in range(self.cols))
            print(row)
        print()

    def bactrace(self):
        """Geri iz sürme yöntemi için optimal hizalamayı bulmak"""
        # geri izleme sırasında eşleşmeyi takip edebileceğimiz listeyi oluştururuz.
        self.alignment = []
        print("BACKTRACE (GERİ İZ SÜRME)")

        # max score'u arayacağımız yer son satır ve son sütun, bunun için bir index tanımlanır
        max_i = self.rows -1 # en alt satır index tanımı
        max_j = self.cols -1 # en sağ sütun index tanımı
        max_score = self.score_matrix[max_i][max_j]

        #Son satırı tara
        for j in range(self.cols):
            if self.score_matrix[self.rows - 1][j] > max_score:
                max_score = self.score_matrix[self.rows - 1][j] # score bu satırda güncellendi
                max_i = self.rows - 1 # satır indeksi kaydedildi
                max_j = j # sütun indeksi kaydedildi

        # Son sütunu tara
        for i in range(self.rows):
            if self.score_matrix[i][self.cols - 1] > max_score:
                max_score = self.score_matrix[i][self.cols - 1]
                max_i = i
                max_j = self.cols - 1

        i = max_i
        j = max_j
        
        print(f"En yüksek puan pozisyonu: ({i}, {j}), Puan: {max_score}")

        # Eğer köşede değilse, gap'ler var demektir
        if i < self.rows - 1:
            print(f"  → seq1'de {self.rows - 1 - i} gap var (seq1 bitmiş, seq2 devam ediyor)")
        if j < self.cols - 1:
            print(f"  → seq2'de {self.cols - 1 - j} gap var (seq2 bitmiş, seq1 devam ediyor)")
        print()

        path = [(i, j, self.score_matrix[i][j])]

        